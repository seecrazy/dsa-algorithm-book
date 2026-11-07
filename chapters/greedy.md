## 1. 贪心的合法性

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

## 一图看懂

![按结束时间选择互不重叠区间](./assets/diagrams/chapter-interval-scheduling.png)
