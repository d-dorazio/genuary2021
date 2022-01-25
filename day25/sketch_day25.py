import vsketch

import numpy as np

from shapely.geometry import *
from shapely.affinity import *


class Day25Sketch(vsketch.SketchClass):
    lines = vsketch.Param(200)
    padding = vsketch.Param(0.1)
    ampli = vsketch.Param(10.0)
    kt = vsketch.Param(0.999, decimals=4)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        line = LineString(
            [(x, vsk.noise(x * 0.05) * self.ampli) for x in np.linspace(0, 16, 100)]
        )

        k = 1
        for i in range(self.lines):
            l, t, r, b = line.bounds
            if r - l <= 0.0 or i * self.padding + b - t > 26:
                break

            vsk.geometry(line)
            vsk.translate(0, self.padding)
            line = scale(line, k, 1)
            k *= self.kt

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day25Sketch.display()
