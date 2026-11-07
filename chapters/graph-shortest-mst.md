## 1. 最短路的四种场景

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

## 一图看懂

![非负边权下的 Dijkstra 最近节点固定过程](./assets/diagrams/problem-p073-dijkstra.svg)
