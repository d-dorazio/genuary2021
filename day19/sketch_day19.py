import vsketch

import math
import random
import numpy as np
from shapely.geometry import *


class Day19Sketch(vsketch.SketchClass):
    cols = vsketch.Param(300)
    rows = vsketch.Param(100)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        def text(w, h, rows, cols):
            lines = []

            paragraph_lines = random.randrange(8, 20)
            empty_lines = 0

            for y0 in np.linspace(0, h, rows):
                empty_lines -= 1
                if empty_lines > 0:
                    continue

                paragraph_lines -= 1

                l = []
                xstart = 0
                to_skip = 0
                for x in np.linspace(0, w, cols):
                    if to_skip > 0:
                        to_skip -= 1
                        xstart = x
                        continue

                    y = y0 + vsk.random(0, h / rows)
                    l.append((x, y))

                    if min(x - xstart, 9) / 9 > vsk.random(1):
                        lines.append(l)
                        xstart = x
                        l = []
                        to_skip = random.randrange(2, 5)

                    if paragraph_lines <= 3 and x > w * 0.7 and vsk.random(1) > 0.8:
                        paragraph_lines = 0
                        break

                if l:
                    lines.append(l)

                if paragraph_lines == 0:
                    empty_lines = 2
                    paragraph_lines = random.randrange(8, 20)

            for l in lines:
                vsk.polygon(l)

        with vsk.pushMatrix():
            vsk.translate(12, 0)
            text(3, 2, 4, 100)

        vsk.translate(0, 4)
        text(16, 16, self.rows, self.cols)

        vsk.translate(10, 17)
        text(6, 1, 1, 100)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day19Sketch.display()
