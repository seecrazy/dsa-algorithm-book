## 1. 图不是格子，是关系

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

## 一图看懂

![BFS 按层扩散与访问标记](./assets/diagrams/chapter-graph-bfs-layers.png)

![DAG 拓扑排序按入度展开](./assets/diagrams/chapter-topological-order.png)
