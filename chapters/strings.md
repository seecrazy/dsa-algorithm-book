## 1. 字符串的三种视角

1. **数组视角**：可下标、可扫描；
2. **计数视角**：只关心频次或等价签名；
3. **结构视角**：前缀、后缀、回文、匹配状态。

## 2. 回文

### 中心扩展

奇偶中心分开处理：

```python
def expand(s, l, r):
    while l >= 0 and r < len(s) and s[l] == s[r]:
        l -= 1
        r += 1
    return l + 1, r

def longest_palindrome(s):
    best = (0, 0)
    for i in range(len(s)):
        for l, r in (expand(s, i, i), expand(s, i, i + 1)):
            if r - l > best[1] - best[0]:
                best = (l, r)
    return s[best[0]:best[1]]
```

### DP

`dp[i][j]` 表示 `s[i:j+1]` 是否回文：

```python
if s[i] == s[j] and (j - i < 2 or dp[i + 1][j - 1]):
    dp[i][j] = True
```

## 3. 前缀和与差分

字符频次可用固定长度数组：

```python
cnt = [0] * 26
for ch in s:
    cnt[ord(ch) - ord('a')] += 1
```

异位词比较时可维护窗口频次，而不是每次重建 Counter。

## 4. 字符串匹配

### 朴素匹配

每个起点比较，O(nm)。小数据够用。

### KMP

`next[i]` 表示模式串 `p[:i+1]` 的最长相等真前后缀长度。

```python
def build_next(p):
    nxt = [0] * len(p)
    k = 0
    for i in range(1, len(p)):
        while k and p[i] != p[k]:
            k = nxt[k - 1]
        if p[i] == p[k]:
            k += 1
        nxt[i] = k
    return nxt
```

匹配失败时，模式串不用回到起点，而是跳到下一个可能的前缀状态。

## 5. 字典序贪心

移除 K 个字符使剩余字典序最小：

```python
stack = []
removals = k
for ch in s:
    while stack and removals and stack[-1] > ch:
        stack.pop()
        removals -= 1
    stack.append(ch)
while removals:
    stack.pop()
    removals -= 1
return ''.join(stack)
```

不变量：栈内前缀在允许删除数内尽量保持上升。

## 6. 规范化键

- 大小写：统一 lower；
- Unicode：必要时 normalization；
- 空格与标点：题面决定是否忽略；
- 分数：约分后 `(a//g, b//g)`。

## 7. 陷阱清单

- 只处理 ASCII，输入却含中文或 emoji。
- 空串、单字符、全相同字符。
- 回文子串和回文子序列不是一回事。
- 大数进制转换溢出。
- 字典序最小不等于字符数最少。

> 字符串题经常在考“你能否找到隐藏的重复结构”。
