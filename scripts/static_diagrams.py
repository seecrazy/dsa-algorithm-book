# -*- coding: utf-8 -*-
"""Chapter and hand-written problem diagrams, rendered with imdraw (Pillow).

Content mirrors the previous SVG builders; layout is computed from measured
text so nothing drifts. Builders return a Diagram; generate_diagrams writes
them as PNG.
"""
from imdraw import Diagram, INK, MUTED, SUB

W = 760
MX = 30
CONTENT_W = W - 2 * MX


def _probe():
    return Diagram(10, 10)


def note_h(lines, w=CONTENT_W, title=None, size=14, first_as_title=False):
    if first_as_title:
        lines, title = lines[1:], lines[0]
    p = _probe()
    n = sum(len(p.wrap(t, w - 28, size)) for t in lines)
    nt = len(p.wrap(title, w - 28, size)) if title else 0
    return 28 + (n + nt) * (size + 7)


def note(d, y, lines, style="green", title=None, w=CONTENT_W, first_as_title=False):
    if first_as_title:
        lines, title = lines[1:], lines[0]
    return d.note_box(MX, y, w, lines, style, title=title)


def finish_h(y, note_height):
    return y + note_height + 24


def cells(d, x, y, values, styles, cw=52, ch=54, gap=6, index=True):
    """Array cells with centered values and small index labels below."""
    if isinstance(styles, str):
        styles = [styles] * len(values)
    for i, (v, st) in enumerate(zip(values, styles)):
        cx = x + i * (cw + gap)
        d.box(cx, y, cw, ch, st)
        d.text(cx + cw / 2, y + ch / 2, str(v), size=16, bold=True, anchor="mm")
        if index:
            d.text(cx + cw / 2, y + ch + 14, str(i), size=11, color=MUTED, anchor="mm")
    return x + len(values) * (cw + gap) - gap


def flow(d, x, y, items, h=64, gap_w=40):
    """Horizontal chain of boxes joined by arrows. items: (label, style, sub)."""
    n = len(items)
    bw = (CONTENT_W - x + MX - (n - 1) * gap_w) // n
    geoms = []
    for i, (label, st, sub) in enumerate(items):
        bx = x + i * (bw + gap_w)
        d.box(bx, y, bw, h, st)
        if sub:
            d.text(bx + bw / 2, y + h / 2 - 12, label, size=15, bold=True, anchor="mm")
            d.text(bx + bw / 2, y + h / 2 + 14, sub, size=12, color=SUB, anchor="mm")
        else:
            d.text(bx + bw / 2, y + h / 2, label, size=15, bold=True, anchor="mm")
        geoms.append((bx, bw))
    for i in range(n - 1):
        bx, bw = geoms[i]
        nx, _ = geoms[i + 1]
        d.arrow(bx + bw + 4, y + h / 2, nx - 4, y + h / 2)
    return y + h


def tree(d, nodes, edges, label_size=15, arrowed=False):
    """nodes: {key: (cx, top_y, w, h, label, style)}; edges: (parent, child, label)."""
    centers = {k: (v[0], v[1], v[2], v[3]) for k, v in nodes.items()}
    for a, b, *rest in edges:
        label = rest[0] if rest else None
        ax, ay, aw, ah = centers[a]
        bx, by, bw, bh = centers[b]
        d.line([(ax, ay + ah), (bx, by)])
        if arrowed:
            d.arrow(ax, ay + ah, bx, by)
        if label:
            d.text((ax + bx) / 2 + 14, (ay + ah + by) / 2, str(label), size=12, color=SUB, anchor="lm")
    for k, (cx, ty, w_, h_, label, style) in nodes.items():
        d.box(cx - w_ / 2, ty, w_, h_, style)
        d.text(cx, ty + h_ / 2, str(label), size=label_size, bold=True, anchor="mm")


def bars(d, x, base_y, values, styles, bw=42, unit=16, gap=10, show_value=True):
    if isinstance(styles, str):
        styles = [styles] * len(values)
    for i, (v, st) in enumerate(zip(values, styles)):
        bx = x + i * (bw + gap)
        h = v * unit
        d.box(bx, base_y - h, bw, h, st, radius=5)
        if show_value:
            d.text(bx + bw / 2, base_y + 15, str(v), size=12, color=SUB, anchor="mm")
    return x + len(values) * (bw + gap) - gap


# ---------------------------------------------------------------------------
# Chapter diagrams
# ---------------------------------------------------------------------------

def chapter_complexity():
    lines = ["横轴看输入规模，纵轴看增长形状：曲线越陡，规模放大后越危险"]
    nh = note_h(lines)
    H = 400
    d = Diagram(W, H + nh)
    d.panel()
    d.header("为什么 O(log n) 比 O(n²) 更像“地图”")
    x0, y0, x1, y1 = 90, 330, 690, 100
    d.line([(x0, y0), (x1, y0)], "#94a3b8", 2)
    d.line([(x0, y0), (x0, y1)], "#94a3b8", 2)
    d.text(x1 + 14, y0, "n", size=14, color=SUB, anchor="lm")
    d.text(x0 - 12, y1 - 8, "工作量", size=14, color=SUB, anchor="rm")
    curves = [
        ([82, 318], [668, 306], "#2563eb", "O(log n)", 300, 296),
        ([82, 318], [668, 200], "#059669", "O(n log n)", 430, 240),
        ([82, 318], [668, 130], "#7c3aed", "O(n)", 560, 122),
        ([82, 318], [300, 92], "#dc2626", "O(n²)", 262, 100),
    ]
    for xa, xb, color, label, lx, ly in curves:
        steps = 24
        pts = []
        for i in range(steps + 1):
            t = i / steps
            fx = xa[0] + (xb[0] - xa[0]) * (i / steps)
            gx = xa[1] + (xb[1] - xa[1]) * t
            pts.append((fx, gx))
        d.line(pts, color, 3)
        d.text(lx, ly, label, size=14, color=color, bold=True, anchor="mm")
    note(d, H, lines)
    return d


def chapter_two_pointers():
    nums = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    lines = [
        "面积 = (right - left) × min(height[left], height[right])",
        "短边决定水面；移动长边不可能变大，所以短边可安全淘汰",
    ]
    nh = note_h(lines, title="计算")
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("对撞双指针：只移动“较弱的一侧”")
    x = 68
    styles = ["blue" if i in (1, 8) else "ghost" for i in range(len(nums))]
    cells(d, x, 100, nums, styles, cw=60, ch=60, gap=8)
    d.chip(68 + 1 * 68 + 30, 82, "left", "blue", r=24, size=12)
    d.chip(68 + 8 * 68 + 30, 82, "right", "blue", r=28, size=12)
    d.text(379, 205, "蓝色是当前候选；灰色是区间内已检查的其他柱子", size=13, color=SUB, anchor="mm")
    note(d, H, lines, title="计算")
    return d


def chapter_sliding_window():
    chars = list("abcabcbb")
    lines = [
        "不变量：窗口内没有重复字符；right 前进扩大答案，left 跳到冲突位置之后",
    ]
    nh = note_h(lines)
    H = 270
    d = Diagram(W, H + nh)
    d.panel()
    d.header("滑动窗口：right 探索，left 修复非法状态")
    x = 76
    d.box(68, 92, 204, 72, "ghost", radius=14)
    styles = ["blue" if i < 3 else ("red" if i == 3 else "plain") for i in range(len(chars))]
    cells(d, x, 100, chars, styles, cw=56, ch=56, gap=8)
    d.text(168, 210, "窗口 [a,b,c] 合法", size=13, color=SUB, anchor="mm")
    d.text(408, 210, "right 读到 d：与窗口冲突（红）", size=13, color=SUB, anchor="mm")
    d.text(650, 210, "left 前进修窗口", size=13, color=SUB, anchor="mm")
    note(d, H, lines)
    return d


def chapter_monotonic_stack():
    lines = [
        "新高度 5 到来：比栈顶小的候选被弹出，并确定它们的“下一个更大值”",
    ]
    nh = note_h(lines)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("单调栈：新证据到来，旧候选立刻退场")
    x = 96
    bars(d, x, 260, [3, 1, 4, 2, 5], ["plain", "plain", "plain", "plain", "blue"], unit=30, bw=44, gap=14)
    d.text(250, 300, "下标 0-4 的高度", size=12, color=SUB, anchor="mm")
    sx, sw = 470, 210
    d.box(sx, 100, sw, 170, "purple")
    d.text(sx + sw / 2, 118, "栈：下标 + 未解决", size=13, bold=True, anchor="mm")
    stack_items = [("2（下标 3）", "blue", 138), ("4（下标 2）", "orange", 186), ("3（下标 0）", "plain", 234)]
    for label, st, sy in stack_items:
        d.box(sx + 18, sy, sw - 36, 34, st, radius=8)
        d.text(sx + sw / 2, sy + 17, label, size=13, anchor="mm")
    d.arrow(330, 180, sx - 6, 180)
    d.text(448, 158, "读入新高度", size=12, color=SUB, anchor="mm")
    note(d, H, lines)
    return d


def chapter_hash_prefix():
    lines = [
        "prefix=1、2、3 都记录进哈希表；扫描到 prefix=3 时查 prefix-k=1，命中次数就是答案",
    ]
    nh = note_h(lines)
    H = 240
    d = Diagram(W, H + nh)
    d.panel()
    d.header("前缀和 + 哈希：把重复求和变成一次查询")
    flow(d, MX, 104, [
        ("nums", "plain", "原始数组"),
        ("prefix", "blue", "前缀和"),
        ("prefix - k", "orange", "需要的历史值"),
        ("哈希表查询", "green", "O(1) 命中"),
    ])
    note(d, H, [
        "数组含负数时不能改成滑动窗口；空间换时间，把“历史是否存在”降为一次查询",
    ], style="purple")
    return d


def chapter_cycle():
    lines = ["fast 和 fast.next 非空才移动；两者指向同一节点即证明有环"]
    nh = note_h(lines)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("快慢指针：环内相对距离每步缩短 1")
    nodes = {
        "1": (140, 120, 76, 50, "1", "plain"),
        "2": (320, 100, 76, 50, "2", "blue"),
        "3": (500, 120, 76, 50, "3", "plain"),
        "4": (580, 230, 76, 50, "4", "orange"),
        "5": (330, 260, 90, 50, "-4", "plain"),
    }
    tree(d, nodes, [("1", "2"), ("2", "3"), ("3", "4"), ("4", "5"), ("5", "2")], arrowed=True)
    d.text(180, 96, "slow · 每次 1 格", size=13, color=SUB, anchor="mm")
    d.text(560, 84, "fast · 每次 2 格", size=13, color=SUB, anchor="mm")
    note(d, H, ["slow == fast 是同一对象判断，不是值相等"], style="purple")
    return d


def chapter_binary_search():
    vals = [1, 3, 5, 7, 9, 11, 13]
    lines = [
        "ok(mid) 后 hi = mid；不满足后 lo = mid + 1",
        "循环结束时 lo == hi，这就是第一个满足条件的边界",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("二分：维持两个“已确定区域”")
    styles = ["green" if i < 3 else ("blue" if i == 3 else "plain") for i in range(len(vals))]
    cells(d, 74, 96, vals, styles, cw=60, ch=56, gap=8)
    d.text(240, 196, "[0, lo)：一定不满足（绿）", size=13, color=SUB, anchor="mm")
    d.text(500, 196, "[hi, n)：可能满足", size=13, color=SUB, anchor="mm")
    d.chip(326, 78, "mid", "blue", r=22, size=12)
    d.arrow(326, 96, 326, 150)
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def chapter_tree_recursion():
    lines = [
        "depth(n) = 1 + max(depth(left), depth(right))",
        "父节点不关心子树内部形状，只接收“子问题已解决”的值",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("树的后序：先问子树要答案，再合并自己")
    nodes = {
        "root": (379, 96, 130, 54, "根 1", "blue"),
        "l": (215, 200, 120, 52, "左 2", "orange"),
        "r": (545, 200, 120, 52, "右 3", "orange"),
        "ll": (120, 300, 100, 48, "空", "green"),
        "lr": (300, 300, 100, 48, "空", "green"),
        "rl": (460, 300, 100, 48, "空", "green"),
        "rr": (640, 300, 100, 48, "空", "green"),
    }
    tree(d, nodes, [("root", "l"), ("root", "r"), ("l", "ll"), ("l", "lr"), ("r", "rl"), ("r", "rr")])
    for key, label in (("ll", "depth=0"), ("lr", "depth=0"), ("rl", "depth=0"), ("rr", "depth=0")):
        cx, ty, w_, h_ = nodes[key][0], nodes[key][1], nodes[key][2], nodes[key][3]
        d.text(cx, ty - 10, label, size=11, color=MUTED, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def chapter_heap():
    lines = [
        "插入/弹出 O(log n)，看堆顶 O(1)；数组 [2,5,4,8,7,6,9]，父子有序，兄弟不比较",
    ]
    nh = note_h(lines)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("堆：只保证最优先者在顶部")
    nodes = {
        "a": (379, 92, 120, 52, "最小 2", "blue"),
        "b": (240, 190, 96, 48, "5", "orange"),
        "c": (520, 190, 96, 48, "4", "orange"),
        "d": (140, 286, 88, 46, "8", "plain"),
        "e": (300, 286, 88, 46, "7", "plain"),
        "f": (460, 286, 88, 46, "6", "plain"),
        "g": (620, 286, 88, 46, "9", "plain"),
    }
    tree(d, nodes, [("a", "b"), ("a", "c"), ("b", "d"), ("b", "e"), ("c", "f"), ("c", "g")])
    note(d, H, lines, style="purple")
    return d


def chapter_graph_bfs():
    lines = [
        "第 0 层：起点；第 1 层：A、B；第 2 层：C、D、E",
        "入队时立刻标记访问，避免同一层重复加入",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 340
    d = Diagram(W, H + nh)
    d.panel()
    d.header("BFS：按层扩散，所以无权图第一到达即最短")
    nodes = {
        "s": (379, 96, 120, 52, "起点", "blue"),
        "a": (200, 200, 100, 50, "A", "orange"),
        "b": (558, 200, 100, 50, "B", "orange"),
        "c": (90, 290, 96, 48, "C", "green"),
        "e": (268, 290, 96, 48, "D", "green"),
        "f": (470, 290, 96, 48, "E", "green"),
    }
    tree(d, nodes, [("s", "a"), ("s", "b"), ("a", "c"), ("a", "e"), ("b", "f")])
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def chapter_topological():
    lines = [
        "0 学完后，依赖 0 的课程入度减 1；入度变 0 才能进入队列",
        "若最终输出的节点数 < 总节点数，说明剩余依赖形成环",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("拓扑排序：先处理没有未完成前置的节点")
    nodes = {
        "0": (140, 96, 130, 54, "0 · 入度 0", "green"),
        "1": (380, 96, 130, 54, "1 · 入度 1", "orange"),
        "2": (620, 96, 110, 54, "2 · 入度 1", "orange"),
        "3": (280, 220, 130, 54, "3 · 入度 2", "red"),
        "4": (520, 220, 130, 54, "4 · 入度 2", "red"),
    }
    tree(d, nodes, [("0", "1"), ("1", "2"), ("0", "3"), ("1", "3"), ("1", "4")], arrowed=True)
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def chapter_dp_grid():
    lines = [
        "状态是什么？状态值表示什么？转移从哪些子问题来？",
        "边界是递推的“地基”；顺序错，整个表格会依赖还没算出的格子",
    ]
    nh = note_h(lines)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("DP：先定义状态，再看格子来自哪里")
    x0, y0, cw, ch, gap = 156, 104, 100, 52, 16
    names = ["dp0", "dp1", "dp2", "dp3", "dp4", "dp5", "dp6", "dp7"]
    k = 0
    for r in range(2):
        for c in range(4):
            cx = x0 + c * (cw + gap)
            cy = y0 + r * (ch + gap)
            d.box(cx, cy, cw, ch, "blue" if (r, c) == (0, 2) or (r, c) == (1, 1) else "plain")
            d.text(cx + cw / 2, cy + ch / 2, names[k], size=14, bold=True, anchor="mm")
            k += 1
    gx = x0 + 2 * (cw + gap)
    gy = y0 + 1 * (ch + gap)
    d.arrow(gx - 12, gy + ch / 2, gx - 2, gy + ch / 2)
    d.arrow(gx + cw / 2, gy - 8, gx + cw / 2, gy + 4)
    d.text(379, 240, "dp6 由左侧 dp5 / 上方 dp2 / 左上 dp1 转移而来", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def chapter_backtracking():
    lines = [
        "绿色是记录点；回到父节点必须删除刚做的选择，否则状态污染",
    ]
    nh = note_h(lines)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("回溯：选择 → 探索 → 撤销")
    nodes = {
        "root": (379, 90, 100, 50, "[]", "blue"),
        "a": (210, 190, 100, 50, "[1]", "orange"),
        "b": (548, 190, 100, 50, "[2]", "orange"),
        "a1": (110, 290, 100, 50, "[1,2]", "green"),
        "a2": (260, 290, 100, 50, "[1,3]", "green"),
        "b1": (450, 290, 100, 50, "[2,1]", "green"),
        "b2": (600, 290, 100, 50, "[2,3]", "green"),
    }
    tree(d, nodes, [("root", "a"), ("root", "b"), ("a", "a1"), ("a", "a2"), ("b", "b1"), ("b", "b2")])
    note(d, H, ["红色剪枝用于整棵子树都不可能满足约束的情况"], style="purple")
    return d


def chapter_union_find():
    lines = [
        "路径压缩：find 时把沿途节点直接挂到根",
        "按大小合并：小树挂到大树，避免变成长链",
    ]
    nh = note_h(lines)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("并查集：不关心路径，只关心“谁和谁同根”")
    nodes = {
        "A": (280, 92, 110, 52, "A 根", "blue"),
        "B": (520, 92, 110, 52, "B 根", "red"),
        "C": (150, 200, 96, 48, "C", "orange"),
        "D": (395, 200, 96, 48, "D", "orange"),
        "E": (630, 200, 96, 48, "E", "plain"),
    }
    tree(d, nodes, [("A", "C"), ("B", "D"), ("B", "E")])
    d.arrow(160, 224, 470, 122, "#059669", 3)
    d.text(300, 276, "union(C, B)：找到两个根，再把一个根挂到另一个根下面", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def chapter_interval_schedule():
    rows = [
        ("A", 60, 260, "blue", "选中"),
        ("B", 210, 200, "red", "与 A 重叠，淘汰"),
        ("C", 350, 260, "blue", "选中"),
        ("D", 480, 200, "plain", "未处理"),
    ]
    lines = [
        "A 结束最早，不会减少后续机会；任何最优解都可以把第一个区间换成 A",
    ]
    nh = note_h(lines, title="交换论证直觉")
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("区间调度：按结束时间排序，保留最早结束者")
    y = 96
    for name, bx, bw, st, tag in rows:
        d.box(bx, y, bw, 46, st)
        d.text(bx + 20, y + 23, name, size=14, bold=True, anchor="lm")
        d.text(bx + bw + 14, y + 23, tag, size=12, color=SUB, anchor="lm")
        y += 62
    note(d, H, lines, style="purple", title="交换论证直觉")
    return d


def chapter_sorting_models():
    lines = [
        "稳定排序能保持相等元素原序；基数排序的每一位必须稳定",
        "通用数组常选快排；链表/外部排序常用归并；小整数用计数",
    ]
    nh = note_h(lines)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("排序选型：先看值域和顺序要求")
    flow(d, MX, 100, [
        ("比较排序", "blue", None),
        ("值域/位数受限？", "orange", None),
        ("非比较排序", "green", None),
    ], h=54)
    panels = [
        (MX, 190, "快排 / 归并 / 堆排", "平均 O(n log n)", "按稳定性与原地性选择", "blue"),
        (392, 190, "计数 / 基数 / 桶", "利用值域或位数", "可突破比较下界", "purple"),
    ]
    for px, py, t1, t2, t3, st in panels:
        d.box(px, py, 338, 110, st)
        d.text(px + 169, py + 24, t1, size=15, bold=True, anchor="mm")
        d.text(px + 169, py + 54, t2, size=13, color=SUB, anchor="mm")
        d.text(px + 169, py + 84, t3, size=13, color=SUB, anchor="mm")
    note(d, H, lines)
    return d


def chapter_trie_prefix():
    lines = [
        "插入/查找/前缀判断都是 O(L)",
        "is_end 标记“到此是一个完整词”；子节点保存下一字符",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 380
    d = Diagram(W, H + nh)
    d.panel()
    d.header("Trie：共享前缀只走一次")
    nodes = {
        "root": (300, 92, 96, 48, "root", "blue"),
        "a": (180, 190, 84, 46, "a", "green"),
        "b": (430, 190, 84, 46, "b", "plain"),
        "p": (180, 284, 84, 46, "p", "green"),
        "end": (180, 330, 110, 48, "p · end", "blue"),
    }
    tree(d, nodes, [("root", "a"), ("root", "b"), ("a", "p"), ("p", "end")])
    d.text(430, 260, "b 分支与其他词共享根", size=13, color=SUB, anchor="mm")
    d.text(310, 356, "apple 的唯一路径", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def chapter_avl_rotation():
    lines = [
        "中序仍是 A < x < B < y < C；只有父子关系被旋转",
        "更新高度顺序：先孩子，再父节点",
    ]
    nh = note_h(lines)
    H = 380
    d = Diagram(W, H + nh)
    d.panel()
    d.header("AVL 旋转：恢复高度，不破坏中序")
    d.text(190, 90, "失衡：左左", size=14, bold=True, anchor="mm")
    d.text(570, 118, "右旋后", size=14, bold=True, anchor="mm")
    left = {
        "y": (190, 104, 96, 48, "y", "red"),
        "x": (110, 196, 90, 46, "x", "blue"),
        "C": (285, 196, 80, 46, "C", "plain"),
        "A": (70, 288, 76, 44, "A", "green"),
        "B": (170, 288, 76, 44, "B", "orange"),
    }
    tree(d, left, [("y", "x"), ("y", "C"), ("x", "A"), ("x", "B")])
    d.text(380, 200, "右旋", size=16, bold=True, color="#2563eb", anchor="mm")
    d.arrow(352, 200, 408, 200, "#2563eb", 3)
    right = {
        "x2": (560, 140, 90, 46, "x", "blue"),
        "A2": (460, 240, 76, 44, "A", "green"),
        "y2": (660, 240, 90, 46, "y", "orange"),
        "B2": (600, 320, 76, 44, "B", "green"),
        "C2": (716, 320, 76, 44, "C", "plain"),
    }
    tree(d, right, [("x2", "A2"), ("x2", "y2"), ("y2", "B2"), ("y2", "C2")])
    note(d, H, lines, style="purple")
    return d


def chapter_btree_split():
    lines = [
        "内部节点只放索引键；真实数据在叶子",
        "叶子链表支持范围扫描：定位起点后顺序读",
    ]
    nh = note_h(lines + ["一次节点读取对应一次磁盘页，而不是一个二叉节点"], first_as_title=True)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("B+ 树：满节点分裂，中间键上移")
    d.box(80, 100, 200, 56, "red")
    d.text(180, 128, "[10, 20, 30, 40]", size=15, bold=True, anchor="mm")
    d.arrow(292, 128, 356, 128)
    d.box(360, 100, 110, 56, "orange")
    d.text(415, 128, "分裂", size=15, bold=True, anchor="mm")
    d.box(150, 210, 150, 54, "green")
    d.text(225, 237, "[10, 20]", size=15, bold=True, anchor="mm")
    d.box(430, 210, 150, 54, "green")
    d.text(505, 237, "[30, 40]", size=15, bold=True, anchor="mm")
    d.box(280, 168, 120, 40, "blue")
    d.text(340, 188, "20 上移", size=13, bold=True, anchor="mm")
    d.line([(225, 210), (300, 208)])
    d.line([(505, 210), (380, 208)])
    note(d, H, lines + ["一次节点读取对应一次磁盘页，而不是一个二叉节点"], style="purple", first_as_title=True)
    return d


def chapter_branch_bound():
    lines = [
        "最小化问题用下界；最大化问题用上界",
        "bound 不可能优于 best 时，整棵子树都可剪掉",
    ]
    nh = note_h(lines)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("分支限界：用界剪掉注定更差的子树")
    nodes = {
        "root": (379, 92, 120, 50, "部分解", "blue"),
        "a": (210, 186, 110, 50, "分支 A", "orange"),
        "b": (548, 186, 110, 50, "分支 B", "orange"),
        "a1": (140, 280, 130, 48, "界 12", "green"),
        "a2": (330, 280, 130, 48, "界 17", "red"),
        "b1": (520, 280, 130, 48, "界 19", "plain"),
    }
    tree(d, nodes, [("root", "a"), ("root", "b"), ("a", "a1"), ("a", "a2"), ("b", "b1")])
    d.text(180, 336, "剪掉", size=12, color="#dc2626", anchor="mm")
    d.text(500, 336, "继续扩展", size=12, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def chapter_graph_representation():
    lines = [
        "建模四问：点是什么？边是什么？权是什么？方向如何？",
        "选错容器，算法仍正确，但时间或空间可能不可承受",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 360
    d = Diagram(W, H + nh)
    d.panel()
    d.header("图表示法：空间、查边和遍历都不同")
    panels = [
        (MX, 100, "邻接表 O(V+E)", "遍历稀疏边最省", "查边要看度数", "blue"),
        (392, 100, "矩阵 O(V²)", "O(1) 判断 u-v", "密集图 / Floyd", "orange"),
        (MX, 226, "边数组 O(E)", "Kruskal / Bellman", "不适合查邻居", "purple"),
        (392, 226, "隐式图", "按状态生成邻居", "控制状态爆炸", "green"),
    ]
    for px, py, t1, t2, t3, st in panels:
        d.box(px, py, 338, 104, st)
        d.text(px + 169, py + 22, t1, size=15, bold=True, anchor="mm")
        d.text(px + 169, py + 52, t2, size=13, color=SUB, anchor="mm")
        d.text(px + 169, py + 80, t3, size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="plain", first_as_title=True)
    return d


# ---------------------------------------------------------------------------
# Hand-written problem diagrams
# ---------------------------------------------------------------------------

def problem_two_sum():
    lines = ["扫描到 7 时，同伴 target - x = 2 已出现过；不需要回头再扫"]
    nh = note_h(lines)
    H = 240
    d = Diagram(W, H + nh)
    d.panel()
    d.header("两数之和：把“找同伴”变成一次历史查询")
    flow(d, MX, 100, [
        ("x = 7", "blue", None),
        ("需要 2", "orange", None),
        ("seen[2] = 0", "green", None),
    ])
    note(d, H, ["seen 记录历史值 → 下标：{2: 0}；答案返回 [0, 1]"], style="purple")
    return d


def problem_max_subarray():
    nums = [-2, 1, -3, 4, -1, 2, 1]
    lines = [
        "cur = 以 i 结尾的最大和：cur = max(nums[i], cur + nums[i])；ans 记录历史最大",
    ]
    nh = note_h(lines)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("最大子数组和：负前缀不值得携带")
    styles = ["red" if i == 0 else ("blue" if i == 3 else "plain") for i in range(len(nums))]
    cells(d, 76, 100, nums, styles)
    d.text(102, 210, "-2：cur<0 丢弃", size=13, color="#dc2626", anchor="mm")
    d.text(300, 210, "从 4 重新开始", size=13, color=SUB, anchor="mm")
    d.arrow(430, 122, 560, 122, "#059669", 3)
    d.text(500, 106, "后续累计", size=12, color="#059669", anchor="mm")
    note(d, H, ["后续 4, -1, 2, 1 形成最大连续和 6"], style="green")
    return d


def problem_container():
    hs = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    lines = [
        "宽 = 8 - 1 = 7；高 = min(8, 7) = 7；面积 = 49",
        "移动较长右边不会增加上限，因此右指针可安全左移",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("盛水容器：面积由短边和宽度共同决定")
    base = 240
    x = bars(d, 80, base, hs, ["blue" if i in (1, 8) else "plain" for i in range(len(hs))], unit=18, bw=44, gap=12)
    d.line([(100, 240 - 8 * 18 + 6), (x - 46, 240 - 8 * 18 + 6)], "#2563eb", 2)
    d.text(96, 84, "left=1 · 高 8", size=12, color=SUB, anchor="mm")
    d.text(664, 84, "right=8 · 高 7", size=12, color=SUB, anchor="mm")
    note(d, H, lines, first_as_title=True)
    return d


def problem_three_sum():
    vals = [-1, 0, 1, 2]
    lines = [
        "sum < 0 右移 l；sum > 0 左移 r；sum = 0 记录并同步跳过重复值",
    ]
    nh = note_h(lines)
    H = 280
    d = Diagram(W, H + nh)
    d.panel()
    d.header("三数之和：固定一个，剩下的变成对撞搜索")
    styles = ["blue", "green", "plain", "orange"]
    cells(d, 120, 100, vals, styles, cw=60, ch=56)
    d.chip(150, 82, "i", "blue", r=14)
    d.chip(243, 180, "l", "green", r=14)
    d.chip(427, 180, "r", "orange", r=14)
    d.text(379, 228, "l：小则右移；r：大则左移", size=13, color=SUB, anchor="mm")
    note(d, H, ["排序不仅提供单调方向，也让重复三元组相邻可见"], style="purple")
    return d


def problem_next_greater():
    lines = [
        "2 大于栈内 1，因此下标 0 的答案确定为 2；仍留在栈中的元素继续等待更大的数",
    ]
    nh = note_h(lines)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("下一个更大元素：新值淘汰无法获胜的旧候选")
    cells(d, 90, 100, [1, 2, 1], ["blue", "green", "orange"], cw=62, ch=56)
    d.arrow(155, 122, 218, 122)
    d.text(185, 84, "新到 2", size=12, color=SUB, anchor="mm")
    d.text(240, 84, "1 出栈", size=12, color=SUB, anchor="mm")
    d.box(460, 96, 210, 84, "purple")
    d.text(565, 120, "栈保存下标", size=13, bold=True, anchor="mm")
    d.text(565, 152, "值保持递减", size=13, color=SUB, anchor="mm")
    note(d, H, ["答案 [2, -1, -1]"])
    return d


def problem_histogram():
    hs = [2, 5, 6, 2]
    lines = [
        "弹出 6 时：右边界是更低柱 2，左边界来自新栈顶；宽度 = i - stack[-1] - 1",
    ]
    nh = note_h(lines)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("柱状图最大矩形：低柱变成左右边界的分界")
    base = 260
    top = base - 5 * 32
    d.box(176, top, 128, 5 * 32, "ghost", radius=3)
    bars(d, 110, base, hs, ["plain", "blue", "blue", "plain"], unit=32, bw=52, gap=14)
    d.text(240, top - 40, "高度 5 的最大矩形", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def problem_prefix_sum():
    lines = ["seen[0] = 1 是边界：从头开始的合法子数组也要被计数"]
    nh = note_h(lines)
    H = 240
    d = Diagram(W, H + nh)
    d.panel()
    d.header("和为 k 的子数组：把区间差转成前缀差")
    flow(d, MX, 100, [
        ("prefix[j]", "blue", None),
        ("prefix[i]", "orange", None),
        ("差 = k", "green", None),
    ])
    note(d, H, ["只查 prefix[i] = prefix[j] - k 出现过几次，就得到几个以 j 结尾的子数组"], style="purple")
    return d


def problem_cycle():
    lines = [
        "进入环后 fast 每步比 slow 多走 1 格，相对距离不断缩小，最终 slow == fast",
    ]
    nh = note_h(lines)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("环检测：追上即证明绕圈")
    nodes = {
        "A": (120, 130, 76, 50, "A", "plain"),
        "B": (290, 105, 76, 50, "B", "blue"),
        "C": (460, 130, 76, 50, "C", "orange"),
        "D": (520, 240, 76, 50, "D", "plain"),
        "E": (300, 275, 76, 50, "E", "plain"),
    }
    tree(d, nodes, [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "B")], arrowed=True)
    d.text(170, 92, "slow · +1", size=13, color=SUB, anchor="mm")
    d.text(400, 92, "fast · +2", size=13, color=SUB, anchor="mm")
    note(d, H, lines)
    return d


def problem_remove_nth():
    vals = ["d", 1, 2, 3, 4, 5]
    lines = [
        "dummy 使头节点也有前驱；fast 从 dummy 先走 n+1 步",
        "fast 到 null 时，slow 停在待删节点的前一个节点",
    ]
    nh = note_h(lines + ["slow.next = slow.next.next，一趟完成删除"], first_as_title=True)
    H = 290
    d = Diagram(W, H + nh)
    d.panel()
    d.header("删除倒数第 n 个：用固定距离找前驱")
    styles = ["blue" if i in (0, 1) else ("orange" if i == 4 else "plain") for i in range(len(vals))]
    cells(d, 66, 100, vals, styles, cw=58, ch=54)
    d.text(95, 84, "slow", size=12, color=SUB, anchor="mm")
    d.text(370, 84, "fast 提前 n+1 步", size=12, color=SUB, anchor="mm")
    note(d, H, lines + ["slow.next = slow.next.next，一趟完成删除"], style="green", first_as_title=True)
    return d


def problem_bst_range():
    lines = [
        "不是只比较左右孩子；整棵左子树都必须小于根",
        "区间继承让祖先约束一直传播到底",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("验证 BST：祖先约束传给整棵子树")
    nodes = {
        "r": (379, 96, 170, 54, "2 · (-∞, +∞)", "blue"),
        "l": (200, 200, 150, 52, "1 · (-∞, 2)", "green"),
        "rr": (560, 200, 150, 52, "3 · (2, +∞)", "green"),
    }
    tree(d, nodes, [("r", "l"), ("r", "rr")])
    d.text(280, 172, "左子树上界变 2", size=12, color=SUB, anchor="mm")
    d.text(490, 172, "右子树下界变 2", size=12, color=SUB, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def problem_topological():
    lines = [
        "学完 0 后，1、2、3 的入度减 1",
        "输出数量小于课程总数，等价于存在环",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 330
    d = Diagram(W, H + nh)
    d.panel()
    d.header("课程表：入度 0 表示可以立刻学习")
    nodes = {
        "c0": (160, 96, 140, 54, "0 · 入度 0", "green"),
        "c1": (420, 96, 140, 54, "1 · 入度 1", "orange"),
        "c2": (650, 96, 100, 54, "2 · 入度 1", "orange"),
        "c3": (300, 220, 140, 54, "3 · 入度 2", "red"),
        "c4": (540, 220, 140, 54, "4 · 入度 2", "red"),
    }
    tree(d, nodes, [("c0", "c1"), ("c1", "c2"), ("c0", "c3"), ("c1", "c4")], arrowed=True)
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def problem_dijkstra():
    lines = [
        "堆弹出 (1, A)：边权非负，A 的 1 不可能再被更长路径改善",
        "如果堆里出现过期距离，必须跳过",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("Dijkstra：每次固定当前最近的未确定节点")
    nodes = {
        "S": (140, 110, 110, 54, "S · 0", "green"),
        "A": (400, 90, 110, 54, "A · 1", "orange"),
        "B": (630, 110, 100, 54, "B · 4", "plain"),
        "T": (400, 210, 110, 54, "T · ?", "plain"),
    }
    tree(d, nodes, [], arrowed=False)
    d.arrow(196, 128, 344, 112, "#059669", 3)
    d.text(262, 100, "1", size=13, color=SUB, anchor="mm")
    d.arrow(459, 110, 576, 122)
    d.text(516, 94, "3", size=13, color=SUB, anchor="mm")
    d.arrow(455, 144, 455, 206)
    d.text(472, 176, "7", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def problem_coin_change():
    lines = ["11 = 5 + 5 + 1；状态只关心剩余金额，不关心硬币顺序"]
    nh = note_h(lines)
    H = 250
    d = Diagram(W, H + nh)
    d.panel()
    d.header("零钱兑换：最后一枚硬币决定转移来源")
    flow(d, MX, 100, [
        ("dp[c - 5]", "blue", None),
        ("+ 1", "orange", None),
        ("dp[c]", "green", None),
    ])
    note(d, H, ["dp[c] = min(dp[c-1], dp[c-2], dp[c-5]) + 1；dp[c] 含义：凑出金额 c 的最少硬币数"], style="purple")
    return d


def problem_lis_tails():
    nums = [10, 9, 2, 5, 3, 7]
    lines = [
        "tails 不一定是真实 LIS，但长度是正确答案",
    ]
    nh = note_h(lines)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("LIS：tail[k] 是长度 k+1 的最小可行尾值")
    styles = ["blue" if i == 3 else ("orange" if i >= 4 else "plain") for i in range(len(nums))]
    cells(d, 80, 96, nums, styles)
    d.box(80, 200, 220, 88, "green")
    d.text(190, 224, "tails = [2, 3]", size=14, bold=True, anchor="mm")
    d.text(190, 252, "长度 2；3 是最小尾值", size=13, color=SUB, anchor="mm")
    d.text(430, 222, "读入 7：比所有尾值大", size=13, color=SUB, anchor="mm")
    d.text(430, 250, "LIS 长度变为 3", size=13, color=SUB, anchor="mm")
    d.arrow(300, 244, 350, 244)
    note(d, H, lines, style="purple")
    return d


def problem_edit_distance():
    lines = [
        "dp[i][j] = min(删除，插入，替换) + 1；字符相等时继承 dp[i-1][j-1]",
    ]
    nh = note_h(lines)
    H = 290
    d = Diagram(W, H + nh)
    d.panel()
    d.header("编辑距离：每个格子表示前缀之间的最小代价")
    boxes = [
        (MX, "dp[1][1]", "h → r", "替换 1", "blue"),
        (282, "dp[2][1]", "ho → r", "删除 1", "plain"),
        (494, "dp[1][2]", "h → ro", "插入 1", "plain"),
    ]
    for bx, t1, t2, t3, st in boxes:
        d.box(bx, 100, 236, 100, st)
        d.text(bx + 118, 122, t1, size=14, bold=True, anchor="mm")
        d.text(bx + 118, 150, t2, size=13, color=SUB, anchor="mm")
        d.text(bx + 118, 178, t3, size=13, color=SUB, anchor="mm")
    note(d, H, ["horse → ros 的答案在右下角：3"], style="green")
    return d


def problem_palindrome():
    chars = list("babad")
    lines = [
        "每个奇中心 + 每个偶中心都向两侧扩展；遇到不相等立即停止，记录最大长度",
    ]
    nh = note_h(lines)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("最长回文子串：奇偶中心都要检查")
    styles = ["plain", "blue", "blue", "orange", "plain"]
    cells(d, 120, 96, chars, styles, cw=56, ch=54)
    d.line([(148, 170), (292, 170)], "#2563eb", 2)
    d.text(220, 196, "中心 1：字符 a，扩展得到 aba", size=13, color=SUB, anchor="mm")
    d.line([(268, 240), (344, 240)], "#d97706", 2)
    d.text(306, 266, "中心 2：a / b 之间，偶数长度候选", size=13, color=SUB, anchor="mm")
    note(d, H, lines)
    return d


def problem_sort_colors():
    vals = ["0", "0", "1", "1", "2", "2"]
    lines = [
        "遇 0：与 left 交换，left++，i++；遇 2：与 right 交换，right--，i 不前进",
        "换回的 2 或 0 必须重新判断",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("颜色分类：三个边界把数组切成四个区")
    styles = ["green", "green", "blue", "blue", "red", "red"]
    cells(d, 84, 100, vals, styles, cw=56, ch=56)
    d.text(120, 196, "[0, left) 全 0", size=12, color=SUB, anchor="mm")
    d.text(310, 196, "[left, i) 全 1", size=12, color=SUB, anchor="mm")
    d.text(510, 196, "(i, right] 未处理", size=12, color=SUB, anchor="mm")
    d.text(672, 196, "(right, n) 全 2", size=12, color=SUB, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def problem_inversions():
    lines = [
        "当前右值 < 当前左值时，跨半逆序数 = m - i + 1",
        "相等用 <=，避免把相等元素算成逆序",
    ]
    nh = note_h(lines, first_as_title=True)
    H = 350
    d = Diagram(W, H + nh)
    d.panel()
    d.header("逆序对：在归并跨越处批量计数")
    d.box(MX, 96, 300, 56, "blue")
    d.text(MX + 150, 124, "左半 [5, 7]（已有序）", size=14, bold=True, anchor="mm")
    d.box(430, 96, 300, 56, "orange")
    d.text(580, 124, "右半 [4, 6]（已有序）", size=14, bold=True, anchor="mm")
    d.arrow(330, 124, 426, 124)
    d.box(120, 190, 150, 48, "red")
    d.text(195, 214, "取 4", size=14, bold=True, anchor="mm")
    d.box(360, 190, 170, 48, "green")
    d.text(445, 214, "左半剩 5, 7", size=14, bold=True, anchor="mm")
    d.text(379, 274, "左半剩余 2 个都大于 4：一次性计 2", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple", first_as_title=True)
    return d


def problem_trie_path():
    lines = [
        "search(app) 走到 p，但 end=false；startsWith(app) 只要求路径存在",
    ]
    nh = note_h(lines)
    H = 380
    d = Diagram(W, H + nh)
    d.panel()
    d.header("Trie：前缀路径与完整词标记")
    nodes = {
        "root": (330, 92, 96, 48, "root", "blue"),
        "a": (200, 190, 84, 46, "a", "plain"),
        "b": (470, 190, 84, 46, "b", "plain"),
        "p": (200, 284, 84, 46, "p", "orange"),
        "end": (200, 330, 104, 48, "p · end", "green"),
    }
    tree(d, nodes, [("root", "a"), ("root", "b"), ("a", "p"), ("p", "end")])
    d.text(470, 250, "b 分支不共享 apple", size=13, color=SUB, anchor="mm")
    d.text(330, 366, "apple 到达 end", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def problem_trie_dfs():
    chars = list("oath")
    lines = [
        "Trie 无边 ⇒ 当前网格子树整体剪枝；匹配完整词后加入答案并清除 end 避免重复",
    ]
    nh = note_h(lines)
    H = 300
    d = Diagram(W, H + nh)
    d.panel()
    d.header("单词搜索 II：网格路径与 Trie 同步走")
    styles = ["blue", "green", "green", "green"]
    cells(d, 110, 100, chars, styles, cw=62, ch=56, gap=10)
    tags = ["网格起点", "匹配 oa", "匹配 oat", "匹配 oath"]
    for i, tag in enumerate(tags):
        d.text(141 + i * 72, 196, tag, size=12, color=SUB, anchor="mm")
    note(d, H, [
        "DFS 进入时临时标记格子，四个方向返回后恢复字符；共享前缀只搜索一次",
    ], style="green")
    return d


def problem_calendar():
    lines = [
        "prev.end <= start 且 next.start >= end：有序结构只需检查两个相邻候选",
    ]
    nh = note_h(lines)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("日程安排：只看前驱与后继")
    d.box(MX, 100, 300, 52, "green")
    d.text(MX + 150, 126, "前驱 [10, 20]", size=14, bold=True, anchor="mm")
    d.box(470, 100, 260, 52, "orange")
    d.text(600, 126, "后继：不存在", size=14, bold=True, anchor="mm")
    d.box(340, 190, 240, 52, "blue")
    d.text(460, 216, "新区间 [20, 30)", size=14, bold=True, anchor="mm")
    d.line([(390, 190), (420, 156)], "#94a3b8", 2)
    d.text(230, 250, "prev.end = 20 <= start = 20：不冲突", size=13, color=SUB, anchor="mm")
    note(d, H, ["端点相接视为不重叠"], style="green")
    return d


def problem_bit_query():
    lines = [
        "BIT 中只包含右侧已处理元素；query(r-1) 返回严格小于当前 rank 的数量",
    ]
    nh = note_h(lines)
    H = 250
    d = Diagram(W, H + nh)
    d.panel()
    d.header("BIT：从右往左先查询再插入")
    flow(d, MX, 100, [
        ("nums[i]", "blue", None),
        ("rank - 1", "orange", None),
        ("query(r-1)", "green", None),
    ])
    note(d, H, ["随后 update(r) 把当前数加入右侧集合；顺序颠倒会把自身或左侧元素算进去"], style="purple")
    return d


def problem_bplus_split():
    lines = [
        "左、右各 t-1 个键；separator 不能留在子节点",
    ]
    nh = note_h(lines)
    H = 320
    d = Diagram(W, H + nh)
    d.panel()
    d.header("B+ 树节点分裂：中间键上移")
    d.box(MX, 100, 230, 56, "red")
    d.text(MX + 115, 128, "[1, 2, 3, 4, 5]", size=15, bold=True, anchor="mm")
    d.arrow(272, 128, 330, 128)
    d.box(334, 100, 76, 56, "blue")
    d.text(372, 128, "3", size=15, bold=True, anchor="mm")
    d.box(120, 210, 150, 54, "green")
    d.text(195, 237, "[1, 2]", size=15, bold=True, anchor="mm")
    d.box(400, 210, 150, 54, "green")
    d.text(475, 237, "[4, 5]", size=15, bold=True, anchor="mm")
    d.line([(195, 210), (330, 170)])
    d.line([(475, 210), (400, 170)])
    d.text(379, 292, "separator = keys[t-1]；键升序保证左右范围不重叠", size=13, color=SUB, anchor="mm")
    note(d, H, lines, style="purple")
    return d


def problem_knapsack_bound():
    lines = [
        "若 bound <= best，整棵子树不可能改善答案，立即剪枝",
    ]
    nh = note_h(lines)
    H = 250
    d = Diagram(W, H + nh)
    d.panel()
    d.header("0/1 背包分支限界：用松弛上界剪枝")
    flow(d, MX, 100, [
        ("部分解 i", "blue", None),
        ("分数背包", "orange", None),
        ("上界 bound", "green", None),
    ])
    note(d, H, [
        "剩余物品能装则整装、装不下按比例计入：这是松弛解，不会低估真实可达价值；最大化问题必须用上界",
    ], style="red")
    return d


CHAPTER_DIAGRAM_BUILDERS = {
    "chapter-complexity-growth": chapter_complexity,
    "chapter-array-two-pointers": chapter_two_pointers,
    "chapter-sliding-window": chapter_sliding_window,
    "chapter-monotonic-stack": chapter_monotonic_stack,
    "chapter-hash-prefix-sum": chapter_hash_prefix,
    "chapter-linked-list-cycle": chapter_cycle,
    "chapter-binary-search-boundary": chapter_binary_search,
    "chapter-tree-recursion": chapter_tree_recursion,
    "chapter-heap-shape": chapter_heap,
    "chapter-graph-bfs-layers": chapter_graph_bfs,
    "chapter-topological-order": chapter_topological,
    "chapter-dp-state-grid": chapter_dp_grid,
    "chapter-backtracking-tree": chapter_backtracking,
    "chapter-union-find": chapter_union_find,
    "chapter-interval-scheduling": chapter_interval_schedule,
    "chapter-sorting-models": chapter_sorting_models,
    "chapter-trie-prefix": chapter_trie_prefix,
    "chapter-avl-rotation": chapter_avl_rotation,
    "chapter-btree-split": chapter_btree_split,
    "chapter-branch-bound": chapter_branch_bound,
    "chapter-graph-representation": chapter_graph_representation,
}

PROBLEM_DIAGRAM_BUILDERS = {
    "problem-p001-two-sum": problem_two_sum,
    "problem-p002-max-subarray": problem_max_subarray,
    "problem-p003-container": problem_container,
    "problem-p008-three-sum": problem_three_sum,
    "problem-p010-sliding-window": chapter_sliding_window,
    "problem-p013-next-greater": problem_next_greater,
    "problem-p015-histogram": problem_histogram,
    "problem-p022-prefix-sum": problem_prefix_sum,
    "problem-p029-cycle": problem_cycle,
    "problem-p032-remove-nth": problem_remove_nth,
    "problem-p047-bst-range": problem_bst_range,
    "problem-p066-topological": problem_topological,
    "problem-p073-dijkstra": problem_dijkstra,
    "problem-p097-coin-change": problem_coin_change,
    "problem-p099-lis-tails": problem_lis_tails,
    "problem-p101-edit-distance": problem_edit_distance,
    "problem-p111-palindrome": problem_palindrome,
    "problem-p125-sort-colors": problem_sort_colors,
    "problem-p126-inversions": problem_inversions,
    "problem-p130-trie-path": problem_trie_path,
    "problem-p132-trie-dfs": problem_trie_dfs,
    "problem-p136-calendar": problem_calendar,
    "problem-p137-bit-query": problem_bit_query,
    "problem-p139-bplus-split": problem_bplus_split,
    "problem-p142-knapsack-bound": problem_knapsack_bound,
}

BUILDERS = {**CHAPTER_DIAGRAM_BUILDERS, **PROBLEM_DIAGRAM_BUILDERS}
