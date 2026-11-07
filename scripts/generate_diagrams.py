#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate every diagram: hand-built PNGs and trace-driven GIFs.

Rendered with Pillow (scripts/imdraw.py). Replaces the earlier hand-rolled
SVG generator; SVG output is no longer produced or referenced.
"""
from pathlib import Path
import json

from imdraw import save_png
from static_diagrams import BUILDERS
from trace_diagrams import diagram_key, trace_state_gif

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chapter_lookup = {
        chapter["id"]: chapter
        for chapter in json.loads((ROOT / "data" / "chapters.json").read_text(encoding="utf-8"))
    }
    problems = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))
    custom_problem_ids = {
        name.split("-")[1]
        for name in BUILDERS
        if name.startswith("problem-")
    }
    trace_count = 0
    for problem in problems:
        if problem["id"] in custom_problem_ids:
            continue
        target = OUT / diagram_key(problem["id"])
        trace_state_gif(problem, chapter_lookup, target)
        trace_count += 1

    for name, builder in BUILDERS.items():
        save_png(builder(), OUT / f"{name}.png")
    print(f"generated {len(BUILDERS)} hand-built PNG diagrams and {trace_count} trace GIFs")


if __name__ == "__main__":
    main()
