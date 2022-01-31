import vsketch

import numpy as np
from shapely.geometry import *
from shapely.affinity import *


class Day31Sketch(vsketch.SketchClass):
    lines = vsketch.Param(10)
    probd = vsketch.Param(0.2)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        parts = MultiPolygon([box(0, 0, 16, 26)])

        for i in range(self.lines):
            if i % 2 == 0:
                xs = np.linspace(0, 16, 100)
                ys = vsk.noise(xs * 0.03, vsk.random(1800)) * 26
            else:
                ys = np.linspace(0, 26, 200)
                xs = vsk.noise(ys * 0.03, vsk.random(1800)) * 16

            l = LineString(zip(xs, ys))

            parts = parts - l.buffer(0.15)

        def break_line(x0, y0, x1, y1, mint=0.2, maxt=0.5):
            line = LineString([(x0, y0), (x1, y1)])
            s = 0
            p = (x0, y0)
            while s < line.length:
                s += vsk.random(mint, maxt)
                pp = line.interpolate(s)
                yield LineString([p, pp])

                s += vsk.random(0.1, 0.2)
                p = line.interpolate(s)

        diags = MultiLineString(
            [
                l
                for x in np.arange(-32, 16, 0.1)
                for l in break_line(x, 0, x, 26, 0.6, 1.3)
                if vsk.random(1) > 0.2
            ]
        )
        adiags = MultiLineString(
            [
                l
                for x in np.arange(0, 32, 0.15)
                for l in break_line(x, 0, x - 16, 26, 0.8, 1.5)
                if vsk.random(1) > self.probd
            ]
        )
        for i, g in enumerate(parts.geoms):
            tex = diags if i % 2 == 0 else adiags
            vsk.geometry(tex & g)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day31Sketch.display()
