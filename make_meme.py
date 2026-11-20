"""Draw an original make.fun GTA 6 meme. Run with Python and Pillow."""

import math
import os
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1080
SCALE = 2  # Work at double resolution to smooth the inked edges.
INK = "#191127"
PAPER = "#FFF4DC"
WHITE = "#FFFCF5"
PINK = "#F44691"
GOLD = "#FFD25F"
TEAL = "#7DE3CA"


class Canvas:
    def __init__(self):
        self.image = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), INK)
        self.draw = ImageDraw.Draw(self.image)

    @staticmethod
    def pixels(values):
        return tuple(round(v * SCALE) for v in values)

    def polygon(self, points, fill, outline=None, width=7):
        verts = [self.pixels(p) for p in points]
        self.draw.polygon(verts, fill=fill)
        if outline:
            self.draw.line(verts + verts[:1], fill=outline, width=width * SCALE, joint="curve")

    def oval(self, box, fill, outline=None, width=7):
        self.draw.ellipse(self.pixels(box), fill, outline, width * SCALE)

    def rect(self, box, fill, radius=0, outline=None, width=7):
        self.draw.rounded_rectangle(self.pixels(box), radius * SCALE, fill, outline, width * SCALE)

    def line(self, points, fill, width):
        self.draw.line([self.pixels(p) for p in points], fill, width * SCALE, joint="curve")

    def curve(self, start, segments, fill, outline=None, width=7):
        """Trace a shape from straight endpoints and cubic Bézier segments."""
        points = [start]
        for segment in segments:
            if len(segment) == 2:
                points.append(segment)
                continue
            x0, y0 = points[-1]
            x1, y1, x2, y2, x3, y3 = segment
            for i in range(1, 25):
                t = i / 24
                u = 1 - t
                points.append((u**3*x0 + 3*u*u*t*x1 + 3*u*t*t*x2 + t**3*x3,
                               u**3*y0 + 3*u*u*t*y1 + 3*u*t*t*y2 + t**3*y3))
        self.polygon(points, fill, outline, width)

    def sparkle(self, x, y, radius, fill, narrow=1):
        r = radius / 3
        self.polygon([(x, y-radius), (x+r*narrow, y-r), (x+radius*narrow, y),
                      (x+r*narrow, y+r), (x, y+radius), (x-r*narrow, y+r),
                      (x-radius*narrow, y), (x-r*narrow, y-r)], fill)


def typeface(role, size):
    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    names = {
        "display": (windows / "impact.ttf", "DejaVuSansCondensed-Bold.ttf", "DejaVuSans-Bold.ttf"),
        "bold": (windows / "arialbd.ttf", "DejaVuSans-Bold.ttf"),
    }[role]
    for name in names:
        try:
            return ImageFont.truetype(str(name), size * SCALE)
        except OSError:
            pass
    return ImageFont.load_default(size=size * SCALE)


def centered(canvas, text, center, size, max_width, role="display", fill=PAPER, stroke=0):
    """Center the visible glyph bounds, not the font's line metrics."""
    font = typeface(role, size)
    left, top, right, bottom = font.getbbox(text)
    for point_size in range(size, 0, -1):
        font = typeface(role, point_size)
        left, top, right, bottom = font.getbbox(text, stroke_width=stroke * SCALE)
        if right - left <= max_width * SCALE:
            break
    x, y = canvas.pixels(center)
    canvas.draw.text((x - (left + right) / 2, y - (top + bottom) / 2), text,
                     font=font, fill=fill, stroke_width=stroke*SCALE, stroke_fill=INK)


def backdrop(canvas):
    """A cream comic frame and a two-tone sunset stage."""
    canvas.rect((28, 28, 1052, 1052), PAPER, radius=35)
    canvas.rect((42, 42, 1038, 1038), INK, radius=25)
    canvas.rect((58, 322, 1022, 825), "#ED6598", radius=27)
    canvas.oval((325, 353, 757, 785), "#FFAD79")
    canvas.oval((364, 392, 718, 746), GOLD)
    for y in range(363, 783, 20):
        for x in range(83 + (10 if y % 40 == 3 else 0), 1008, 20):
            if (x - 540)**2 / 420**2 + (y - 580)**2 / 235**2 > 1:
                canvas.oval((x-2, y-2, x+2, y+2), "#C94C84")
    canvas.oval((207, 746, 861, 797), "#A93671")
    canvas.line([(82, 845), (998, 845)], PINK, 5)


def draw_ghost(c):
    # A domed head, scalloped sheet and two four-point eyes echo the mascot.
    c.oval((177, 603, 328, 684), "#E2D6F2", INK, 9)
    c.curve((279, 536), [
        (275, 439, 342, 392, 433, 389), (534, 385, 592, 459, 597, 558),
        (600, 633, 628, 697, 650, 723), (673, 751, 626, 780, 588, 760),
        (564, 747, 546, 739, 522, 763), (499, 789, 471, 783, 444, 762),
        (421, 740, 403, 749, 379, 769), (352, 790, 326, 781, 306, 758),
        (286, 737, 267, 761, 240, 764), (212, 767, 190, 742, 213, 720),
        (253, 680, 269, 627, 279, 536),
    ], WHITE, INK, 11)
    c.curve((286, 608), [
        (275, 671, 252, 700, 228, 732), (216, 743, 231, 755, 252, 749),
        (284, 739, 294, 727, 315, 750), (342, 779, 357, 772, 378, 756),
        (405, 733, 425, 731, 450, 752), (469, 768, 492, 776, 514, 756),
        (544, 726, 567, 733, 596, 750), (615, 762, 645, 755, 644, 740),
        (598, 742, 571, 708, 553, 687), (523, 722, 485, 726, 442, 701),
        (413, 686, 372, 700, 348, 714), (317, 713, 292, 655, 286, 608),
    ], "#E2D6F2")
    c.sparkle(384, 527, 38, INK, .83)
    c.sparkle(505, 519, 38, INK, .83)
    c.oval((321, 555, 371, 581), "#FFADC6")
    c.oval((511, 548, 561, 574), "#FFADC6")
    c.curve((413, 575), [
        (431, 586, 454, 582, 476, 572), (471, 600, 459, 617, 443, 616),
        (426, 616, 416, 597, 413, 575),
    ], INK)
    c.oval((430, 601, 452, 610), PINK)


def draw_trophy(c):
    # Handles are behind the bowl. The magenta star medallion is on the cup.
    for outer in [(597, 495, 696, 591), (754, 495, 853, 591)]:
        x1, y1, x2, y2 = outer
        c.oval(outer, GOLD, INK, 8)
        c.oval((x1+20, y1+20, x2-19, y2-22), "#E975A0", INK, 5)
    c.rect((702, 586, 749, 696), "#E78934", radius=12, outline=INK, width=8)
    c.rect((656, 680, 796, 730), GOLD, radius=11, outline=INK, width=8)
    c.rect((650, 711, 801, 744), "#692951", radius=9, outline=INK, width=8)
    c.curve((634, 483), [
        (815, 483), (810, 540, 802, 629, 725, 636),
        (648, 632, 638, 546, 634, 483),
    ], GOLD, INK, 9)
    c.curve((783, 499), [
        (799, 499), (796, 560, 776, 605, 737, 622),
        (760, 591, 774, 549, 783, 499),
    ], "#F2A13D")
    c.rect((625, 468, 825, 505), "#FFE994", radius=13, outline=INK, width=8)
    c.oval((688, 532, 762, 606), PINK, INK, 7)
    c.sparkle(725, 569, 24, WHITE)
    # This round paw crosses in front of the stem to make the grip explicit.
    c.curve((566, 657), [
        (589, 642, 615, 659, 641, 658), (660, 656, 672, 636, 694, 633),
        (723, 628, 739, 652, 725, 678), (708, 713, 638, 717, 597, 704),
        (578, 698, 564, 679, 566, 657),
    ], WHITE, INK, 9)
    c.line([(685, 659), (696, 654), (710, 653)], "#D7C5E9", 5)


def draw_confetti(c):
    rng = random.Random(6)
    for left, right, upper, lower in [(91, 241, 385, 733), (862, 984, 472, 747)]:
        for _ in range(14):
            x, y = rng.randint(left, right), rng.randint(upper, lower)
            angle = rng.uniform(-math.pi, math.pi)
            c.line([(x, y), (x+math.cos(angle)*15, y+math.sin(angle)*15)],
                   rng.choice((TEAL, GOLD, PAPER, "#A93671")), 5)
    for x, y, r, color in [(155, 485, 24, PAPER), (240, 436, 14, GOLD),
                            (587, 402, 16, WHITE), (877, 545, 27, PAPER),
                            (941, 664, 17, TEAL), (133, 693, 15, TEAL)]:
        c.sparkle(x, y, r, color, .84)


def draw_banner(c):
    # Split ribbon tails and folded corners put the brand into the stage itself.
    c.polygon([(669, 381), (625, 381), (641, 402), (625, 425), (693, 425),
               (693, 381)], "#AC2E6D", INK, 7)
    c.polygon([(922, 381), (974, 381), (956, 402), (974, 425), (898, 425),
               (898, 381)], "#AC2E6D", INK, 7)
    c.polygon([(670, 409), (691, 425), (691, 396)], INK)
    c.polygon([(929, 409), (903, 425), (903, 396)], INK)
    c.rect((669, 352, 929, 411), INK, radius=5)
    centered(c, "make.fun", (799, 381), 49, 235, role="bold", fill=WHITE)


def draw_captions(c):
    centered(c, "MY AI AGENT MADE", (540, 97), 79, 908)
    centered(c, "THE FINAL OF A PRIZE", (540, 181), 87, 908)
    centered(c, "TOURNAMENT ON make.fun", (540, 269), 80, 910, fill=TEAL)
    # Set the punch line in large, uninterrupted lettering for mobile feeds.
    centered(c, "STILL NO GTA 6", (540, 940), 105, 920, fill=GOLD)


def main():
    canvas = Canvas()
    backdrop(canvas)
    draw_confetti(canvas)
    draw_ghost(canvas)
    draw_trophy(canvas)
    draw_banner(canvas)
    draw_captions(canvas)
    out = Path(__file__).resolve().with_name("meme.png")
    canvas.image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
