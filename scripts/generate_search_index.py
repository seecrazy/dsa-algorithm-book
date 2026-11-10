#!/usr/bin/env python3
"""生成 data/search-index.json，供前端全文搜索使用。

读取 chapters.json 的章节顺序，逐个解析 chapters/*.md：
- 以 ## / ### 标题切分小节；
- 剥离 Markdown 语法后保留纯文本（代码块整体丢弃，表格保留单元格文字）；
- 为每个小节计算 slug 锚点，slug 算法必须与 assets/app.js 的 slugify() 保持一致，
  否则搜索结果无法跳转到对应标题。

输出为确定性 JSON（顺序、缩进固定），重跑结果应当逐字节一致。
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_PATH = ROOT / "data" / "chapters.json"
INDEX_PATH = ROOT / "data" / "search-index.json"

MAX_SECTION_TEXT = 4000

HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*#*\s*$")


def slugify(text: str) -> str:
    """与 assets/app.js 的 slugify 保持同一契约：
    NFKC 归一 + 小写；非字母数字（含下划线以外的标点与空白）折叠为 '-'。"""
    normalized = unicodedata.normalize("NFKC", text).lower()
    slug = re.sub(r"[^\w]+", "-", normalized, flags=re.UNICODE)
    slug = slug.strip("-")
    return slug or "section"


def strip_inline(text: str) -> str:
    text = re.sub(r"!\[([^\]]*)\]\(([^)]*)\)", r"\1", text)  # 图片 -> alt
    text = re.sub(r"\[([^\]]+)\]\(([^)]*)\)", r"\1", text)  # 链接 -> 文本
    text = re.sub(r"`([^`]*)`", r"\1", text)  # 行内代码
    text = re.sub(r"(\*\*\*|\*\*|\*|~~)", "", text)  # 强调标记
    return text.strip()


def section_text_from_lines(lines: list[str]) -> str:
    parts: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("```"):  # 代码块已在切分阶段整体丢弃
            continue
        if re.fullmatch(r"([-*_])\s*\1\s*\1[\s\-*_]*", stripped):  # 分隔线
            continue
        if stripped.startswith("|"):  # 表格行 -> 单元格文字拼接
            cells = [strip_inline(c.strip()) for c in stripped.strip("|").split("|")]
            parts.append("，".join(c for c in cells if c))
            continue
        parts.append(strip_inline(stripped))
    text = "".join(p if p.endswith(("。", "，", "；", "：", "？", "！")) else p + "。" for p in parts)
    return text[:MAX_SECTION_TEXT]


def parse_chapter(chapter: dict) -> list[dict]:
    markdown = (ROOT / "chapters" / chapter["file"]).read_text(encoding="utf-8")
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    sections: list[dict] = []
    seen: dict[str, int] = {}
    current: dict | None = None
    in_code = False

    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue

        match = HEADING_RE.match(line)
        if match:
            heading = strip_inline(match.group(2))
            base = slugify(heading)
            count = seen.get(base, 0)
            seen[base] = count + 1
            slug = base if count == 0 else f"{base}-{count + 1}"
            current = {"heading": heading, "slug": slug, "lines": []}
            sections.append(current)
            continue

        if current is None:
            current = {"heading": chapter["title"], "slug": slugify(chapter["title"]), "lines": []}
            sections.append(current)
        current["lines"].append(line)

    out = []
    for section in sections:
        text = section_text_from_lines(section["lines"])
        if not text:
            continue
        out.append({
            "chapter": chapter["id"],
            "chapterTitle": chapter["title"],
            "heading": section["heading"],
            "slug": section["slug"],
            "text": text,
        })
    return out


def main() -> int:
    chapters = json.loads(CHAPTERS_PATH.read_text(encoding="utf-8"))
    sections: list[dict] = []
    for chapter in chapters:
        parsed = parse_chapter(chapter)
        if not parsed:
            print(f"[error] 章节无可用小节：{chapter['id']} ({chapter['file']})", file=sys.stderr)
            return 1
        slugs = [s["slug"] for s in parsed]
        if len(slugs) != len(set(slugs)):
            print(f"[error] 章节内 slug 重复：{chapter['id']}", file=sys.stderr)
            return 1
        sections.extend(parsed)

    payload = {"chapters": len(chapters), "sections": sections}
    INDEX_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    total_chars = sum(len(s["text"]) for s in sections)
    print(f"search index: {len(chapters)} chapters, {len(sections)} sections, {total_chars} chars")
    print(f"written: {INDEX_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
