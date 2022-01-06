import math

import vsketch

import numpy as np

from shapely.geometry import *
from shapely.ops import *
from shapely.strtree import STRtree


def occult(lines, tolerance):
    lines = list(MultiLineString(lines).geoms)

    tree = STRtree(lines)
    index_by_id = {id(poly): i for i, poly in enumerate(lines)}

    for i, line in enumerate(lines):
        coords = np.array(line.coords)

        if not (
            len(coords) > 3
            and math.hypot(coords[-1, 0] - coords[0, 0], coords[-1, 1] - coords[0, 1])
            < tolerance
        ):
            continue

        p = Polygon(coords)
        geom_idx = [index_by_id[id(g)] for g in tree.query(p)]
        geom_idx = [idx for idx in geom_idx if idx < i]

        for gi in geom_idx:
            lines[gi] = lines[gi].difference(p)

    return lines


def rotate_x(l, a):
    c, s = math.cos(a), math.sin(a)
    for i in range(len(l)):
        x, y, z = l[i]
        l[i] = (x, y * c - z * s, y * s + z * c)


class Day06Sketch(vsketch.SketchClass):
    points = vsketch.Param(30, 0)
    radius = vsketch.Param(8.0, 0)
    noise_radius = vsketch.Param(4.0, 0)
    z_inc = vsketch.Param(0.05, 0, 1)
    a = vsketch.Param(30, 0, 360)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        layers = []

        zt = -1
        while zt <= 1:
            poly = []

            for i in range(self.points):
                a = i / (self.points - 1) * 2 * math.pi
                nx, ny = math.cos(a), math.sin(a)
                dr = self.noise_radius * (vsk.noise(1 + nx, 1 + ny, zt) - 0.5)

                x = (self.radius + dr) * math.cos(a)
                y = (self.radius + dr) * math.sin(a)
                z = zt * (29.7 * 0.8) / 2
                poly.append((x, y, z))

            layers.append(poly)
            zt += self.z_inc

        a = self.a / 180 * math.pi
        for l in layers:
            rotate_x(l, a)

        layers = occult(
            [LineString([(x, z) for x, _, z in l]) for l in layers[::-1]], 0.1
        )
        for l in layers:
            vsk.geometry(l)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day06Sketch.display()
