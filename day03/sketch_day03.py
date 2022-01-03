import math
import itertools

import vsketch

import numpy as np

from shapely.geometry import MultiPoint, box, MultiPolygon, LineString, Point
from shapely.ops import voronoi_diagram, triangulate, unary_union


class Day03Sketch(vsketch.SketchClass):
    divs = vsketch.Param(15)
    radius = vsketch.Param(60)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        ys = np.linspace(-13, 13, self.divs)
        xs = np.linspace(-9, 9, self.divs)

        angs = vsk.noise(ys, xs)

        points = MultiPoint(
            [
                (x, y)
                for r, yy in enumerate(ys)
                for x, y in [
                    (
                        xx + self.radius * math.cos(angs[r][c]),
                        yy + self.radius * math.sin(angs[r][c]),
                    )
                    for c, xx in enumerate(xs)
                ]
            ]
        )

        l, t, r, b = points.bounds
        cx, cy = (l + r) / 2, (t + b) / 2

        vsk.translate(cx, cy)

        polygons = MultiPolygon((p.buffer(-0.1) for p in voronoi_diagram(points).geoms))
        polygons &= box(cx - 9, cy - 13, cx + 9, cy + 13)

        # vsk.stroke(2)
        # vsk.geometry(polygons)
        # for p in polygons.geoms:
        #     vsk.point(p.centroid.x, p.centroid.y)
        # vsk.stroke(1)

        astros = []
        stars = []
        lines = []
        points = [(p.centroid, p.area) for p in polygons.geoms]
        while points:
            largest = max(range(len(points)), key=lambda i: points[i][1])

            l = [points[largest][0]]
            points.pop(largest)

            while points:
                i = min(range(len(points)), key=lambda i: l[-1].distance(points[i][0]))
                p, _ = points[i]

                lr = LineString(l + [p])
                if not lr.is_simple:
                    stars.append(p)
                    break

                if any((ll.intersects(lr) for ll in lines)):
                    stars.append(p)
                    break

                points.pop(i)

                l.append(p)

                if vsk.random(1) > 0.8:
                    break

            if len(l) > 1:
                lines.append(LineString(l).buffer(0.1))

            if len(l) > 3:
                astros.append(lines[-1].buffer(-0.05))
            else:
                stars.extend(l)

        vsk.fill(1)
        while astros:
            astro = astros.pop()

            while True:
                closest = min(astros, key=lambda a: a.distance(astro), default=None)
                if closest is None:
                    break

                d = closest.distance(astro)
                if d >= 0.8:
                    break

                astros.remove(closest)

                mind = None
                pa, pb = None, None
                for (ax, ay), (bx, by) in itertools.product(
                    astro.boundary.coords, closest.boundary.coords
                ):
                    a, b = Point(ax, ay), Point(bx, by)
                    d = a.distance(b)
                    if mind is None or d < mind:
                        mind = d
                        pa, pb = a, b

                if pa is not None and pb is not None:
                    astro = unary_union(
                        [astro, closest, LineString([pa, pb]).buffer(0.07)]
                    )

            vsk.geometry(astro)

        for p in stars:
            vsk.circle(p.x, p.y, 0.2)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day03Sketch.display()
