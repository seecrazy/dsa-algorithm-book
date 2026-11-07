## 1. 堆的承诺

堆不是完全排序，它只承诺**根是当前最优先元素**。

- Python `heapq` 是最小堆；
- 最大堆通常对值取负；
- 插入和弹出都是 O(log n)；
- 查看堆顶是 O(1)。

## 2. Top K 的选择

### 前 K 小

用最大堆维护 K 个最小元素：

```python
import heapq

def k_smallest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]
```

### 前 K 大

用最小堆维护 K 个最大元素：

```python
def k_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap
```

为什么不是维护 K 个“最大堆”？因为要快速淘汰当前候选中最差的那个。

## 3. 双堆求中位数

- 左半部分：最大堆；
- 右半部分：最小堆；
- 两堆大小差不超过 1；
- 每次插入后平衡并移动堆顶。

```text
若新元素 <= 左堆顶，进左堆；否则进右堆。
左堆过大，把左堆顶移入右堆。
右堆比左堆大超过 1，把右堆顶移入左堆。
```

## 4. 合并 K 个有序序列

K 路归并：

```python
import heapq

def merge_sorted(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return result
```

堆项要包含序列编号，避免值相等时比较下一个不可比较对象。

## 5. 延迟删除

堆不支持任意删除。若任务失效，常用延迟删除：

```python
while heap and invalid(heap[0]):
    heapq.heappop(heap)
```

配合计数器记录每个元素应存在多少次。

## 6. 陷阱清单

- Python 没有内置最大堆，取负后要还原符号。
- 堆项是元组时，第二个元素也要可比较。
- Top K 题先问是前 K 大、前 K 小、按频次还是按距离。
- 流式数据不能排序全量，要用固定大小堆。
- 删除堆顶后才检查新堆顶可能过期，要循环清理。

> 堆教会我们一件事：很多问题不需要全部顺序，只需要随时知道最该处理谁。

## 一图看懂

![堆父子顺序与 Top K 维护](./assets/diagrams/chapter-heap-shape.png)
