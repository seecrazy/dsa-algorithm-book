## 1. 先选表示，再选算法

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

## 一图看懂

![邻接表、矩阵、边数组和隐式图对比](./assets/diagrams/chapter-graph-representation.png)
