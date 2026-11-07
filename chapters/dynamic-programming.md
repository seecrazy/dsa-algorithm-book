## 1. DP 不是背公式

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

## 一图看懂

![DP 状态来源与边界顺序](./assets/diagrams/chapter-dp-state-grid.svg)
