import random
import vsketch

from shapely.geometry import *
import numpy as np


class Day20Sketch(vsketch.SketchClass):
    lines = vsketch.Param(100)
    sky_segs = vsketch.Param(30)
    amplitude = vsketch.Param(4)
    moon_segs = vsketch.Param(150)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        mb = vsk.random(6, 10) + vsk.random(1, 2)

        sky = []
        for y in np.linspace(0, mb * 0.87, self.lines // 10 * 2):
            n = random.randrange(1, self.sky_segs)
            for _ in range(n):
                x0 = vsk.random(0, 15)
                x1 = x0 + vsk.random(0.3, 1)
                sky.append([(x0, y), (x1, y)])

        lh = self.amplitude * 26 / self.lines
        lines = []
        for y in np.linspace(mb * 0.95, 26, self.lines // 10 * 8):
            l = []
            to_skip = random.randrange(0, 10)
            for x in np.linspace(0, 16, 100):
                if to_skip > 0:
                    to_skip -= 1
                    continue
                l.append((x, y - lh * vsk.noise(x * 2.35, y * 2.35)))
                if len(l) > 2 and vsk.random(1) > 0.7:
                    lines.append(l)
                    l = []
                    to_skip = random.randrange(4, 10)
            if len(l) > 2:
                lines.append(l)

        vsk.geometry(MultiLineString(sky))
        vsk.geometry(MultiLineString(lines))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day20Sketch.display()
