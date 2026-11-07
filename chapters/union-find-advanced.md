## 1. 并查集解决什么

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

面试高频度上，并查集 > Trie > 线段树/BIT。BIT 至少要会手写，核心是 `lowbit(i) = i & (-i)`：它把下标按二进制末位 1 分层，让每个下标只负责一段固定区间的和：

```python
class BIT:
    def __init__(self, n): self.tree = [0] * (n + 1)   # 1-indexed
    def update(self, i, delta):            # 位置 i 增加 delta
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & (-i)                  # 跳向包含 i 的上层
    def query(self, i):                    # 前缀和 [1..i]
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)                  # 剥掉末位 1
        return s
```

更新和查询都是 O(log n)。经典应用是逆序对：把数组离散化成 1..n 的排名，从左往右扫描，每个元素先查“已入库的数里比它大的个数”再入库——这是排序章逆序对题在归并计数之外的另一条路线。

## 6. 陷阱清单

- 初始化大小不是节点数。
- `find` 没有路径压缩，退化成链。
- 无向图判断环时忘了比较两个根。
- 并查集只能处理无向连通关系，不能直接表达方向依赖。
- 动态删点困难，通常需要离线倒序处理或可持久化。

> 并查集的美在于：不需要知道完整路径，只需要知道“谁和你是一伙的”。

## 一图看懂

![并查集按根判断连通](./assets/diagrams/chapter-union-find.png)
