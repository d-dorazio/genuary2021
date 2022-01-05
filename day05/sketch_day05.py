import math

import vsketch

from shapely.geometry import Polygon


def edge_lerp(poly, i, t):
    ax, ay = poly[i]
    bx, by = poly[(i + 1) % len(poly)]
    return ax + (bx - ax) * t, ay + (by - ay) * t


def edge_length2(poly, i):
    ax, ay = poly[i]
    bx, by = poly[(i + 1) % len(poly)]
    return (bx - ax) ** 2 + (by - ay) ** 2


def split_quad(poly, e0, e1, t):
    p0 = edge_lerp(poly, e0, t)
    p1 = edge_lerp(poly, e1, t)

    poly0 = [poly[e0], p0, p1]
    i = (e1 + 1) % len(poly)
    while True:
        poly0.append(poly[i])
        if i == e0:
            break
        i = (i + 1) % len(poly)

    poly1 = [poly[e1], p1, p0]
    i = (e0 + 1) % len(poly)
    while True:
        poly1.append(poly[i])
        if i == e1:
            break
        i = (i + 1) % len(poly)

    return [poly0, poly1]


def rect(w, h):
    return [
        (-w / 2, -h / 2),
        (w / 2, -h / 2),
        (w / 2, h / 2),
        (-w / 2, h / 2),
    ]


def triangle(side):
    return [
        (0, -side / 2),
        (-side / 2, side / 2),
        (side / 2, side / 2),
    ]


def hexagon(r):
    a = math.sqrt(3) / 2
    coords = [(-0.5, -a), (0.5, -a), (1, 0), (0.5, a), (-0.5, a), (-1, 0)]
    return [(x * r, y * r) for x, y in coords]


class Day05Sketch(vsketch.SketchClass):
    shape = vsketch.Param("square", choices=["square", "triangle", "hexagon"])

    width = vsketch.Param(16.0)
    height = vsketch.Param(16.0)

    cuts = vsketch.Param(20)
    columns = vsketch.Param(1)
    min_erosion = vsketch.Param(0.1)
    max_erosion = vsketch.Param(0.5)
    min_area = vsketch.Param(0.1)
    padding = vsketch.Param(0.0)
    progress = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        for r in range(self.columns):
            if self.shape == "square":
                polygons = [rect(self.width, self.height)]
            elif self.shape == "triangle":
                polygons = [triangle(min(self.width, self.height))]
            elif self.shape == "hexagon":
                polygons = [hexagon(min(self.width, self.height) / 2)]

            snapshots = [[polygons[0][:]]]

            for _ in range(self.cuts):
                # random.shuffle(polygons)
                poly = max(polygons, key=lambda p: Polygon(p).area)
                polygons.remove(poly)

                edges = sorted(
                    range(len(poly)),
                    key=lambda i: (edge_length2(poly, i) * vsk.random(0.98, 1)),
                    reverse=True,
                )
                e0, e1 = edges[0], edges[1]

                t = vsk.random(0.3, 0.7)
                polygons.extend(split_quad(poly, e0, e1, t))

                snapshots.append(polygons[:])

            for i, polygons in enumerate(
                snapshots if self.progress else snapshots[-1:]
            ):
                vsk.pushMatrix()
                vsk.translate(
                    self.width / 2 + r * (self.padding + self.width),
                    self.height / 2 + i * (self.padding + self.height),
                )

                for poly in polygons:
                    p = Polygon(poly).buffer(
                        -vsk.random(self.min_erosion, self.max_erosion)
                    )

                    if p.area < self.min_area:
                        continue

                    vsk.geometry(p)

                vsk.popMatrix()

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day05Sketch.display()
