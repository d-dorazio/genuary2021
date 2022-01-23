import math
import vsketch
import random

import numpy as np
from shapely.geometry import *
from shapely.affinity import *


def lerp(a, b, t):
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


class Day23Sketch(vsketch.SketchClass):
    corner_cuts = vsketch.Param(4)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        l, t, r, b = -6, -6, 6, 6

        flower = box(l, t, r, b)
        petals = []

        pts = flower.boundary.coords[:-1]
        for i in range(4):
            for _ in range(self.corner_cuts):
                a, b, c = (
                    pts[(i - 1 + len(pts) % len(pts))],
                    pts[i],
                    pts[(i + 1) % len(pts)],
                )
                t0 = vsk.random(0.2, 0.8)
                t1 = vsk.random(0.2, 0.8)

                d, e = lerp(b, a, t0), lerp(b, c, t1)
                petal = Polygon([d, b, e]) - MultiPolygon(petals)
                if petal.area < 1.5:
                    continue
                flower = (flower - petal).buffer(-vsk.random(0.1, 0.3))
                petals.append(petal)

        flower = rotate(flower, 45, origin=(0, 0))
        petals = [
            rotate(
                p.buffer(-0.2),
                45,
                origin=(0, 0),
            )
            for p in petals
        ]
        _, _, _, b = flower.bounds
        petals = [
            rotate(
                p,
                math.atan2(p.centroid.y, p.centroid.y) / 10,
                origin=(0, b),
                use_radians=True,
            )
            & box(-16, -20, 16, 4.9)
            for p in petals
            if p.centroid
        ]

        diags = MultiLineString(
            [[(x - 8, -13), (8 + x, 13)] for x in np.linspace(-16, 16, 100)]
        )
        adiags = MultiLineString(
            [[(x + 8, -13), (x - 8, 13)] for x in np.linspace(-16, 16, 100)]
        )
        hor = MultiLineString([[(-10, y), (10, y)] for y in np.linspace(-13, 13, 200)])

        vsk.geometry(flower)
        for p in petals:
            texture = random.choice([diags, hor, adiags])
            vsk.geometry(texture & p)
            vsk.geometry(p)

        x0, y0 = 0, 5.3
        x1, y1 = x0 + vsk.random(-3, 3), 13

        l = LineString(
            [
                (x0, y0),
                (x1, y1),
            ]
        ).buffer(0.15, cap_style=2)
        vsk.geometry(l)
        vsk.geometry(hor & l)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day23Sketch.display()
