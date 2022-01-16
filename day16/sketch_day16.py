import vsketch
import math

import numpy as np


class Day16Sketch(vsketch.SketchClass):
    xdivs = vsketch.Param(200)
    ydivs = vsketch.Param(100)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        ta, tb = vsk.random(2), vsk.random(5)

        for x in np.linspace(0, 16, self.xdivs):
            for i in range(self.ydivs):
                xt = 1 - min(x / 16, (16 - x) / 16)
                yt = 1 - min(i / self.ydivs, (self.ydivs - i) / self.ydivs)
                # xt = 16 / x
                # yt = 1 - i / self.ydivs

                t = (xt ** ta) * (yt ** tb)
                if vsk.random(1) > t:
                    continue

                h = 26 / self.ydivs
                vsk.line(x, i * h, x, i * h + h)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day16Sketch.display()
