## 1. 树是递归定义的结构

一棵树要么为空，要么有一个根和若干互不相交的子树。因此树题通常有两个视角：

### 自顶向下

从根向子节点传递状态：

```python
def dfs(node, acc):
    if not node:
        return
    new_acc = update(acc, node.val)
    update_global(new_acc)
    dfs(node.left, new_acc)
    dfs(node.right, new_acc)
```

### 自底向上

从子树返回信息给父节点：

```python
def dfs(node):
    if not node:
        return base
    left = dfs(node.left)
    right = dfs(node.right)
    return combine(node.val, left, right)
```

## 2. 遍历顺序的用途

| 遍历 | 用途 |
|---|---|
| 前序 | 复制树、序列化根、进入节点时决策 |
| 中序 | BST 输出有序序列、找中序后继 |
| 后序 | 自底向上统计、删除或释放子树 |
| 层序 | 按深度处理、最短层数、右视图 |

层序是唯一不靠递归的主流遍历，用队列 + 按层计数：

```python
from collections import deque
def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        out.append([node.val for node in q])   # 本层全部值
        for _ in range(len(q)):
            node = q.popleft()
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
    return out
```

O(n)。不变量：每轮 while 开始时，队列里恰好是同一层的全部节点，`len(q)` 就是本层宽度——“按层处理”和“右视图取每层末元素”都建立在这个不变量上。

## 3. BST 的核心性质

对任意节点：

```text
左子树所有值 < node.val < 右子树所有值
```

注意不是“只和左右孩子比较”。验证 BST 应传递上下界：

```python
def valid(node, lo, hi):
    if not node:
        return True
    if not (lo < node.val < hi):
        return False
    return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)
```

## 4. 常见模型

### 路径和

路径可能不需要经过根。后序返回“从当前节点向下延伸的最大路径和”，全局答案再合并左右。

### 序列化

先序 + 空节点标记可以唯一重建二叉树：

```python
def serialize(node):
    if not node:
        return "#"
    return f"{node.val},{serialize(node.left)},{serialize(node.right)}"
```

### LCA

对于普通二叉树：

```python
def lca(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root
    return left or right
```

BST 版本利用大小关系不用全搜索，两边同侧才下探，走到分叉点即答案，O(h)：

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val > q.val:
            root = root.left            # 都在左边
        elif p.val > root.val < q.val:
            root = root.right           # 都在右边
        else:
            return root                 # 分叉点或命中之一
```

每次至少排除一棵子树，复杂度 O(h)。

## 5. 陷阱清单

- 空树返回值要明确定义，深度是 0，路径和可能是 None。
- 重复值会让“按值找节点”失效，应按节点对象或下标。
- 只比较父子节点无法验证 BST。
- 构造树时中序分割点找错。
- 递归深度过大时，要转成显式栈或层序。

> 树题的关键不是背遍历，而是定义“子树返回什么信息”。

## 一图看懂

![树的后序遍历先取子问题答案再合并](./assets/diagrams/chapter-tree-recursion.png)
