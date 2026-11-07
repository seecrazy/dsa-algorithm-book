## 1. 哈希表的价值

哈希表的核心不是“更快”，而是**把等价关系变成键**。

它常用在：

- 判断见过与否；
- 前缀和首次出现位置；
- 分组同构元素；
- 频次统计；
- O(1) 索引从值到下标。

## 2. 计数三件套

### 存在性

```python
seen = set()
if x in seen: ...
seen.add(x)
```

### 频次

```python
from collections import Counter
freq = Counter(nums)
```

### 分组键

```python
groups = {}
for x in xs:
    groups[key(x)].append(x)
```

设计 `key()` 是这类题的真正难点：

- 异位词：排序字符串，或字符计数元组；
- 位移词：相邻字符差值规范化；
- 分数：化简为最简比值；
- 网格状态：序列化成字符串或元组。

## 3. 前缀和 + 哈希

求和为 k 的子数组数量：

```python
from collections import defaultdict

def subarray_sum(nums, k):
    count = 0
    seen = defaultdict(int)
    seen[0] = 1
    prefix = 0
    for x in nums:
        prefix += x
        count += seen[prefix - k]
        seen[prefix] += 1
    return count
```

不变量：`seen[p]` 表示前缀和 p 之前出现的次数。`prefix - k` 若出现过，每个出现点都是一个合法起点前缀。

## 4. 哈希不能解决一切

哈希适合等值查找，不适合：

- 保序遍历，除非额外维护顺序；
- 区间最值；
- 范围排名；
- 邻近查找；
- 需要最坏复杂度保证的实时系统。

这些场景考虑排序数组、堆、树状结构或平衡树。

## 5. 陷阱清单

- 用 list 当 dict 键会报错，要换成 tuple。
- `defaultdict` 在读取时会创建键，统计前要先想清楚。
- 浮点数不要直接当精确键。
- 有重复元素时，返回下标不能用“值 -> 唯一下标”。
- 字符串哈希在多语言环境中可能受 Unicode 规范化影响。

> 哈希是一种观点：我关心的不是完整对象，而是它的等价签名。

## 一图看懂

![前缀和与哈希表查询关系](./assets/diagrams/chapter-hash-prefix-sum.svg)
