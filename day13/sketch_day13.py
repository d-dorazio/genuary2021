import vsketch

import random
import numpy as np

from skimage.measure import find_contours


class Day13Sketch(vsketch.SketchClass):
    xs = vsketch.Param(400)
    ys = vsketch.Param(200)
    n = vsketch.Param(18)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("800x400", landscape=False)

        n = random.randrange(256) if self.n < 0 else self.n

        grid = []
        for si in range(self.ys):
            if not grid:
                grid.append([random.randrange(2) for _ in range(self.xs)])
                continue

            prev = grid[si - 2] if si > 1 else [0 for _ in range(self.xs)]
            current = grid[si - 1]
            new_state = []

            for i in range(self.xs):
                m = current[i] << 1
                if i > 0:
                    m |= current[i - 1] << 2
                if i < len(current) - 1:
                    m |= current[i + 1]

                s = (n >> m) & 1
                new_state.append(s ^ prev[i])

            grid.append(new_state)

        for i in range(4):
            y = (i + 1) * self.ys // 5
            for dy in range(3):
                for x in range(self.xs):
                    grid[y + dy][x] = 0

        res = find_contours(np.array(grid), 0.9)

        vsk.scale(800 / self.xs, 400 / self.ys)
        for l in res:
            vsk.polygon(((x, y) for y, x in l))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day13Sketch.display()
