import random
import itertools
import vsketch

import numpy as np

from shapely.geometry import *
from shapely.affinity import *


class Day09Sketch(vsketch.SketchClass):
    room_prob = vsketch.Param(0.4)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        vsk.scale(1, -1)

        rows = []
        y = 0
        while True:
            h = vsk.random(1.5, 3.5)
            if y + h > 24:
                break

            cells = []
            x = vsk.random(1)
            while True:
                w = vsk.random(1, 5)
                if x + w > 16:
                    break

                def is_below(p):
                    l, _, r, _ = p.bounds
                    return l <= x <= r or l <= x + w <= r

                if vsk.random(1) > (1 - self.room_prob) and (
                    not rows or any((is_below(p) for p in rows[-1]))
                ):
                    cells.append(box(x, y, x + w, y + h))
                x += w

            rows.append(cells)
            y += h

        decorations = []
        for row in rows:
            decs = []

            for room in row:
                poly = []

                d = room.buffer(-vsk.random(0.9, 1.3))
                if d.area > 0.4:
                    x0, y0, _, _ = room.bounds
                    l, t, _, _ = d.bounds
                    dx, dy = (
                        0.3 + vsk.random((l - x0 - 0.4) * 2),
                        0.3 + vsk.random((t - y0 - 0.4) * 2),
                    )
                    d = translate(d, -(l - x0) + dx, -(t - y0) + dy)
                    poly.append(d)

                decs.append(MultiPolygon(poly))

            decorations.append(decs)

        vsk.line(-1, 0, 17, 0)
        for i, r, ds in zip(itertools.count(), rows, decorations):
            for c, d in zip(r, ds):
                room = Polygon(
                    c.boundary.coords,
                    holes=[dd.boundary.coords for dd in d.geoms],
                )
                vsk.geometry(room)

                l, t, r, b = room.bounds

                lines = []
                if vsk.random(1) > i / len(rows):
                    w = vsk.random(0.5)
                    lines.append([(l, b - 0.1), (l + w / 3, b - 0.1)])
                    lines.append([(l, b - 0.2), (l + w / 3 * 2, b - 0.2)])
                    lines.append([(l, b - 0.3), (l + w, b - 0.3)])

                if vsk.random(1) > (1 - i / len(rows)):
                    h = vsk.random(0.1, 0.9 * (b - t))
                    lines.append([(l + 0.1, b), (l + 0.1, b - h / 3)])
                    lines.append([(l + 0.2, b), (l + 0.2, b - h / 2)])
                    lines.append([(l + 0.3, b), (l + 0.3, b - h)])

                vsk.geometry(MultiLineString(lines) & room)

                dec_lines = []
                if vsk.random(1) > 0.7:
                    dec_lines.extend(
                        [
                            [(x, 0), (x, 100)]
                            for x in np.linspace(l, r, random.randrange(15, 40))
                        ]
                    )

                if vsk.random(1) > 0.4:
                    dec_lines.extend(
                        [
                            [(0, y), (100, y)]
                            for y in np.linspace(t, b, random.randrange(15, 40))
                        ]
                    )

                vsk.geometry(MultiLineString(dec_lines) & MultiPolygon(d))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day09Sketch.display()
