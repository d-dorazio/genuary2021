import vsketch

from shapely.geometry import *


class Day07Sketch(vsketch.SketchClass):
    step = vsketch.Param(0.1)
    padding = vsketch.Param(0.5)

    def frange(self, start, stop):
        if start <= stop:
            while start < stop:
                yield start
                start += self.step
        else:
            while start > stop:
                yield start
                start -= self.step

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=True)
        vsk.scale("cm")

        w, h = 26 // 4, 18 // 2

        cols = []

        def draw_col(i, lines):
            if i == 0:
                fun = lambda j: vsk.random(0.5) * len(lines) < j
            else:
                fun = lambda j: vsk.random(0.8) * len(lines) < j

            clipped = box(0, -h, w, h) & MultiLineString(
                [l for li, l in enumerate(lines) if fun(li)]
            )

            for l in clipped.geoms:
                vsk.geometry(l)

        cols.append([[(x, -h), (x, h)] for x in self.frange(0, w)])
        cols.append([[(0, y), (w, y)] for y in self.frange(-h, h)])
        cols.append(
            [[(x, -h), (x + 100, -h + 100)] for x in self.frange(0, w)]
            + [[(0, y), (100, y + 100)] for y in self.frange(-h, h)]
        )
        cols.append(
            [[(x, -h), (x - 100, -h + 100)] for x in self.frange(0, w)]
            + [[(w, y), (w - 100, y + 100)] for y in self.frange(-h, h)]
        )

        for i, c in enumerate(cols):
            draw_col(i, c)
            vsk.translate(w + self.padding, 0)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day07Sketch.display()
