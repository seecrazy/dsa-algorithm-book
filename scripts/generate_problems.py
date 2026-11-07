#!/usr/bin/env python3
"""Generate the ordered problem bank used by the static reader."""
from __future__ import annotations

import json
from pathlib import Path

from java_solutions import JAVA_SOLUTIONS
from teaching_notes import TEACHING_NOTES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "problems.json"
CHAPTER_IDS = {
    "how-to-use", "complexity", "array-two-pointers", "stack-queue-monotonic",
    "hash-and-counting", "linked-list", "recursion-divide-binary-search",
    "trees", "heaps", "graph-search", "graph-shortest-mst", "backtracking",
    "greedy", "dynamic-programming", "strings", "union-find-advanced",
    "math-bit-probability", "engineering-interview",
}

P = []

def add(pid, title, difficulty, chapter, tags, summary, prompt, constraints,
        examples, idea, complexity, pitfalls, code):
    P.append({
        "id": pid, "title": title, "difficulty": difficulty,
        "tags": tags, "chapter": chapter, "summary": summary,
        "prompt": prompt, "constraints": constraints,
        "examples": examples,
        "solution": {
            "idea": idea, "complexity": complexity,
            "pitfalls": pitfalls, "code": [{"language": "Python", "source": code}],
        },
    })

# Arrays and two pointers: 10
add("p001", "两数之和", "easy", "array-two-pointers", ["数组", "哈希表"],
    "找出和为目标值的两个下标。",
    "给定整数数组 nums 和目标值 target，返回和为 target 的两个元素下标。保证恰好一组答案。",
    ["2 <= len(nums) <= 10^4", "-10^9 <= nums[i] <= 10^9"],
    [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "2 + 7 = 9"}],
    "遍历时用哈希表记录值到下标；对每个 x 查 target-x 是否已出现。",
    "时间 O(n)，空间 O(n)。",
    ["有重复元素时不能预建值到唯一下标映射。", "不要先找到自身。", "返回下标而不是值。"],
    "def two_sum(nums, target):\n    seen = {}\n    for i, x in enumerate(nums):\n        if target - x in seen:\n            return [seen[target - x], i]\n        seen[x] = i\n    return []")

add("p002", "最大子数组和", "medium", "array-two-pointers", ["数组", "动态规划"],
    "求连续子数组的最大和。",
    "给定整数数组，返回连续子数组的最大和，至少包含一个元素。",
    ["1 <= len(nums) <= 10^5", "-10^4 <= nums[i] <= 10^4"],
    [{"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "[4,-1,2,1]"}],
    "维护以当前元素结尾的最大和；负前缀直接丢弃。",
    "时间 O(n)，空间 O(1)。",
    ["全负数组不能初始化答案为 0。", "不能在中间断开后允许空子数组。", "要返回和而非长度。"],
    "def max_sub_array(nums):\n    ans = cur = nums[0]\n    for x in nums[1:]:\n        cur = max(x, cur + x)\n        ans = max(ans, cur)\n    return ans")

add("p003", "盛最多水的容器", "medium", "array-two-pointers", ["数组", "双指针"],
    "两条竖线与 x 轴组成容器，求最大水量。",
    "height[i] 表示第 i 条竖线高度，选两条线使容纳水量最大。",
    ["2 <= len(height) <= 10^5", "0 <= height[i] <= 10^4"],
    [{"input": "[1,8,6,2,5,4,8,3,7]", "output": "49"}],
    "左右指针向内收缩；每次移动较短一边，因为不动较长边不可能更优。",
    "时间 O(n)，空间 O(1)。",
    ["面积由较短边决定。", "移动错误边会漏最优。", "宽度是下标差。"],
    "def max_area(height):\n    left, right, ans = 0, len(height) - 1, 0\n    while left < right:\n        ans = max(ans, (right-left) * min(height[left], height[right]))\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return ans")

add("p004", "接雨水", "hard", "array-two-pointers", ["数组", "双指针", "前缀最大值"],
    "柱状图能接多少雨水。",
    "给定非负柱高，计算下雨后可接水量。",
    ["1 <= len(height) <= 2*10^4", "0 <= height[i] <= 10^5"],
    [{"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"}],
    "每个位置的储水量由左右最大高度较小值决定；双指针维护两侧最大值，短边可定答。",
    "时间 O(n)，空间 O(1)。",
    ["位置本身高度要扣掉。", "相等高度时移动哪边都可以，但不能两边都算。", "左右最大值初值错误。"],
    "def trap(height):\n    l, r = 0, len(height)-1\n    lm = rm = water = 0\n    while l < r:\n        if height[l] <= height[r]:\n            lm = max(lm, height[l]); water += lm-height[l]; l += 1\n        else:\n            rm = max(rm, height[r]); water += rm-height[r]; r -= 1\n    return water")

add("p005", "移动零", "easy", "array-two-pointers", ["数组", "原地操作"],
    "把所有 0 移到末尾并保持非零相对顺序。",
    "原地修改数组，返回不影响原数组内容的操作结果。",
    ["1 <= len(nums) <= 10^4", "-10^3 <= nums[i] <= 10^3"],
    [{"input": "[0,1,0,3,12]", "output": "[1,3,12,0,0]"}],
    "快指针扫描非零并写入 slow，最后把 slow 后清零。",
    "时间 O(n)，空间 O(1)。",
    ["必须保持非零顺序。", "先写后清零，不能一边跳过一边覆盖。", "不要创建额外数组。"],
    "def move_zeroes(nums):\n    slow = 0\n    for fast, x in enumerate(nums):\n        if x != 0:\n            nums[slow] = x; slow += 1\n    for i in range(slow, len(nums)):\n        nums[i] = 0")

add("p006", "合并两个有序数组", "easy", "array-two-pointers", ["数组", "归并"],
    "把有序数组 B 合并进 A 的预留空间。",
    "nums1 前 m 个有效有序，nums2 有 n 个；原地合并 nums1。",
    ["0 <= m,n <= 200", "nums1 长度为 m+n"],
    [{"input": "nums1=[1,2,3,0,0,0], m=3, nums2=[2,5,6], n=3", "output": "[1,2,2,3,5,6]"}],
    "从后向前填充，避免覆盖 nums1 有效数据。",
    "时间 O(m+n)，空间 O(1)。",
    ["从前往后会覆盖。", "m 或 n 可为 0。", "循环后剩余元素要复制。"],
    "def merge(nums1, m, nums2, n):\n    i, j, k = m-1, n-1, m+n-1\n    while i >= 0 and j >= 0:\n        if nums1[i] >= nums2[j]: nums1[k]=nums1[i]; i-=1\n        else: nums1[k]=nums2[j]; j-=1\n        k-=1\n    while j >= 0: nums1[k]=nums2[j]; j-=1; k-=1")

add("p007", "有序数组去重", "easy", "array-two-pointers", ["数组", "快慢指针"],
    "删除有序数组重复项，返回新长度。",
    "原地删除重复项，使每个元素只出现一次。",
    ["1 <= len(nums) <= 3*10^4"],
    [{"input": "[0,0,1,1,1,2]", "output": "4", "explanation": "前 4 位是 [0,1,2,_]"}],
    "slow 指向已保留最后位置；fast 与 slow 相同则跳过。",
    "时间 O(n)，空间 O(1)。",
    ["数组无序时不能这样。", "从 slow+1 开始写入。", "返回长度而不是切片。"],
    "def remove_duplicates(nums):\n    slow = 0\n    for fast in range(1, len(nums)):\n        if nums[fast] != nums[slow]:\n            slow += 1; nums[slow] = nums[fast]\n    return slow + 1")

add("p008", "三数之和", "medium", "array-two-pointers", ["数组", "排序", "双指针"],
    "找出所有不重复的三元组，使其和为 0。",
    "返回所有唯一三元组，不能重复记录同一组。",
    ["3 <= len(nums) <= 3000", "-10^5 <= nums[i] <= 10^5"],
    [{"input": "[-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"}],
    "排序后固定 i，对右侧区间用对撞双指针；跳过重复 i 与重复左右值。",
    "时间 O(n^2)，空间 O(log n) 排序辅助。",
    ["不排序无法去重。", "找到答案后 left/right 都要继续去重。", "固定数重复要跳过。"],
    "def three_sum(nums):\n    nums.sort(); ans=[]\n    for i in range(len(nums)-2):\n        if i and nums[i]==nums[i-1]: continue\n        l,r=i+1,len(nums)-1\n        while l<r:\n            s=nums[i]+nums[l]+nums[r]\n            if s<0: l+=1\n            elif s>0: r-=1\n            else:\n                ans.append([nums[i],nums[l],nums[r]])\n                l+=1; r-=1\n                while l<r and nums[l]==nums[l-1]: l+=1\n                while l<r and nums[r]==nums[r+1]: r-=1\n    return ans")

add("p009", "乘积除以自身", "medium", "array-two-pointers", ["数组", "前缀乘积"],
    "返回除自身外所有元素乘积。",
    "不使用除法，在 O(n) 内返回 answer[i] = product(nums except i)。",
    ["2 <= len(nums) <= 10^5", "乘积保证在 32 位内"],
    [{"input": "[1,2,3,4]", "output": "[24,12,8,6]"}],
    "先存左侧乘积，再从右向左乘右侧乘积。",
    "时间 O(n)，空间 O(1) 输出外。",
    ["不能使用除法。", "存在 0 时除法方案失效。", "要从右到左累计右侧乘积。"],
    "def product_except_self(nums):\n    n=len(nums); ans=[1]*n\n    for i in range(1,n): ans[i]=ans[i-1]*nums[i-1]\n    right=1\n    for i in range(n-1,-1,-1): ans[i]*=right; right*=nums[i]\n    return ans")

add("p010", "无重复字符最长子串", "medium", "array-two-pointers", ["滑动窗口", "哈希表"],
    "求不含重复字符的最长连续子串长度。",
    "给定字符串 s，返回最长无重复字符子串长度。",
    ["0 <= len(s) <= 5*10^4", "字符包含 ASCII"],
    [{"input": "abcabcbb", "output": "3"}],
    "滑动窗口；记录字符最后位置，left 跳到冲突位置后一位。",
    "时间 O(n)，空间 O(min(n, alphabet))。",
    ["left 只能前进。", "重复字符在窗口外时不能回跳。", "空串返回 0。"],
    "def length_of_longest_substring(s):\n    last={}; left=ans=0\n    for right,ch in enumerate(s):\n        if ch in last and last[ch]>=left: left=last[ch]+1\n        last[ch]=right; ans=max(ans,right-left+1)\n    return ans")

# Stack / queue / monotonic: 8
add("p011", "有效括号", "easy", "stack-queue-monotonic", ["栈", "字符串"],
    "判断括号串是否完整闭合。",
    "只包含 ()[]{}，判断是否有效。",
    ["1 <= len(s) <= 10^4"],
    [{"input": "({[]})", "output": "true"}],
    "左括号入栈，右括号必须匹配栈顶；最后栈为空才有效。",
    "时间 O(n)，空间 O(n)。",
    ["右括号时栈可能为空。", "字符串结束后栈必须空。", "括号类型要精确匹配。"],
    "def is_valid(s):\n    pairs={')':'(',']':'[','}':'{'}; st=[]\n    for ch in s:\n        if ch in '([{': st.append(ch)\n        elif not st or st.pop()!=pairs[ch]: return False\n    return not st")

add("p012", "最小栈", "medium", "stack-queue-monotonic", ["栈", "设计"],
    "支持 O(1) push/pop/top/getMin。",
    "设计一个栈，能在常数时间返回当前最小值。",
    ["调用次数 <= 3*10^4", "-2^31 <= val <= 2^31-1"],
    [{"input": "push(-2),push(0),push(-3),getMin(),pop(),top(),getMin()", "output": "-3,0,-2"}],
    "辅助栈同步保存每一层当前最小值，弹出时一起弹出。",
    "每种操作 O(1)，空间 O(n)。",
    ["pop 空栈行为要定义。", "辅助栈不能只在更小值入栈时不同步。", "相等最小值要重复保存。"],
    "class MinStack:\n    def __init__(self): self.st=[]; self.mn=[]\n    def push(self,x):\n        self.st.append(x); self.mn.append(min(x,self.mn[-1] if self.mn else x))\n    def pop(self): self.st.pop(); self.mn.pop()\n    def top(self): return self.st[-1]\n    def getMin(self): return self.mn[-1]")

add("p013", "下一个更大元素", "medium", "stack-queue-monotonic", ["单调栈", "数组"],
    "返回每个元素右侧第一个更大值。",
    "不存在则输出 -1。",
    ["1 <= len(nums) <= 10^4", "0 <= nums[i] <= 10^9"],
    [{"input": "[1,2,1]", "output": "[2,-1,-1]"}],
    "单调递减栈存下标；更大值到达时弹出并赋答案。",
    "时间 O(n)，空间 O(n)。",
    ["要存下标以便填答案。", "栈中剩余填 -1。", "相等元素是否互为更大值要确认。"],
    "def next_greater(nums):\n    ans=[-1]*len(nums); st=[]\n    for i,x in enumerate(nums):\n        while st and nums[st[-1]]<x: ans[st.pop()]=x\n        st.append(i)\n    return ans")

add("p014", "每日温度", "medium", "stack-queue-monotonic", ["单调栈", "区间"],
    "等待几天后温度升高。",
    "返回每天需要等待的天数，没有则为 0。",
    ["1 <= len(T) <= 10^5", "30 <= T[i] <= 100"],
    [{"input": "[73,74,75,71,69,72,76,73]", "output": "[1,1,4,2,1,1,0,0]"}],
    "单调递减下标栈；更高温度弹出旧下标，距离为 i-j。",
    "时间 O(n)，空间 O(n)。",
    ["栈存下标不是温度。", "距离是 i 减弹出下标。", "栈空剩余保持 0。"],
    "def daily_temperatures(T):\n    ans=[0]*len(T); st=[]\n    for i,x in enumerate(T):\n        while st and T[st[-1]]<x: j=st.pop(); ans[j]=i-j\n        st.append(i)\n    return ans")

add("p015", "柱状图最大矩形", "hard", "stack-queue-monotonic", ["单调栈", "区间宽度"],
    "求柱状图中最大矩形面积。",
    "给定非负高度数组，可选连续柱组成矩形。",
    ["1 <= len(heights) <= 10^5", "0 <= heights[i] <= 10^4"],
    [{"input": "[2,1,5,6,2,3]", "output": "10"}],
    "对每个高度找左右第一个更低边界；哨兵让所有高度出栈。",
    "时间 O(n)，空间 O(n)。",
    ["宽度计算依赖栈内前一个下标。", "相等问题要统一边界定义。", "末尾必须清栈或加哨兵。"],
    "def largest_rect(heights):\n    hs=heights+[0]; st=[-1]; ans=0\n    for i,h in enumerate(hs):\n        while st[-1]!=-1 and hs[st[-1]]>=h:\n            height=hs[st.pop()]\n            ans=max(ans,height*(i-st[-1]-1))\n        st.append(i)\n    return ans")

add("p016", "解码字符串", "medium", "stack-queue-monotonic", ["栈", "解析"],
    "解码 k[encoded_string] 形式。",
    "重复次数总为正整数，括号可嵌套。",
    ["1 <= len(s) <= 30", "输入保证合法"],
    [{"input": "3[a2[c]]", "output": "accaccacc"}],
    "数字栈和字符串栈保存括号外状态；遇右括号拼接并重复。",
    "时间 O(n+输出长度)，空间同。",
    ["多位数字要累计。", "嵌套时当前串要清空。", "不要用 eval。"],
    "def decode_string(s):\n    cnt=[]; st=[]; cur=''; n=0\n    for ch in s:\n        if ch.isdigit(): n=n*10+int(ch)\n        elif ch=='[': cnt.append(n); st.append(cur); n=0; cur=''\n        elif ch==']': cur=st.pop()*cnt.pop()+cur\n        else: cur+=ch\n    return cur")

add("p017", "滑动窗口最大值", "hard", "stack-queue-monotonic", ["单调队列", "双端队列"],
    "返回每个长度 k 窗口最大值。",
    "给定数组和窗口长度。",
    ["1 <= len(nums) <= 10^5", "1 <= k <= len(nums)"],
    [{"input": "nums=[1,3,-1,-3,5,3,6,7], k=3", "output": "[3,3,5,5,6,7]"}],
    "双端队列保存下标且值递减；队首过期弹出，队尾小于新值弹出。",
    "时间 O(n)，空间 O(k)。",
    ["只存值无法判断过期。", "队首过期条件是 dq[0] <= i-k。", "进入结果前窗口必须完整。"],
    "from collections import deque\ndef max_window(nums,k):\n    dq=deque(); ans=[]\n    for i,x in enumerate(nums):\n        while dq and nums[dq[-1]]<=x: dq.pop()\n        dq.append(i)\n        if dq[0]<=i-k: dq.popleft()\n        if i>=k-1: ans.append(nums[dq[0]])\n    return ans")

add("p018", "逆波兰表达式求值", "medium", "stack-queue-monotonic", ["栈", "表达式"],
    "计算后缀表达式。",
    "运算符只有 + - * /，除法向零截断。",
    ["1 <= len(tokens) <= 10^4", "中间结果在 32 位内"],
    [{"input": "['2','1','+','3','*']", "output": "9"}],
    "数字入栈；运算符弹出两个操作数，注意顺序。",
    "时间 O(n)，空间 O(n)。",
    ["除法不能直接 Python // 处理负数向零截断。", "第二弹出数是右操作数。", "非法表达式要报错。"],
    "def eval_rpn(tokens):\n    st=[]\n    for x in tokens:\n        if x in '+-*/':\n            b=st.pop(); a=st.pop()\n            if x=='+': st.append(a+b)\n            elif x=='-': st.append(a-b)\n            elif x=='*': st.append(a*b)\n            else: st.append(int(a/b))\n        else: st.append(int(x))\n    return st[0]")

# Hash / counting: 8
add("p019", "字母异位词分组", "medium", "hash-and-counting", ["哈希表", "字符串"],
    "将异位词分组。",
    "输入字符串数组，输出互为异位词的组合。",
    ["1 <= len(strs) <= 10^4", "字符串只含小写字母"],
    [{"input": "['eat','tea','tan','ate','nat','bat']", "output": "[['eat','tea','ate'],['tan','nat'],['bat']]"}],
    "排序字符串或字符计数元组作为分组键。",
    "时间 O(n k log k) 或 O(nk)，空间 O(nk)。",
    ["list 不能作 dict key。", "排序键会多 log k。", "空字符串也要分组。"],
    "from collections import defaultdict\ndef group_anagrams(strs):\n    g=defaultdict(list)\n    for s in strs: g[tuple(sorted(s))].append(s)\n    return list(g.values())")

add("p020", "前 K 个高频元素", "medium", "hash-and-counting", ["哈希表", "堆"],
    "返回出现频率最高的 k 个元素。",
    "答案顺序任意，保证答案唯一。",
    ["1 <= len(nums) <= 10^5", "1 <= k <= 不同元素数"],
    [{"input": "nums=[1,1,1,2,2,3], k=2", "output": "[1,2]"}],
    "哈希统计频次，再用大小为 k 的小根堆保留高频元素。",
    "时间 O(n log k)，空间 O(n)。",
    ["不要只按元素值排序。", "频次相等时结果必须确定。", "k 可能等于不同元素数。"],
    "from collections import Counter\nimport heapq\ndef top_k_freq(nums,k):\n    freq=Counter(nums)\n    return [x for x,_ in heapq.nlargest(k,freq.items(),key=lambda p:p[1])]\n# 或用大小为 k 的堆进行流式维护")

add("p021", "最长连续序列", "medium", "hash-and-counting", ["哈希表", "区间"],
    "求数字可组成的最长连续序列长度。",
    "不要求数组顺序，希望 O(n)。",
    ["0 <= len(nums) <= 10^5", "-10^9 <= nums[i] <= 10^9"],
    [{"input": "[100,4,200,1,3,2]", "output": "4"}],
    "放进 set；只从每个序列起点开始向右扩张。",
    "时间 O(n)，空间 O(n)。",
    ["必须判断 x-1 不在 set 才是起点。", "重复元素不影响长度。", "空数组返回 0。"],
    "def longest_consecutive(nums):\n    s=set(nums); ans=0\n    for x in s:\n        if x-1 not in s:\n            y=x\n            while y+1 in s: y+=1\n            ans=max(ans,y-x+1)\n    return ans")

add("p022", "和为 K 的子数组", "medium", "hash-and-counting", ["前缀和", "哈希表"],
    "统计和为 k 的连续子数组数量。",
    "数组可含负数。",
    ["1 <= len(nums) <= 2*10^4", "-10^3 <= nums[i],k <= 10^3"],
    [{"input": "nums=[1,1,1], k=2", "output": "2"}],
    "前缀和哈希记录出现次数，当前前缀减 k 的次数即答案增量。",
    "时间 O(n)，空间 O(n)。",
    ["不能滑动窗口，因为有负数。", "seen[0] 初始化为 1。", "先取答案再插入当前前缀。"],
    "from collections import defaultdict\ndef subarray_sum(nums,k):\n    seen=defaultdict(int); seen[0]=1; p=ans=0\n    for x in nums:\n        p+=x; ans+=seen[p-k]; seen[p]+=1\n    return ans")

add("p023", "第一个只出现一次的字符", "easy", "hash-and-counting", ["计数", "字符串"],
    "返回第一个唯一字符下标。",
    "不存在返回 -1。",
    ["1 <= len(s) <= 10^5"],
    [{"input": "leetcode", "output": "0"}],
    "统计频次后按原序找第一个次数为 1 的字符。",
    "时间 O(n)，空间 O(alphabet)。",
    ["第二次扫描必须按原序。", "大小写按题意处理。", "空串被约束排除。"],
    "from collections import Counter\ndef first_unique_char(s):\n    freq=Counter(s)\n    for i,ch in enumerate(s):\n        if freq[ch]==1: return i\n    return -1")

add("p024", "存在重复元素 II", "easy", "hash-and-counting", ["哈希表", "滑动窗口"],
    "判断同值下标距离是否不超过 k。",
    "存在 nums[i]==nums[j] 且 abs(i-j)<=k 返回 true。",
    ["1 <= len(nums) <= 10^5", "0 <= k <= 10^5"],
    [{"input": "nums=[1,2,3,1], k=3", "output": "true"}],
    "哈希记录值最近下标；遇到同值检查距离。",
    "时间 O(n)，空间 O(n)。",
    ["保存最近下标即可。", "距离是绝对值。", "不等于 k 时应拒绝。"],
    "def contains_nearby(nums,k):\n    last={}\n    for i,x in enumerate(nums):\n        if x in last and i-last[x]<=k: return True\n        last[x]=i\n    return False")

add("p025", "四数相加 II", "medium", "hash-and-counting", ["哈希表", "分组"],
    "统计四数组各取一数和为 0 的组合数。",
    "四个数组长度相同，可重复选择下标组合。",
    ["1 <= n <= 200", "-2^28 <= value <= 2^28"],
    [{"input": "A=[1,2],B=[-2,-1],C=[-1,2],D=[0,2]", "output": "2"}],
    "哈希记录 A+B 的和频次，枚举 C+D 取相反和。",
    "时间 O(n^2)，空间 O(n^2)。",
    ["不是同一数组去重问题。", "统计次数不能只用 set。", "答案可很大。"],
    "from collections import Counter\ndef four_sum_count(A,B,C,D):\n    ab=Counter(a+b for a in A for b in B)\n    return sum(ab[-(c+d)] for c in C for d in D)")

add("p026", "随机按权重选择", "medium", "hash-and-counting", ["前缀和", "随机化"],
    "按权重随机返回下标。",
    "pick 调用次数可能很大。",
    ["1 <= len(w) <= 10^4", "1 <= w[i] <= 10^5"],
    [{"input": "w=[1,3]", "output": "0 概率 0.25，1 概率 0.75"}],
    "构建前缀和，随机取 [1,total]，二分找第一个 >= r 的前缀。",
    "预处理 O(n)，每次 O(log n)。",
    ["随机数范围要含 total。", "二分返回插入点。", "每次调用都要基于同一前缀。"],
    "import random,bisect\nclass WeightPicker:\n    def __init__(self,w):\n        self.p=[]; s=0\n        for x in w: s+=x; self.p.append(s)\n    def pick(self): return bisect.bisect_left(self.p,random.randint(1,self.p[-1]))")

# Linked list: 10
add("p027", "反转链表", "easy", "linked-list", ["链表", "指针"],
    "反转单向链表。",
    "返回新头节点。",
    ["节点数 0..5000"],
    [{"input": "1->2->3->NULL", "output": "3->2->1->NULL"}],
    "三指针 prev/cur/nxt 迭代反转。",
    "时间 O(n)，空间 O(1)。",
    ["先保存 next。", "空链返回 None。", "最终返回 prev。"],
    "def reverse_list(head):\n    prev=None; cur=head\n    while cur: nxt=cur.next; cur.next=prev; prev=cur; cur=nxt\n    return prev")

add("p028", "链表中点", "easy", "linked-list", ["链表", "快慢指针"],
    "返回链表中间节点。",
    "偶数长度返回第二个中点。",
    ["1 <= 节点数 <= 100"],
    [{"input": "1->2->3->4->5", "output": "3"}],
    "快慢指针；fast 每次两步，slow 一步。",
    "时间 O(n)，空间 O(1)。",
    ["循环条件是 fast and fast.next。", "偶数语义要确认。", "不能假设长度已知。"],
    "def middle_node(head):\n    slow=fast=head\n    while fast and fast.next: slow=slow.next; fast=fast.next.next\n    return slow")

add("p029", "环形链表", "easy", "linked-list", ["链表", "双指针"],
    "判断链表是否有环。",
    "不允许 O(n) 额外空间。",
    ["节点数 0..10^4"],
    [{"input": "3->2->0->-4 指向节点 1", "output": "true"}],
    "快慢指针相遇则有环。",
    "时间 O(n)，空间 O(1)。",
    ["先检查 fast 和 fast.next。", "比较同一对象用 is。", "空链无环。"],
    "def has_cycle(head):\n    slow=fast=head\n    while fast and fast.next:\n        slow=slow.next; fast=fast.next.next\n        if slow is fast: return True\n    return False")

add("p030", "合并两个有序链表", "easy", "linked-list", ["链表", "归并"],
    "合并为一条有序链表。",
    "返回 dummy.next。",
    ["节点数 0..50"],
    [{"input": "1->2->4, 1->3->4", "output": "1->1->2->3->4->4"}],
    "dummy 尾插较小节点，最后接剩余。",
    "时间 O(m+n)，空间 O(1)。",
    ["末尾必须接剩余。", "用 dummy 避免头特判。", "稳定性用 <=。"],
    "def merge_lists(l1,l2):\n    dummy=tail=ListNode()\n    while l1 and l2:\n        if l1.val<=l2.val: tail.next,l1=l1,l1.next\n        else: tail.next,l2=l2,l2.next\n        tail=tail.next\n    tail.next=l1 or l2\n    return dummy.next")

add("p031", "排序链表", "medium", "linked-list", ["链表", "归并排序"],
    "O(n log n) 排序链表。",
    "要求常数空间优先。",
    ["节点数 0..5*10^4"],
    [{"input": "4->2->1->3", "output": "1->2->3->4"}],
    "快慢切半，递归归并；也可自底向上避免递归栈。",
    "时间 O(n log n)，空间递归 O(log n)。",
    ["中点切分要断开。", "空链返回 None。", "相等节点保持稳定。"],
    "def sort_list(head):\n    if not head or not head.next: return head\n    slow,fast=head,head.next\n    while fast and fast.next: slow=slow.next; fast=fast.next.next\n    mid=slow.next; slow.next=None\n    return merge_lists(sort_list(head),sort_list(mid))")

add("p032", "删除倒数第 N 个节点", "medium", "linked-list", ["链表", "双指针"],
    "一趟删除倒数第 n 个节点。",
    "n 合法且不超过长度。",
    ["1 <= n <= 节点数 <= 30"],
    [{"input": "1->2->3->4->5, n=2", "output": "1->2->3->5"}],
    "dummy 后快指针先走 n+1 步，再同步移动找前驱。",
    "时间 O(n)，空间 O(1)。",
    ["删除头需要 dummy。", "快指针先走 n+1 步。", "返回 dummy.next。"],
    "def remove_nth(head,n):\n    dummy=ListNode(0,head); fast=slow=dummy\n    for _ in range(n+1): fast=fast.next\n    while fast: fast=fast.next; slow=slow.next\n    slow.next=slow.next.next\n    return dummy.next")

add("p033", "回文链表", "easy", "linked-list", ["链表", "快慢指针"],
    "判断链表是否回文。",
    "希望 O(n) 时间和 O(1) 空间。",
    ["节点数 1..10^5"],
    [{"input": "1->2->2->1", "output": "true"}],
    "找中点，反转后半段，逐个比较；如需可恢复链表。",
    "时间 O(n)，空间 O(1)。",
    ["偶数长度中点位置。", "比较后恢复时要再次反转。", "不能假设值范围小而用数组哈希。"],
    "def is_palindrome_list(head):\n    a=[]\n    while head: a.append(head.val); head=head.next\n    return a==a[::-1]\n# O(1) 版本使用中点反转后半段")

add("p034", "两数相加", "medium", "linked-list", ["链表", "模拟"],
    "逆序存储两个数相加。",
    "返回同格式链表。",
    ["节点数 1..100", "0 <= Node.val <= 9"],
    [{"input": "2->4->3 + 5->6->4", "output": "7->0->8"}],
    "同步遍历，维护进位，最后进位建新节点。",
    "时间 O(max(m,n))，空间 O(1) 输出外。",
    ["长度不同要补 0。", "末尾进位不能丢。", "顺序是低位在前。"],
    "def add_two_numbers(l1,l2):\n    dummy=tail=ListNode(); carry=0\n    while l1 or l2 or carry:\n        s=(l1.val if l1 else 0)+(l2.val if l2 else 0)+carry\n        carry,val=divmod(s,10); tail.next=ListNode(val); tail=tail.next\n        l1=l1.next if l1 else None; l2=l2.next if l2 else None\n    return dummy.next")

add("p035", "复制带随机指针链表", "medium", "linked-list", ["链表", "哈希表"],
    "深拷贝 random 链表。",
    "random 可为空或指向任意节点。",
    ["节点数 0..1000"],
    [{"input": "7->13->11 random: 7->None,13->7,11->1", "output": "完全独立副本"}],
    "哈希表建立旧节点到新节点映射，分两次复制 next/random。",
    "时间 O(n)，空间 O(n)。",
    ["先创建所有节点再连接 random。", "空链返回 None。", "不要共享旧节点对象。"],
    "def copy_random(head):\n    m={None:None}; cur=head\n    while cur: m[cur]=ListNode(cur.val); cur=cur.next\n    cur=head\n    while cur: m[cur].next=m[cur.next]; m[cur].random=m[cur.random]; cur=cur.next\n    return m[head]")

add("p036", "LRU 缓存", "medium", "linked-list", ["设计", "哈希表", "双向链表"],
    "实现 O(1) get/put。",
    "容量正数；put 已存在键不增加使用次数以外的容量。",
    ["1 <= capacity <= 3000"],
    [{"input": "capacity=2, put(1,1),put(2,2),get(1),put(3,3)", "output": "get(1)=1；3 淘汰 2"}],
    "哈希表映射 key 到双向链表节点；get/put 都移到头部，满时删尾部。",
    "get/put O(1)，空间 O(capacity)。",
    ["删除节点要同时改前后指针。", "更新已有 key 要移到最新。", "淘汰后从哈希表删除。"],
    "class LRUCache:\n    def __init__(self,cap):\n        self.cap=cap; self.m={}; self.head=Node(); self.tail=Node(); self.head.next=self.tail; self.tail.prev=self.head\n    def _remove(self,n): n.prev.next=n.next; n.next.prev=n.prev\n    def _add(self,n): n.next=self.head.next; n.prev=self.head; self.head.next.prev=n; self.head.next=n\n    def get(self,k):\n        if k not in self.m: return -1\n        n=self.m[k]; self._remove(n); self._add(n); return n.v\n    def put(self,k,v):\n        if k in self.m: n=self.m[k]; n.v=v; self._remove(n)\n        else: n=Node(k,v); self.m[k]=n\n        self._add(n)\n        if len(self.m)>self.cap: old=self.tail.prev; self._remove(old); del self.m[old.k]")

# Recursion/divide/binary search: 8
add("p037", "快速幂", "medium", "recursion-divide-binary-search", ["数学", "分治"],
    "计算 x^n。",
    "n 可为负，结果可能很大。",
    ["-100 <= x <= 100", "-2^31 <= n <= 2^31-1"],
    [{"input": "x=2,n=10", "output": "1024"}],
    "指数折半；负指数转换为 1/(x^-n)。",
    "时间 O(log n)，空间 O(log n)。",
    ["n 为最小负数取反要小心语言溢出。", "0^0 按题意。", "奇偶指数分支要写清。"],
    "def my_pow(x,n):\n    if n<0: return 1/my_pow(x,-n)\n    ans=1\n    while n:\n        if n&1: ans*=x\n        x*=x; n>>=1\n    return ans")

add("p038", "x 的平方根", "easy", "recursion-divide-binary-search", ["二分", "数学"],
    "返回平方根整数部分。",
    "非负整数 x。",
    ["0 <= x <= 2^31-1"],
    [{"input": "x=8", "output": "2"}],
    "二分最大的 mid 满足 mid*mid <= x。",
    "时间 O(log x)，空间 O(1)。",
    ["0 和 1 单独处理。", "乘积可能溢出语言。", "返回左边界而非 mid。"],
    "def my_sqrt(x):\n    if x<2: return x\n    lo,hi=1,x//2+1\n    while lo<hi:\n        mid=(lo+hi)//2\n        if mid<=x//mid: lo=mid+1\n        else: hi=mid\n    return lo-1")

add("p039", "搜索旋转排序数组", "medium", "recursion-divide-binary-search", ["二分", "数组"],
    "在旋转有序数组中找 target。",
    "值互异，要求 O(log n)。",
    ["1 <= len(nums) <= 5000"],
    [{"input": "nums=[4,5,6,7,0,1,2], target=0", "output": "4"}],
    "判断哪半有序，target 是否落在该有序范围内。",
    "时间 O(log n)，空间 O(1)。",
    ["无重复值是前提。", "先判断有序半边。", "边界包含关系要正确。"],
    "def search_rotated(nums,t):\n    lo,hi=0,len(nums)-1\n    while lo<=hi:\n        mid=(lo+hi)//2\n        if nums[mid]==t: return mid\n        if nums[lo]<=nums[mid]:\n            if nums[lo]<=t<nums[mid]: hi=mid-1\n            else: lo=mid+1\n        else:\n            if nums[mid]<t<=nums[hi]: lo=mid+1\n            else: hi=mid-1\n    return -1")

add("p040", "二分查找", "easy", "recursion-divide-binary-search", ["二分", "数组"],
    "返回 target 下标。",
    "升序数组，不存在返回 -1。",
    ["1 <= len(nums) <= 10^4"],
    [{"input": "nums=[-1,0,3,5,9,12], target=9", "output": "4"}],
    "标准闭区间二分。",
    "时间 O(log n)，空间 O(1)。",
    ["循环条件与边界更新匹配。", "不存在返回 -1。", "mid 向下取整。"],
    "def binary_search(nums,t):\n    lo,hi=0,len(nums)-1\n    while lo<=hi:\n        mid=(lo+hi)//2\n        if nums[mid]==t: return mid\n        if nums[mid]<t: lo=mid+1\n        else: hi=mid-1\n    return -1")

add("p041", "第一个错误版本", "easy", "recursion-divide-binary-search", ["二分", "单调性"],
    "找第一个坏版本。",
    "is_bad(v) 单调：坏版本后都坏。",
    ["1 <= n <= 2^31-1"],
    [{"input": "n=5，bad=4", "output": "4"}],
    "维护左边界为首个可能坏版本。",
    "时间 O(log n)，空间 O(1)。",
    ["mid 相加溢出语言。", "不要调用过多 is_bad。", "返回 left。"],
    "def first_bad_version(n):\n    lo,hi=1,n\n    while lo<hi:\n        mid=lo+(hi-lo)//2\n        if is_bad(mid): hi=mid\n        else: lo=mid+1\n    return lo")

add("p042", "寻找峰值", "medium", "recursion-divide-binary-search", ["二分", "数组"],
    "返回任意峰值下标。",
    "边界外为负无穷，相邻值不相等。",
    ["1 <= len(nums) <= 1000"],
    [{"input": "[1,2,3,1]", "output": "2"}],
    "若 mid < mid+1，右侧必有峰；否则左侧有峰。",
    "时间 O(log n)，空间 O(1)。",
    ["必须利用相邻不等。", "返回任意峰合法。", "边界也算峰。"],
    "def find_peak(nums):\n    lo,hi=0,len(nums)-1\n    while lo<hi:\n        mid=(lo+hi)//2\n        if nums[mid]<nums[mid+1]: lo=mid+1\n        else: hi=mid\n    return lo")

add("p043", "数组中第 K 大元素", "medium", "recursion-divide-binary-search", ["快速选择", "堆"],
    "返回第 k 大。",
    "第 k 大按降序位置计算，可重复。",
    ["1 <= k <= len(nums) <= 10^5"],
    [{"input": "nums=[3,2,1,5,6,4], k=2", "output": "5"}],
    "快速选择第 len-k 小，也可维护大小 k 最小堆。",
    "平均 O(n)，最坏 O(n^2)；堆 O(n log k)。",
    ["第 k 大对应第 n-k 小。", "pivot 分区要含重复。", "最坏数据可随机化。"],
    "import heapq\ndef find_kth_largest(nums,k):\n    heap=[]\n    for x in nums:\n        heapq.heappush(heap,x)\n        if len(heap)>k: heapq.heappop(heap)\n    return heap[0]")

add("p044", "两个有序数组中位数", "hard", "recursion-divide-binary-search", ["二分", "分治"],
    "求合并后中位数。",
    "要求 O(log(m+n))。",
    ["0 <= m,n <= 1000", "不同时为空"],
    [{"input": "nums1=[1,3], nums2=[2]", "output": "2.0"}],
    "在较短数组二分分割，使左半最大 <= 右半最小。",
    "时间 O(log(min(m,n)))，空间 O(1)。",
    ["分割点索引写错。", "空数组边界。", "偶数总长取两数平均。"],
    "def find_median(A,B):\n    if len(A)>len(B): A,B=B,A\n    m,n=len(A),len(B); lo,hi=0,m; half=(m+n+1)//2\n    while lo<=hi:\n        i=(lo+hi)//2; j=half-i\n        LA=A[i-1] if i else float('-inf'); RA=A[i] if i<m else float('inf')\n        LB=B[j-1] if j else float('-inf'); RB=B[j] if j<n else float('inf')\n        if LA>RB: hi=i-1\n        elif LB>RA: lo=i+1\n        else:\n            left=max(LA,LB); right=min(RA,RB)\n            return left if (m+n)%2 else (left+right)/2\n    raise ValueError('invalid input')")

# Trees: 10
add("p045", "二叉树最大深度", "easy", "trees", ["树", "递归"],
    "返回最大深度。",
    "空树深度为 0。",
    ["节点数 0..10^4"],
    [{"input": "3->9,20/15,7", "output": "3"}],
    "后序返回左右深度最大值加一。",
    "时间 O(n)，空间 O(h)。",
    ["空树基线。", "不是节点数。", "递归深度过大可层序。"],
    "def max_depth(root):\n    if not root: return 0\n    return 1+max(max_depth(root.left),max_depth(root.right))")

add("p046", "翻转二叉树", "easy", "trees", ["树", "递归"],
    "镜像翻转左右子树。",
    "返回根。",
    ["节点数 0..100"],
    [{"input": "4->2,7/1,3,6,9", "output": "4->7,2/9,6,3,1"}],
    "交换当前左右，再递归翻转。",
    "时间 O(n)，空间 O(h)。",
    ["交换后左右引用变化。", "空树返回 None。", "不能只交换一层。"],
    "def invert_tree(root):\n    if root: root.left,root.right=invert_tree(root.right),invert_tree(root.left)\n    return root")

add("p047", "验证二叉搜索树", "medium", "trees", ["BST", "递归"],
    "判断是否为合法 BST。",
    "左子树所有节点小于根，右子树所有节点大于根。",
    ["节点数 1..10^4"],
    [{"input": "2->1,3", "output": "true"}],
    "递归传递开区间上下界，或中序保持递增。",
    "时间 O(n)，空间 O(h)。",
    ["不能只比较孩子。", "重复值不合法。", "INT 边界要用可扩展上下界。"],
    "def is_valid_bst(root,lo=float('-inf'),hi=float('inf')):\n    if not root: return True\n    if not lo<root.val<hi: return False\n    return is_valid_bst(root.left,lo,root.val) and is_valid_bst(root.right,root.val,hi)")

add("p048", "二叉树层序遍历", "medium", "trees", ["树", "BFS"],
    "按层返回节点值。",
    "空树返回 []。",
    ["节点数 0..2000"],
    [{"input": "3->9,20/15,7", "output": "[[3],[9,20],[15,7]]"}],
    "队列保存每层节点；先记录层大小。",
    "时间 O(n)，空间 O(n)。",
    ["动态 qlen 变化时不能直接 range(len(q))。", "空树处理。", "每层新建列表。"],
    "from collections import deque\ndef level_order(root):\n    if not root: return []\n    q=deque([root]); ans=[]\n    while q:\n        ans.append([x.val for x in q])\n        for _ in range(len(ans[-1])):\n            x=q.popleft()\n            if x.left: q.append(x.left)\n            if x.right: q.append(x.right)\n    return ans")

add("p049", "锯齿形层序遍历", "medium", "trees", ["树", "BFS"],
    "奇数层左到右，偶数层右到左。",
    "返回嵌套数组。",
    ["节点数 0..2000"],
    [{"input": "3->9,20/15,7", "output": "[[3],[20,9],[15,7]]"}],
    "层序后按层号反转，或用双端队列方向插入。",
    "时间 O(n)，空间 O(n)。",
    ["根层通常左到右。", "不要破坏队列顺序。", "空树返回 []。"],
    "def zigzag(root):\n    levels=level_order(root)\n    return [lv if i%2==0 else lv[::-1] for i,lv in enumerate(levels)]")

add("p050", "二叉树直径", "easy", "trees", ["树", "后序遍历"],
    "返回任意两节点最长路径边数。",
    "路径可不经过根。",
    ["节点数 1..10^4"],
    [{"input": "1->2,3/4,5", "output": "3"}],
    "后序返回深度，同时用左右深度和维护全局直径。",
    "时间 O(n)，空间 O(h)。",
    ["直径是边数，要减 1。", "全局答案在递归中更新。", "单链树返回 n-1。"],
    "def diameter_of_binary_tree(root):\n    ans=0\n    def depth(n):\n        nonlocal ans\n        if not n: return 0\n        l,r=depth(n.left),depth(n.right); ans=max(ans,l+r)\n        return 1+max(l,r)\n    depth(root); return ans")

add("p051", "平衡二叉树", "easy", "trees", ["树", "后序遍历"],
    "判断每个节点左右子树高度差不超过 1。",
    "空树平衡。",
    ["节点数 0..5000"],
    [{"input": "1->2,2/3,3,4,4", "output": "false"}],
    "后序返回高度；不平衡返回 -1 剪枝。",
    "时间 O(n)，空间 O(h)。",
    ["不能自顶向下重复算高度。", "空树 true。", "子树不平衡时提前剪枝。"],
    "def is_balanced(root):\n    def h(n):\n        if not n: return 0\n        l,r=h(n.left),h(n.right)\n        if l<0 or r<0 or abs(l-r)>1: return -1\n        return 1+max(l,r)\n    return h(root)!=-1")

add("p052", "二叉搜索树最近公共祖先", "medium", "trees", ["BST", "LCA"],
    "利用 BST 性质找 LCA。",
    "p、q 均存在且值不同。",
    ["节点数 2..10^5"],
    [{"input": "BST 6->2,8/0,4,p=2,q=8", "output": "6"}],
    "若 p、q 都小于当前向左，都大于向右，否则当前是分叉点。",
    "时间 O(h)，空间 O(1)。",
    ["普通二叉树解法可行但不利用性质。", "值可能很大。", "返回节点不是值。"],
    "def lowest_common_ancestor_bst(root,p,q):\n    while root:\n        if p.val<root.val and q.val<root.val: root=root.left\n        elif p.val>root.val and q.val>root.val: root=root.right\n        else: return root")

add("p053", "二叉树的序列化与反序列化", "hard", "trees", ["树", "设计"],
    "把树编码为字符串并还原。",
    "结构可任意，空节点也要编码。",
    ["节点数 0..10^4"],
    [{"input": "1->2,3/None,4,5,6", "output": "反序列化后结构相同"}],
    "先序遍历，空节点用 #，节点间分隔符；反序列化用迭代器消费。",
    "时间 O(n)，空间 O(n)。",
    ["必须编码空子树。", "分隔符不能与值冲突。", "递归深度可改显式栈。"],
    "def serialize(root):\n    if not root: return '#'\n    return f\"{root.val},{serialize(root.left)},{serialize(root.right)}\"\ndef deserialize(data):\n    vals=iter(data.split(','))\n    def build():\n        v=next(vals)\n        if v=='#': return None\n        node=TreeNode(int(v)); node.left=build(); node.right=build(); return node\n    return build()")

add("p054", "路径总和 III", "medium", "trees", ["树", "前缀和"],
    "统计和为 targetSum 的向下路径数。",
    "路径方向必须父到子，不要求起止为根/叶。",
    ["节点数 0..1000", "-10^9 <= sum <= 10^9"],
    [{"input": "root=10->5,-3/3,2,None,11/3,-2,None,1; target=8", "output": "3"}],
    "树上前缀和；哈希记录路径前缀出现次数，进入时记录、离开时回溯。",
    "时间 O(n)，空间 O(n)。",
    ["前缀计数要初始化 {0:1}。", "递归离开必须回溯。", "路径不能跨子树折返。"],
    "from collections import defaultdict\ndef path_sum(root,target):\n    seen=defaultdict(int); seen[0]=1; ans=0\n    def dfs(n,cur):\n        nonlocal ans\n        if not n: return\n        cur+=n.val; ans+=seen[cur-target]; seen[cur]+=1\n        dfs(n.left,cur); dfs(n.right,cur); seen[cur]-=1\n    dfs(root,0); return ans")

add("p055", "二叉树右视图", "medium", "trees", ["树", "BFS"],
    "返回每层最右节点值。",
    "空树返回 []。",
    ["节点数 0..100"],
    [{"input": "1->2,3/None,5,4", "output": "[1,3,4]"}],
    "层序记录每层最后节点，或先右后左 DFS 首次到达。",
    "时间 O(n)，空间 O(n)。",
    ["DFS 先右才可记录首次。", "空树处理。", "不要把所有最右子链都加入。"],
    "def right_side_view(root):\n    ans=[]\n    def dfs(n,d):\n        if not n: return\n        if d==len(ans): ans.append(n.val)\n        dfs(n.right,d+1); dfs(n.left,d+1)\n    dfs(root,0); return ans")

add("p056", "从中序与先序构造二叉树", "medium", "trees", ["树", "分治"],
    "根据两种遍历重建树。",
    "无重复值。",
    ["1 <= n <= 3000"],
    [{"input": "preorder=[3,9,20,15,7], inorder=[9,3,15,20,7]", "output": "3->9,20/None,None,15,7"}],
    "先序首元素为根；哈希定位中序根，递归确定左右长度。",
    "时间 O(n)，空间 O(n)。",
    ["不重复哈希查找避免 O(n^2)。", "左右区间长度必须一致。", "递归深度大可转迭代。"],
    "def build_tree(preorder,inorder):\n    idx={v:i for i,v in enumerate(inorder)}; pos=0\n    def build(l,r):\n        nonlocal pos\n        if l>r: return None\n        root=TreeNode(preorder[pos]); k=idx[preorder[pos]]; pos+=1\n        root.left=build(l,k-1); root.right=build(k+1,r)\n        return root\n    return build(0,len(inorder)-1)")

# Heap: 7
add("p057", "数据流第 K 大", "easy", "heaps", ["堆", "设计"],
    "流式添加后返回第 K 大。",
    "初始化按升序给出前 k 个元素。",
    ["0 <= nums.length <= 10^4", "1 <= k <= 10^4"],
    [{"input": "k=3, nums=[4,5,8,2], add(3)", "output": "4"}],
    "维护大小为 k 的最小堆，堆顶即第 k 大。",
    "add O(log k)，空间 O(k)。",
    ["初始元素也要过滤到 k 个。", "第 k 大不是最大。", "堆为空时行为定义。"],
    "import heapq\nclass KthLargest:\n    def __init__(self,k,nums):\n        self.k=k; self.h=[]\n        for x in nums: self.add(x)\n    def add(self,x):\n        heapq.heappush(self.h,x)\n        if len(self.h)>self.k: heapq.heappop(self.h)\n        return self.h[0]")

add("p058", "最接近原点的 K 个点", "medium", "heaps", ["堆", "几何"],
    "返回距原点最近 K 点。",
    "距离相等答案任意。",
    ["1 <= k <= n <= 10^4"],
    [{"input": "points=[[1,3],[-2,2]], k=1", "output": "[[-2,2]]"}],
    "维护大小为 k 的最大堆；比较平方距离。",
    "时间 O(n log k)，空间 O(k)。",
    ["不必开方。", "Python 最大堆取负。", "返回原坐标。"],
    "import heapq\ndef k_closest(points,k):\n    heap=[]\n    for x,y in points:\n        d=-(x*x+y*y)\n        if len(heap)<k: heapq.heappush(heap,(d,x,y))\n        elif d>heap[0][0]: heapq.heapreplace(heap,(d,x,y))\n    return [(x,y) for _,x,y in heap]")

add("p059", "合并 K 个升序链表", "hard", "heaps", ["堆", "链表"],
    "合并 k 条有序链表。",
    "返回单条升序链表。",
    ["k <= 10^4", "总节点数 <= 10^5"],
    [{"input": "[[1,4,5],[1,3,4],[2,6]]", "output": "1->1->2->3->4->4->5->6"}],
    "小根堆保存每条链当前节点；弹出接入结果并推进。",
    "时间 O(N log k)，空间 O(k)。",
    ["堆项需要链编号避免同值比较节点对象。", "空链跳过。", "不要重复创建节点。"],
    "import heapq\ndef merge_k_lists(lists):\n    heap=[]\n    for i,node in enumerate(lists):\n        if node: heapq.heappush(heap,(node.val,i,node))\n    dummy=tail=ListNode()\n    while heap:\n        _,i,node=heapq.heappop(heap); tail.next=node; tail=tail.next\n        if node.next: heapq.heappush(heap,(node.next.val,i,node.next))\n    return dummy.next")

add("p060", "前 K 个高频单词", "medium", "heaps", ["哈希表", "堆"],
    "频次降序，同频字典序升序。",
    "返回 k 个单词。",
    ["1 <= words.length <= 10^4", "1 <= k <= 不同单词数"],
    [{"input": "['i','love','leetcode','i','love','coding'], k=2", "output": "['i','love']"}],
    "统计频次；排序键 (-freq, word) 或自定义堆。",
    "时间 O(n + m log m)，空间 O(m)。",
    ["同频必须字典序。", "不要只按频次稳定排序假设输入顺序。", "k 可能等于 m。"],
    "from collections import Counter\ndef top_k_words(words,k):\n    c=Counter(words)\n    return sorted(c,key=lambda w:(-c[w],w))[:k]")

add("p061", "数据流中位数", "hard", "heaps", ["双堆", "设计"],
    "支持 addNum/findMedian。",
    "调用次数可达 5*10^4。",
    ["-10^5 <= num <= 10^5"],
    [{"input": "add(1),add(2),findMedian(),add(3),findMedian()", "output": "1.5,2"}],
    "左最大堆 + 右最小堆，保持大小平衡且左 <= 右。",
    "add O(log n)，findMedian O(1)。",
    ["平衡方向要固定。", "Python 左堆取负。", "偶数取平均。"],
    "import heapq\nclass MedianFinder:\n    def __init__(self): self.left=[]; self.right=[]\n    def add(self,x):\n        heapq.heappush(self.left,-x)\n        heapq.heappush(self.right,-heapq.heappop(self.left))\n        if len(self.right)>len(self.left): heapq.heappush(self.left,-heapq.heappop(self.right))\n    def find(self):\n        return -self.left[0] if len(self.left)>len(self.right) else (-self.left[0]+self.right[0])/2")

add("p062", "任务调度器", "medium", "heaps", ["贪心", "计数"],
    "含冷却时间的最少执行时间。",
    "相同任务间隔至少 n。",
    ["1 <= tasks.length <= 10^4", "0 <= n <= 100"],
    [{"input": "tasks=['A','A','A','B','B','B'], n=2", "output": "8"}],
    "最高频任务形成骨架，其他任务填空隙；公式或模拟。",
    "时间 O(n log 26)，空间 O(26)。",
    ["冷却时间以任务为单位。", "多任务同最高频可并排。", "不需要具体执行顺序。"],
    "from collections import Counter\ndef least_interval(tasks,n):\n    c=Counter(tasks); m=max(c.values())\n    max_count=sum(v==m for v in c.values())\n    return max(len(tasks),(m-1)*(n+1)+max_count)")

add("p063", "和最小的 K 个数对", "medium", "heaps", ["堆", "双数组"],
    "从两个升序数组找和最小 K 个数对。",
    "答案顺序任意。",
    ["1 <= len(nums1),len(nums2) <= 10^4", "1 <= k <= min(10^4, m*n)"],
    [{"input": "nums1=[1,7,11], nums2=[2,4,6], k=3", "output": "[[1,2],[1,4],[1,6]]"}],
    "堆保存 (和, i, j)，弹出后尝试 (i,j+1)，初始只入 (i,0)。",
    "时间 O(k log k)，空间 O(k)。",
    ["初始不要把 m*n 全入堆。", "去重可加 visited。", "数组长度不等要边界。"],
    "import heapq\ndef k_smallest_pairs(A,B,k):\n    if not A or not B: return []\n    heap=[(A[i]+B[0],i,0) for i in range(min(k,len(A)))]\n    heapq.heapify(heap); ans=[]\n    while heap and len(ans)<k:\n        _,i,j=heapq.heappop(heap); ans.append([A[i],B[j]])\n        if j+1<len(B): heapq.heappush(heap,(A[i]+B[j+1],i,j+1))\n    return ans")

# Graph search: 9
add("p064", "岛屿数量", "medium", "graph-search", ["网格", "DFS"],
    "统计 '1' 组成的岛屿数量。",
    "水平垂直相连算同一岛。",
    ["1 <= m,n <= 300"],
    [{"input": "[['1','1','0'],['0','1','0'],['1','0','1']]", "output": "3"}],
    "遍历未访问陆地，DFS/BFS 标记整块。",
    "时间 O(mn)，空间 O(mn)。",
    ["允许修改网格时可原地标记。", "八方向不对。", "访问标记不要漏。"],
    "def num_islands(grid):\n    if not grid: return 0\n    m,n=len(grid),len(grid[0])\n    def dfs(i,j):\n        if not(0<=i<m and 0<=j<n) or grid[i][j]!='1': return\n        grid[i][j]='0'\n        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)): dfs(i+di,j+dj)\n    ans=0\n    for i in range(m):\n        for j in range(n):\n            if grid[i][j]=='1': dfs(i,j); ans+=1\n    return ans")

add("p065", "克隆图", "medium", "graph-search", ["图", "哈希表", "BFS"],
    "深拷贝无向图。",
    "节点值唯一。",
    ["节点数 0..100"],
    [{"input": "1--2,2--3,3--1", "output": "结构相同的新图"}],
    "哈希旧节点到新节点；BFS 复制邻居。",
    "时间 O(V+E)，空间 O(V)。",
    ["先创建节点再连接。", "循环引用要查哈希。", "空图返回 None。"],
    "def clone_graph(node):\n    if not node: return None\n    m={node:Node(node.val)}; q=[node]\n    while q:\n        cur=q.pop()\n        for nb in cur.neighbors:\n            if nb not in m: m[nb]=Node(nb.val); q.append(nb)\n            m[cur].neighbors.append(m[nb])\n    return m[node]")

add("p066", "课程表", "medium", "graph-search", ["拓扑排序", "DAG"],
    "判断课程依赖能否完成。",
    " prerequisites [a,b] 表示先修 b 才能修 a。",
    ["1 <= numCourses <= 2000"],
    [{"input": "numCourses=2, prerequisites=[[1,0]]", "output": "true"}],
    "建图统计入度；Kahn 队列处理入度 0。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["方向不能反。", "有环剩余入度不全为 0。", "重复边入度会翻倍，按输入约定处理。"],
    "from collections import deque,defaultdict\ndef can_finish(n,edges):\n    g=defaultdict(list); indeg=[0]*n\n    for a,b in edges: g[b].append(a); indeg[a]+=1\n    q=deque(i for i in range(n) if indeg[i]==0); seen=0\n    while q:\n        u=q.popleft(); seen+=1\n        for v in g[u]:\n            indeg[v]-=1\n            if indeg[v]==0: q.append(v)\n    return seen==n")

add("p067", "课程表 II", "medium", "graph-search", ["拓扑排序", "DAG"],
    "返回合法修课顺序。",
    "无解返回 []；任意合法顺序都可。",
    ["1 <= numCourses <= 2000"],
    [{"input": "numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]", "output": "[0,1,2,3] 或 [0,2,1,3]"}],
    "Kahn 输出所有入度 0 节点；若长度不足返回空。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["返回长度必须等于课程数。", "方向同课程表。", "重复依赖会影响入度，注意输入语义。"],
    "def find_order(n,edges):\n    g=[[] for _ in range(n)]; indeg=[0]*n\n    for a,b in edges: g[b].append(a); indeg[a]+=1\n    q=deque(i for i in range(n) if indeg[i]==0); ans=[]\n    while q:\n        u=q.popleft(); ans.append(u)\n        for v in g[u]:\n            indeg[v]-=1\n            if indeg[v]==0: q.append(v)\n    return ans if len(ans)==n else []")

add("p068", "太平洋大西洋水流", "medium", "graph-search", ["网格", "多源 DFS"],
    "返回可流入两个海洋的坐标。",
    "水只能从高或相等高度流向低或相等。",
    ["1 <= m,n <= 200"],
    [{"input": "heights=[[1,2,2],[3,2,2]]", "output": "[[0,0],[0,1],[0,2],[1,0],[1,1],[1,2]]"}],
    "从两个海洋边界反向搜索可达格子，求两集合交集。",
    "时间 O(mn)，空间 O(mn)。",
    ["反向条件是高度大于等于。", "不要对每个点都 DFS。", "两个海洋初始化边界不同。"],
    "def pacific_atlantic(h):\n    m,n=len(h),len(h[0]); pac=set(); atl=set()\n    def dfs(i,j,seen):\n        seen.add((i,j))\n        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):\n            a,b=i+di,j+dj\n            if 0<=a<m and 0<=b<n and (a,b) not in seen and h[a][b]>=h[i][j]: dfs(a,b,seen)\n    for i in range(m): dfs(i,0,pac); dfs(i,n-1,atl)\n    for j in range(n): dfs(0,j,pac); dfs(m-1,j,atl)\n    return [list(x) for x in pac&atl]")

add("p069", "腐烂的橘子", "medium", "graph-search", ["网格", "多源 BFS"],
    "所有橘子腐烂的最少分钟。",
    "无法全腐烂返回 -1。",
    ["1 <= m,n <= 10"],
    [{"input": "[[2,1,1],[1,1,0],[0,1,1]]", "output": "4"}],
    "多源 BFS 从所有腐烂橘子同层扩散，最后检查新鲜橘子。",
    "时间 O(mn)，空间 O(mn)。",
    ["初始源点要全部入队。", "分钟从第 0 层计算。", "没有新鲜橘子返回 0。"],
    "from collections import deque\ndef oranges_rotting(grid):\n    m,n=len(grid),len(grid[0]); q=deque(); fresh=0\n    for i in range(m):\n        for j in range(n):\n            if grid[i][j]==2: q.append((i,j,0))\n            elif grid[i][j]==1: fresh+=1\n    ans=0\n    while q and fresh:\n        i,j,t=q.popleft()\n        for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):\n            a,b=i+di,j+dj\n            if 0<=a<m and 0<=b<n and grid[a][b]==1:\n                grid[a][b]=2; fresh-=1; ans=t+1; q.append((a,b,t+1))\n    return -1 if fresh else ans")

add("p070", "单词接龙", "hard", "graph-search", ["BFS", "状态图"],
    "从 beginWord 到 endWord 最短转换序列长度。",
    "每次只改一个字母，必须使用 wordList。",
    ["1 <= len(wordList) <= 5000", "单词等长"],
    [{"input": "begin='hit',end='cog',list=['hot','dot','dog','lot','log','cog']", "output": "5"}],
    "以单词为节点，一次替换为边；BFS 求无权最短路。",
    "时间 O(N L^2)，空间 O(NL)。",
    ["endWord 不在列表无解。", "生成邻接时不要修改原模式键。", "访问后立刻移除避免回头。"],
    "from collections import deque\ndef ladder_length(begin,end,words):\n    words=set(words)\n    if end not in words: return 0\n    q=deque([(begin,1)]); words.discard(begin)\n    while q:\n        word,d=q.popleft()\n        if word==end: return d\n        for i,ch in enumerate(word):\n            for c in 'abcdefghijklmnopqrstuvwxyz':\n                nxt=word[:i]+c+word[i+1:]\n                if nxt in words: q.append((nxt,d+1)); words.remove(nxt)\n    return 0")

add("p071", "无向图连通分量数", "medium", "graph-search", ["图", "DFS"],
    "统计无向图连通块数。",
    "节点编号 0..n-1。",
    ["1 <= n <= 2000"],
    [{"input": "n=5, edges=[[0,1],[1,2],[3,4]]", "output": "2"}],
    "从每个未访问节点 DFS/BFS 计数。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["无向边加两方向。", "孤立节点也算分量。", "边可能重复。"],
    "def count_components(n,edges):\n    g=[[] for _ in range(n)]\n    for a,b in edges: g[a].append(b); g[b].append(a)\n    seen=[False]*n\n    def dfs(u):\n        seen[u]=True\n        for v in g[u]:\n            if not seen[v]: dfs(v)\n    ans=0\n    for i in range(n):\n        if not seen[i]: dfs(i); ans+=1\n    return ans")

add("p072", "判断二分图", "medium", "graph-search", ["图", "染色"],
    "判断能否将节点分成两集合，边都跨集合。",
    "无自环，可能不连通。",
    ["1 <= n <= 100"],
    [{"input": "n=4, edges=[[1,2],[2,3],[3,4],[4,1]]", "output": "true"}],
    "BFS/DFS 染色；相邻必须异色，连通块逐个处理。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["不要只从 0 开始。", "奇环非二分。", "颜色数组初始未知。"],
    "from collections import deque\ndef is_bipartite(n,edges):\n    g=[[] for _ in range(n)]\n    for a,b in edges: g[a].append(b); g[b].append(a)\n    color=[None]*n\n    for start in range(n):\n        if color[start] is not None: continue\n        color[start]=0; q=deque([start])\n        while q:\n            u=q.popleft()\n            for v in g[u]:\n                if color[v] is None: color[v]=color[u]^1; q.append(v)\n                elif color[v]==color[u]: return False\n    return True")

# Shortest/MST: 6
add("p073", "网络延迟时间", "medium", "graph-shortest-mst", ["Dijkstra", "图"],
    "信号从源点到所有节点最短时间。",
    "边权非负；不可达返回 -1。",
    ["1 <= n <= 100", "1 <= times.length <= 6000"],
    [{"input": "times=[[2,1,1],[2,3,1],[3,4,1]], n=4,k=2", "output": "2"}],
    "Dijkstra，返回最大最短距离。",
    "时间 O(E log V)，空间 O(V+E)。",
    ["堆过期距离要跳过。", "源点距离初始化 0。", "不可达用 inf 判断。"],
    "import heapq\ndef network_delay(times,n,k):\n    g=[[] for _ in range(n+1)]\n    for u,v,w in times: g[u].append((v,w))\n    dist=[float('inf')]*(n+1); dist[k]=0; heap=[(0,k)]\n    while heap:\n        d,u=heapq.heappop(heap)\n        if d>dist[u]: continue\n        for v,w in g[u]:\n            nd=d+w\n            if nd<dist[v]: dist[v]=nd; heapq.heappush(heap,(nd,v))\n    ans=max(dist[1:])\n    return -1 if ans==float('inf') else ans")

add("p074", "K 站内最便宜航班", "medium", "graph-shortest-mst", ["Bellman-Ford", "状态约束"],
    "最多经过 K 站的最低价格。",
    "可能存在负价或不连通。",
    ["1 <= n <= 100", "0 <= k < n"],
    [{"input": "n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0,dst=2,k=1", "output": "200"}],
    "Bellman-Ford 只松弛 K+1 轮，每轮用上一轮距离。",
    "时间 O(K*E)，空间 O(V)。",
    ["必须临时复制距离。", "经过 K 站表示最多 K+1 条边。", "源点初始为 0。"],
    "def cheapest_flights(n,flights,src,dst,k):\n    dist=[float('inf')]*n; dist[src]=0\n    for _ in range(k+1):\n        temp=dist[:]\n        for u,v,w in flights:\n            if dist[u]<float('inf'): temp[v]=min(temp[v],dist[u]+w)\n        dist=temp\n    return -1 if dist[dst]==float('inf') else dist[dst]")

add("p075", "最小体力消耗路径", "medium", "graph-shortest-mst", ["二分答案", "图"],
    "路径最大相邻高度差最小。",
    "可上下左右移动。",
    ["1 <= row,col <= 100"],
    [{"input": "[[1,2,2],[3,8,2],[5,3,5]]", "output": "2"}],
    "二分最大允许差，用 BFS 判断可达；或 Dijkstra 边权为相邻差。",
    "时间 O(mn log(maxDiff))，空间 O(mn)。",
    ["路径代价是最大差不是总和。", "二分范围包含 0。", "起点也要标记。"],
    "from collections import deque\ndef minimum_effort(h):\n    m,n=len(h),len(h[0])\n    def ok(limit):\n        seen={(0,0)}; q=deque([(0,0)])\n        while q:\n            i,j=q.popleft()\n            if (i,j)==(m-1,n-1): return True\n            for di,dj in ((1,0),(-1,0),(0,1),(0,-1)):\n                a,b=i+di,j+dj\n                if 0<=a<m and 0<=b<n and (a,b) not in seen and abs(h[a][b]-h[i][j])<=limit:\n                    seen.add((a,b)); q.append((a,b))\n        return False\n    lo,hi=0,max(map(max,h))\n    while lo<hi:\n        mid=(lo+hi)//2\n        if ok(mid): hi=mid\n        else: lo=mid+1\n    return lo")

add("p076", "连接所有点最低成本", "medium", "graph-shortest-mst", ["MST", "Prim"],
    "曼哈顿距离建图求 MST。",
    "点可能重合。",
    ["1 <= points.length <= 1000"],
    [{"input": "[[0,0],[2,2],[3,10],[5,2],[7,0]]", "output": "20"}],
    "Prim：堆保存到已选集合的最小边，扩张所有点。",
    "时间 O(n^2 log n)，空间 O(n^2)。",
    ["跳过已在集合中的点。", "重合边权为 0 合法。", "n=1 成本 0。"],
    "import heapq\ndef min_cost_connect(points):\n    n=len(points); seen=set(); heap=[(0,0)]; ans=0\n    while len(seen)<n:\n        d,u=heapq.heappop(heap)\n        if u in seen: continue\n        seen.add(u); ans+=d\n        x1,y1=points[u]\n        for v,(x2,y2) in enumerate(points):\n            if v not in seen: heapq.heappush(heap,(abs(x1-x2)+abs(y1-y2),v))\n    return ans")

add("p077", "冗余连接", "medium", "graph-shortest-mst", ["并查集", "图"],
    "找出加入后形成环的边。",
    "若有多个答案返回输入中最后出现者。",
    ["3 <= n <= 1000"],
    [{"input": "[[1,2],[1,3],[2,3]]", "output": "[2,3]"}],
    "按输入顺序用并查集连接；两个端点已同根即为答案。",
    "时间 O(n α(n))，空间 O(n)。",
    ["先 find 后比较。", "边编号按输入顺序。", "1-based 编号不要错位。"],
    "def find_redundant(edges):\n    p=list(range(len(edges)+1))\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    for a,b in edges:\n        ra,rb=find(a),find(b)\n        if ra==rb: return [a,b]\n        p[ra]=rb\n    return []")

add("p078", "最低成本连通所有设备", "hard", "graph-shortest-mst", ["MST", "Kruskal"],
    "可选铺设边或购买模块，求最小成本。",
    "每台设备可购买模块独立连通； edges 提供铺设候选。",
    ["1 <= n <= 1000", "1 <= edges.length <= n*(n-1)/2"],
    [{"input": "n=3, modules=[1,2,3], edges=[[1,2,100],[2,3,5],[3,1,4]]", "output": "9"}],
    "把“购买设备 i”视作与虚拟节点 0 相连、权为 moduleCost 的边；跑 MST。",
    "时间 O(E log E)，空间 O(E)。",
    ["必须加入虚拟节点。", "图不连通时需要模块保证连通。", "成本可超过普通 int。"],
    "def min_cost(n,module,edges):\n    all_edges=[(module[i],0,i+1) for i in range(n)]+[(w,a,b) for a,b,w in edges]\n    all_edges.sort(); p=list(range(n+1))\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    ans=used=0\n    for w,a,b in all_edges:\n        ra,rb=find(a),find(b)\n        if ra!=rb: p[ra]=rb; ans+=w; used+=1\n        if used==n: return ans\n    return -1")

# Backtracking: 8
add("p079", "全排列", "medium", "backtracking", ["回溯", "排列"],
    "返回所有全排列。",
    "输入元素互异。",
    ["1 <= len(nums) <= 6"],
    [{"input": "[1,2,3]", "output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"}],
    "回溯选未用元素，选后撤销。",
    "时间 O(n*n!)，空间 O(n)。",
    ["记录排列必须复制 path。", "used 状态要撤销。", "有重复值需另加同层去重。"],
    "def permute(nums):\n    ans=[]; used=[False]*len(nums); path=[]\n    def dfs():\n        if len(path)==len(nums): ans.append(path.copy()); return\n        for i,x in enumerate(nums):\n            if not used[i]: used[i]=True; path.append(x); dfs(); path.pop(); used[i]=False\n    dfs(); return ans")

add("p080", "子集", "medium", "backtracking", ["回溯", "子集"],
    "返回所有子集。",
    "元素互异，顺序任意。",
    ["1 <= len(nums) <= 10"],
    [{"input": "[1,2,3]", "output": "[[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]"}],
    "每个节点都是一个子集；从 start 递归避免重复组合。",
    "时间 O(n*2^n)，空间 O(n)。",
    ["进入递归先记录。", "起点用 i+1。", "不能记录同一列表引用。"],
    "def subsets(nums):\n    ans=[]; path=[]\n    def dfs(start):\n        ans.append(path.copy())\n        for i in range(start,len(nums)):\n            path.append(nums[i]); dfs(i+1); path.pop()\n    dfs(0); return ans")

add("p081", "组合总和", "medium", "backtracking", ["回溯", "可重复选择"],
    "候选数可重复使用，找出和为 target 的组合。",
    "候选互异且正数。",
    ["1 <= len(candidates) <= 30", "2 <= target <= 40"],
    [{"input": "candidates=[2,3,6,7], target=7", "output": "[[2,2,3],[7]]"}],
    "排序后回溯；允许重复使用时递归仍从 i 开始。",
    "时间上界 O(2^target)，空间 O(target)。",
    ["递归起点不要写成 i+1。", "同层可排序剪枝。", "结果必须复制。"],
    "def combination_sum(candidates,target):\n    candidates.sort(); ans=[]; path=[]\n    def dfs(start,rest):\n        if rest==0: ans.append(path.copy()); return\n        for i in range(start,len(candidates)):\n            if candidates[i]>rest: break\n            path.append(candidates[i]); dfs(i,rest-candidates[i]); path.pop()\n    dfs(0,target); return ans")

add("p082", "分割回文串", "medium", "backtracking", ["回溯", "字符串"],
    "把字符串分割成全回文子串。",
    "返回所有分割方案。",
    ["1 <= len(s) <= 16"],
    [{"input": "aab", "output": "[['a','a','b'],['aa','b']]"}],
    "回溯每个切点，DP 预处理区间回文。",
    "最坏 O(n*2^n)，空间 O(n^2)。",
    ["空子串不是回文切法。", "预处理循环方向。", "切到末尾才记录。"],
    "def partition(s):\n    n=len(s); pal=[[False]*n for _ in range(n)]\n    for i in range(n-1,-1,-1):\n        for j in range(i,n): pal[i][j]=s[i]==s[j] and (j-i<2 or pal[i+1][j-1])\n    ans=[]; path=[]\n    def dfs(start):\n        if start==n: ans.append(path.copy()); return\n        for end in range(start,n):\n            if pal[start][end]: path.append(s[start:end+1]); dfs(end+1); path.pop()\n    dfs(0); return ans")

add("p083", "单词搜索", "medium", "backtracking", ["回溯", "网格"],
    "判断网格中是否存在相邻字符组成单词。",
    "同格不能重复使用。",
    ["1 <= m,n <= 6", "1 <= len(word) <= 15"],
    [{"input": "board=[['A','B'],['C','D']], word='ABDC'", "output": "true"}],
    "从每个格子 DFS，匹配后临时标记并恢复。",
    "时间 O(mn*3^L)，空间 O(L)。",
    ["先判断字符再越界更高效。", "恢复必须写原字符。", "单词到达末尾立即 true。"],
    "def exist(board,word):\n    m,n=len(board),len(board[0])\n    def dfs(i,j,k):\n        if k==len(word): return True\n        if not(0<=i<m and 0<=j<n) or board[i][j]!=word[k]: return False\n        old=board[i][j]; board[i][j]='#'\n        ok=any(dfs(i+di,j+dj,k+1) for di,dj in ((1,0),(-1,0),(0,1),(0,-1)))\n        board[i][j]=old; return ok\n    return any(dfs(i,j,0) for i in range(m) for j in range(n))")

add("p084", "N 皇后", "hard", "backtracking", ["回溯", "剪枝"],
    "返回所有 n 皇后方案。",
    "皇后不同行、列、对角线。",
    ["1 <= n <= 9"],
    [{"input": "n=4", "output": "2 个方案"}],
    "按行放置，用集合记录列和两条对角线。",
    "时间 O(n!)，空间 O(n)。",
    ["主对角线是 row-col。", "副对角线是 row+col。", "回溯要移除三个状态。"],
    "def solve_n_queens(n):\n    ans=[]; cols=set(); d1=set(); d2=set(); qs=[]\n    def dfs(row):\n        if row==n:\n            ans.append(['.'*c+'Q'+'.'*(n-c-1) for c in qs]); return\n        for col in range(n):\n            if col in cols or row-col in d1 or row+col in d2: continue\n            cols.add(col); d1.add(row-col); d2.add(row+col); qs.append(col)\n            dfs(row+1)\n            cols.remove(col); d1.remove(row-col); d2.remove(row+col); qs.pop()\n    dfs(0); return ans")

add("p085", "解数独", "hard", "backtracking", ["回溯", "约束满足"],
    "填充完整数独。",
    "输入保证有唯一解。",
    ["9x9 board", "空格为 '.'"],
    [{"input": "标准数独棋盘", "output": "填满后每行/列/宫 1-9"}],
    "回溯空格，尝试 1-9；集合检查行列宫。",
    "最坏指数，实际剪枝强。",
    ["宫索引是 (i//3)*3+j//3。", "失败必须清除状态。", "找到解后应停止搜索。"],
    "def solve_sudoku(board):\n    rows=[set() for _ in range(9)]; cols=[set() for _ in range(9)]; boxes=[set() for _ in range(9)]; empties=[]\n    for i in range(9):\n        for j in range(9):\n            if board[i][j]=='.': empties.append((i,j))\n            else: rows[i].add(v:=int(board[i][j])); cols[j].add(v); boxes[(i//3)*3+j//3].add(v)\n    def dfs(k=0):\n        if k==len(empties): return True\n        i,j=empties[k]; b=(i//3)*3+j//3\n        for v in range(1,10):\n            if v not in rows[i] and v not in cols[j] and v not in boxes[b]:\n                board[i][j]=str(v); rows[i].add(v); cols[j].add(v); boxes[b].add(v)\n                if dfs(k+1): return True\n                rows[i].remove(v); cols[j].remove(v); boxes[b].remove(v); board[i][j]='.'\n        return False\n    dfs()")

add("p086", "电话号码字母组合", "medium", "backtracking", ["回溯", "字符串"],
    "数字串对应所有字母组合。",
    "数字 2-9；空串返回 []。",
    ["0 <= len(digits) <= 4"],
    [{"input": "'23'", "output": "['ad','ae','af','bd','be','bf','cd','ce','cf']"}],
    "逐位回溯每个按键字母。",
    "时间 O(4^n*n)，空间 O(n)。",
    ["空输入返回空数组不是空串。", "数字 0/1 无字母。", "结果复制。"],
    "def letter_combinations(digits):\n    if not digits: return []\n    mp={'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}\n    ans=[]; path=[]\n    def dfs(i):\n        if i==len(digits): ans.append(''.join(path)); return\n        for ch in mp[digits[i]]: path.append(ch); dfs(i+1); path.pop()\n    dfs(0); return ans")

# Greedy: 8
add("p087", "跳跃游戏", "medium", "greedy", ["贪心", "数组"],
    "判断能否到达最后下标。",
    "nums[i] 是最大跳跃步数。",
    ["1 <= len(nums) <= 10^4", "0 <= nums[i] <= 10^5"],
    [{"input": "[2,3,1,1,4]", "output": "true"}],
    "维护可达最右边界，遇到 i>far 返回 false。",
    "时间 O(n)，空间 O(1)。",
    ["不能只看当前值。", "首个 0 前若已达末尾仍可行。", "far 初始 0。"],
    "def can_jump(nums):\n    far=0\n    for i,x in enumerate(nums):\n        if i>far: return False\n        far=max(far,i+x)\n    return True")

add("p088", "跳跃游戏 II", "medium", "greedy", ["贪心", "层次"],
    "最少跳跃次数到达末尾。",
    "保证可达。",
    ["1 <= len(nums) <= 10^4", "0 <= nums[i] <= 1000"],
    [{"input": "[2,3,1,1,4]", "output": "2"}],
    "按当前层边界遍历，跨层时步数加一并更新下一层最远点。",
    "时间 O(n)，空间 O(1)。",
    ["最后一格不需要起跳。", "current_end 更新时机。", "无解约束排除。"],
    "def jump(nums):\n    steps=end=far=0\n    for i in range(len(nums)-1):\n        far=max(far,i+nums[i])\n        if i==end: steps+=1; end=far\n    return steps")

add("p089", "合并区间", "medium", "greedy", ["排序", "区间"],
    "合并所有重叠区间。",
    "端点相邻视题意，这里起点 <= 上一个终点则重叠。",
    ["1 <= len(intervals) <= 10^4"],
    [{"input": "[[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"}],
    "按起点排序，维护当前合并区间的最大终点。",
    "时间 O(n log n)，空间 O(n)。",
    ["不能只比较相邻原区间终点。", "嵌套区间终点取 max。", "排序会改变返回顺序语义。"],
    "def merge_intervals(intervals):\n    intervals.sort(); merged=[]\n    for s,e in intervals:\n        if merged and s<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],e)\n        else: merged.append([s,e])\n    return merged")

add("p090", "无重叠区间", "medium", "greedy", ["区间调度", "贪心"],
    "移除最少区间使剩余互不重叠。",
    "端点相接视为不重叠。",
    ["1 <= len(intervals) <= 10^5"],
    [{"input": "[[1,2],[2,3],[3,4],[1,3]]", "output": "1"}],
    "按结束时间排序，保留最早结束区间，统计冲突移除数。",
    "时间 O(n log n)，空间 O(1)。",
    ["排序键必须是终点。", "start >= end 才可保留。", "不能求最多保留后忘记转换答案。"],
    "def erase_overlap(intervals):\n    intervals.sort(key=lambda x:x[1]); end=float('-inf'); remove=0\n    for s,e in intervals:\n        if s>=end: end=e\n        else: remove+=1\n    return remove")

add("p091", "用最少数量的箭引爆气球", "medium", "greedy", ["区间", "贪心"],
    "端点重叠的区间可被一支箭引爆。",
    "箭射在 x，x_start <= x <= x_end 有效。",
    ["1 <= points.length <= 10^5"],
    [{"input": "[[10,16],[2,8],[1,6],[7,12]]", "output": "2"}],
    "按终点排序；当前箭位置为已选区间最小终点，新起点 > 箭位则新增箭。",
    "时间 O(n log n)，空间 O(1)。",
    ["端点相等可共用箭。", "不要按起点排序直接贪。", "空输入返回 0。"],
    "def find_min_arrows(points):\n    if not points: return 0\n    points.sort(key=lambda p:p[1]); arrows=1; pos=points[0][1]\n    for s,e in points[1:]:\n        if s>pos: arrows+=1; pos=e\n    return arrows")

add("p092", "分发饼干", "easy", "greedy", ["排序", "匹配"],
    "尽量满足最多孩子。",
    "每个饼干只能给一个孩子。",
    ["1 <= g.length,s.length <= 2*10^4"],
    [{"input": "g=[1,2,3], s=[1,1]", "output": "1"}],
    "孩子需求和饼干尺寸升序，双指针满足最小可行孩子。",
    "时间 O(n log n)，空间 O(1)。",
    ["不能用大饼干随便浪费。", "指针各只前进。", "无饼干返回 0。"],
    "def find_content_children(g,s):\n    g.sort(); s.sort(); i=j=0\n    while i<len(g) and j<len(s):\n        if s[j]>=g[i]: i+=1\n        j+=1\n    return i")

add("p093", "划分字母区间", "medium", "greedy", ["贪心", "区间"],
    "切分最多片段，使每字母只出现在一个片段。",
    "返回各片段长度。",
    ["1 <= len(s) <= 500"],
    [{"input": "ababcbacadefegdehijhklij", "output": "[9,7,8]"}],
    "记录每字符最后位置；扫描扩展当前片段终点。",
    "时间 O(n)，空间 O(alphabet)。",
    ["终点是 max(当前, last[ch])。", "到达终点才切片。", "返回长度不是子串。"],
    "def partition_labels(s):\n    last={ch:i for i,ch in enumerate(s)}; ans=[]; start=end=0\n    for i,ch in enumerate(s):\n        end=max(end,last[ch])\n        if i==end: ans.append(end-start+1); start=end+1\n    return ans")

add("p094", "分发糖果", "hard", "greedy", ["双向贪心", "数组"],
    "相邻评分更高者糖果更多，求最少总数。",
    "每个孩子至少 1。",
    ["1 <= ratings.length <= 2*10^4"],
    [{"input": "[1,0,2]", "output": "5"}],
    "左到右满足右比左大，右到左满足左比右大，取两次约束最大值。",
    "时间 O(n)，空间 O(n)。",
    ["两个方向都要满足。", "相等评分无额外约束。", "不能只单遍贪心。"],
    "def candy(ratings):\n    n=len(ratings); left=[1]*n\n    for i in range(1,n):\n        if ratings[i]>ratings[i-1]: left[i]=left[i-1]+1\n    ans=right=1\n    for i in range(n-2,-1,-1):\n        if ratings[i]>ratings[i+1]: right+=1\n        else: right=1\n        ans+=max(left[i],right)\n    return ans")

# DP: 12
add("p095", "爬楼梯", "easy", "dynamic-programming", ["线性 DP", "斐波那契"],
    "每次 1 或 2 阶，求到达 n 的方案数。",
    "n 正整数。",
    ["1 <= n <= 45"],
    [{"input": "n=3", "output": "3"}],
    "dp[i]=dp[i-1]+dp[i-2]。",
    "时间 O(n)，空间 O(1)。",
    ["dp[1]=1，dp[2]=2。", "不要递归无记忆。", "大 n 可矩阵快速幂。"],
    "def climb_stairs(n):\n    a=b=1\n    for _ in range(2,n+1): a,b=b,a+b\n    return b")

add("p096", "打家劫舍", "medium", "dynamic-programming", ["线性 DP"],
    "不能偷相邻房屋，求最大金额。",
    "金额非负。",
    ["1 <= len(nums) <= 100"],
    [{"input": "[2,7,9,3,1]", "output": "12"}],
    "dp[i]=max(dp[i-1], dp[i-2]+nums[i])。",
    "时间 O(n)，空间 O(1)。",
    ["首屋也可不偷。", "空数组约束排除但接口可防御。", "不是子序列。"],
    "def rob(nums):\n    prev=cur=0\n    for x in nums: prev,cur=cur,max(cur,prev+x)\n    return cur")

add("p097", "零钱兑换", "medium", "dynamic-programming", ["完全背包"],
    "凑出 amount 的最少硬币数。",
    "每种硬币无限；无法凑出返回 -1。",
    ["1 <= coins.length <= 12", "0 <= amount <= 10^4"],
    [{"input": "coins=[1,2,5], amount=11", "output": "3"}],
    "完全背包正序容量；dp[c]=min(dp[c], dp[c-coin]+1)。",
    "时间 O(amount*n)，空间 O(amount)。",
    ["coin > amount 跳过。", "初始化 inf。", "求最少不是方案数。"],
    "def coin_change(coins,amount):\n    dp=[0]+[float('inf')]*amount\n    for c in coins:\n        for x in range(c,amount+1): dp[x]=min(dp[x],dp[x-c]+1)\n    return -1 if dp[amount]==float('inf') else dp[amount]")

add("p098", "零钱兑换 II", "medium", "dynamic-programming", ["完全背包", "组合数"],
    "统计凑出金额的组合数。",
    "顺序不同视为同一组合。",
    ["1 <= coins.length <= 300", "0 <= amount <= 5000"],
    [{"input": "coins=[1,2,5], amount=5", "output": "4"}],
    "外层物品，内层容量正序，dp[c]+=dp[c-coin]。",
    "时间 O(amount*n)，空间 O(amount)。",
    ["外层容量会算成排列数。", "amount=0 返回 1。", "coin=0 要特殊处理。"],
    "def change(coins,amount):\n    dp=[1]+[0]*amount\n    for coin in coins:\n        for c in range(coin,amount+1): dp[c]+=dp[c-coin]\n    return dp[amount]")

add("p099", "最长上升子序列", "medium", "dynamic-programming", ["子序列", "二分"],
    "求严格上升子序列最大长度。",
    "可有重复和负数。",
    ["1 <= len(nums) <= 2500"],
    [{"input": "[10,9,2,5,3,7,101,18]", "output": "4"}],
    "tails[k] 存长度 k+1 的最小尾值，二分替换。",
    "时间 O(n log n)，空间 O(n)。",
    ["严格上升用 bisect_left。", "tails 不一定是真实 LIS。", "相等元素不延长。"],
    "from bisect import bisect_left\ndef length_of_lis(nums):\n    tails=[]\n    for x in nums:\n        i=bisect_left(tails,x)\n        if i==len(tails): tails.append(x)\n        else: tails[i]=x\n    return len(tails)")

add("p100", "最长公共子序列", "medium", "dynamic-programming", ["子序列", "字符串"],
    "返回两字符串 LCS 长度。",
    "子序列可不连续但保持顺序。",
    ["1 <= len(text) <= 1000"],
    [{"input": "abcde, ace", "output": "3"}],
    "相等取左上+1，否则取左/上最大。",
    "时间 O(mn)，空间可滚动 O(n)。",
    ["子串和子序列不同。", "空串 LCS 为 0。", "循环下标对应 i-1/j-1。"],
    "def lcs(a,b):\n    m,n=len(a),len(b); dp=[[0]*(n+1) for _ in range(m+1)]\n    for i in range(1,m+1):\n        for j in range(1,n+1):\n            dp[i][j]=dp[i-1][j-1]+1 if a[i-1]==b[j-1] else max(dp[i-1][j],dp[i][j-1])\n    return dp[m][n]")

add("p101", "编辑距离", "hard", "dynamic-programming", ["字符串", "DP"],
    "把 word1 变成 word2 的最少操作。",
    "操作为插入、删除、替换。",
    ["0 <= len(word) <= 500"],
    [{"input": "horse, ros", "output": "3"}],
    "字符相等继承左上；否则 1+min(删、插、换)。",
    "时间 O(mn)，空间可滚动。",
    ["空串边界 dp[0][j]=j。", "删除方向要明确。", "相等时不能再加一。"],
    "def min_distance(a,b):\n    m,n=len(a),len(b); dp=[[0]*(n+1) for _ in range(m+1)]\n    for i in range(m+1): dp[i][0]=i\n    for j in range(n+1): dp[0][j]=j\n    for i in range(1,m+1):\n        for j in range(1,n+1):\n            dp[i][j]=dp[i-1][j-1] if a[i-1]==b[j-1] else 1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1])\n    return dp[m][n]")

add("p102", "不同路径", "medium", "dynamic-programming", ["网格 DP"],
    "机器人只能右/下，求路径数。",
    "起点左上，终点右下。",
    ["1 <= m,n <= 100"],
    [{"input": "m=3,n=7", "output": "28"}],
    "dp[i][j]=dp[i-1][j]+dp[i][j-1]。",
    "时间 O(mn)，空间 O(n)。",
    ["第一行/列为 1。", "可滚动优化。", "也可组合数学 C(m+n-2,m-1)。"],
    "def unique_paths(m,n):\n    dp=[1]*n\n    for _ in range(1,m):\n        for j in range(1,n): dp[j]+=dp[j-1]\n    return dp[-1]")

add("p103", "最小路径和", "medium", "dynamic-programming", ["网格 DP"],
    "右/下移动求最小数字和。",
    "非负网格。",
    ["1 <= grid.length <= 200"],
    [{"input": "[[1,3,1],[1,5,1],[4,2,1]]", "output": "7"}],
    "dp[i][j]=grid[i][j]+min(上,左)。",
    "时间 O(mn)，空间 O(n)。",
    ["第一列只能从上。", "不是路径数。", "可原地或滚动。"],
    "def min_path_sum(grid):\n    m,n=len(grid),len(grid[0]); dp=[float('inf')]*n; dp[0]=0\n    for row in grid:\n        dp[0]+=row[0]\n        for j in range(1,n): dp[j]=row[j]+min(dp[j],dp[j-1])\n    return dp[-1]")

add("p104", "分割等和子集", "medium", "dynamic-programming", ["0/1背包", "子集和"],
    "判断能否分成两个和相等的子集。",
    "元素非负。",
    ["1 <= len(nums) <= 200", "1 <= nums[i] <= 100"],
    [{"input": "[1,5,11,5]", "output": "true"}],
    "目标和为 total/2，0/1 背包倒序容量判断可达。",
    "时间 O(n*target)，空间 O(target)。",
    ["总和奇数 false。", "必须倒序防止重复取。", "可含 0 时注意可达。"],
    "def can_partition(nums):\n    total=sum(nums)\n    if total%2: return False\n    target=total//2; dp=[True]+[False]*target\n    for x in nums:\n        for c in range(target,x-1,-1): dp[c]=dp[c] or dp[c-x]\n    return dp[target]")

add("p105", "单词拆分", "medium", "dynamic-programming", ["字符串", "DP"],
    "判断字符串能否由字典单词拼接。",
    "字典单词可重复使用。",
    ["1 <= len(s) <= 300"],
    [{"input": "s='leetcode', wordDict=['leet','code']", "output": "true"}],
    "dp[i] 表示前 i 个字符可拆；枚举上一个切点或字典词。",
    "时间 O(n^2) 或 O(n*m)，空间 O(n)。",
    ["dp[0]=true。", "拼接必须连续。", "字典长词可优化 Trie。"],
    "def word_break(s,words):\n    words=set(words); n=len(s); dp=[True]+[False]*n\n    for i in range(1,n+1):\n        for j in range(i):\n            if dp[j] and s[j:i] in words: dp[i]=True; break\n    return dp[n]")

add("p106", "解码方法", "medium", "dynamic-programming", ["字符串", "DP"],
    "数字串按 1-26 解码的方案数。",
    "'0' 不能单独解码。",
    ["1 <= len(s) <= 100"],
    [{"input": "'226'", "output": "3"}],
    "dp[i] 依赖单字符和两位数是否合法。",
    "时间 O(n)，空间 O(1)。",
    ["前导 0 为 0。", "两位数必须 10..26。", "空串约束排除。"],
    "def num_decodings(s):\n    if s[0]=='0': return 0\n    prev=cur=1\n    for i in range(1,len(s)):\n        nxt=0\n        if s[i]!='0': nxt=cur\n        if 10<=int(s[i-1:i+1])<=26: nxt+=prev\n        if not nxt: return 0\n        prev,cur=cur,nxt\n    return cur")

add("p107", "最大正方形", "medium", "dynamic-programming", ["网格 DP", "矩阵"],
    "求只含 1 的最大正方形面积。",
    "二进制矩阵。",
    ["1 <= m,n <= 300"],
    [{"input": "[[0,1],[1,1]]", "output": "1"}],
    "dp[i][j]=min(上,左,左上)+1；返回边长平方。",
    "时间 O(mn)，空间 O(n)。",
    ["面积是边长平方。", "滚动数组保存左上。", "字符 1 转数值。"],
    "def maximal_square(matrix):\n    m,n=len(matrix),len(matrix[0]); dp=[0]*(n+1); best=0; prev_diag=0\n    for i in range(m):\n        prev_diag=0\n        for j in range(1,n+1):\n            old=dp[j]\n            if matrix[i][j-1]=='1': dp[j]=min(dp[j],dp[j-1],prev_diag)+1; best=max(best,dp[j])\n            else: dp[j]=0\n            prev_diag=old\n    return best*best")

add("p108", "戳气球", "hard", "dynamic-programming", ["区间 DP"],
    "戳破气球获得最大硬币数。",
    "边界视为 1；最后戳破 i 收益 left*i*right。",
    ["1 <= n <= 300"],
    [{"input": "[3,1,5,8]", "output": "167"}],
    "枚举区间内最后戳破的气球；dp[l][r] 表示开区间最大收益。",
    "时间 O(n^3)，空间 O(n^2)。",
    ["逆向思考最后一步。", "边界补 1。", "区间长度从小到大。"],
    "def max_coins(nums):\n    a=[1]+[x for x in nums if x]+[1]; n=len(a)\n    dp=[[0]*n for _ in range(n)]\n    for length in range(2,n):\n        for l in range(n-length):\n            r=l+length\n            dp[l][r]=max(dp[l][k]+a[l]*a[k]*a[r]+dp[k][r] for k in range(l+1,r))\n    return dp[0][n-1]")

# Strings: 6
add("p109", "验证回文串", "easy", "strings", ["字符串", "双指针"],
    "忽略大小写和非字母数字判断回文。",
    "空串视为回文。",
    ["1 <= len(s) <= 2*10^5"],
    [{"input": "A man, a plan, a canal: Panama", "output": "true"}],
    "左右指针跳过非字母数字后比较。",
    "时间 O(n)，空间 O(1)。",
    ["忽略标点和空格。", "大小写统一。", "数字也参与比较。"],
    "def is_palindrome(s):\n    l,r=0,len(s)-1\n    while l<r:\n        while l<r and not s[l].isalnum(): l+=1\n        while l<r and not s[r].isalnum(): r-=1\n        if s[l].lower()!=s[r].lower(): return False\n        l+=1; r-=1\n    return True")

add("p110", "字符串转整数 atoi", "medium", "strings", ["字符串", "模拟"],
    "解析前导空格后的整数并截断。",
    "溢出截断到 32 位范围。",
    ["0 <= len(s) <= 200"],
    [{"input": "'   -42'", "output": "-42"}],
    "状态机：空格、符号、数字；越界时立即截断。",
    "时间 O(n)，空间 O(1)。",
    ["只忽略一次前导空格。", "非数字立即停止。", "INT_MIN 截断方向。"],
    "def my_atoi(s):\n    i=0; sign=1\n    while i<len(s) and s[i]==' ': i+=1\n    if i<len(s) and s[i] in '+-': sign=-1 if s[i]=='-' else 1; i+=1\n    num=0\n    while i<len(s) and s[i].isdigit():\n        num=num*10+int(s[i]); i+=1\n    num=sign*num\n    return max(-2**31,min(2**31-1,num))")

add("p111", "最长回文子串", "medium", "strings", ["回文", "中心扩展"],
    "返回最长回文子串。",
    "多个答案返回任意一个。",
    ["1 <= len(s) <= 1000"],
    [{"input": "babad", "output": "bab 或 aba"}],
    "奇偶中心扩展，记录最大区间。",
    "时间 O(n^2)，空间 O(1)。",
    ["偶数长度中心是两字符间。", "返回区间闭开一致。", "全相同字符。"],
    "def longest_palindrome(s):\n    best=(0,0)\n    def expand(l,r):\n        while l>=0 and r<len(s) and s[l]==s[r]: l-=1; r+=1\n        return l+1,r\n    for i in range(len(s)):\n        for l,r in (expand(i,i),expand(i,i+1)):\n            if r-l>best[1]-best[0]: best=(l,r)\n    return s[best[0]:best[1]]")

add("p112", "找出字符串第一个匹配项", "easy", "strings", ["字符串匹配", "KMP"],
    "返回 needle 在 haystack 首次下标。",
    "不存在返回 -1。",
    ["1 <= len(haystack),len(needle) <= 10^4"],
    [{"input": "haystack='sadbutsad', needle='sad'", "output": "0"}],
    "KMP 构建最长相等前后缀，失败时模式串跳转。",
    "时间 O(n+m)，空间 O(m)。",
    ["next 数组下标含义要固定。", "空 needle 按题意。", "不要每次切子串。"],
    "def str_str(h,n):\n    if not n: return 0\n    nxt=[0]*len(n); k=0\n    for i in range(1,len(n)):\n        while k and n[i]!=n[k]: k=nxt[k-1]\n        if n[i]==n[k]: k+=1\n        nxt[i]=k\n    k=0\n    for i,ch in enumerate(h):\n        while k and ch!=n[k]: k=nxt[k-1]\n        if ch==n[k]: k+=1\n        if k==len(n): return i-k+1\n    return -1")

add("p113", "移除 K 位数字", "medium", "strings", ["单调栈", "字典序"],
    "删除 k 位使剩余数字最小。",
    "结果去掉前导零；可为空返回 0。",
    ["1 <= len(num) <= 10^4", "num 无前导零"],
    [{"input": "num='1432219', k=3", "output": "1219"}],
    "单调栈：栈顶大于新字符则弹出，直到删满；不足再删尾部。",
    "时间 O(n)，空间 O(n)。",
    ["不是求最长上升子序列。", "不足 k 删尾部。", "去前导零。"],
    "def remove_kdigits(num,k):\n    st=[]\n    for ch in num:\n        while st and k and st[-1]>ch: st.pop(); k-=1\n        st.append(ch)\n    while k: st.pop(); k-=1\n    return ''.join(st).lstrip('0') or '0'")

add("p114", "验证外星语词典", "easy", "strings", ["排序", "自定义顺序"],
    "按自定义字母序判断单词数组有序。",
    "字符可能不是常规字母顺序。",
    ["1 <= len(words) <= 100"],
    [{"input": "words=['hello','leetcode'], order='hlabcdefgijkmnopqrstuvwxyz'", "output": "true"}],
    "两两比较：前一单词必须是后一单词前缀或按字典序更小。",
    "时间 O(total chars)，空间 O(alphabet)。",
    ["前缀长单词在前应 false。", "自定义 rank 映射。", "逐字符比较不排序全表。"],
    "def is_alien_sorted(words,order):\n    rank={ch:i for i,ch in enumerate(order)}\n    def le(a,b):\n        for x,y in zip(a,b):\n            if rank[x]<rank[y]: return True\n            if rank[x]>rank[y]: return False\n        return len(a)<=len(b)\n    return all(le(words[i],words[i+1]) for i in range(len(words)-1))")

# Union-find/advanced: 4
add("p115", "省份数量", "medium", "union-find-advanced", ["并查集", "图"],
    " isConnected 表示城市直接相连，求省份数。",
    "矩阵对称。",
    ["1 <= n <= 200"],
    [{"input": "isConnected=[[1,1,0],[1,1,0],[0,0,1]]", "output": "2"}],
    "并查集合并相连城市；最终统计根数。",
    "时间 O(n^2 α(n))，空间 O(n)。",
    ["只扫上三角即可。", "合并后 count 要递减。", "自环忽略。"],
    "def find_circle_num(m):\n    n=len(m); p=list(range(n)); size=[1]*n\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    ans=n\n    for i in range(n):\n        for j in range(i+1,n):\n            if m[i][j]==1:\n                a,b=find(i),find(j)\n                if a!=b:\n                    if size[a]<size[b]: a,b=b,a\n                    p[b]=a; size[a]+=size[b]; ans-=1\n    return ans")

add("p116", "岛屿数量 II", "hard", "union-find-advanced", ["并查集", "动态网格"],
    "逐步添加陆地，返回每次添加后的岛屿数。",
    "坐标可能重复添加。",
    ["1 <= m,n <= 3*10^4", "positions.length <= 10^4"],
    [{"input": "m=3,n=3, positions=[[0,0],[0,1],[1,2],[2,1]]", "output": "[1,1,2,3]"}],
    "每添加新格建立集合，检查四邻合并并更新计数。",
    "时间 O(k α(mn))，空间 O(mn)。",
    ["重复添加不增加数量。", "邻居必须已在岛屿集合。", "1D 编码要防越界。"],
    "def num_islands2(m,n,pos):\n    p={}; dirs=((1,0),(-1,0),(0,1),(0,-1)); ans=[]; count=0\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    def add(x,y):\n        nonlocal count\n        key=(x,y)\n        if key in p: ans.append(count); return\n        p[key]=key; count+=1\n        for di,dj in dirs:\n            nb=(x+di,y+dj)\n            if nb in p:\n                ra,rb=find(key),find(nb)\n                if ra!=rb: p[ra]=rb; count-=1\n        ans.append(count)\n    for x,y in pos: add(x,y)\n    return ans")

add("p117", "账户合并", "medium", "union-find-advanced", ["并查集", "哈希表"],
    "合并同邮箱账户。",
    "同一账户内邮箱本身属于同一人。",
    ["1 <= accounts.length <= 1000"],
    [{"input": "accounts=[['John','a@x','b@x'],['John','c@x'],['John','a@x','c@x']]", "output": "两个 John 账户合并"}],
    "邮箱编号并查集；同账户邮箱合并，最后按根聚合并排序。",
    "时间 O(N log N)，空间 O(N)。",
    ["邮箱字符串映射唯一编号。", "同名不同人不能按名字合并。", "输出邮箱排序且名字保留。"],
    "from collections import defaultdict\ndef accounts_merge(accounts):\n    email_id={}; emails=[]\n    for acc in accounts:\n        for e in acc[1:]:\n            if e not in email_id: email_id[e]=len(emails); emails.append(e)\n    p=list(range(len(emails)))\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    def union(a,b):\n        ra,rb=find(a),find(b)\n        if ra!=rb: p[ra]=rb\n    for acc in accounts:\n        ids=[email_id[e] for e in acc[1:]]\n        for x in ids[1:]: union(ids[0],x)\n    groups=defaultdict(set)\n    for e,i in email_id.items(): groups[find(i)].add(e)\n    owner={email_id[acc[1]]:acc[0] for acc in accounts}\n    return [[owner[root]]+sorted(emails) for root,emails in groups.items()]")

add("p118", "等式方程的可满足性", "medium", "union-find-advanced", ["并查集", "约束"],
    "判断所有等式约束是否可能同时成立。",
    "变量为小写字母，== 表示相等，!= 表示不等。",
    ["1 <= equations.length <= 500"],
    [{"input": "['a==b','b!=a']", "output": "false"}],
    "先合并所有 ==；再检查每个 != 两端是否同根。",
    "时间 O(n α(26))，空间 O(26)。",
    ["必须先处理等式。", "!= 同根则矛盾。", "只有 26 个变量可固定数组。"],
    "def equations_possible(equations):\n    p=list(range(26))\n    def find(x):\n        while p[x]!=x: p[x]=p[p[x]]; x=p[x]\n        return x\n    for eq in equations:\n        if eq[1]=='=':\n            a,b=find(ord(eq[0])-97),find(ord(eq[3])-97)\n            if a!=b: p[a]=b\n    for eq in equations:\n        if eq[1]=='!' and find(ord(eq[0])-97)==find(ord(eq[3])-97): return False\n    return True")

# Math / bit / probability: 4
add("p119", "只出现一次的数字", "easy", "math-bit-probability", ["位运算", "异或"],
    "其他数出现两次，唯一数出现一次。",
    "要求常数空间。",
    ["1 <= len(nums) <= 3*10^4"],
    [{"input": "[4,1,2,1,2]", "output": "4"}],
    "异或所有数；成对抵消。",
    "时间 O(n)，空间 O(1)。",
    ["不能用哈希则空间不符合。", "0 初值正确。", "负数异或仍适用。"],
    "def single_number(nums):\n    ans=0\n    for x in nums: ans^=x\n    return ans")

add("p120", "比特位计数", "easy", "math-bit-probability", ["DP", "位运算"],
    "返回 0..num 每个数的二进制 1 个数。",
    "要求 O(n)。",
    ["0 <= num <= 10^5"],
    [{"input": "num=5", "output": "[0,1,1,2,1,2]"}],
    "dp[i]=dp[i>>1]+(i&1)，或 dp[i]=dp[i&(i-1)]+1。",
    "时间 O(n)，空间 O(n)。",
    ["dp[0]=0。", "右移不是减 1。", "奇偶分支可合并。"],
    "def count_bits(num):\n    dp=[0]*(num+1)\n    for i in range(1,num+1): dp[i]=dp[i>>1]+(i&1)\n    return dp")

add("p121", "缺失数字", "easy", "math-bit-probability", ["数学", "位运算"],
    "求 0..n 中缺失的数。",
    "数组长度 n 且升序或可乱序。",
    ["1 <= len(nums) <= 10^4"],
    [{"input": "[3,0,1]", "output": "2"}],
    "异或下标与值，或求总差值。",
    "时间 O(n)，空间 O(1)。",
    ["范围是 0..n。", "缺失可能是 n。", "不要排序增加复杂度。"],
    "def missing_number(nums):\n    ans=len(nums)\n    for i,x in enumerate(nums): ans^=i^x\n    return ans")

add("p122", "打乱数组", "medium", "math-bit-probability", ["随机化", "设计"],
    "支持 reset 和等概率 shuffle。",
    "每个排列概率相同。",
    ["1 <= nums.length <= 200"],
    [{"input": "[1,2,3]", "output": "所有 6 种排列概率 1/6"}],
    "Fisher-Yates：从后往前，i 与 [0,i] 随机交换。",
    "shuffle O(n)，reset O(1)。",
    ["范围不能是 [0,n-1]。", "保留原始数组。", "不要用 sort(random key)。"],
    "import random\nclass ShuffleArray:\n    def __init__(self,nums): self.original=nums[:]; self.a=nums[:]\n    def reset(self): self.a=self.original[:]; return self.a\n    def shuffle(self):\n        for i in range(len(self.a)-1,0,-1):\n            j=random.randint(0,i); self.a[i],self.a[j]=self.a[j],self.a[i]\n        return self.a")

# Engineering: 2
add("p123", "设计有限阻塞队列", "medium", "engineering-interview", ["并发", "设计"],
    "实现容量有限的 FIFO 队列。",
    "push 满时阻塞，pop 空时阻塞；也可提供超时。",
    ["1 <= capacity <= 1000", "多消费者安全"],
    [{"input": "capacity=2，生产/消费交错", "output": "不丢失、不越界"}],
    "锁保护状态；两个条件变量分别等待非满/非空。",
    "push/pop 均摊 O(1)，空间 O(capacity)。",
    ["条件变量必须用 while 防惊群和虚假唤醒。", "锁粒度要覆盖状态修改。", "关闭状态要定义。"],
    "import threading\nclass BoundedQueue:\n    def __init__(self,cap):\n        self.cap=cap; self.items=[]; self.lock=threading.Lock(); self.not_full=threading.Condition(self.lock); self.not_empty=threading.Condition(self.lock)\n    def put(self,x):\n        with self.not_full:\n            while len(self.items)==self.cap: self.not_full.wait()\n            self.items.append(x); self.not_empty.notify()\n    def get(self):\n        with self.not_empty:\n            while not self.items: self.not_empty.wait()\n            x=self.items.pop(0); self.not_full.notify(); return x")

add("p124", "设计公平调度器", "hard", "engineering-interview", ["系统设计", "调度"],
    "按任务优先级和用户公平性调度。",
    "同优先级下不能让一个用户长期占满；deadline 先于 priority。",
    ["任务量 <= 10^5", "并发读写需要考虑"],
    [{"input": "用户 A 1000 个任务，用户 B 10 个任务", "output": "B 不会饿死"}],
    "按 deadline 放堆；同 deadline 用用户配额轮转；记录每用户最近调度比例。",
    "插入 O(log n)，调度 O(log n)。",
    ["公平不等于完全轮询。", "系统时间回拨要处理。", "任务取消需要惰性删除。"],
    "import heapq,time\nclass FairScheduler:\n    def __init__(self): self.heap=[]; self.seq=0; self.usage={}\n    def submit(self,task,deadline,user,base_priority):\n        self.seq+=1\n        fairness=self.usage.get(user,0)*0.001\n        heapq.heappush(self.heap,(deadline,base_priority+fairness,self.seq,user,task))\n    def next_task(self):\n        if not self.heap: return None\n        deadline,priority,seq,user,task=heapq.heappop(self.heap)\n        self.usage[user]=self.usage.get(user,0)+1\n        return task")


def validate(problems):
    ids = [p["id"] for p in problems]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate problem id")
    if len(problems) != 124:
        raise ValueError(f"expected 124 problems, got {len(problems)}")
    for p in problems:
        if p["chapter"] not in CHAPTER_IDS:
            raise ValueError(f"invalid chapter reference {p['chapter']} in {p['id']}")
        if p["difficulty"] not in {"easy", "medium", "hard"}:
            raise ValueError(f"invalid difficulty in {p['id']}")
        if not p["constraints"] or not p["examples"] or len(p["solution"]["pitfalls"]) < 3:
            raise ValueError(f"incomplete problem {p['id']}")
        languages = [item["language"] for item in p["solution"]["code"]]
        if set(languages) != {"Python", "Java"}:
            raise ValueError(f"expected Python and Java in {p['id']}, got {languages}")


def main():
    for problem in P:
        problem_id = problem["id"]
        if problem_id not in JAVA_SOLUTIONS:
            raise ValueError(f"missing Java solution: {problem_id}")
        problem["solution"]["code"].append({"language": "Java", "source": JAVA_SOLUTIONS[problem_id]})
        if problem_id in TEACHING_NOTES:
            problem["solution"]["understanding"] = TEACHING_NOTES[problem_id]

    validate(P)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(P, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {}
    for p in P: counts[p["chapter"]] = counts.get(p["chapter"], 0) + 1
    print(f"generated {len(P)} problems")
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
