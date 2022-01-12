import vsketch

import random
import math

from shapely.geometry import *


class Day11Sketch(vsketch.SketchClass):
    divisions = vsketch.Param(100)
    padding = vsketch.Param(0.1)
    min_size = vsketch.Param(0.1)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.rectMode("corners")
        rects = [(0, 0, 14, 20)]

        for _ in range(self.divisions):
            i = random.choices(
                range(len(rects)), weights=[(r - l) * (b - t) for l, t, r, b in rects]
            )[0]
            l, t, r, b = rects[i]
            w, h = r - l, b - t

            mins = self.padding * 2 + self.min_size

            if vsk.random(1) > (h / w) / 2:
                k = vsk.random(0.1, 0.9)
                if w * min(k, 1 - k) < mins:
                    continue
                rects.extend(
                    (
                        (l, t, l + k * w, b),
                        (l + k * w, t, r, b),
                    )
                )
            else:
                k = vsk.random(0.1, 0.9)
                if h * min(k, 1 - k) < mins:
                    continue
                rects.extend(
                    (
                        (l, t, r, t + k * h),
                        (l, t + k * h, r, b),
                    )
                )

            rects.pop(i)

        wa, wb, wd = random.randrange(1, 10), random.randrange(1, 10), vsk.random(1, 3)

        def warp(x, y):
            x, y = x * math.sqrt(1 - y ** wa / wd), y * math.sqrt(1 - x ** wb / wd)
            return x, y

        for r in rects:
            rr = box(*r).buffer(-self.padding)
            if not rr.is_valid:
                continue

            p = []
            for (x0, y0), (x1, y1) in zip(
                rr.boundary.coords, rr.boundary.coords[1:] + [rr.boundary.coords[0]]
            ):
                t = 0
                while t <= 1.0:
                    x = x0 + t * (x1 - x0)
                    y = y0 + t * (y1 - y0)
                    x, y = warp((x - 7) / 7, (y - 10) / 10)
                    p.append((x * 8, y * 12))
                    t += 0.1

            vsk.polygon(p)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day11Sketch.display()
