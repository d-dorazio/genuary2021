import vsketch
import random
from shapely.geometry import *
import numpy as np


def sign(n):
    return -1 if n < 0 else 1


class Day18Sketch(vsketch.SketchClass):
    vlines = vsketch.Param(3)
    hlines = vsketch.Param(3)
    thickness = vsketch.Param(0.2)

    def vertical(self, vsk):
        p = [(random.randrange(-7, 8), 0)]
        while p[-1][1] < 26 and abs(p[-1][0]) < 8:
            x, y = p[-1]
            dx, dy = random.randrange(-1, 2), random.randrange(1, 7)
            p.append((x, y + dy))
            p.append((x + dx, y + dy))

        p = [(sign(x) * min(abs(x), 8), min(26, y)) for x, y in p]
        return p

    def horizontal(self, vsk):
        p = [(-7, random.randrange(22))]

        while p[-1][1] < 26 and abs(p[-1][0]) < 8:
            x, y = p[-1]
            dx, dy = random.randrange(3, 7), random.randrange(-1, 2)
            p.append((x + dx, y))
            p.append((x + dx, y + dy))

        p = [(sign(x) * min(abs(x), 8), min(26, y)) for x, y in p]
        return p

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        lines = []
        for _ in range(self.vlines):
            lines.append(self.vertical(vsk))

        for _ in range(self.hlines):
            lines.append(self.horizontal(vsk))

        lls = []
        for l in lines:
            ll = LineString(l).buffer(self.thickness * 2)
            for p in lls:
                ll = ll - p
                if ll.is_empty or not ll.is_valid:
                    break

            if not ll.is_empty and ll.is_valid:
                lls.append(ll)

        dd, dh, da = 0.1, 0.3, 0.2

        diags = MultiLineString(
            [[(x, -1), (x + 20, 30)] for x in np.linspace(-30, 30, int(60 / dd))]
        )
        horzs = MultiLineString(
            [[(-10, y), (10, y)] for y in np.linspace(-1, 30, int(31 / dh))]
        )
        adiags = MultiLineString(
            [[(x, -1), (x - 20, 30)] for x in np.linspace(-30, 30, int(60 / da))]
        )

        for p in lls:
            p = p.buffer(-self.thickness)
            color = random.randrange(3)
            texture = [diags, horzs, adiags][color]
            vsk.stroke(color + 1)
            vsk.geometry(p)

            vsk.geometry(texture & p)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day18Sketch.display()
