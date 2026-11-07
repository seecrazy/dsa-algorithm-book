## 1. 排序不是背 API

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

## 一图看懂

![比较排序、计数、基数和桶排序的选型路径](./assets/diagrams/chapter-sorting-models.png)
