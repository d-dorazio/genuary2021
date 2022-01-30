import vsketch

import numpy as np
from shapely.geometry import *


class Day30Sketch(vsketch.SketchClass):
    rects = vsketch.Param(200)
    step = vsketch.Param(0.2)
    rows = vsketch.Param(40)
    cols = vsketch.Param(20)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        rects = []
        for y in np.linspace(0, 20, self.rows):
            for x in np.linspace(0, 13, self.cols):
                if vsk.random(1) > y / 20:
                    continue

                if vsk.random(1) < abs(x - 6.5) / 6.5:
                    continue

                w = vsk.random(0.3, 0.3 + 2.7 * y / 20)
                h = vsk.random(0.3, 0.6 + 5.4 * y / 15)
                rects.append(box(x, y, x + w, y + h))

        prev = []
        for rect in rects:
            for pp in prev:
                rect -= pp
            if rect.is_empty:
                continue
            prev.append(rect)
        rects = prev

        textures = []
        for rect in rects:
            texture = []
            l, t, r, b = rect.bounds

            if vsk.random(1) > 0.5:
                for x in np.arange(l, r, self.step / 2):
                    texture.append(LineString([(x, t), (x, b)]))
            else:
                for x in np.arange(l - (r - l), r, self.step):
                    ll = LineString([(x, t), (x + (r - l), b)])
                    texture.append(ll)
            textures.append(MultiLineString(texture) & rect)

        for r, t in zip(rects, textures):
            vsk.geometry(r)
            vsk.geometry(t)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day30Sketch.display()
