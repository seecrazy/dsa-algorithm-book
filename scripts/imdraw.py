# -*- coding: utf-8 -*-
"""Pillow-based diagram kit for the ebook.

Replaces the hand-rolled SVG writer: every box, label and arrow is placed
from measured text, so labels can neither drift nor overflow their boxes.
Static diagrams are saved as 2x-supersampled PNG; a list of Diagram frames
is saved as an animated GIF with a shared palette (no flicker).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_REGULAR_INDEX = 0
FONT_BOLD_INDEX = 1
FALLBACK_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

_HIRAGINO_CMAP = None


def _covered(ch):
    """True when Hiragino can render ch; ASCII assumed safe."""
    global _HIRAGINO_CMAP
    code = ord(ch)
    if code < 128:
        return True
    if _HIRAGINO_CMAP is None:
        from fontTools.ttLib import TTCollection

        _HIRAGINO_CMAP = set()
        for font in TTCollection(FONT_PATH).fonts:
            try:
                _HIRAGINO_CMAP |= set(font.getBestCmap().keys())
            except Exception:
                pass
    return code in _HIRAGINO_CMAP

INK = "#0f172a"
SUB = "#475569"
MUTED = "#94a3b8"
FAINT = "#cbd5e1"
ARROW = "#334155"

STYLES = {
    "plain": ("#f8fafc", "#94a3b8"),
    "blue": ("#dbeafe", "#2563eb"),
    "green": ("#dcfce7", "#059669"),
    "orange": ("#ffedd5", "#d97706"),
    "red": ("#fee2e2", "#dc2626"),
    "purple": ("#ede9fe", "#7c3aed"),
    "ghost": ("#f1f5f9", "#cbd5e1"),
}

ACCENT = {
    "blue": "#2563eb",
    "green": "#059669",
    "orange": "#d97706",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "plain": "#334155",
}


class Diagram:
    """A fixed-size canvas; all coordinates are in logical (1x) pixels."""

    SCALE = 2

    def __init__(self, width, height, bg="#ffffff"):
        self.w = width
        self.h = height
        s = self.SCALE
        self.img = Image.new("RGB", (width * s, height * s), bg)
        self.d = ImageDraw.Draw(self.img)
        self._fonts = {}

    # -- primitives ---------------------------------------------------------

    def font(self, size, bold=False, fallback=False):
        key = (size, bold, fallback)
        if key not in self._fonts:
            if fallback:
                self._fonts[key] = ImageFont.truetype(
                    FALLBACK_PATH, round(size * self.SCALE)
                )
            else:
                index = FONT_BOLD_INDEX if bold else FONT_REGULAR_INDEX
                self._fonts[key] = ImageFont.truetype(
                    FONT_PATH, round(size * self.SCALE), index=index
                )
        return self._fonts[key]

    def text_w(self, s, size, bold=False):
        return self.font(size, bold).getlength(s) / self.SCALE

    def wrap(self, s, max_w, size, bold=False):
        """Greedy wrap; ASCII runs (identifiers, numbers) stay unbroken."""
        import re

        tokens = re.findall(r"[A-Za-z0-9\[\]().,<>=+\-*/_#&|~^%$@'\"?:]+|\s+|.", s)
        lines = []
        cur = ""

        def flush():
            nonlocal cur
            if cur:
                lines.append(cur)
                cur = ""

        for tok in tokens:
            if not tok:
                continue
            if cur and self.text_w(cur + tok, size, bold) > max_w:
                if self.text_w(tok, size, bold) <= max_w:
                    flush()
                    if not tok.isspace():
                        cur = tok
                    continue
                for ch in tok:  # oversized token: hard-break it
                    if cur and self.text_w(cur + ch, size, bold) > max_w:
                        flush()
                    cur += ch
                continue
            cur += tok
        flush()
        return lines or [""]

    def text(self, x, y, s, size=14, color=INK, bold=False, anchor="la"):
        runs = self._runs(s, size, bold)
        if len(runs) == 1:
            font, chunk = runs[0]
            if font is None:
                font = self.font(size, bold)
            self.d.text(
                (x * self.SCALE, y * self.SCALE), chunk,
                font=font, fill=color, anchor=anchor,
            )
            return
        # Mixed-font string: lay runs left-to-right honoring the horizontal anchor.
        widths = [self.d.textlength(chunk, font=f) for f, chunk in runs]
        total = sum(widths) / self.SCALE
        start = {"l": x, "m": x - total / 2, "r": x - total}.get(anchor[0], x)
        sx = start * self.SCALE
        for (font, chunk), w in zip(runs, widths):
            if font is None:
                font = self.font(size, bold)
            self.d.text(
                (sx, y * self.SCALE), chunk, font=font, fill=color,
                anchor="l" + anchor[1],
            )
            sx += w

    def _runs(self, s, size, bold):
        """Split into (font_or_None, chunk) runs; None means primary font."""
        runs = []
        for ch in s:
            fb = not _covered(ch)
            if runs and runs[-1][0] is not None and fb:
                runs[-1] = (runs[-1][0], runs[-1][1] + ch)
            elif runs and runs[-1][0] is None and not fb:
                runs[-1] = (None, runs[-1][1] + ch)
            else:
                runs.append((self.font(size, bold, fallback=True) if fb else None, ch))
        return runs

    def box(self, x, y, w, h, style="plain", radius=10, line_w=2):
        fill, border = STYLES.get(style, STYLES["plain"])
        s = self.SCALE
        self.d.rounded_rectangle(
            [x * s, y * s, (x + w) * s, (y + h) * s],
            radius=radius * s, fill=fill, outline=border, width=line_w * s,
        )

    def line(self, points, color=ARROW, width=2):
        s = self.SCALE
        self.d.line([(x * s, y * s) for x, y in points], fill=color, width=width * s)

    def arrow(self, x1, y1, x2, y2, color=ARROW, width=2):
        self.line([(x1, y1), (x2, y2)], color, width)
        import math

        angle = math.atan2(y2 - y1, x2 - x1)
        head = 9.0
        for offset in (2.5, -2.5):
            wx = x2 - head * math.cos(angle + offset)
            wy = y2 - head * math.sin(angle + offset)
            self.line([(x2, y2), (wx, wy)], color, width)

    def chip(self, cx, cy, label, style="blue", r=13, size=14):
        """Filled circle with a short label (step number, pointer name)."""
        accent = ACCENT.get(style, ARROW)
        s = self.SCALE
        self.d.ellipse(
            [(cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s],
            fill="#eff6ff", outline=accent, width=2 * s,
        )
        self.text(cx, cy, label, size=size, color=accent, bold=True, anchor="mm")

    def panel(self):
        s = self.SCALE
        self.d.rounded_rectangle(
            [8 * s, 8 * s, (self.w - 8) * s, (self.h - 8) * s],
            radius=16 * s, fill="#ffffff", outline="#e2e8f0", width=s,
        )

    def header(self, title, subtitle=None):
        self.text(30, 26, title, size=21, bold=True)
        if subtitle:
            self.text(30, 60, subtitle, size=13, color=SUB)

    # composite: a panel with a bold label line and wrapped body text -------

    def note_box(self, x, y, w, lines, style="plain", title=None, size=14, pad=14):
        """Box sized from wrapped content; returns its height."""
        body = []
        for line in lines:
            body.extend(self.wrap(line, w - 2 * pad, size))
        title_lines = self.wrap(title, w - 2 * pad, size) if title else []
        line_h = size + 7
        height = pad * 2 + (len(body) + len(title_lines)) * line_h
        self.box(x, y, w, height, style)
        ty = y + pad
        for tl in title_lines:
            self.text(x + w / 2, ty, tl, size=size, bold=True, anchor="ma")
            ty += line_h
        for line in body:
            self.text(x + w / 2, ty, line, size=size, color=SUB, anchor="ma")
            ty += line_h
        return height

    # -- exports ------------------------------------------------------------

    def finalize(self):
        return self.img.resize((self.w, self.h), Image.LANCZOS)


def save_png(diagram, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    diagram.finalize().save(path, optimize=True)


def save_gif(path, frames, durations):
    """frames: list[Diagram]; durations: ms per frame (list, same length)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    images = [f.finalize() for f in frames]
    sample = Image.new("RGB", (images[0].width, images[0].height * len(images)))
    for i, im in enumerate(images):
        sample.paste(im, (0, i * images[0].height))
    palette = sample.quantize(colors=96, method=Image.MEDIANCUT)
    quantized = [im.quantize(palette=palette, dither=Image.NONE) for im in images]
    quantized[0].save(
        path, save_all=True, append_images=quantized[1:],
        duration=durations, loop=0, disposal=2, optimize=True,
    )
