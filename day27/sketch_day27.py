import vsketch
import random

from shapely.geometry import *
from shapely.ops import *
from shapely.affinity import *


class Day27Sketch(vsketch.SketchClass):
    lines = vsketch.Param(
        10,
        0,
    )

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        if self.lines == 0:
            data = [
                [int(b) for b in bin(int(c, 16))[2:]]
                for c in ("2E294E", "541388", "F1E9DA", "FFD400", "D90368")
            ]
        else:
            data = [[random.randrange(2) for _ in range(24)] for _ in range(self.lines)]

        lines = []
        for i, bits in enumerate(data):
            if i % 2 == 0:
                line = [(0, 0)]
                for b in bits:
                    x, y = line[-1]
                    x, y = x + b * 2 - 1, y + 1

                    if abs(x) > 8:
                        break

                    line.append((x, y))
            else:
                line = [(-8, 12)]
                dx = 1
                for b in bits:
                    x, y = line[-1]
                    x, y = x + dx, y + b * 2 - 1

                    if y < 0 or y > 24:
                        break
                    if x > 12:
                        dx = -1

                    line.append((x, y))

            lines.append(LineString(line))

        prev = []
        for l in lines:
            t = vsk.random(0.7, 0.95)
            l = scale(l, t, t)
            for p in prev:
                l -= p
            vsk.geometry(l)
            prev.append(l.buffer(0.3))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day27Sketch.display()
