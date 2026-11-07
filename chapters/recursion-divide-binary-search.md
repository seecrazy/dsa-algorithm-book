## 1. 递归的三要素

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

## 一图看懂

![二分搜索维持已确定边界](./assets/diagrams/chapter-binary-search-boundary.png)
