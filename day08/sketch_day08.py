import vsketch

import numpy as np


class Day08Sketch(vsketch.SketchClass):
    points = vsketch.Param(80)
    hlines = vsketch.Param(50)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.scale(1, -1)

        xs = np.linspace(0, 16, self.points)
        ys = vsk.noise(xs / 16 * 3) * 24

        vsk.polygon(zip(xs, ys))

        for x, y in zip(xs, ys):
            vsk.line(x, 24, x, y)

        for t in np.linspace(0, 1, self.hlines):
            t = t ** 0.5
            vsk.polygon(((x, y * t) for x, y in zip(xs, ys)))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day08Sketch.display()
