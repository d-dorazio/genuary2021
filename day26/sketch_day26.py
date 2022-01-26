import vsketch
import random

import numpy as np
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import *


class Day26Sketch(vsketch.SketchClass):
    size = vsketch.Param(0.25)
    texture_lines = vsketch.Param(40)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        pts = {(random.randrange(0, 4), random.randrange(0, 6)) for _ in range(7)}

        rects = [box(x - 0.5, y - 0.5, x + 0.5, y + 0.5) for x, y in pts]
        _, _, r, b = MultiPolygon(rects).bounds
        rects += [scale(rr, -1, 1, origin=(r, b)) for rr in rects]
        rects += [scale(rr, 1, -1, origin=(r, b)) for rr in rects]

        pattern = unary_union(MultiPolygon(rects))
        if isinstance(pattern, Polygon):
            pattern = MultiPolygon([pattern])

        pattern = scale(pattern, self.size, self.size)
        l, t, r, b = pattern.bounds
        w, h = r - l, b - t

        texture = [
            (LineString([(x, t), (x + (r - l), b)]) & box(l, t, r, b)) - pattern
            for x in np.linspace(l - (r - l), r, self.texture_lines)
        ]

        y = 0
        while y + h < 26:
            x = 0
            while x + w < 16:
                with vsk.pushMatrix():
                    vsk.translate(x, y)
                    for g in pattern.geoms:
                        vsk.geometry(g)
                    for g in texture:
                        vsk.geometry(g)
                x += w

            y += h

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day26Sketch.display()
