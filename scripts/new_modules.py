# -*- coding: utf-8 -*-
"""Supplementary algorithm and data-structure chapters."""

NEW_CHAPTERS = [
    {
        "id": "sorting", "title": "排序：从比较到分桶", "subtitle": "稳定、原地、期望与最坏，不只是 sort()",
        "section": "techniques", "file": "sorting.md", "minutes": 28,
        "tags": ["排序", "分治", "计数排序", "工程选型"],
    },
    {
        "id": "trie", "title": "Trie：前缀就是路径", "subtitle": "把共享前缀变成树边",
        "section": "structures", "file": "trie.md", "minutes": 20,
        "tags": ["Trie", "字典树", "前缀"],
    },
    {
        "id": "balanced-search-trees", "title": "AVL 与红黑树", "subtitle": "让 BST 不退化为链",
        "section": "structures", "file": "balanced-search-trees.md", "minutes": 30,
        "tags": ["AVL", "红黑树", "平衡树", "BST"],
    },
    {
        "id": "b-trees", "title": "B 树与 B+ 树", "subtitle": "为磁盘页和范围扫描设计",
        "section": "advanced", "file": "b-trees.md", "minutes": 26,
        "tags": ["B树", "B+树", "索引", "磁盘"],
    },
    {
        "id": "branch-and-bound", "title": "分支限界", "subtitle": "用界剪掉注定更差的子树",
        "section": "techniques", "file": "branch-and-bound.md", "minutes": 26,
        "tags": ["分支限界", "剪枝", "优先队列", "组合优化"],
    },
    {
        "id": "graph-representation", "title": "图的表示与建模选型", "subtitle": "先选容器，再选算法",
        "section": "advanced", "file": "graph-representation.md", "minutes": 20,
        "tags": ["图", "邻接表", "邻接矩阵", "建模"],
    },
]

NEW_CONTENT = {}

NEW_CONTENT["sorting"] = """## 1. 排序不是背 API

排序回答一个更根本的问题：顺序应该由什么决定？

比较排序每次只能得到“谁在前、谁在后”，决策树必须区分 `n!` 个排列，所以比较排序下界是：

```text
O(log(n!)) = O(n log n)
```

要想突破它，必须使用值的结构，例如数字位数、值域范围或桶边界。

## 2. 比较排序

### 快速排序

随机选 pivot，把数组分成 `< pivot` 和 `>= pivot` 两段，再递归两侧。列表拼接版好懂，但每层都要复制数组，不是原地排序；实战要掌握原地分区版：

```python
def quick_sort(a, lo=0, hi=None):
    if hi is None: hi = len(a) - 1
    if lo >= hi: return
    p = random.randint(lo, hi); a[p], a[hi] = a[hi], a[p]
    pivot, i = a[hi], lo
    for j in range(lo, hi):        # 不变量：[lo,i) < pivot，[i,j) >= pivot
        if a[j] < pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]      # pivot 落进最终位置 i
    quick_sort(a, lo, i - 1); quick_sort(a, i + 1, hi)
```

期望 O(n log n)、原地，辅助空间 O(log n) 是递归栈；最坏 O(n^2)。期望成立靠随机 pivot：它把“输入已排序”从必然退化变成概率事件。重复元素多时，上面的二路分区会把相等的元素全甩到一侧，分区失衡——这时换三路分区：

```python
def partition3(a, lo, hi, pivot):
    lt, i, gt = lo, lo, hi
    while i <= gt:                 # [lo,lt)<p，[lt,i]=p，(gt,hi]>p
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]; gt -= 1
        else:
            i += 1
    return lt, gt                  # a[lt..gt] 全是 pivot，不再递归
```

一趟结束后与 pivot 相等的元素整体归位、不再参与递归，重复元素海量时也能保持期望 O(n log n)。

### 归并排序

分成两半，排序后合并。稳定，时间稳定 O(n log n)，但通常需要 O(n) 辅助数组。

### 堆排序

建堆后反复取堆顶放末尾。原地、最坏 O(n log n)，但缓存不友好且不稳定。

## 3. 非比较排序

### 计数排序

值域较小时，统计每个值出现次数，再做前缀和得到“每个值的输出边界”，最后反向回填。反向是稳定性的全部来源：相等的元素，数组里靠后的会被放进更靠后的位置，原序得以保留。

```python
def counting_sort(a, max_value):
    count = [0] * (max_value + 1)
    for x in a:
        count[x] += 1
    for i in range(1, max_value + 1):
        count[i] += count[i - 1]           # 前缀和 = 输出边界
    out = [0] * len(a)
    for x in reversed(a):                  # 反向回填保证稳定
        count[x] -= 1
        out[count[x]] = x
    return out
```

时间 O(n + r)、空间 O(r)，r 是值域大小。按值直接铺平输出的写法更短，但相等的元素原序全丢——选型表里“稳定 可实现”四个字，指的就是上面这个版本；基数排序借计数排序当“每位排序器”时，必须用它。

### 基数排序

按最低位到最高位依次稳定排序。每位使用计数排序，总复杂度 `O(d * (n + base))`。

### 桶排序

把近似均匀分布的数据放入桶，桶内再排序。桶数取 n、桶宽取 `(max - min) / n` 是常见起点：均匀假设下每桶期望只落 O(1) 个元素，桶内排序期望 O(1)，总计期望接近 O(n)。数据倾斜时少数桶塞进大多数元素，桶内排序退化主导整体，最坏回到 O(n^2)——桶排序成立的前提是“均匀”这个假设，不是代码本身。

## 4. 选型表

| 算法 | 平均 | 最坏 | 空间 | 稳定 | 适合 |
|---|---:|---:|---:|---|---|
| 快排 | O(n log n) | O(n^2) | O(log n) | 否 | 通用数组、缓存友好 |
| 归并 | O(n log n) | O(n log n) | O(n) | 是 | 链表、外部排序 |
| 堆排 | O(n log n) | O(n log n) | O(1) | 否 | 原地且要最坏保证 |
| 计数 | O(n+r) | O(n+r) | O(r) | 可实现 | 小整数、值域小 |
| 基数 | O(d(n+b)) | 同左 | O(n+b) | 是 | 定长整数/字符串 |
| 桶 | 接近 O(n) | O(n^2) | O(n) | 可实现 | 均匀分布 |

## 5. 陷阱

- 只有需要“相等元素保持原序”时，稳定性才重要。
- Python 的 `sort` 稳定；`sorted(key=...)` 依赖 key，而不是原对象比较。
- 基数排序每一位必须使用稳定排序。
- 快排重复元素多时，三路分区更稳。
- 大对象排序先考虑 key 的构建成本和比较成本。

> 排序不是目的，是把混乱输入变成可扫描、可二分、可分桶的结构。
"""

NEW_CONTENT["trie"] = """## 1. Trie 的动机

哈希表能回答“这个词在吗”，但不能高效回答：

- 有哪些词以前缀 `ap` 开头？
- 是否存在一个词以 `app` 为前缀？
- 把所有共享前缀的词压缩存储。

Trie 把字符串的每个字符看作一条边，从根到某个节点构成前缀。

## 2. 节点模型

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self.find(word)
        return bool(node and node.is_end)

    def starts_with(self, prefix):
        return self.find(prefix) is not None

    def find(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

插入、查找、前缀判断都是 `O(L)`，L 是字符串长度。

## 3. 前缀统计

如果不仅要判断存在，还要统计前缀次数，节点里保存 `pass_count` 和 `end_count`：

```text
insert(word): 沿途 pass_count++；末尾 end_count++
count_prefix(p): find(p).pass_count
count_word(w): find(w).end_count
```

删除 = 沿途 pass_count--，末尾 end_count--，再把 pass_count 归零的节点从父节点摘掉：

```python
def delete(self, word):
    stack = [self.root]
    for ch in word:                      # 沿途记录路径
        if ch not in stack[-1].children: return False
        stack.append(stack[-1].children[ch])
    if not stack[-1].end_count: return False   # 词不存在
    stack[-1].end_count -= 1
    for i in range(len(word), -1, -1):   # 自底向上回收
        stack[i].pass_count -= 1
        if i and stack[i].pass_count == 0:
            stack[i - 1].children.pop(word[i - 1])
    return True
```

O(L)，配合使用时给 TrieNode 加上 `pass_count = end_count = 0` 两个字段即可。回收的唯一依据是 `pass_count == 0`：只要还有别的词共享这段前缀，它就大于 0，节点必须保留——这就是“删除不能破坏共享前缀”的具体含义。另外 `count_prefix(p)` 前记得判 `find(p) is not None`，前缀不存在时没有 pass_count 可读。

## 4. Trie + DFS

二维网格搜多个单词时，不要对每个单词都做一次 DFS。先把单词表建 Trie；DFS 每走到一个字符，就在 Trie 上同步走一步。剪枝更早，重复共享前缀只探索一次。

## 5. 变体

压缩 Trie 值得单独说：把只有一个孩子的节点并进边里，边存字符串片段（边标签），节点数从 O(总字符数) 降到 O(关键码数)；代价是查询要逐段比对边标签，词库大且共享前缀多时（路由表、URL 树）才划算，几十个短词直接用哈希表更省事。Radix Tree 就是它的工程形态。

| 结构 | 作用 |
|---|---|
| 压缩 Trie | 单链路径压成一条边，减少节点 |
| Radix Tree | 压缩 Trie 的工程形式 |
| Aho-Corasick | 多模式串自动机 |
| 三叉搜索树 | 节省稀疏子节点空间 |

## 6. 陷阱

- 子节点数量可能很大，稀疏字符集用哈希表而不是 256 长度数组。
- 删除节点时不能破坏仍被其他单词共享的前缀。
- Unicode 字符可能由多个码点组成，先明确规范化规则。
- 大量短字符串时，哈希表可能更快；Trie 的优势在前缀和共享结构。

> Trie 的价值不在“查单词”，而在“查所有共享前缀的东西”。
"""

NEW_CONTENT["balanced-search-trees"] = """## 1. 为什么普通 BST 不够

按顺序插入 1,2,3,4,5，普通 BST 会变成右链：

```text
1 -> 2 -> 3 -> 4 -> 5
```

查找从 O(log n) 退化到 O(n)。自平衡搜索树的承诺是：即使输入有序，树高仍保持 O(log n)。

## 2. AVL 树

AVL 给每个节点维护：

```text
balance = height(left) - height(right)
```

合法值只能是 `-1, 0, 1`。插入或删除后如果失衡，用旋转恢复。

### 四种失衡

| 情况 | 插入位置 | 处理 |
|---|---|---|
| LL | 左孩子的左子树 | 右旋 |
| RR | 右孩子的右子树 | 左旋 |
| LR | 左孩子的右子树 | 先左旋左孩子，再右旋 |
| RL | 右孩子的左子树 | 先右旋右孩子，再左旋 |

### 右旋直觉

```text
    y            x
   / \\          / \\
  x   C  =>    A   y
 / \\              / \\
A   B            B   C
```

旋转不是把树重排，而是改变根，同时保持 BST 中序顺序不变——对照上图，旋转前后中序都是 `A, x, B, y, C`，BST 性质毫发无损，这就是旋转合法的全部原因。左旋是完全对称的镜像：根 `x` 的右孩子 `y` 上提，`y` 原来的左子树挂给 `x` 当右子树。

LR 和 RL 的“双旋”没有引入第三种旋转：先对失衡节点的孩子做一次反向单旋，把“拐弯”掰直成 LL 或 RR，再做第二次单旋。以 LR 为例，先左旋左孩子后，新插入的节点就落到了左孩子的外侧，三层结构变成标准 LL，再对根右旋即可。

## 3. 红黑树

红黑树通过颜色近似平衡，保证最长路径不超过最短路径两倍。五个性质：

1. 节点是红或黑。
2. 根是黑。
3. 叶 NIL 是黑。
4. 红节点的孩子都是黑。
5. 任一节点到后代 NIL 的黑高相同。

性质 4 和 5 合起来直接给出两倍界：所有路径黑高相同（性质 5），红不能连续（性质 4），所以每条路径的黑节点数一样多，路径总节点数至多是黑节点数的两倍，树高 ≤ 2 × 黑高；而 n 个节点的树黑高至多 log(n+1)，于是树高 ≤ 2log(n+1) = O(log n)。“近似平衡”不是口号，是两条性质算出来的结论。

插入新节点通常先染红——红色不改变黑高，是最便宜的选择。如果父节点也是红，违反性质 4，按叔叔颜色分两种情况：

- 叔叔是红：父、叔改黑，祖父改红，冲突上推两层由祖父继续处理。便宜，但可能一路推到根。
- 叔叔是黑：先旋转把“三角形”摆成“直线”（化归方式同 AVL 的 LR/RL），再父黑祖红换色，一次终结。

红黑树旋转次数少于 AVL，正是因为多数插入走“变色上推”这条便宜路径；写操作成本更低，读密集场景则 AVL 的更严格平衡更有优势。

## 4. 工程取舍

| 树 | 平衡强度 | 修改成本 | 常见用途 |
|---|---|---|---|
| AVL | 更严格 | 旋转多 | 查询密集 |
| 红黑树 | 近似平衡 | 旋转少 | map/set、内核调度 |
| 跳表 | 概率平衡 | 简单 | Redis 有序集合 |

## 5. 陷阱

- 旋转后要自下而上更新高度：先更新被旋下去的原根，再更新新根；顺序反了，新根会拿旧高度做失衡判断。
- LR 和 RL 必须先处理孩子，再旋转祖孙三层。
- 红黑树的 NIL 也要视为黑。
- 删除比插入复杂很多，不能只用插入直觉套用。

> 平衡树的本质是：用局部旋转维护全局 O(log n)。
"""

NEW_CONTENT["b-trees"] = """## 1. 为什么内存树不够

二叉树每个节点只有两个孩子，磁盘读取一个节点可能只利用很少数据。数据库不能为每一层都做一次随机磁盘读，还要控制树高和写放大。

B 树 / B+ 树把一个节点做成一页：一次 I/O 读入多个键。

## 2. B 树

一棵最小度数为 `t` 的 B 树（等价说法是 `2t` 阶：内部节点最多 `2t` 棵子树）：

- 每个节点最多 `2t - 1` 个键；
- 内部节点最多 `2t` 个孩子，除根外至少 `t` 个；
- 除根外至少 `t - 1` 个键；
- 所有叶子在同一层；
- 键把子树范围切开：`k` 个键正好对应 `k + 1` 个子指针，键是路标，查询落在哪两个键之间就走对应区间那个孩子。

插入时若节点已满，先分裂：

```text
[x y z]        y
              / \\
           [x]   [z]
```

分裂把中间键上移，保持所有叶子深度相同——新节点来自分裂而不是下探，叶子只会在根分裂时同时长高。工程实现常自顶向下预分裂：下探途中遇到满节点先裂再走，用少量不必要的分裂换来回溯自由的插入。

## 3. B+ 树

B+ 树与 B 树最大的差异：

- 内部节点通常只存索引键；
- 真实数据都在叶子；
- 内部键只是路标副本，同一个键会在叶子里再出现一次；
- 叶子通常用链表连接；
- 范围扫描顺着叶子链走，不需要回溯。

这也是数据库索引常用 B+ 树的原因：

```text
范围查询 a <= key <= b:
1. 从根定位到叶子；
2. 在叶子内二分找起点；
3. 沿叶子链表顺序扫描；
4. 超过 b 停止。
```

## 4. 代价

| 操作 | B/B+ 树 | 说明 |
|---|---:|---|
| 查找 | O(log n) | 树高乘节点内查找 |
| 插入 | O(log n) | 可能触发分裂 |
| 删除 | O(log n) | 可能借键、合并 |
| 范围扫描 | O(log n + m) | m 是返回数量 |

节点越大，树高越低，但节点内查找、写放大和缓存开销也要平衡。量化一下：t = 100 时，高度 3 的 B 树至少能容纳 `2t^3 - 1` 个键，约 200 万，百万级索引只需 3 次 I/O 就能定位——这是 B/B+ 树在磁盘上的全部卖点。

## 5. 陷阱

- B+ 树的叶子链表需要维护插入和分裂后的前后指针。
- 节点内可以用二分查找，不要线性扫描大页。
- 删除不一定要立刻收缩树高，过度合并会增加写放大。
- 数据库索引还涉及页大小、聚簇索引、二级索引、事务和缓存，不能只看理论复杂度。

> B+ 树不是更高级的二叉树，而是把“树高、磁盘页、顺序 I/O”一起设计出来的结构。
"""

NEW_CONTENT["branch-and-bound"] = """## 1. 回溯与分支限界

把搜索过程画成一棵状态空间树：每个节点是一个部分解（已做出的一部分选择），叶子是完整解，边是“多做一个决定”。回溯系统性枚举这棵树，用合法性剪枝去掉非法分支；分支限界更进一步：为部分解计算一个界，证明它不可能优于当前最优解，然后整棵子树剪掉。两章的分水岭一句话：要“所有解”用回溯，要“最优解”先给界——回溯章的模板是这里的起点。

## 2. 四个组件

```text
1. 状态：已做选择 + 剩余资源/剩余变量
2. 分支：扩展下一个变量或任务
3. 界：部分解能达到的最好/最差估计
4. 剪枝：bound 不可能击败当前 best 时停止
```

最小化问题常用下界；最大化问题常用上界。

## 3. 与回溯的对比

| 方法 | 搜索顺序 | 剪枝依据 | 适合 |
|---|---|---|---|
| 回溯 | DFS | 合法性、可行性、简单最优性 | 排列、组合、构造 |
| 分支限界 | BFS/最佳优先 | 可证明的上下界 | 最优组合问题 |

最佳优先分支限界的主循环只有一个形状：

```text
heap 装 (界, 状态)，best 先给平凡解或 +∞
while heap:
    界, 状态 = 弹出界最小的状态      # 最小堆：先探索最有希望的分支
    if 界 >= best: continue          # 已不可能更优，丢弃
    if 状态是完整解: best = min(best, 该解代价); continue
    for child in 扩展(状态): 堆入 (child 的界, child)
```

最小化问题用下界配最小堆，最大化问题用上界配最大堆，方向不能混。

## 4. 0/1 背包示例

状态：

```text
(index, current_value, current_weight)
```

上界可以取当前价值加上剩余物品按单位价值贪婪装满的松弛值。

```python
def upper_bound(items, i, value, capacity_left):
    bound = value
    for w, v in items[i:]:
        if w <= capacity_left:
            bound += v
            capacity_left -= w
        else:
            bound += v * capacity_left / w
            break
    return bound
```

若 `upper_bound <= best_value`，该分支无需继续。

## 5. TSP 示例

状态是“已访问集合 + 当前城市 + 已走路程”。下界可以用剩余城市的最小出边之和估计：任何完整回路都要从每个剩余城市恰好离开一次，所以真实代价不可能低于各城最小出边之和——这就是它作为下界合法的原因。优先队列每次扩展当前下界最小的部分路径，尽快找到强上界，从而剪掉更多分支。

## 6. 陷阱

- 界必须松弛且可证明，否则可能剪掉最优解。
- 优先队列只改善搜索顺序，不减少最坏复杂度。
- 上界/下界方向不能弄反。
- 全局 best 要尽早更新，界剪枝才有威力。
- 并行或重复状态要去重，否则状态空间爆炸。

> 分支限界的艺术是构造“足够紧、计算又便宜”的界。
"""

NEW_CONTENT["graph-representation"] = """## 1. 先选表示，再选算法

图算法的常数和可行性往往由表示法决定。常见表示有四类：

| 表示法 | 空间 | 判断边 | 遍历所有边 | 适合 |
|---|---:|---:|---:|---|
| 邻接表 | O(V+E) | O(degree) | O(V+E) | 稀疏图、DFS/BFS |
| 邻接矩阵 | O(V^2) | O(1) | O(V^2) | 密集图、Floyd |
| 边数组 | O(E) | O(E) | O(E) | Kruskal、Bellman-Ford |
| 隐式图 | 按状态数 | 生成邻居 | 生成邻居 | 状态搜索、拼图 |

## 2. 邻接表

```python
from collections import defaultdict

def build_undirected(edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph
```

无向边必须加入两个方向。带权边存 `(neighbor, weight)`，否则只存邻居。

## 3. 邻接矩阵

```python
dist[u][v]
```

优点是 O(1) 判断边和快速自环/重复边处理；缺点是 V 大时空爆。适合 Floyd-Warshall、小型密集图。

## 4. 边数组

```python
edges = [(u, v, w), ...]
```

Kruskal 只需要按边排序；Bellman-Ford 只需要逐轮松弛边。它不擅长快速查“u 有哪些邻居”。

## 5. 隐式图

很多题不给出图，而是给出状态转移：

- 迷宫格子；
- 换一个字母的单词接龙；
- 滑块拼图；
- 正则状态。

不显式建图，在 BFS/DFS 中调用 `neighbors(state)` 即可。但要控制状态总数，否则会爆炸。

## 6. 反向图与网格图

有向图求“谁能到达 t”，可以建反向边再从 t 出发。网格图天然是隐式图：

```python
dirs = [(1,0), (-1,0), (0,1), (0,-1)]
```

八方向只在题目明确允许时使用。

## 7. 建模检查

1. 点是什么？物理位置、任务、状态还是变量？
2. 边是什么？可达、依赖、冲突还是转换？
3. 权是什么？时间、成本、次数还是风险？
4. 有向还是无向？
5. 需要反向查询吗？
6. 状态数会不会爆炸？

> 图题的一半在算法，另一半在把现实约束翻译成正确的点、边和权。
"""

NEW_CHAPTER_DIAGRAMS = {
    "sorting": ("chapter-sorting-models.png", "比较排序、计数、基数和桶排序的选型路径"),
    "trie": ("chapter-trie-prefix.png", "Trie 共享前缀与查询路径"),
    "balanced-search-trees": ("chapter-avl-rotation.png", "AVL 旋转保持中序顺序"),
    "b-trees": ("chapter-btree-split.png", "B+ 树节点分裂与叶子链表"),
    "branch-and-bound": ("chapter-branch-bound.png", "分支限界按界剪枝"),
    "graph-representation": ("chapter-graph-representation.png", "邻接表、矩阵、边数组和隐式图对比"),
}
