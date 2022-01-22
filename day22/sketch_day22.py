import vsketch

import random
import time


class Day22Sketch(vsketch.SketchClass):
    t = vsketch.Param(-1)
    rows = vsketch.Param(10)
    cols = vsketch.Param(40)
    spacing = vsketch.Param(0.1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        rows, cols = self.rows, self.cols
        if self.t == 0:
            t = int(time.time())
            rows, cols = 4, 8
        elif self.t < 0:
            t = sum((random.randrange(2) * 2 ** i for i in range(rows * cols)))
        else:
            t = self.t
            rows, cols = 4, 8

        bits = [int(b) for b in bin(t)[2:].rjust(32, "0")]

        w, h = 16 / cols, 26 / rows

        for r in range(rows):
            for c in range(cols):
                i = len(bits) - 1 - (r * cols + c)

                x0, y0 = c * w, r * h
                x1, y1 = x0 + w, y0 + h
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2

                if bits[i] == 1:
                    for j in range(-6, 7):
                        dx, dy = self.spacing * w * j, self.spacing * h * j
                        vsk.line(x0, my - dy, mx + dx, y0)
                        vsk.line(mx + dx, y1, x1, my - dy)
                else:
                    for j in range(-6, 7):
                        dx, dy = self.spacing * w * j, self.spacing * h * j
                        vsk.line(x0, my + dy, mx + dx, y1)
                        vsk.line(mx + dx, y0, x1, my + dy)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day22Sketch.display()
