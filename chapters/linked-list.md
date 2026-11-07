## 1. 链表的真实难点

链表访问是 O(n)，但难点不是访问，而是**引用一致性**。每一步都可能改变三个东西：

- 前驱的 next；
- 当前节点的 next；
- 未来需要访问的节点。

所以常见缓解手段是：

- dummy head，消除头部特判；
- 先保存 `nxt`；
- 画图标注指针；
- 明确返回哪个节点。

## 2. 核心模板

### 反转链表

```python
prev = None
cur = head
while cur:
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
return prev
```

不变量：`prev` 是已完成反转部分的头，`cur` 是未处理部分的头。

### 快慢指针找中点

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
```

偶数长度时 `slow` 在右半部分开头；需要左中点时，应在分裂前明确处理。

### 合并两个有序链表

```python
dummy = tail = ListNode()
while l1 and l2:
    if l1.val <= l2.val:
        tail.next, l1 = l1, l1.next
    else:
        tail.next, l2 = l2, l2.next
    tail = tail.next
tail.next = l1 or l2
return dummy.next
```

### 环检测

```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        return True
return False
```

## 3. LRU 缓存的两个核心

LRU 需要同时完成：

1. O(1) 查键值；
2. O(1) 移动到最近使用位置并淘汰最久未用。

方案：哈希表保存 key 到节点；双向链表维护使用顺序。

```python
node = self.map[key]
self._remove(node)
self._add_front(node)
```

淘汰时：

```python
tail = self.dummy_tail.prev
self._remove(tail)
del self.map[tail.key]
```

## 4. 陷阱清单

- 头节点可能被删除，必须使用 dummy。
- 反转前没有保存 `next`，链会断。
- 判断环用 `is` 还是 `==` 要清楚；结构相等和同一对象不同。
- 双向链表删除时要同时修改 `prev` 和 `next`。
- 合并链表末尾忘记接剩余部分。
- 只返回节点不返回长度时，不要假设调用方知道长度。

> dummy 不是偷懒，是把“没有前驱”和“有前驱”统一成一种处理。

## 一图看懂

![快慢指针在环内追上](./assets/diagrams/chapter-linked-list-cycle.png)
