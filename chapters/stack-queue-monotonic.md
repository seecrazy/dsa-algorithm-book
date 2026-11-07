## 1. 栈：最近的优先

栈只暴露顶端，天然适合：

- 括号配对；
- 表达式求值；
- 递归转迭代；
- 撤销最近一次选择；
- 维护“最近未解决的元素”。

加一根辅助栈就能 O(1) 取最小值：

```python
class MinStack:
    def __init__(self):
        self.stack, self.min = [], []
    def push(self, x):
        self.stack.append(x)
        self.min.append(min(x, self.min[-1] if self.min else x))
    def pop(self):
        self.stack.pop(); self.min.pop()
    def get_min(self):
        return self.min[-1]
```

三个操作都是 O(1)：辅助栈与主栈同步生长，`min[-1]` 永远是“到当前位置为止”的最小值；弹栈时一起弹出，历史最小值自动回退到上一个状态。

## 2. 单调栈：遇到更强的人，旧候选退场

单调栈维护栈内值单调。新元素到来时，把不可能成为答案的旧元素弹出。

### 下一个更大元素

```python
stack = []           # 下标，值递减
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:
        j = stack.pop()
        answer[j] = x
    stack.append(i)
```

不变量：栈内元素还没有找到下一个更大值；它们的值从底到顶递减。

### 柱状图最大矩形

对每个高度，找左右第一个更低的位置：

```python
heights.append(0)
stack = [-1]
best = 0
for i, h in enumerate(heights):
    while stack[-1] != -1 and heights[stack[-1]] >= h:
        height = heights[stack.pop()]
        width = i - stack[-1] - 1
        best = max(best, height * width)
    stack.append(i)
```

关键：哨兵让所有剩余元素都有出栈机会。

## 3. 队列：顺序不可插队

队列适合：

- BFS；
- 任务调度；
- 缓冲区；
- 按时间顺序处理事件。

## 4. 单调队列：滑动窗口的最大值

双端队列维护下标，值从队首到队尾递减。

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    result = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

三个不变量：

1. 队列下标递增；
2. 对应值递减；
3. 队首在窗口内且是最大值。

## 5. 陷阱清单

- 栈存值还是存下标？需要宽度或距离时必须存下标。
- 弹出条件用 `<` 还是 `<=`，取决于相等元素是否互为答案。
- 循环结束后栈内元素可能还没有答案，要赋默认值。
- 双端队列只存下标时，不要忘记判断过期。
- 非空栈访问 `stack[-1]` 前，必须处理空栈。

> 单调结构的优雅在于：新证据到来时，立刻淘汰不可能的旧候选。

## 一图看懂

![单调栈维护未解决候选](./assets/diagrams/chapter-monotonic-stack.png)
