# -*- coding: utf-8 -*-
"""Trace-driven animated solution diagrams.

Each problem's five-question ``trace`` becomes a GIF: one frame per step,
the current step highlighted, future steps shown as ghost slots, and the
invariant footer emphasized on the final frame. Rendered with Pillow via
scripts/imdraw.py so text is measured, never estimated.
"""
from html import escape

from imdraw import INK, MUTED, SUB, Diagram, save_gif

CANVAS_W = 760
BOX_X = 52
BOX_W = 668
CHIP_CX = 26
GAP = 22
STEP_SIZE = 15
LINE_H = 24


def diagram_key(problem_id: str) -> str:
    return f"problem-{problem_id}-trace.gif"


def trace_diagram_meta(problem: dict, chapter_lookup=None) -> dict:
    understanding = problem["solution"]["understanding"]
    title = problem.get("title", problem["id"])
    steps = understanding.get("trace") or []
    chapter_id = problem.get("chapter", "")
    chapter_title = chapter_id
    if chapter_lookup:
        chapter = chapter_lookup.get(chapter_id)
        if chapter:
            chapter_title = chapter.get("title", chapter_id)
    observation = understanding.get("key_observation", "")
    caption = f"{len(steps)} 步动画跟踪：{observation}"
    if len(caption) > 110:
        caption = caption[:108].rstrip() + "…"
    return {
        "src": f"./assets/diagrams/{diagram_key(problem['id'])}",
        "alt": f"{title} 的题解跟踪动画（{chapter_title}）",
        "caption": caption,
    }


class StepLayout:
    """Precomputed geometry shared by every frame of one GIF."""

    def __init__(self, problem, chapter_lookup):
        understanding = problem["solution"]["understanding"]
        self.title = problem.get("title", problem["id"])
        self.steps = understanding.get("trace") or ["初始状态"]
        self.why_correct = understanding.get("why_correct", "")
        chapter_id = problem.get("chapter", "")
        self.chapter_title = chapter_id
        if chapter_lookup:
            chapter = chapter_lookup.get(chapter_id)
            if chapter:
                self.chapter_title = chapter.get("title", chapter_id)

        self.step_lines = [_layout_lines(s, BOX_W - 40, STEP_SIZE) for s in self.steps]
        self.step_h = [
            max(52, 20 + len(lines) * LINE_H) for lines in self.step_lines
        ]
        self.step_y = []
        y = 112
        for height in self.step_h:
            self.step_y.append(y)
            y += height + GAP
        self.footer_body_n = len(_layout_lines(self.why_correct, BOX_W - 40, STEP_SIZE))
        self.footer_y = y
        self.footer_h = 34 + (1 + self.footer_body_n) * LINE_H
        self.height = self.footer_y + self.footer_h + 26

    def style(self, index):
        last = len(self.steps) - 1
        return "blue" if index == 0 else ("green" if index == last else "orange")


def _layout_lines(text, max_w, size):
    probe = Diagram(10, 10)
    return probe.wrap(text, max_w, size)


def _frame(layout, shown, total):
    """Render one frame: steps 1..shown revealed, current = `shown`."""
    d = Diagram(CANVAS_W, layout.height)
    d.panel()
    d.header(layout.title + " · 题解跟踪", f"示例驱动 · {layout.chapter_title} · 每个节点是本题示例的一个状态")
    d.text(CANVAS_W - 30, 30, f"第 {shown} / {total} 步", size=14, color=SUB, bold=True, anchor="ra")

    bar_y = 92
    d.d.rounded_rectangle(
        [40 * 2, bar_y * 2, (CANVAS_W - 40) * 2, (bar_y + 4) * 2],
        radius=4, fill="#e2e8f0",
    )
    if shown:
        frac = shown / total
        fill_w = round(((CANVAS_W - 80) * frac))
        d.d.rounded_rectangle(
            [40 * 2, bar_y * 2, (40 + fill_w) * 2, (bar_y + 4) * 2],
            radius=4, fill="#2563eb",
        )

    for index, (y, height) in enumerate(zip(layout.step_y, layout.step_h)):
        step_no = index + 1
        if step_no > shown:
            d.box(BOX_X, y, BOX_W, height, "ghost")
            d.text(BOX_X + BOX_W / 2, y + height / 2, "…", size=16, color=MUTED, anchor="mm")
            d.chip(CHIP_CX, y + height / 2, str(step_no), "plain", r=14)
            continue
        current = step_no == shown
        d.box(BOX_X, y, BOX_W, height, layout.style(index), line_w=3 if current else 2)
        lines = layout.step_lines[index]
        text_color = INK if current else SUB
        ty = y + (height - len(lines) * LINE_H) / 2
        for line in lines:
            d.text(BOX_X + BOX_W / 2, ty, line, size=STEP_SIZE, color=text_color, anchor="ma")
            ty += LINE_H
        d.chip(CHIP_CX, y + height / 2, str(step_no), layout.style(index), r=14)
        if index:
            prev_bottom = layout.step_y[index - 1] + layout.step_h[index - 1]
            d.arrow(BOX_X + BOX_W / 2, prev_bottom + 2, BOX_X + BOX_W / 2, y - 2)

    fy = layout.footer_y
    final = shown == total
    d.box(BOX_X, fy, BOX_W, layout.footer_h, "purple", line_w=3 if final else 2)
    d.text(BOX_X + BOX_W / 2, fy + 20, "为什么正确（本题不变量）", size=14, bold=True, anchor="ma")
    probe = Diagram(10, 10)
    body = probe.wrap(layout.why_correct, BOX_W - 40, STEP_SIZE)
    ty = fy + 26 + LINE_H
    for line in body:
        d.text(BOX_X + BOX_W / 2, ty + STEP_SIZE * 0.72, line, size=STEP_SIZE, color=SUB, anchor="ma")
        ty += LINE_H
    return d


def trace_state_gif(problem, chapter_lookup, out_path):
    layout = StepLayout(problem, chapter_lookup)
    total = len(layout.steps)
    frames = [_frame(layout, shown, total) for shown in range(1, total + 1)]
    per_step = 1250 if total <= 5 else 1050
    durations = [per_step] * (total - 1) + [per_step * 2]
    save_gif(out_path, frames, durations)


# Backwards-compatible alias for callers that still expect a static render.
def trace_state_svg(problem, chapter_lookup):
    raise NotImplementedError("trace diagrams are animated GIFs now; call trace_state_gif()")
