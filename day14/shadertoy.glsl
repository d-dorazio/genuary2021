vec3 cameraPos = vec3(0., 0.25, -1.5);
vec3 lookAt = vec3(0,0,0);
vec3 lightPos = vec3(-0.25, 4., -8);
vec3 diffuseCol = vec3(0.2, 0.7, 0.5);


float sdSphere(float r, vec3 pos)
{
    return length(pos) - r;

}

float sdPlane( vec3 pos, vec3 n, float h )
{
  return dot(pos, n) + h;
}

float sdCapsule( vec3 p, vec3 a, vec3 b, float r )
{
  vec3 pa = p - a, ba = b - a;
  float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
  return length( pa - ba*h ) - r;
}

float sunion( float d1, float d2, float k ) {
    float h = clamp( 0.5 + 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) - k*h*(1.0-h); }

float ssub( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2+d1)/k, 0.0, 1.0 );
    return mix( d2, -d1, h ) + k*h*(1.0-h); }

float sand( float d1, float d2, float k ) {
    float h = clamp( 0.5 - 0.5*(d2-d1)/k, 0.0, 1.0 );
    return mix( d2, d1, h ) + k*h*(1.0-h); }
    

float scene(vec3 pos)
{    

    vec3 p = mod(pos + 0.5*vec3(0.4), vec3(0.4))-0.5*vec3(0.4);
    float dd = sdSphere(0.1, p);
    
    
    pos.x = abs(pos.x);
    pos.x -= 0.6;
    pos.y = pos.y + sin(iTime)*0.05;
    
    float ds = sdSphere(0.5, pos);
    float sdC1 = sdCapsule(pos, vec3(0.0, 1.0, -0.0), vec3(0.0, -1.0, 0.0),   0.2);
    float sdC2 = sdCapsule(pos, vec3(-1, 0, -0.), vec3(1.0, .0, -0.),         0.3);
    
    float d = ssub(sunion(sdC1, sdC2, 0.1), ds, 0.1);
    d = ssub(sdSphere(0.1+0.3*(cos(iTime)*0.5+0.5), pos+vec3(0,0,0.4)), ds, 0.1);
    
    d = sunion(d, sdPlane(pos, vec3(0, 1, 0), 0.1) + 0.03*(sin(pos.x*30.0)*0.5+0.5), 0.2);
    
    
    return max(d, -dd);
    
}

vec3 normal(vec3 pos)
{
    float eps = 0.001;

    float gx = scene(pos + vec3(eps, 0, 0)) - scene(pos - vec3(eps, 0, 0));
    float gy = scene(pos + vec3(0, eps, 0)) - scene(pos - vec3(0, eps, 0));
    float gz = scene(pos + vec3(0, 0, eps)) - scene(pos - vec3(0, 0, eps));

    vec3 normal = vec3(gx, gy, gz);

    return normalize(normal);
}


float shadow(vec3 ro, vec3 rd)
{
    float t = 0.1;
    float res = 1.0;
    
    for (int i = 0; i < 10; ++i) {
          float d = scene(ro + t * rd);
          if (d < 0.001) {
              return d;
          }
          res = min(res, d/t);
          t += d;
    }
    
    return res;
}


vec3 march(vec3 ro, vec3 rd)
{
    float t = 0.0;
    for (int i = 0; i < 128; ++i) {
        vec3 pos = ro + t * rd;
        float d = scene(pos);
        
        if (d < 0.001) {
            vec3 n = normal(pos);
            
            vec3 lr = normalize(lightPos + vec3(cos(iTime)*0.5+0.5, 0., sin(iTime)*0.5+0.5) - pos);

            vec3 col = (diffuseCol + vec3(0, 0, 0.3 * sin(iTime) * sin(pos.x*4.0)  )) * max(0.0, dot(n, lr));

            return mix(vec3(0), col, shadow(pos, lr));
        }
        
        t += d;
    }
    
    return vec3(0.0);
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 xy = (2.0 * fragCoord.xy - iResolution.xy) / iResolution.y;
    
    
    vec3 ro = cameraPos;
    vec3 rd = vec3(xy.x, xy.y, 1);
    
    vec3 color = pow(march(ro, rd), vec3(0.4545));
    
    fragColor = vec4(color, 1.0);
}
