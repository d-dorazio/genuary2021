import vsketch

import numpy as np
from shapely.geometry import *
from shapely.ops import *


def clamp(v, a, b):
    return min(b, max(v, a))


class Day15Sketch(vsketch.SketchClass):
    lines = vsketch.Param(10)
    ampli = vsketch.Param(4)

    def break_line(self, vsk, lg, density):
        step = min(0.01, lg.length / 100.0)
        t = vsk.random(0.01, step)
        while t <= 1.0:
            tt = min(1.0, t + vsk.random(0.01, step))
            pp, cp = (
                lg.interpolate(t, normalized=True),
                lg.interpolate(tt, normalized=True),
            )

            if vsk.random(1) < density:
                yield pp, cp

            t = tt + vsk.random(0.01, step)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        def hor(h):
            z = vsk.random(10 ** 3)
            xs = np.linspace(0, 16, 200)
            ys = vsk.noise(z + xs / 16) * h
            return xs, ys

        lines = []
        dunes = []

        for i in reversed(range(self.lines)):
            xs, ys = hor(28 / (self.lines - 1) * self.ampli)
            ys += 20 / self.lines * i

            pts = [(0, 20)]
            pts.extend(((clamp(x, 0, 16), clamp(y, 0, 20)) for x, y in zip(xs, ys)))
            pts.append((16, 20))
            pts.append(pts[0])

            lines.append(pts)
            geo = Polygon(pts)

            if not dunes:
                dunes.append(geo)
                continue

            for l in dunes:
                geo = geo - l
            dunes.append(geo)

        r = box(0.1, 0.1, 15.9, 27.9)
        for p, l in zip(dunes, lines):
            density = vsk.random(0.1, min(p.length, 1) * 0.2)

            while True:
                l = [(x, y + density) for x, y in l]
                g = LineString(l) & p & r

                if not g.is_valid or g.length < 0.3:
                    break

                lines = g.geoms if isinstance(g, GeometryCollection) else [g]
                for lg in lines:
                    lgs = lg.geoms if isinstance(lg, MultiLineString) else [lg]
                    for lg in lgs:
                        if isinstance(lg, Point):
                            continue
                        for a, b in self.break_line(vsk, lg, 1 - density):
                            vsk.line(a.x, a.y, b.x, b.y + vsk.random(0.01))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day15Sketch.display()
