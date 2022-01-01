import vsketch
import math
import numpy as np


class Day01Sketch(vsketch.SketchClass):
    yDivs = vsketch.Param(100)
    xDivs = vsketch.Param(50)
    l = vsketch.Param(0.8)
    t = vsketch.Param(0.1, 0.0, 0.5)
    symmetric = vsketch.Param(1, 0, 1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        ys = np.linspace(-13, 13, self.yDivs)
        xs = np.linspace(-8, 8, self.xDivs)

        if self.symmetric:
            angs = vsk.noise(ys, xs)
        else:
            angs = vsk.noise(ys - ys[0], xs - xs[0])

        grid = [
            [
                (x + self.l * math.cos(angs[r][c]), y + self.l * math.sin(angs[r][c]))
                for c, x in enumerate(xs)
            ]
            for r, y in enumerate(ys)
        ]

        for line in grid:
            for (x0, y0), (x1, y1) in zip(line, line[1:]):
                x0, x1 = vsk.lerp(x0, x1, self.t), vsk.lerp(x0, x1, 1 - self.t)
                vsk.line(x0, y0, x1, y1)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day01Sketch.display()
