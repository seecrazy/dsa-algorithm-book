## 1. Trie 的动机

哈希表能回答“这个词在吗”，但不能高效回答：

- 有哪些词以前缀 `ap` 开头？
- 是否存在一个词以 `app` 为前缀？
- 把所有共享前缀的词压缩存储。

Trie 把字符串的每个字符看作一条边，从根到某个节点构成前缀。

## 2. 节点模型

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word):
        node = self.find(word)
        return bool(node and node.is_end)

    def starts_with(self, prefix):
        return self.find(prefix) is not None

    def find(self, s):
        node = self.root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
```

插入、查找、前缀判断都是 `O(L)`，L 是字符串长度。

## 3. 前缀统计

如果不仅要判断存在，还要统计前缀次数，节点里保存 `pass_count` 和 `end_count`：

```text
insert(word): 沿途 pass_count++；末尾 end_count++
delete(word): 沿途 pass_count--；末尾 end_count--；必要时回收节点
count_prefix(p): find(p).pass_count
count_word(w): find(w).end_count
```

## 4. Trie + DFS

二维网格搜多个单词时，不要对每个单词都做一次 DFS。先把单词表建 Trie；DFS 每走到一个字符，就在 Trie 上同步走一步。剪枝更早，重复共享前缀只探索一次。

## 5. 变体

| 结构 | 作用 |
|---|---|
| 压缩 Trie | 单链路径压成一条边，减少节点 |
| Radix Tree | 压缩 Trie 的工程形式 |
| Aho-Corasick | 多模式串自动机 |
| 三叉搜索树 | 节省稀疏子节点空间 |

## 6. 陷阱

- 子节点数量可能很大，稀疏字符集用哈希表而不是 256 长度数组。
- 删除节点时不能破坏仍被其他单词共享的前缀。
- Unicode 字符可能由多个码点组成，先明确规范化规则。
- 大量短字符串时，哈希表可能更快；Trie 的优势在前缀和共享结构。

> Trie 的价值不在“查单词”，而在“查所有共享前缀的东西”。

## 一图看懂

![Trie 共享前缀与查询路径](./assets/diagrams/chapter-trie-prefix.png)
