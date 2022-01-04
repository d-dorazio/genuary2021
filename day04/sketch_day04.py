import math

import vsketch

import numpy as np
from shapely.geometry import LineString, MultiPolygon, Point, CAP_STYLE


def cut_line(line: LineString, t: float) -> list[LineString]:
    assert 0 <= t <= 1

    coords = list(line.coords)

    for i, p in enumerate(coords):
        pt = line.project(Point(p), normalized=True)

        if pt == t:
            return [LineString(coords[: i + 1]), LineString(coords[i:])]

        if pt > t:
            cp = line.interpolate(t, normalized=True)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:]),
            ]

    return []


class Day04Sketch(vsketch.SketchClass):
    divs = vsketch.Param(15)
    radius = vsketch.Param(1.0)
    padding = vsketch.Param(1.0)
    min_length = vsketch.Param(1.0)
    pen_width = vsketch.Param(1.5)
    max_colors = vsketch.Param(10)
    standard_fill = vsketch.Param(True)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        xs = np.linspace(-8, 8, self.divs)
        ys = np.linspace(-13, 13, self.divs)

        lines = MultiPolygon([])

        i = 0

        for oy in ys:
            for ox in xs:
                l = [(ox, oy)]

                while True:
                    x, y = l[-1]
                    a = vsk.noise(x * 0.05, y * 0.05) * math.pi * 2
                    x += self.radius * math.cos(a)
                    y += self.radius * math.sin(a)

                    if abs(x) > 8 or abs(y) > 13:
                        break

                    l.append((x, y))

                # vsk.stroke(self.max_colors + 10)
                # if len(l) > 2:
                #     vsk.geometry(LineString(l))
                # vsk.stroke(1)
                # continue

                vsk.penWidth(f"{self.pen_width}mm")

                if len(l) > 1:
                    ls = [LineString(l)]
                    while ls[-1].length >= self.min_length:
                        ll = ls.pop()
                        t = vsk.random(0.4, 0.8)
                        children = cut_line(ll, t)
                        ls.extend(children)
                        if len(children) == 1:
                            break

                    i = i + 1 if i != self.max_colors else 1
                    if self.standard_fill:
                        vsk.fill(i)
                    vsk.stroke(i)
                    for ll in ls:
                        if ll.length < self.min_length:
                            continue

                        lr = LineString(ll).buffer(
                            self.padding + 0.01,
                            cap_style=CAP_STYLE.flat,
                        )
                        if not lr.intersects(lines):
                            lines = MultiPolygon(list(lines.geoms) + [lr])
                            lr = lr.buffer(-0.01, cap_style=CAP_STYLE.flat)
                            vsk.geometry(lr)

                            while not self.standard_fill:
                                if not lr.is_valid or lr.is_empty:
                                    break
                                vsk.geometry(lr)
                                lr = lr.buffer(
                                    -self.pen_width, cap_style=CAP_STYLE.flat
                                )

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day04Sketch.display()
