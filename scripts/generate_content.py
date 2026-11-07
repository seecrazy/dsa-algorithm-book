#!/usr/bin/env python3
"""Generate and validate chapter Markdown plus ordered chapter metadata."""
from __future__ import annotations

import json
from pathlib import Path

from new_modules import NEW_CHAPTERS, NEW_CHAPTER_DIAGRAMS, NEW_CONTENT

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS_DIR = ROOT / "chapters"
DATA_DIR = ROOT / "data"

CHAPTERS = [
    {
        "id": "how-to-use", "title": "如何使用这本书", "subtitle": "把学习变成一条可复用的拆题流水线",
        "section": "start", "file": "how-to-use.md", "minutes": 10,
        "tags": ["学习方法", "总览"],
    },
    {
        "id": "complexity", "title": "复杂度：性能的地图", "subtitle": "不要背复杂度，学会看见代价",
        "section": "start", "file": "complexity.md", "minutes": 16,
        "tags": ["复杂度", "分析", "总览"],
    },
    {
        "id": "array-two-pointers", "title": "数组与双指针", "subtitle": "连续内存、区间收缩和不变量",
        "section": "structures", "file": "array-two-pointers.md", "minutes": 18,
        "tags": ["数组", "双指针", "滑动窗口"],
    },
    {
        "id": "stack-queue-monotonic", "title": "栈、队列与单调结构", "subtitle": "处理最近依赖和过期元素",
        "section": "structures", "file": "stack-queue-monotonic.md", "minutes": 18,
        "tags": ["栈", "队列", "单调栈"],
    },
    {
        "id": "hash-and-counting", "title": "哈希表与计数", "subtitle": "用空间买时间，用键定义等价",
        "section": "structures", "file": "hash-and-counting.md", "minutes": 16,
        "tags": ["哈希表", "计数", "映射"],
    },
    {
        "id": "linked-list", "title": "链表与边界控制", "subtitle": "指针是纪律，dummy 是温柔",
        "section": "structures", "file": "linked-list.md", "minutes": 18,
        "tags": ["链表", "指针", "缓存"],
    },
    {
        "id": "recursion-divide-binary-search", "title": "递归、分治与二分", "subtitle": "问题缩小、答案合并、边界可靠",
        "section": "techniques", "file": "recursion-divide-binary-search.md", "minutes": 22,
        "tags": ["递归", "分治", "二分"],
    },
    {
        "id": "trees", "title": "树与递归思维", "subtitle": "每个节点都是一个子问题",
        "section": "structures", "file": "trees.md", "minutes": 24,
        "tags": ["树", "递归", "遍历"],
    },
    {
        "id": "heaps", "title": "堆与优先队列", "subtitle": "只维护最重要的顺序",
        "section": "structures", "file": "heaps.md", "minutes": 18,
        "tags": ["堆", "优先队列", "Top K"],
    },
    {
        "id": "graph-search", "title": "图论：搜索、拓扑与连通性", "subtitle": "关系建模是图题的一半",
        "section": "techniques", "file": "graph-search.md", "minutes": 26,
        "tags": ["图", "DFS", "BFS", "拓扑排序"],
    },
    {
        "id": "graph-shortest-mst", "title": "最短路、最小生成树与图建模", "subtitle": "把世界抽象成点和边权",
        "section": "advanced", "file": "graph-shortest-mst.md", "minutes": 26,
        "tags": ["最短路", "最小生成树", "图"],
    },
    {
        "id": "backtracking", "title": "回溯：排列、组合与搜索剪枝", "subtitle": "选择、探索、撤销",
        "section": "techniques", "file": "backtracking.md", "minutes": 24,
        "tags": ["回溯", "排列", "组合", "剪枝"],
    },
    {
        "id": "greedy", "title": "贪心：局部决策与全局证明", "subtitle": "勇气必须带证明",
        "section": "techniques", "file": "greedy.md", "minutes": 20,
        "tags": ["贪心", "区间", "排序"],
    },
    {
        "id": "dynamic-programming", "title": "动态规划：状态、转移与记忆", "subtitle": "不要背转移，先定义状态",
        "section": "techniques", "file": "dynamic-programming.md", "minutes": 34,
        "tags": ["动态规划", "背包", "子序列"],
    },
    {
        "id": "strings", "title": "字符串算法", "subtitle": "文本也是结构，前缀也是地图",
        "section": "advanced", "file": "strings.md", "minutes": 24,
        "tags": ["字符串", "回文", "匹配"],
    },
    {
        "id": "union-find-advanced", "title": "并查集与高级结构", "subtitle": "动态连通性的小型魔法",
        "section": "advanced", "file": "union-find-advanced.md", "minutes": 20,
        "tags": ["并查集", "连通性", "数据结构"],
    },
    {
        "id": "math-bit-probability", "title": "数学、位运算与概率思维", "subtitle": "从约束里挖出隐藏不变量",
        "section": "advanced", "file": "math-bit-probability.md", "minutes": 22,
        "tags": ["数学", "位运算", "概率"],
    },
    {
        "id": "engineering-interview", "title": "工程化调试与面试作战手册", "subtitle": "把正确性、可维护性和表达一起交付",
        "section": "advanced", "file": "engineering-interview.md", "minutes": 20,
        "tags": ["调试", "面试", "工程实践"],
    },
]

CHAPTERS.extend(NEW_CHAPTERS)

NEW_BY_ID = {chapter["id"]: chapter for chapter in NEW_CHAPTERS}
for after_id, new_id in [
    ("recursion-divide-binary-search", "sorting"),
    ("hash-and-counting", "trie"),
    ("trees", "balanced-search-trees"),
    ("balanced-search-trees", "b-trees"),
    ("graph-search", "graph-representation"),
    ("backtracking", "branch-and-bound"),
]:
    chapter = NEW_BY_ID[new_id]
    CHAPTERS.remove(chapter)
    after_index = next(i for i, item in enumerate(CHAPTERS) if item["id"] == after_id)
    CHAPTERS.insert(after_index + 1, chapter)

CONTENT = {}

CONTENT["how-to-use"] = """## 1. 这本书解决什么问题

很多人学算法的困境不是“没看过答案”，而是答案看了就忘。原因通常是：只记住了代码形状，没有记住代码背后的决策链。本书把每个主题拆成五层：

1. **动机**：为什么会有这个结构？
2. **承诺**：它在哪些操作上省时间？
3. **不变量**：正确性靠什么维持？
4. **模板**：常见形状怎么写？
5. **陷阱**：什么样的问题会让人写崩？

## 2. 三遍学习法

### 第一遍：读直觉

不看题解代码，先回答：

- 输入规模在哪里？
- 我要维护什么状态？
- 每次决策能否安全丢弃一部分候选？

### 第二遍：写小例子

选规模为 0、1、2 的例子。小例子不是浪费时间，它们专门攻击空指针、越界、重复元素、并列最大值这些“小怪兽”。

### 第三遍：复述与迁移

合上书，用一句话说出：

```text
这类问题的核心状态是 ______；
转移/移动规则是 ______；
停止条件是 ______；
我通过 ______ 保证不漏解。
```

## 3. 题目怎么用

每道题都分成两层：

- **题面层**：先自己写暴力，确认理解约束。
- **解法层**：展开思路后，不要照抄，先复述复杂度和易错点。

建议用“红黄绿”标记：

- 绿：能独立写出且解释复杂度。
- 黄：有思路但边界写错。
- 红：完全没方向。

三天后只看黄题，一周后重看红题。

## 4. 代码约定

示例偏 Python，因为它接近伪代码，同时足够严格。学习时不必纠结语言细节，应关注：

- 函数输入和输出契约；
- 循环不变量；
- 是否会修改输入；
- 整数溢出、空集合、重复元素、负数边界。

## 5. 快速路线

| 目标 | 路线 |
|---|---|
| 零基础系统学习 | 第 1-9 章，按顺序 |
| 面试前 4 周 | 复杂度、数组、哈希、树、图、DP、题库 |
| 面试前 2 周 | 每章“陷阱清单” + 题库按主题刷 |
| 工程复习 | 并查集、堆、缓存、调试与面试手册 |

> 学习算法不是为了崇拜聪明解法，而是为了在压力下仍有一条可靠的思考路径。
"""

CONTENT["complexity"] = """## 1. 复杂度不是分数，是放大器

时间复杂度回答一个问题：当输入变大时，工作量的增长形状是什么？

```text
O(1)        不随 n 变化
O(log n)    每次砍掉一半
O(n)       摸一遍所有元素
O(n log n)  n 层，每层整理 log n
O(n^2)      所有 pair
O(2^n)      子集型爆炸
O(n!)       排列型爆炸
```

在大约 `10^8` 以内，很多评测环境可以接受；超过后就要考虑换结构、剪枝或状态设计。

## 2. 三个常见误解

### 误解一：嵌套循环一定是 O(n^2)

如果内层总共最多执行 n 次，外层虽然是 `while`，也可能是 O(n)。例如滑动窗口的左右指针都单调前进。

### 误解二：递归深度就是时间复杂度

递归深度是空间上限之一，时间要看“每个节点做多少工作 × 递归节点数”。

### 误解三：哈希操作永远是 O(1)

平均情况是 O(1)，最坏可能退化到 O(n)。哈希函数、冲突策略和输入分布决定稳定性。

## 3. 分析模板

### 循环型

```text
总工作量 = Σ 每轮工作
```

### 递归型

常用递推式：

```text
T(n) = 2T(n/2) + O(n)      -> O(n log n)
T(n) = T(n/2) + O(1)       -> O(log n)
T(n) = 2T(n-1) + O(1)      -> O(2^n)
```

### 空间型

空间包括：

- 显式数组、哈希、堆；
- 递归栈；
- 排序库可能使用的辅助空间。

## 4. 用约束倒推算法

| n 的量级 | 可接受复杂度 | 常见方向 |
|---|---|---|
| `n <= 20` | O(2^n) | 子集、状压 |
| `n <= 5,000` | O(n^2) | 区间 DP、双循环 |
| `n <= 10^5` | O(n log n) | 排序、堆、树 |
| `n <= 10^6` | O(n) | 双指针、计数、BFS |
| `n >= 10^9` | O(log n) / O(1) | 二分、数学 |

## 5. 摊还分析

一个操作偶尔昂贵，不代表平均昂贵。动态数组扩容就是例子：虽然某次 append 可能搬移所有元素，但 n 次 append 总搬移量是 O(n)，摊还每次 O(1)。

## 6. 工程视角

面试里说复杂度要精确，工程里还要问：

- 常数是否影响 P99？
- 内存是否导致缓存失效？
- 是否可以在离线预处理后在线查询？
- 最坏输入是否由用户控制？

> 复杂度是第一张地图，不是终点。写完代码后，真实数据和性能画像才是最终裁决。
"""

CONTENT["array-two-pointers"] = """## 1. 数组的本质

数组用连续内存换来了一个承诺：`a[i]` 可以 O(1) 到达。这个承诺带来三件事：

- 下标就是状态；
- 排序后局部具有方向性；
- 插入删除通常要搬移元素。

## 2. 双指针的三种基本形状

### 2.1 对撞指针

用于有序数组或回文判断。

```python
left, right = 0, len(a) - 1
while left < right:
    # 根据比较移动一边
    left += 1
    right -= 1
```

不变量：`[0, left)` 和 `(right, n)` 是已经排除的区域。

### 2.2 快慢指针

用于原地删除、找中点、判断循环。

```python
slow = 0
for fast in range(len(a)):
    if keep(a[fast]):
        a[slow] = a[fast]
        slow += 1
return slow
```

不变量：`a[:slow]` 是满足条件的最终前缀。

### 2.3 滑动窗口

用于连续区间统计。

```python
left = 0
for right, x in enumerate(a):
    add(x)
    while invalid():
        remove(a[left])
        left += 1
    update_answer(left, right)
```

不变量：窗口 `[left, right]` 要么始终满足条件，要么处于收缩修复中。必须明确定义到底维护哪一种。

## 3. 什么时候数组题会变难

- 有重复元素；
- 修改输入与保留输入的需求冲突；
- 正负数混合导致排序性质失效；
- 最优区间不满足单调性；
- 需要维护多个统计量，如最大值、最小值、乘积、计数。

## 4. 陷阱清单

- `left <= right` 还是 `left < right`，必须跟答案定义一致。
- 空数组先返回，再访问 `a[0]`。
- 乘积题不能只维护最大值，要同时维护最小值，因为负负得正。
- 滑动窗口中删除元素时，计数变 0 必须真的从状态中移除。
- 排序可能破坏“返回原数组下标”的要求。

## 5. 自查三问

1. 每个指针代表什么边界？
2. 哪段区域已经处理完？
3. 循环结束时，`left`、`right`、`slow` 的语义是什么？

> 双指针不是技巧，是“用两个下标维护一段被证明安全的区域”。
"""

CONTENT["stack-queue-monotonic"] = """## 1. 栈：最近的优先

栈只暴露顶端，天然适合：

- 括号配对；
- 表达式求值；
- 递归转迭代；
- 撤销最近一次选择；
- 维护“最近未解决的元素”。

## 2. 单调栈：遇到更强的人，旧候选退场

单调栈维护栈内值单调。新元素到来时，把不可能成为答案的旧元素弹出。

### 下一个更大元素

```python
stack = []           # 下标，值递减
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:
        j = stack.pop()
        answer[j] = x
    stack.append(i)
```

不变量：栈内元素还没有找到下一个更大值；它们的值从底到顶递减。

### 柱状图最大矩形

对每个高度，找左右第一个更低的位置：

```python
heights.append(0)
stack = [-1]
best = 0
for i, h in enumerate(heights):
    while stack[-1] != -1 and heights[stack[-1]] >= h:
        height = heights[stack.pop()]
        width = i - stack[-1] - 1
        best = max(best, height * width)
    stack.append(i)
```

关键：哨兵让所有剩余元素都有出栈机会。

## 3. 队列：顺序不可插队

队列适合：

- BFS；
- 任务调度；
- 缓冲区；
- 按时间顺序处理事件。

## 4. 单调队列：滑动窗口的最大值

双端队列维护下标，值从队首到队尾递减。

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    result = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

三个不变量：

1. 队列下标递增；
2. 对应值递减；
3. 队首在窗口内且是最大值。

## 5. 陷阱清单

- 栈存值还是存下标？需要宽度或距离时必须存下标。
- 弹出条件用 `<` 还是 `<=`，取决于相等元素是否互为答案。
- 循环结束后栈内元素可能还没有答案，要赋默认值。
- 双端队列只存下标时，不要忘记判断过期。
- 非空栈访问 `stack[-1]` 前，必须处理空栈。

> 单调结构的优雅在于：新证据到来时，立刻淘汰不可能的旧候选。
"""

CONTENT["hash-and-counting"] = """## 1. 哈希表的价值

哈希表的核心不是“更快”，而是**把等价关系变成键**。

它常用在：

- 判断见过与否；
- 前缀和首次出现位置；
- 分组同构元素；
- 频次统计；
- O(1) 索引从值到下标。

## 2. 计数三件套

### 存在性

```python
seen = set()
if x in seen: ...
seen.add(x)
```

### 频次

```python
from collections import Counter
freq = Counter(nums)
```

### 分组键

```python
groups = {}
for x in xs:
    groups[key(x)].append(x)
```

设计 `key()` 是这类题的真正难点：

- 异位词：排序字符串，或字符计数元组；
- 位移词：相邻字符差值规范化；
- 分数：化简为最简比值；
- 网格状态：序列化成字符串或元组。

## 3. 前缀和 + 哈希

求和为 k 的子数组数量：

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    seen = defaultdict(int)
    seen[0] = 1
    prefix = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]
        seen[prefix] += 1
    return count
```

不变量：`seen[p]` 表示前缀和 p 之前出现的次数。`prefix - k` 若出现过，每个出现点都是一个合法起点前缀。

## 4. 哈希不能解决一切

哈希适合等值查找，不适合：

- 保序遍历，除非额外维护顺序；
- 区间最值；
- 范围排名；
- 邻近查找；
- 需要最坏复杂度保证的实时系统。

这些场景考虑排序数组、堆、树状结构或平衡树。

## 5. 陷阱清单

- 用 list 当 dict 键会报错，要换成 tuple。
- `defaultdict` 在读取时会创建键，统计前要先想清楚。
- 浮点数不要直接当精确键。
- 有重复元素时，返回下标不能用“值 -> 唯一下标”。
- 字符串哈希在多语言环境中可能受 Unicode 规范化影响。

> 哈希是一种观点：我关心的不是完整对象，而是它的等价签名。
"""

CONTENT["linked-list"] = """## 1. 链表的真实难点

链表访问是 O(n)，但难点不是访问，而是**引用一致性**。每一步都可能改变三个东西：

- 前驱的 next；
- 当前节点的 next；
- 未来需要访问的节点。

所以常见缓解手段是：

- dummy head，消除头部特判；
- 先保存 `nxt`；
- 画图标注指针；
- 明确返回哪个节点。

## 2. 核心模板

### 反转链表

```python
prev = None
cur = head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
return prev
```

不变量：`prev` 是已完成反转部分的头，`cur` 是未处理部分的头。

### 快慢指针找中点

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

偶数长度时 `slow` 在右半部分开头；需要左中点时，应在分裂前明确处理。

### 合并两个有序链表

```python
dummy = tail = ListNode()
while l1 and l2:
    if l1.val <= l2.val:
        tail.next, l1 = l1, l1.next
    else:
        tail.next, l2 = l2, l2.next
    tail = tail.next
tail.next = l1 or l2
return dummy.next
```

### 环检测

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        return True
return False
```

## 3. LRU 缓存的两个核心

LRU 需要同时完成：

1. O(1) 查键值；
2. O(1) 移动到最近使用位置并淘汰最久未用。

方案：哈希表保存 key 到节点；双向链表维护使用顺序。

```python
node = self.map[key]
self._remove(node)
self._add_front(node)
```

淘汰时：

```python
tail = self.dummy_tail.prev
self._remove(tail)
del self.map[tail.key]
```

## 4. 陷阱清单

- 头节点可能被删除，必须使用 dummy。
- 反转前没有保存 `next`，链会断。
- 判断环用 `is` 还是 `==` 要清楚；结构相等和同一对象不同。
- 双向链表删除时要同时修改 `prev` 和 `next`。
- 合并链表末尾忘记接剩余部分。
- 只返回节点不返回长度时，不要假设调用方知道长度。

> dummy 不是偷懒，是把“没有前驱”和“有前驱”统一成一种处理。
"""

CONTENT["recursion-divide-binary-search"] = """## 1. 递归的三要素

1. **子问题更小**；
2. **基线条件正确**；
3. **合并逻辑可信**。

写递归前先说清：

```text
f(n) 表示 ______
f(n) 可以由 f(smaller) 通过 ______ 得到
最小 n 的答案显然是 ______
```

## 2. 分治四步

1. 分：把输入分成互斥子问题；
2. 治：递归解决；
3. 合：合并结果；
4. 特判：空、单元素、重复元素、不可分。

归并排序是标准样例：

```text
T(n) = 2T(n/2) + O(n) = O(n log n)
```

## 3. 二分不是“找中间”

二分是在**单调决策空间**中维护一个不变量：

```text
左边一定不满足；
右边可能满足。
```

### 找第一个满足条件的位置

```python
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
return lo
```

不变量：

- `[0, lo)` 全部不满足；
- `[hi, n)` 全部满足；
- 循环结束时 `lo == hi`，即边界。

## 4. 二分答案

当“最小化最大值”或“最大化最小值”出现时，可以尝试：

1. 证明答案具有单调性；
2. 设计 `ok(target)`；
3. 二分 target。

例如 splitting array：允许的分割数随最大段限制单调增加。

## 5. 快速选择

求第 k 大不必全排序。随机选 pivot，根据分区位置只递归一边，平均 O(n)。

```python
import random

def quickselect(a, k):
    pivot = random.choice(a)
    lows = [x for x in a if x < pivot]
    highs = [x for x in a if x > pivot]
    pivots = [x for x in a if x == pivot]
    if k < len(lows):
        return quickselect(lows, k)
    if k < len(lows) + len(pivots):
        return pivot
    return quickselect(highs, k - len(lows) - len(pivots))
```

## 6. 陷阱清单

- `mid = (lo + hi) // 2` 在某些语言会溢出，可写 `lo + (hi - lo) // 2`。
- 无限循环常因为 `mid` 没有严格收缩边界。
- 旋转数组中有重复元素时，无法总判断哪半有序，需要收缩边界。
- 分治合并时忘记处理剩余子数组。
- 递归基线只写了空输入，漏掉单元素。

> 二分的力量来自单调性；没有单调性，硬写二分只是在掷骰子。
"""

CONTENT["trees"] = """## 1. 树是递归定义的结构

一棵树要么为空，要么有一个根和若干互不相交的子树。因此树题通常有两个视角：

### 自顶向下

从根向子节点传递状态：

```python
def dfs(node, acc):
    if not node:
        return
    new_acc = update(acc, node.val)
    update_global(new_acc)
    dfs(node.left, new_acc)
    dfs(node.right, new_acc)
```

### 自底向上

从子树返回信息给父节点：

```python
def dfs(node):
    if not node:
        return base
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(node.val, left, right)
```

## 2. 遍历顺序的用途

| 遍历 | 用途 |
|---|---|
| 前序 | 复制树、序列化根、进入节点时决策 |
| 中序 | BST 输出有序序列、找中序后继 |
| 后序 | 自底向上统计、删除或释放子树 |
| 层序 | 按深度处理、最短层数、右视图 |

## 3. BST 的核心性质

对任意节点：

```text
左子树所有值 < node.val < 右子树所有值
```

注意不是“只和左右孩子比较”。验证 BST 应传递上下界：

```python
def valid(node, lo, hi):
    if not node:
        return True
    if not (lo < node.val < hi):
        return False
    return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
```

## 4. 常见模型

### 路径和

路径可能不需要经过根。后序返回“从当前节点向下延伸的最大路径和”，全局答案再合并左右。

### 序列化

先序 + 空节点标记可以唯一重建二叉树：

```python
def serialize(node):
    if not node:
        return "#"
    return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
```

### LCA

对于普通二叉树：

```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right
```

BST 版本可利用大小关系不用全搜索。

## 5. 陷阱清单

- 空树返回值要明确定义，深度是 0，路径和可能是 None。
- 重复值会让“按值找节点”失效，应按节点对象或下标。
- 只比较父子节点无法验证 BST。
- 构造树时中序分割点找错。
- 递归深度过大时，要转成显式栈或层序。

> 树题的关键不是背遍历，而是定义“子树返回什么信息”。
"""

CONTENT["heaps"] = """## 1. 堆的承诺

堆不是完全排序，它只承诺**根是当前最优先元素**。

- Python `heapq` 是最小堆；
- 最大堆通常对值取负；
- 插入和弹出都是 O(log n)；
- 查看堆顶是 O(1)。

## 2. Top K 的选择

### 前 K 小

用最大堆维护 K 个最小元素：

```python
import heapq

def k_smallest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]
```

### 前 K 大

用最小堆维护 K 个最大元素：

```python
def k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

为什么不是维护 K 个“最大堆”？因为要快速淘汰当前候选中最差的那个。

## 3. 双堆求中位数

- 左半部分：最大堆；
- 右半部分：最小堆；
- 两堆大小差不超过 1；
- 每次插入后平衡并移动堆顶。

```text
若新元素 <= 左堆顶，进左堆；否则进右堆。
左堆过大，把左堆顶移入右堆。
右堆比左堆大超过 1，把右堆顶移入左堆。
```

## 4. 合并 K 个有序序列

K 路归并：

```python
import heapq

def merge_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result
```

堆项要包含序列编号，避免值相等时比较下一个不可比较对象。

## 5. 延迟删除

堆不支持任意删除。若任务失效，常用延迟删除：

```python
while heap and invalid(heap[0]):
    heapq.heappop(heap)
```

配合计数器记录每个元素应存在多少次。

## 6. 陷阱清单

- Python 没有内置最大堆，取负后要还原符号。
- 堆项是元组时，第二个元素也要可比较。
- Top K 题先问是前 K 大、前 K 小、按频次还是按距离。
- 流式数据不能排序全量，要用固定大小堆。
- 删除堆顶后才检查新堆顶可能过期，要循环清理。

> 堆教会我们一件事：很多问题不需要全部顺序，只需要随时知道最该处理谁。
"""

CONTENT["graph-search"] = """## 1. 图不是格子，是关系

先选表示法：

| 表示 | 适合 | 空间 |
|---|---|---|
| 邻接表 | 稀疏图，常见题 | O(V+E) |
| 邻接矩阵 | 密集图、O(1) 判断边 | O(V^2) |
| 边数组 | Kruskal、离线排序边 | O(E) |
| 隐式图 | 状态转移，不显式建图 | 按状态数 |

## 2. BFS 与 DFS

### BFS：无权最短路

```python
from collections import deque

def bfs(start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

BFS 的正确性来自按层扩展。

### DFS：深入结构

适合连通块、路径存在性、拓扑排序、强连通分量。

```python
def dfs(u, parent):
    visited.add(u)
    for v in graph[u]:
        if v not in visited:
            dfs(v, u)
        elif v != parent:
            # 可能存在环
            pass
```

## 3. 网格图

网格是隐式图：每个格子是节点，四方向是边。

```python
dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
```

必须处理：

- 访问标记；
- 越界；
- 修改原数组是否允许；
- 多源 BFS 初始化所有源点。

## 4. 拓扑排序

用于 DAG 和依赖调度。

Kahn 算法：

```python
from collections import deque, defaultdict

def topo_order(n, edges):
    graph = defaultdict(list)
    indeg = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == n else []
```

若不能完成所有节点，说明有环。

## 5. 连通性与颜色

- 连通块：遍历未访问节点，计数。
- 无向图环：DFS 遇到 visited 且不是 parent。
- 二分图：BFS/DFS 染色，相邻节点颜色必须不同。
- 桥和割点：Tarjan 算法维护 `dfn` 与 `low`。

## 6. 陷阱清单

- 忘记标记起点。
- 入队时标记，而不是出队时才标记，否则重复入队。
- 无向图每条边要加入两个方向。
- 状态图可能维度爆炸，要剪枝。
- DAG 顺序题不一定要求字典序，若要求需用小根堆。

> 图题的难点常在建图：把对象、状态、依赖或冲突正确地变成点和边。
"""

CONTENT["graph-shortest-mst"] = """## 1. 最短路的四种场景

| 场景 | 算法 | 复杂度 |
|---|---|---|
| 无权图 | BFS | O(V+E) |
| 非负边权 | Dijkstra | O(E log V) |
| 可含负边 | Bellman-Ford | O(VE) |
| 全源 | Floyd-Warshall | O(V^3) |

## 2. Dijkstra

```python
import heapq
from collections import defaultdict

def dijkstra(n, graph, start):
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
```

不变量：弹出堆顶时，如果它仍是当前最短距离，该距离已经最终确定（要求边权非负）。

## 3. 带限制的最短路

例如最多经过 K 个边。普通 Dijkstra 状态是节点，但这里状态要扩展成：

```text
(节点，已用边数)
```

或者使用 Bellman-Ford 的 K 轮松弛。

```python
for _ in range(k + 1):
    temp = dist.copy()
    for u, v, w in edges:
        temp[v] = min(temp[v], dist[u] + w)
    dist = temp
```

## 4. 最小生成树

MST 选择 n-1 条边，使图连通且总权最小。

### Kruskal：按边贪心 + 并查集

```text
边按权排序；
依次选不会形成环的边；
直到选满 n-1 条。
```

### Prim：从点扩张 + 堆

```text
维护已连接集合；
堆保存 (边权, 目标点)；
每次取连接集合外代价最小的点。
```

稠密图可用数组版 Prim，稀疏图用堆版更直观。

## 5. 差分约束

形如 `xv - xu <= w` 的不等式，可建边 `u -> v` 权重 w，再用最短路求可行解。若存在负环则无解。

## 6. 建模技巧

- 把物理点、状态、任务、语言、开关都抽象成节点；
- 把等待、转换、破坏、修复成本抽象成边权；
- 多约束时扩展状态；
- 答案不是路径而是可行性时，可考虑二分边权限制后建图。

## 7. 陷阱清单

- Dijkstra 遇到负边不再正确。
- 堆中存在过期距离，弹出时要检查 `d > dist[u]`。
- MST 必须先判断图是否连通。
- 并查集按边建图时不要把节点编号搞混。
- 多源最短路要初始化所有源点距离为 0。

> 权重不是只有距离，可以是时间、金钱、风险或状态转换成本。
"""

CONTENT["backtracking"] = """## 1. 回溯的基本循环

回溯系统地枚举所有可能，并在不合法时剪掉整棵子树。

```python
def backtrack(path, choices):
    if is_complete(path):
        record(path.copy())
        return
    for choice in choices:
        if valid(path, choice):
            make(path, choice)
            backtrack(path, next_choices)
            undo(path, choice)
```

三个动作必须完整：选择、探索、撤销。

## 2. 去重是最大难点

### 排列去重

先排序，同层跳过重复起点：

```python
nums.sort()
used = [False] * len(nums)

def dfs(path):
    if len(path) == len(nums):
        result.append(path.copy())
        return
    for i in range(len(nums)):
        if used[i]:
            continue
        if i and nums[i] == nums[i - 1] and not used[i - 1]:
            continue
        used[i] = True
        path.append(nums[i])
        dfs(path)
        path.pop()
        used[i] = False
```

不变量：同一层中，若上一个相等元素没有被使用，当前元素作为起点会产生重复排列。

### 组合起点

```python
def dfs(start, path):
    for i in range(start, len(nums)):
        path.append(nums[i])
        dfs(i + 1, path)
        path.pop()
```

## 3. 剪枝的三类条件

1. **合法性剪枝**：列冲突、越界、超预算；
2. **可行性剪枝**：剩余资源不足以完成；
3. **最优性剪枝**：当前代价已不劣于已知最优。

N Queens 判断：

```text
同列冲突：col[c]
主对角线：row - col
副对角线：row + col
```

## 4. 网格搜索

Word Search 模板：

```python
def search(r, c, idx):
    if idx == len(word):
        return True
    if not in_board(r, c) or board[r][c] != word[idx]:
        return False
    board[r][c] = '#'
    ok = any(search(r + dr, c + dc, idx + 1) for dr, dc in dirs)
    board[r][c] = word[idx]
    return ok
```

临时标记就是撤销机制。

## 5. 复杂度心态

回溯复杂度通常是候选树的上界：

- 排列：O(n × n!)；
- 子集：O(n × 2^n)；
- 组合：取决于剪枝。

面试中应说明剪枝如何实际降低树规模，而不是只报最坏复杂度。

## 6. 陷阱清单

- 忘记 `path.copy()`，记录的是同一列表引用。
- 撤销顺序与选择不对称。
- 有重复输入但没有排序。
- 组合题允许重复使用元素时，递归起点应仍是 `i` 而不是 `i + 1`。
- 网格恢复字符时写成了恢复标记。

> 回溯的本质是“诚实地枚举”，剪枝只是省去注定失败的分支。
"""

CONTENT["greedy"] = """## 1. 贪心的合法性

贪心不是“感觉当前最好”，而是要证明：

1. **选择性质**：存在一个最优解包含当前贪心选择；
2. **子问题独立性**：选择后，剩余子问题仍可独立求解；
3. **交换论证**：任何最优解都可以交换成贪心解而不变差。

## 2. 区间调度：最多不重叠区间

按结束时间排序。

```python
intervals.sort(key=lambda x: x[1])
count = 0
end = float('-inf')
for start, finish in intervals:
    if start >= end:
        count += 1
        end = finish
return count
```

证明直觉：若最优解第一个区间不是最早结束的，可换成最早结束的，腾出更多空间。

## 3. 区间合并

按起点排序，然后维护当前区间：

```python
intervals.sort()
merged = []
for start, end in intervals:
    if merged and start <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], end)
    else:
        merged.append([start, end])
return merged
```

注意已合并区间的终点要取 max，不能只看当前起点。

## 4. 跳跃游戏

### 能否到达

维护可达最右边界：

```python
far = 0
for i, step in enumerate(nums):
    if i > far:
        return False
    far = max(far, i + step)
return far >= len(nums) - 1
```

### 最少跳跃次数

按“当前层”和“下一层”计数：

```python
steps = 0
current_end = 0
far = 0
for i in range(len(nums) - 1):
    far = max(far, i + nums[i])
    if i == current_end:
        steps += 1
        current_end = far
return steps
```

## 5. 分发问题

### 分糖果

双向约束：

```python
ratings = [1,2,2]
left = [1] * n
right = [1] * n
# 左到右满足递增
# 右到左满足递增
ans = [max(l, r) for l, r in zip(left, right)]
```

贪心结论来自同时满足相邻约束的最小必要值。

## 6. 常见可贪心信号

- 区间有明确结束时间；
- 排序后每一步只关心边界；
- 要最小化最大等待或最大段；
- 任务按 deadline 或利润有支配关系；
- 字符串按字典序选择时只需看候选首字符和后续安全长度。

## 7. 陷阱清单

- 排序键选错，如按起点而不是结束时间。
- 区间重叠定义没弄清：端点相等算不算重叠。
- 多个目标冲突时单维贪心失败。
- 贪心没有反例也不代表正确，仍需证明。
- 需要字典序时，忘记检查剩余资源是否足够。

> 贪心的浪漫在于决断，贪心的严谨在于证明。
"""

CONTENT["dynamic-programming"] = """## 1. DP 不是背公式

DP 是用历史子问题的答案避免重复计算。核心只有四个问题：

1. **状态是什么？**
2. **状态值表示什么？**
3. **状态之间如何转移？**
4. **边界和答案在哪里？**

建议先写状态定义，再写转移，最后写循环。

## 2. 线性 DP

### 爬楼梯

```python
dp[0] = 1
dp[1] = 1
dp[i] = dp[i - 1] + dp[i - 2]
```

### 打家劫舍

```python
dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
```

状态含义：前 i 个房屋最大收益；第 i 个可选可不选。

## 3. 子序列 DP

### 最长上升子序列

O(n^2)：

```python
dp[i] = 1 + max(dp[j] for j in range(i) if nums[j] < nums[i], default=0)
```

O(n log n)：维护 `tails[k]` 表示长度为 k+1 的 LIS 的最小尾值。

```python
import bisect

def lis(nums):
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
```

### 编辑距离

状态：`dp[i][j]` 表示 `word1[:i]` 变成 `word2[:j]` 的最少操作。

```python
if a[i - 1] == b[j - 1]:
    dp[i][j] = dp[i - 1][j - 1]
else:
    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
```

## 4. 背包 DP

### 0/1 背包

每个物品最多一次，容量倒序：

```python
for weight, value in items:
    for c in range(capacity, weight - 1, -1):
        dp[c] = max(dp[c], dp[c - weight] + value)
```

### 完全背包

物品无限，容量正序：

```python
for weight, value in items:
    for c in range(weight, capacity + 1):
        dp[c] = max(dp[c], dp[c - weight] + value)
```

### 组合数与排列数

- 求组合数：外层物品，内层容量；
- 求排列数：外层容量，内层物品。

顺序不同，语义不同。

## 5. 区间 DP

状态通常是左端点和右端点。

石子合并、戳气球一类先思考：

```text
最后一次操作发生在哪个分割点？
```

## 6. 状态压缩 DP

当状态是集合时，用位掩码。

```python
dp[1 << i][i] = cost[start][i]
```

常用于旅行商、任务分配、覆盖问题。n 通常不超过 20。

## 7. 记忆化 vs 递推

| 方式 | 优点 | 注意 |
|---|---|---|
| 记忆化 DFS | 状态转移直观 | 递归深度、重复状态定义 |
| 递推 | 可优化空间、顺序清晰 | 循环方向容易错 |

## 8. 陷阱清单

- 状态定义不清，转移自然混乱。
- 初始化用了 0，但合法路径数应为 1。
- 负数、零、重复元素破坏最长上升子序列逻辑。
- 0/1 背包误用正序导致物品重复选取。
- 字符串 DP 中 `dp[i]` 到底表示前 i 个字符还是下标 i，必须固定。
- 求方案数忘了取模。

> DP 的美感是把混乱的未来拆成已知的过去。
"""

CONTENT["strings"] = """## 1. 字符串的三种视角

1. **数组视角**：可下标、可扫描；
2. **计数视角**：只关心频次或等价签名；
3. **结构视角**：前缀、后缀、回文、匹配状态。

## 2. 回文

### 中心扩展

奇偶中心分开处理：

```python
def expand(s, l, r):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        l -= 1
        r += 1
    return l + 1, r

def longest_palindrome(s):
    best = (0, 0)
    for i in range(len(s)):
        for l, r in (expand(s, i, i), expand(s, i, i + 1)):
            if r - l > best[1] - best[0]:
                best = (l, r)
    return s[best[0]:best[1]]
```

### DP

`dp[i][j]` 表示 `s[i:j+1]` 是否回文：

```python
if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
    dp[i][j] = True
```

## 3. 前缀和与差分

字符频次可用固定长度数组：

```python
cnt = [0] * 26
for ch in s:
    cnt[ord(ch) - ord('a')] += 1
```

异位词比较时可维护窗口频次，而不是每次重建 Counter。

## 4. 字符串匹配

### 朴素匹配

每个起点比较，O(nm)。小数据够用。

### KMP

`next[i]` 表示模式串 `p[:i+1]` 的最长相等真前后缀长度。

```python
def build_next(p):
    nxt = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = nxt[k - 1]
        if p[i] == p[k]:
            k += 1
        nxt[i] = k
    return nxt
```

匹配失败时，模式串不用回到起点，而是跳到下一个可能的前缀状态。

## 5. 字典序贪心

移除 K 个字符使剩余字典序最小：

```python
stack = []
removals = k
for ch in s:
    while stack and removals and stack[-1] > ch:
        stack.pop()
        removals -= 1
    stack.append(ch)
while removals:
    stack.pop()
    removals -= 1
return ''.join(stack)
```

不变量：栈内前缀在允许删除数内尽量保持上升。

## 6. 规范化键

- 大小写：统一 lower；
- Unicode：必要时 normalization；
- 空格与标点：题面决定是否忽略；
- 分数：约分后 `(a//g, b//g)`。

## 7. 陷阱清单

- 只处理 ASCII，输入却含中文或 emoji。
- 空串、单字符、全相同字符。
- 回文子串和回文子序列不是一回事。
- 大数进制转换溢出。
- 字典序最小不等于字符数最少。

> 字符串题经常在考“你能否找到隐藏的重复结构”。
"""

CONTENT["union-find-advanced"] = """## 1. 并查集解决什么

并查集维护不相交集合，支持：

- `find(x)`：找代表元；
- `union(a,b)`：合并两个集合；
- `connected(a,b)`：判断是否同集合。

路径压缩 + 按大小合并后，单次操作近似 O(α(n))，其中 α 是极慢增长的反阿克曼函数。

## 2. 基本实现

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True
```

`union` 返回 False 表示本来已连通，常用于检测冗余边。

## 3. 常见应用

- 无向图连通分量；
- Kruskal MST；
- 冗余连接；
- 账户合并；
- 可交换位置字符串；
- 离线区间合并；
- 网格岛屿动态增加。

## 4. 带权并查集

当需要知道同类关系或相对偏移时，维护到根的权重。

```python
weight[x] = x 到 parent[x] 的关系
```

路径压缩时同步更新：

```python
root_x = find(parent[x])
weight[x] = combine(weight[x], weight[parent[x]])
parent[x] = root_x
```

适合等式/不等式、比例传递、颜色交替关系。

## 5. 其他高级结构一瞥

| 结构 | 典型用途 |
|---|---|
| 线段树 | 区间更新、区间查询 |
| Fenwick/BIT | 单点更新、前缀和 |
| Trie | 前缀检索、字典树 DP |
| 稀疏表 | 静态区间最值 |
| 平衡树 | 动态有序集合 |

面试高频度上，并查集 > Trie > 线段树/BIT。

## 6. 陷阱清单

- 初始化大小不是节点数。
- `find` 没有路径压缩，退化成链。
- 无向图判断环时忘了比较两个根。
- 并查集只能处理无向连通关系，不能直接表达方向依赖。
- 动态删点困难，通常需要离线倒序处理或可持久化。

> 并查集的美在于：不需要知道完整路径，只需要知道“谁和你是一伙的”。
"""

CONTENT["math-bit-probability"] = """## 1. 位运算基础

```text
x & 1       判断奇偶
x >> 1      除以 2 向下取整（非负）
1 << k      2^k
x & (x - 1) 清除最低位 1
x & (-x)    取最低位 1
^           相同抵消，不同保留
```

## 2. 只出现一次的数字

### 一个唯一数

```python
ans = 0
for x in nums:
    ans ^= x
return ans
```

### 其他数出现三次

使用每一位计数：

```python
ans = 0
for bit in range(32):
    total = sum((x >> bit) & 1 for x in nums)
    if total % 3:
        ans |= 1 << bit
# Python 中负数需按题意转换为有符号数
```

## 3. 二进制状态压缩

用每一位表示“是否选择/已访问”：

```python
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            ...
```

n 一般不超过 20。状态转移可以从已选集合推未选项。

## 4. 数学常用方法

### 约束收缩

- 最大公约数：欧几里得；
- 最小公倍数：`a*b/gcd(a,b)`；
- 质数筛：埃氏筛；
- 快速幂：指数二分。

### 计数与抽屉

当结果空间巨大时，考虑：

- 只统计对答案有影响的维度；
- 排序后相邻关系；
- 前缀计数；
- 哈希分桶。

## 5. 随机化

### Fisher-Yates 洗牌

```python
for i in range(len(a) - 1, 0, -1):
    j = random.randint(0, i)
    a[i], a[j] = a[j], a[i]
```

### 蓄水池抽样

不知道流长度时，等概率保留 k 个：

```python
for i, x in enumerate(stream):
    if i < k:
        reservoir[i] = x
    else:
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = x
```

第 i 个元素进入样本的概率是 k/i。

## 6. 隐藏不变量

数学题常需要找守恒量：

- 总和不变；
- 奇偶性不变；
- 最大最小差值只由全局边界决定；
- 每次操作等价于移动一个指针；
- 相同余数可以归为同一类。

## 7. 陷阱清单

- Python 负数右移语义与 C/Java 不同。
- 乘法取模要分步 `((a * b) % mod) * c % mod`。
- `random.shuffle` 不是自己重写的原因；若手写，索引范围必须正确。
- 位掩码题忽略 0 号位。
- 概率题把“均匀选择下标”写成“均匀选择值”。

> 数学题的突破口常常是：什么东西从头到尾没有变？
"""

CONTENT["engineering-interview"] = """## 1. 面试不是考试，是协作调试

面试官想看到：

1. 能否澄清约束；
2. 能否提出暴力解并分析瓶颈；
3. 能否选择合适的结构；
4. 能否写出可运行边界；
5. 能否主动测试和修复。

推荐节奏：

```text
重复题面 -> 举例子 -> 暴力解 -> 瓶颈 -> 优化状态 -> 伪代码 -> 编码 -> 自测
```

## 2. 从暴力到优化

| 暴力形态 | 常见优化 |
|---|---|
| 两层循环找 pair | 哈希、排序 + 双指针 |
| 所有子数组 | 前缀和、滑动窗口 |
| 所有子集 | 状压 DP、位运算 |
| 所有排列 | 回溯剪枝 |
| 每次扫描最值 | 堆、单调栈/队列 |
| 判断连通 | DFS/BFS、并查集 |

## 3. 写代码前回答四问

1. 输入可能为空吗？
2. 有重复值吗？
3. 是否允许修改输入？
4. 答案不唯一时返回哪个？

这四问能避免大量边界 Bug。

## 4. 自测模板

写完后至少检查：

```text
空输入
单元素
两个相等元素
全部递增/递减
目标在开头/结尾/不存在
负数或零
最大规模
```

面试时不要默写测试名，要具体说值。

## 5. 工程化设计题

### Rate Limiter

可选算法：

- 固定窗口：简单，有边界突刺；
- 滑动日志：精确，内存大；
- 滑动窗口计数：折中；
- Token Bucket：允许短时突发。

需要讨论分布式锁、Redis TTL、时间同步和失败降级。

### LRU / LFU

- LRU：哈希 + 双向链表；
- LFU：频次桶 + 每个频次内 LRU；
- 工程中还要考虑容量、TTL、并发读写和缓存穿透。

### Top K 流式统计

- Count-Min Sketch 估计频次；
- 小根堆维护 K；
- 分片统计后聚合；
- 时间窗口滚动重置。

### 数据一致性

- 数据库索引：B+ tree 支持范围；
- 缓存：旁路缓存、失效策略；
- 消息：幂等键、去重表；
- 校验：哈希校验和、版本号。

## 6. Debug 纪律

遇到错误不要乱改：

1. 复现最小输入；
2. 打印关键不变量；
3. 二分定位失败步骤；
4. 解释为什么修复后正确；
5. 再补一个针对该 Bug 的测试。

## 7. 沟通句式

```text
我先假设输入规模是 ______；
暴力做法是 ______，复杂度 ______；
瓶颈在 ______；
我可以把 ______ 变成键/状态/有序边界；
这样把 ______ 降到 ______；
边界包括 ______。
```

> 专业不是没有 Bug，而是有办法快速把错误变成可解释、可修复、可预防的事实。
"""

CONTENT.update(NEW_CONTENT)

CHAPTER_DIAGRAMS = {
    "complexity": ("chapter-complexity-growth.svg", "复杂度增长形状对比：O(log n)、O(n)、O(n log n)、O(n²)"),
    "array-two-pointers": [("chapter-array-two-pointers.svg", "对撞双指针淘汰较弱一侧"), ("chapter-sliding-window.svg", "滑动窗口用 left 修复非法区间")],
    "stack-queue-monotonic": ("chapter-monotonic-stack.svg", "单调栈维护未解决候选"),
    "hash-and-counting": ("chapter-hash-prefix-sum.svg", "前缀和与哈希表查询关系"),
    "linked-list": ("chapter-linked-list-cycle.svg", "快慢指针在环内追上"),
    "recursion-divide-binary-search": ("chapter-binary-search-boundary.svg", "二分搜索维持已确定边界"),
    "trees": ("chapter-tree-recursion.svg", "树的后序遍历先取子问题答案再合并"),
    "heaps": ("chapter-heap-shape.svg", "堆父子顺序与 Top K 维护"),
    "graph-search": [("chapter-graph-bfs-layers.svg", "BFS 按层扩散与访问标记"), ("chapter-topological-order.svg", "DAG 拓扑排序按入度展开")],
    "graph-shortest-mst": ("problem-p073-dijkstra.svg", "非负边权下的 Dijkstra 最近节点固定过程"),
    "backtracking": ("chapter-backtracking-tree.svg", "回溯的选择、探索与撤销"),
    "greedy": ("chapter-interval-scheduling.svg", "按结束时间选择互不重叠区间"),
    "dynamic-programming": ("chapter-dp-state-grid.svg", "DP 状态来源与边界顺序"),
    "union-find-advanced": ("chapter-union-find.svg", "并查集按根判断连通"),
}
CHAPTER_DIAGRAMS.update(NEW_CHAPTER_DIAGRAMS)


def build_chapter_metadata():
    return CHAPTERS


def write_chapters():
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for item in CHAPTERS:
        target = CHAPTERS_DIR / item["file"]
        markdown = CONTENT[item["id"]].strip()
        diagrams = CHAPTER_DIAGRAMS.get(item["id"], [])
        if diagrams:
            if isinstance(diagrams, tuple):
                diagrams = [diagrams]
            figures = "\n\n".join(f"![{caption}](./assets/diagrams/{filename})" for filename, caption in diagrams)
            markdown += f"\n\n## 一图看懂\n\n{figures}\n"
        target.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    (DATA_DIR / "chapters.json").write_text(
        json.dumps(CHAPTERS, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def validate():
    ids = [item["id"] for item in CHAPTERS]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate chapter id")
    allowed_sections = {"start", "structures", "techniques", "advanced"}
    missing = [item["id"] for item in CHAPTERS if item["id"] not in CONTENT]
    if missing:
        raise ValueError(f"missing content: {missing}")
    invalid = [item["id"] for item in CHAPTERS if item["section"] not in allowed_sections]
    if invalid:
        raise ValueError(f"invalid section: {invalid}")
    files = {item["file"] for item in CHAPTERS}
    for path in CHAPTERS_DIR.glob("*.md"):
        if path.name not in files:
            print(f"warning: orphan chapter file {path.name}")


def main():
    write_chapters()
    validate()
    print(f"generated {len(CHAPTERS)} chapters")


if __name__ == "__main__":
    main()
