import vsketch

from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import *

import math


class Day02Sketch(vsketch.SketchClass):
    shapes = vsketch.Param(10, 0)
    min_radius = vsketch.Param(0.1)
    y_divisions = vsketch.Param(100)
    shape = vsketch.Param(0, -1, 2)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        shapes = []
        for _ in range(self.shapes):
            while True:
                t = vsk.random(1)
                if (self.shape == -1 and t < 0.33) or self.shape == 0:
                    x, y = vsk.random(-6, 6), vsk.random(-7, 7)
                    p = Point(x, y)

                    r = min(
                        (cc.distance(p) for cc in shapes),
                        default=vsk.random(3),
                    )
                    r = min(r, 8 - r)
                    if r >= self.min_radius:
                        shapes.append(p.buffer(r - r * 0.2))
                        break

                if (self.shape == -1 and t < 0.67) or self.shape == 1:
                    x, y = vsk.random(-6, 6), vsk.random(-7, 7)
                    x1, y1 = vsk.random(x, 6), vsk.random(y, 7)
                    if (x1 - x) <= self.min_radius or (y1 - y) <= self.min_radius:
                        continue
                    shapes.append(box(x, y, x1, y1))
                    break

                if (self.shape == -1 and t <= 1.0) or self.shape == 2:
                    x, y = vsk.random(-6, 6), vsk.random(-7, 7)
                    r = vsk.random(1, 2.5)

                    a = vsk.random(math.pi)
                    ax, ay = x + r * math.cos(a), y + r * math.sin(a)
                    bx, by = x + r * math.cos(a + math.pi / 3), y + r * math.sin(
                        a + math.pi / 3
                    )
                    cx, cy = x + r * math.cos(a + 2 * math.pi / 3), y + r * math.sin(
                        a + 2 * math.pi / 3
                    )
                    shapes.append(Polygon([(ax, ay), (bx, by), (cx, cy)]))
                    break

        shapes = unary_union(shapes)

        for r in range(self.y_divisions):
            y = vsk.map(r, 0, self.y_divisions, -8, 8)

            x = -8 + vsk.random(0.4)
            while x < 8:
                d = vsk.random(0.2, 1)
                l = LineString([(x, y), (x + d, y)]).difference(shapes)
                l = scale(l, 0.9)

                if vsk.random(1) < r / self.y_divisions:
                    vsk.geometry(l)
                x += d

            l = LineString([(-8, y), (8, y)]).intersection(shapes.buffer(-0.1))

            xx = -8
            mask = [xx]
            while xx < 8:
                xx += vsk.random(0.3, 0.7)
                mask.append(xx)

            mask = MultiLineString([[(xx, -8), (xx, 8)] for xx in mask])

            t = 0.1 + 0.1 * r / self.y_divisions
            vsk.geometry(l.difference(mask.buffer(t)))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day02Sketch.display()
