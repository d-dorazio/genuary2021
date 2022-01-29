import vsketch
import math

from shapely.geometry import *
from shapely.affinity import *


class Day29Sketch(vsketch.SketchClass):
    lines = vsketch.Param(30)
    reps = vsketch.Param(1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        dx, dy = math.sqrt(3) / 2, 0.5
        lx, ly = 16 / dx, 26 / dy
        vsk.scale(dx, dy)

        lines = []

        for li in range(self.lines):
            if li % 3 == 0:
                x, y = vsk.random(-lx / 2 + 0.1, lx / 2 - 0.1), -ly / 2 + 0.1
                line = [(x, y)]
                while abs(y) < ly / 2:
                    dy = vsk.random(0.5, 2)
                    line.append((x, y + dy))
                    y += dy
                    if abs(y) >= ly / 2:
                        break

                    i = vsk.random(-0.8, 0.8)
                    if abs(x + i) > lx / 2 or abs(y + i) > ly / 2:
                        break
                    line.append((x + i, y + abs(i)))
                    x += i
                    y += abs(i)
            else:
                x, y = -lx / 2 + 0.1, vsk.random(-ly / 2 + 0.1, ly / 2 - 0.1)
                line = [(x, y)]
                while abs(x) < lx / 2:
                    dx = vsk.random(0.5, 2)
                    line.append((x + dx, y))
                    x += dx
                    if abs(x) >= lx / 2:
                        break

                    i = vsk.random(-1.8, 1.8)
                    if abs(x + i) > lx / 2 or abs(y + i) > ly / 2:
                        break
                    line.append((x + abs(i), y + i))
                    x += abs(x)
                    y += i

            lines.append(LineString(line))

        drawn = []

        def draw_l(l):
            for p in drawn:
                l -= p.buffer(0.3)
            l = l.geoms if isinstance(l, MultiLineString) else [l]
            for ll in l:
                if ll.length > 0.7:
                    vsk.geometry(ll)
                    drawn.append(ll)

        for l in lines:
            draw_l(l)
            for r in range(1, self.reps):
                draw_l(translate(l, 0.35 * r, 0.35 * r))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day29Sketch.display()
