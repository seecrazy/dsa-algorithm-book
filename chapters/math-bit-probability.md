## 1. 位运算基础

```text
x & 1       判断奇偶
x >> 1      除以 2 向下取整（非负）
1 << k      2^k
x & (x - 1) 清除最低位 1
x & (-x)    取最低位 1
^           相同抵消，不同保留
```

## 2. 只出现一次的数字

### 一个唯一数

```python
ans = 0
for x in nums:
    ans ^= x
return ans
```

### 其他数出现三次

使用每一位计数：

```python
ans = 0
for bit in range(32):
    total = sum((x >> bit) & 1 for x in nums)
    if total % 3:
        ans |= 1 << bit
# Python 中负数需按题意转换为有符号数
```

## 3. 二进制状态压缩

用每一位表示“是否选择/已访问”：

```python
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            ...
```

n 一般不超过 20。状态转移可以从已选集合推未选项。

## 4. 数学常用方法

### 约束收缩

- 最大公约数：欧几里得；
- 最小公倍数：`a*b/gcd(a,b)`；
- 质数筛：埃氏筛；
- 快速幂：指数二分。

```python
def qpow(a, b, mod):
    result = 1
    a %= mod
    while b:
        if b & 1:
            result = result * a % mod
        a = a * a % mod
        b >>= 1
    return result
```

O(log b)。为什么对？b 的二进制位决定“这一位对应的 a 要不要乘进结果”，`a` 每轮自乘翻倍，把 O(b) 次乘法压成 O(log b) 次。

### 计数与抽屉

当结果空间巨大时，考虑：

- 只统计对答案有影响的维度；
- 排序后相邻关系；
- 前缀计数；
- 哈希分桶。

## 5. 随机化

### Fisher-Yates 洗牌

```python
for i in range(len(a) - 1, 0, -1):
    j = random.randint(0, i)
    a[i], a[j] = a[j], a[i]
```

### 蓄水池抽样

不知道流长度时，等概率保留 k 个：

```python
for i, x in enumerate(stream):
    if i < k:
        reservoir[i] = x
    else:
        j = random.randint(0, i)
        if j < k:
            reservoir[j] = x
```

第 i 个元素进入样本的概率是 k/i。

## 6. 隐藏不变量

数学题常需要找守恒量：

- 总和不变；
- 奇偶性不变；
- 最大最小差值只由全局边界决定；
- 每次操作等价于移动一个指针；
- 相同余数可以归为同一类。

## 7. 陷阱清单

- Python 负数右移语义与 C/Java 不同。
- 乘法取模要分步 `((a * b) % mod) * c % mod`。
- `random.shuffle` 不是自己重写的原因；若手写，索引范围必须正确。
- 位掩码题忽略 0 号位。
- 概率题把“均匀选择下标”写成“均匀选择值”。

> 数学题的突破口常常是：什么东西从头到尾没有变？
