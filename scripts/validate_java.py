#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile every reference Java snippet with shared competitive-programming types."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from java_solutions import JAVA_SOLUTIONS
from new_module_problems import NEW_JAVA


def main() -> int:
    snippets = {**JAVA_SOLUTIONS, **NEW_JAVA}
    with tempfile.TemporaryDirectory(prefix="dsa_java_") as name:
        root = Path(name)
        common = root / "common"
        common.mkdir(parents=True)
        (common / "ListNode.java").write_text(
            "package common;\npublic class ListNode{public int val;public ListNode next;"
            "public ListNode(){}public ListNode(int v){val=v;}}\n", encoding="utf-8")
        (common / "TreeNode.java").write_text(
            "package common;\npublic class TreeNode{public int val;public TreeNode left,right;"
            "public TreeNode(){}public TreeNode(int v){val=v;}}\n", encoding="utf-8")
        (common / "Node.java").write_text(
            "package common;\nimport java.util.*;\npublic class Node{public int val;"
            "public List<Node> neighbors=new ArrayList<>();public Node next,random;"
            "public Node(){}public Node(int v){val=v;}}\n", encoding="utf-8")
        (common / "VersionControl.java").write_text(
            "package common;\npublic abstract class VersionControl{"
            "public boolean isBadVersion(int version){return false;}}\n", encoding="utf-8")

        common_out = root / "common_out"
        snippet_out = root / "snippet_out"
        common_out.mkdir()
        snippet_out.mkdir()

        sources = []
        for problem_id, source in snippets.items():
            package = f"check{problem_id}"
            text = f"package {package};\n"
            if any(token in source for token in ("ListNode", "TreeNode", "Node", "VersionControl")):
                text += "import common.*;\n"
            text += source.replace("public class ", "class ") + "\n"
            directory = root / package
            directory.mkdir()
            path = directory / "Snippet.java"
            path.write_text(text, encoding="utf-8")
            sources.append(str(path))

        list_path = root / "sources.txt"
        list_path.write_text("\n".join(sources) + "\n", encoding="utf-8")

        common_process = subprocess.run(
            ["javac", "-d", str(common_out), *[str(path) for path in common.glob("*.java")]],
            capture_output=True, text=True,
        )
        if common_process.returncode:
            print(common_process.stderr, file=sys.stderr)
            return common_process.returncode

        process = subprocess.run(
            ["javac", "-cp", str(common_out), "-d", str(snippet_out), f"@{list_path}"],
            capture_output=True, text=True,
        )
        if process.returncode:
            print(process.stderr, file=sys.stderr)
            return process.returncode

    print(f"java snippets compiled: {len(snippets)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
