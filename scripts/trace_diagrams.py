# -*- coding: utf-8 -*-
"""Trace-driven solution diagrams built from each problem's five-question notes.

Every diagram renders the problem's own example trace: nodes are example
states, edges are the operations between them, and the footer carries the
invariant behind correctness. No chapter-level model placeholders.
"""

CJK_WIDTH = 15.0
ASCII_WIDTH = 8.0
LINE_HEIGHT = 24
TEXT_MAX_WIDTH = 540.0
SVG_WIDTH = 720


def wrap_text(value: str, max_width: float = TEXT_MAX_WIDTH) -> list:
    lines = []
    current = ""
    width = 0.0
    for ch in value:
        w = CJK_WIDTH if ord(ch) > 0x2E7F else ASCII_WIDTH
        if width + w > max_width and current:
            lines.append(current)
            current = ch
            width = w
        else:
            current += ch
            width += w
    if current:
        lines.append(current)
    return lines or [""]


def diagram_key(problem_id: str) -> str:
    return f"problem-{problem_id}-trace.svg"


def _text_block(x: float, y: float, w: float, h: float, lines: list, label=None):
    """Centered multi-line text inside a box of height h starting at y."""
    parts = []
    total = len(lines) * LINE_HEIGHT
    top = y + h / 2 - total / 2 + LINE_HEIGHT / 2 + 5
    for index, line in enumerate(lines):
        cls = "t" if (label and index == 0) else "s"
        parts.append(
            f'<text class="{cls}" x="{x + w / 2:g}" y="{top + index * LINE_HEIGHT:g}">{line}</text>'
        )
    return parts


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
    caption = f"{len(steps)} 步示例跟踪：{observation}"
    if len(caption) > 110:
        caption = caption[:108].rstrip() + "…"
    return {
        "src": f"./assets/diagrams/{diagram_key(problem['id'])}",
        "alt": f"{title} 的题解跟踪图（{chapter_title}）",
        "caption": caption,
    }


def trace_state_svg(problem: dict, chapter_lookup=None) -> str:
    from html import escape

    from generate_diagrams import svg, rect, path

    understanding = problem["solution"]["understanding"]
    title = problem.get("title", problem["id"])
    steps = understanding.get("trace") or ["初始状态"]
    why_correct = understanding.get("why_correct", "")

    chapter_id = problem.get("chapter", "")
    chapter_title = chapter_id
    if chapter_lookup:
        chapter = chapter_lookup.get(chapter_id)
        if chapter:
            chapter_title = chapter.get("title", chapter_id)

    body = [
        f'<text class="title" x="32" y="52">{escape(title + " · 题解跟踪", quote=False)}</text>',
        f'<text class="small" x="360" y="80">{escape("示例驱动：" + chapter_title + " · 每个节点是本题示例的一个状态", quote=False)}</text>',
    ]

    y = 104
    arrow_slots = []
    gap = 26
    for index, step in enumerate(steps):
        lines = wrap_text(step)
        height = max(56, 20 + len(lines) * LINE_HEIGHT)
        cls = "blue" if index == 0 else ("green" if index == len(steps) - 1 else "orange")
        body.append(rect(76, y, 592, height, cls))
        body += _text_block(76, y, 592, height, [escape(line, quote=False) for line in lines])
        body.append(
            f'<circle cx="38" cy="{y + height / 2:g}" r="17" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>'
        )
        body.append(
            f'<text class="t" x="38" y="{y + height / 2 + 6:g}">{index + 1}</text>'
        )
        arrow_slots.append((y, height))
        y += height + gap

    for index in range(len(arrow_slots) - 1):
        top_y, top_h = arrow_slots[index]
        bottom_y, _ = arrow_slots[index + 1]
        start = top_y + top_h + 3
        end = bottom_y - 3
        body.append(path([(372, start), (372, end)], "arrow"))
        body.append(
            f'<text class="small" x="414" y="{(start + end) / 2 + 5:g}">{escape("操作", quote=False)}</text>'
        )

    footer_label = ["为什么正确（本题不变量）"] + wrap_text(why_correct)
    footer_height = 24 + len(footer_label) * LINE_HEIGHT
    footer_y = y
    body.append(rect(76, footer_y, 592, footer_height, "purple"))
    body += _text_block(
        76,
        footer_y,
        592,
        footer_height,
        [escape(line, quote=False) for line in footer_label],
        label=True,
    )

    height = footer_y + footer_height + 30
    return svg(SVG_WIDTH, height, "".join(body))
