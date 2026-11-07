## 1. 回溯的基本循环

回溯系统地枚举所有可能，并在不合法时剪掉整棵子树。

```python
def backtrack(path, choices):
    if is_complete(path):
        record(path.copy())
        return
    for choice in choices:
        if valid(path, choice):
            make(path, choice)
            backtrack(path, next_choices)
            undo(path, choice)
```

三个动作必须完整：选择、探索、撤销。

## 2. 去重是最大难点

### 排列去重

先排序，同层跳过重复起点：

```python
nums.sort()
used = [False] * len(nums)

def dfs(path):
    if len(path) == len(nums):
        result.append(path.copy())
        return
    for i in range(len(nums)):
        if used[i]:
            continue
        if i and nums[i] == nums[i - 1] and not used[i - 1]:
            continue
        used[i] = True
        path.append(nums[i])
        dfs(path)
        path.pop()
        used[i] = False
```

不变量：同一层中，若上一个相等元素没有被使用，当前元素作为起点会产生重复排列。

### 组合起点

```python
def dfs(start, path):
    for i in range(start, len(nums)):
        path.append(nums[i])
        dfs(i + 1, path)
        path.pop()
```

## 3. 剪枝的三类条件

1. **合法性剪枝**：列冲突、越界、超预算；
2. **可行性剪枝**：剩余资源不足以完成；
3. **最优性剪枝**：当前代价已不劣于已知最优。

N Queens 判断：

```text
同列冲突：col[c]
主对角线：row - col
副对角线：row + col
```

## 4. 网格搜索

Word Search 模板：

```python
def search(r, c, idx):
    if idx == len(word):
        return True
    if not in_board(r, c) or board[r][c] != word[idx]:
        return False
    board[r][c] = '#'
    ok = any(search(r + dr, c + dc, idx + 1) for dr, dc in dirs)
    board[r][c] = word[idx]
    return ok
```

临时标记就是撤销机制。

## 5. 复杂度心态

回溯复杂度通常是候选树的上界：

- 排列：O(n × n!)；
- 子集：O(n × 2^n)；
- 组合：取决于剪枝。

面试中应说明剪枝如何实际降低树规模，而不是只报最坏复杂度。

## 6. 陷阱清单

- 忘记 `path.copy()`，记录的是同一列表引用。
- 撤销顺序与选择不对称。
- 有重复输入但没有排序。
- 组合题允许重复使用元素时，递归起点应仍是 `i` 而不是 `i + 1`。
- 网格恢复字符时写成了恢复标记。

> 回溯的本质是“诚实地枚举”，剪枝只是省去注定失败的分支。

## 一图看懂

![回溯的选择、探索与撤销](./assets/diagrams/chapter-backtracking-tree.png)
