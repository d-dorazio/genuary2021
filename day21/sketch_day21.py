import vsketch
import random
import numpy as np
from shapely.geometry import *
from shapely.ops import voronoi_diagram

from skimage.measure import find_contours


class Day21Sketch(vsketch.SketchClass):
    xs = vsketch.Param(400)
    ys = vsketch.Param(200)
    n = vsketch.Param(18)
    points = vsketch.Param(30)
    max_erosion = vsketch.Param(0.7)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

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

        res = find_contours(np.array(grid), 0.9)
        res = MultiLineString(
            [[(x / self.xs * 16, y / self.ys * 28) for y, x in l] for l in res]
        )
        pts = np.random.random((self.points, 2)) * (16, 28)
        vor = MultiPolygon(
            [
                p.buffer(-vsk.random(0.1, self.max_erosion)) & box(0, 0, 16, 28)
                for p in voronoi_diagram(MultiPoint(pts)).geoms
            ]
        )
        vsk.geometry(vor)
        vsk.geometry(res & vor)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day21Sketch.display()
