import math
import vsketch

import numpy as np

from shapely.geometry import *
from shapely.ops import *


class Day17Sketch(vsketch.SketchClass):
    points = vsketch.Param(10)
    max_erosion = vsketch.Param(0.7)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        pts = []
        for _ in range(self.points):
            a = vsk.random(math.pi * 2)
            r = vsk.random(10)
            pts.append((r * math.cos(a), r * math.sin(a)))

        pts = MultiPoint(pts)
        vor = voronoi_diagram(pts)

        dd, dh, dv = 0.1, 0.3, 0.5

        diags = MultiLineString(
            [[(x, -14), (x + 20, 14)] for x in np.linspace(-28, 28, int(28 / dd))]
        )
        horzs = MultiLineString(
            [[(-10, y), (10, y)] for y in np.linspace(-14, 14, int(28 / dh))]
        )
        verts = MultiLineString(
            [[(x, -14), (x, 14)] for x in np.linspace(-10, 10, int(20 / dv))]
        )

        for v in vor.geoms:
            v &= Point(0, 0).buffer(9)
            v = v.buffer(-vsk.random(0.1, self.max_erosion))
            vsk.geometry(v)

            ti = vsk.random(1)
            if ti <= 0.33:
                vsk.geometry(diags & v)
            elif ti <= 0.67:
                vsk.geometry(horzs & v)
            else:
                vsk.geometry(verts & v)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day17Sketch.display()
