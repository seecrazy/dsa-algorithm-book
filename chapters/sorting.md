## 1. 排序不是背 API

排序回答一个更根本的问题：顺序应该由什么决定？

比较排序每次只能得到“谁在前、谁在后”，决策树必须区分 `n!` 个排列，所以比较排序下界是：

```text
O(log(n!)) = O(n log n)
```

要想突破它，必须使用值的结构，例如数字位数、值域范围或桶边界。

## 2. 比较排序

### 快速排序

随机选 pivot，把数组分成 `< pivot` 和 `>= pivot` 两段，再递归两侧。

```python
def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = random.choice(a)
    less = [x for x in a if x < pivot]
    equal = [x for x in a if x == pivot]
    greater = [x for x in a if x > pivot]
    return quick_sort(less) + equal + quick_sort(greater)
```

期望 O(n log n)，最坏 O(n^2)；原地版本空间 O(log n)，但重复元素、已排序输入和递归深度都要处理。

### 归并排序

分成两半，排序后合并。稳定，时间稳定 O(n log n)，但通常需要 O(n) 辅助数组。

### 堆排序

建堆后反复取堆顶放末尾。原地、最坏 O(n log n)，但缓存不友好且不稳定。

## 3. 非比较排序

### 计数排序

值域较小时，统计每个值出现次数，再顺序还原。

```python
def counting_sort(a, max_value):
    count = [0] * (max_value + 1)
    for x in a:
        count[x] += 1
    out = []
    for value, times in enumerate(count):
        out.extend([value] * times)
    return out
```

### 基数排序

按最低位到最高位依次稳定排序。每位使用计数排序，总复杂度 `O(d * (n + base))`。

### 桶排序

把近似均匀分布的数据放入桶，桶内再排序。期望接近 O(n)，数据倾斜时退化。

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

## 一图看懂

![比较排序、计数、基数和桶排序的选型路径](./assets/diagrams/chapter-sorting-models.png)
