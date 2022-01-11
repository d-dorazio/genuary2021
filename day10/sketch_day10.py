import vsketch

import random
import numpy as np


class Day10Sketch(vsketch.SketchClass):
    numbers = vsketch.Param(10)
    bits = vsketch.Param(10)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        xs = np.linspace(0, 16, self.numbers)

        i = 1
        for x0, x1 in zip(xs, xs[1:]):
            ys = np.linspace(0, 24, random.randrange(i, i * 5))
            i += 1
            for y0, y1 in zip(ys, ys[1:]):
                if vsk.random(1) > 0.5:
                    mx = (x0 + x1) / 2
                    vsk.line(mx, y0, mx, y1)
                else:
                    vsk.line(x1, y0, x0, y1)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day10Sketch.display()
