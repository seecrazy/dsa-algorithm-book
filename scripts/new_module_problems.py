# -*- coding: utf-8 -*-
"""Dedicated problems for the six supplementary modules."""

NEW_PROBLEMS = []
NEW_JAVA = {}

def add(pid, title, difficulty, chapter, tags, summary, prompt, constraints,
        examples, idea, complexity, pitfalls, code):
    NEW_PROBLEMS.append({
        "id": pid, "title": title, "difficulty": difficulty,
        "tags": tags, "chapter": chapter, "summary": summary,
        "prompt": prompt, "constraints": constraints,
        "examples": examples,
        "solution": {
            "idea": idea, "complexity": complexity,
            "pitfalls": pitfalls, "code": [{"language": "Python", "source": code}],
        },
    })

def java(pid, source):
    NEW_JAVA[pid] = source

# sorting
add("p125", "颜色分类", "medium", "sorting", ["数组", "三路分区", "原地排序"],
    "只含 0/1/2 的数组按颜色原地排序。",
    "给定只包含 0、1、2 的数组，原地排序，使相同颜色相邻。",
    ["1 <= len(nums) <= 300", "必须使用常数空间", "尽量只遍历一次"],
    [{"input": "[2,0,2,1,1,0]", "output": "[0,0,1,1,2,2]"}],
    "维护 zero 之前的边界和 two 之后的边界；遇 0 与 left 交换，遇 2 与 right 交换。",
    "时间 O(n)，空间 O(1)，一次遍历。",
    ["遇 2 交换后 i 不能前进，因为换来的数还未处理。", "left <= right 的条件不能写成 <。", "不要使用计数排序破坏一次遍历约束。"],
    "def sort_colors(nums):\n    left=i=0; right=len(nums)-1\n    while i<=right:\n        if nums[i]==0:\n            nums[i],nums[left]=nums[left],nums[i]; left+=1; i+=1\n        elif nums[i]==2:\n            nums[i],nums[right]=nums[right],nums[i]; right-=1\n        else: i+=1\n    return nums")
java("p125", "class Solution {\n    public void sortColors(int[] nums) {\n        int left = 0, i = 0, right = nums.length - 1;\n        while (i <= right) {\n            if (nums[i] == 0) { int t = nums[i]; nums[i++] = nums[left]; nums[left++] = t; }\n            else if (nums[i] == 2) { int t = nums[i]; nums[i] = nums[right]; nums[right--] = t; }\n            else i++;\n        }\n    }\n}")

add("p126", "数组中的逆序对", "hard", "sorting", ["归并排序", "分治", "计数"],
    "统计满足 i<j 且 nums[i]>nums[j] 的下标对数量。",
    "给定数组，返回逆序对数量。结果可能很大，对 1e9+7 取模。",
    ["1 <= len(nums) <= 5*10^4", "-10^5 <= nums[i] <= 10^5"],
    [{"input": "[7,5,6,4]", "output": "5", "explanation": "(7,5),(7,6),(7,4),(5,4),(6,4)"}],
    "归并排序时，当右半元素被取出，剩余左半元素都与它构成逆序对；批量累加。",
    "时间 O(n log n)，空间 O(n)。",
    ["相等元素不是逆序对。", "必须在合并时计数，排序完成后原顺序信息丢失。", "计数要用 long，避免溢出。"],
    "def count_inversions(nums):\n    MOD=10**9+7; a=list(nums)\n    def sort(l,r):\n        if l>=r: return 0\n        m=(l+r)//2; ans=sort(l,m)+sort(m+1,r); tmp=[]; i,j=l,m+1\n        while i<=m and j<=r:\n            if a[i]<=a[j]: tmp.append(a[i]); i+=1\n            else: ans+=m-i+1; tmp.append(a[j]); j+=1\n        tmp.extend(a[i:m+1] or a[j:r+1]); a[l:r+1]=tmp; return ans%MOD\n    return sort(0,len(a)-1)")
java("p126", "class Solution {\n    private int[] temp;\n    public int countInversions(int[] nums) {\n        temp = new int[nums.length];\n        return (int) (merge(nums, 0, nums.length - 1) % 1_000_000_007L);\n    }\n    private long merge(int[] a, int l, int r) {\n        if (l >= r) return 0;\n        int m = (l + r) / 2, i = l, j = m + 1, k = l;\n        long ans = merge(a, l, m) + merge(a, m + 1, r);\n        while (i <= m && j <= r) {\n            if (a[i] <= a[j]) temp[k++] = a[i++];\n            else { ans += m - i + 1; temp[k++] = a[j++]; }\n        }\n        while (i <= m) temp[k++] = a[i++];\n        while (j <= r) temp[k++] = a[j++];\n        System.arraycopy(temp, l, a, l, r - l + 1);\n        return ans;\n    }\n}")

add("p127", "无序数组的最大间距", "medium", "sorting", ["桶排序", "鸽巢原理"],
    "排序后相邻元素最大差值，要求线性时间。",
    "给定非负整数数组，返回排序后相邻元素最大差；少于两个数返回 0。",
    ["1 <= len(nums) <= 10^5", "0 <= nums[i] <= 10^9", "期望 O(n)"],
    [{"input": "[3,6,9,1]", "output": "3"}, {"input": "[10]", "output": "0"}],
    "n 个数排序后有 n-1 个间隙，而值域被 n-1 个桶覆盖时，最大间距一定不小于桶宽，因此答案只会出现在桶间最小值与前一桶最大值之间。",
    "时间 O(n)，空间 O(n)。",
    ["桶宽要 max(1, ...)，避免除零。", "空桶必须跳过，不能当值 0。", "少于 2 个元素直接返回 0。"],
    "def maximum_gap(nums):\n    if len(nums)<2: return 0\n    lo,hi,n=min(nums),max(nums),len(nums)\n    if lo==hi: return 0\n    size=max(1,(hi-lo)//(n-1)); count=(hi-lo)//size+1\n    buckets=[[None,None] for _ in range(count)]\n    for x in nums:\n        i=(x-lo)//size\n        buckets[i][0]=x if buckets[i][0] is None else min(buckets[i][0],x)\n        buckets[i][1]=x if buckets[i][1] is None else max(buckets[i][1],x)\n    ans=0; prev=lo\n    for mn,mx in buckets:\n        if mn is None: continue\n        ans=max(ans,mn-prev); prev=mx\n    return ans")
java("p127", "class Solution {\n    public int maximumGap(int[] nums) {\n        if (nums.length < 2) return 0;\n        int lo = Integer.MAX_VALUE, hi = Integer.MIN_VALUE;\n        for (int x : nums) { lo = Math.min(lo, x); hi = Math.max(hi, x); }\n        if (lo == hi) return 0;\n        int n = nums.length, size = Math.max(1, (hi - lo) / (n - 1)), count = (hi - lo) / size + 1;\n        int[][] buckets = new int[count][2];\n        for (int[] b : buckets) { b[0] = Integer.MAX_VALUE; b[1] = Integer.MIN_VALUE; }\n        for (int x : nums) {\n            int i = (x - lo) / size;\n            buckets[i][0] = Math.min(buckets[i][0], x);\n            buckets[i][1] = Math.max(buckets[i][1], x);\n        }\n        int ans = 0, prev = lo;\n        for (int[] b : buckets) {\n            if (b[0] == Integer.MAX_VALUE) continue;\n            ans = Math.max(ans, b[0] - prev); prev = b[1];\n        }\n        return ans;\n    }\n}")

add("p128", "相对排序", "medium", "sorting", ["计数排序", "稳定排序", "自定义顺序"],
    "按 arr2 的顺序排 arr1，剩余元素升序放后。",
    "arr1 和 arr2 都无重复，但 arr1 可有重复；arr2 中的元素按 arr2 顺序排，不在 arr2 的按升序排在末尾。",
    ["1 <= len(arr1),len(arr2) <= 1000", "0 <= value <= 1000", "arr2 无重复"],
    [{"input": "arr1=[2,3,1,3,2,4,6,7,5,5], arr2=[2,1,4,3,9,6]", "output": "[2,2,1,4,3,3,5,5,6,7]"}],
    "计数 arr1；先按 arr2 顺序输出；剩余值升序补尾。",
    "时间 O(n+m+r)，空间 O(r)。",
    ["剩余元素不能按输入顺序，必须升序。", "arr2 长度小于值域，不能用单层数组直接假定全覆盖。", "计数清零后再补尾，避免重复输出。"],
    "from collections import Counter\ndef relative_sort(arr1,arr2):\n    c=Counter(arr1); out=[]\n    for x in arr2:\n        out.extend([x]*c[x]); del c[x]\n    for x in sorted(c):\n        out.extend([x]*c[x])\n    return out")
java("p128", "class Solution {\n    public int[] relativeSortArray(int[] arr1, int[] arr2) {\n        int[] count = new int[1001];\n        for (int x : arr1) count[x]++;\n        int[] ans = new int[arr1.length]; int k = 0;\n        for (int x : arr2) while (count[x]-- > 0) ans[k++] = x;\n        for (int x = 0; x <= 1000; x++) while (count[x]-- > 0) ans[k++] = x;\n        return ans;\n    }\n}")

add("p129", "最大拼接数", "medium", "sorting", ["比较器", "字典序", "贪心"],
    "非负整数数组拼接出最大数字字符串。",
    "给定非负整数数组，重排后拼接成最大数；结果可能极大，返回字符串。全零时返回 \"0\"。",
    ["1 <= len(nums) <= 100", "0 <= nums[i] <= 10^9"],
    [{"input": "[10,2]", "output": "210"}, {"input": "[3,30,34,5,9]", "output": "9534330"}],
    "比较器定义 ab 与 ba 的字典序；ba 更大则 b 在前。全零要压缩为 \"0\"。",
    "排序 O(n log n)，拼接 O(n)，空间 O(n)。",
    ["不能用整数大小直接比较，长度影响字典序结果。", "不能保留多个 \"0\"。", "比较器必须覆盖任意前缀关系，如 3 和 30。"],
    "from functools import cmp_to_key\ndef largest_number(nums):\n    ss=list(map(str,nums))\n    ss.sort(key=cmp_to_key(lambda a,b:-1 if a+b>b+a else 1))\n    ans=''.join(ss)\n    return '0' if ans[0]=='0' else ans")
java("p129", "import java.util.*;\nclass Solution {\n    public String largestNumber(int[] nums) {\n        String[] a = Arrays.stream(nums).mapToObj(String::valueOf).toArray(String[]::new);\n        Arrays.sort(a, (x,y) -> (y+x).compareTo(x+y));\n        if (a[0].equals(\"0\")) return \"0\";\n        return String.join(\"\", a);\n    }\n}")

# trie
add("p130", "实现 Trie", "medium", "trie", ["Trie", "设计", "前缀"],
    "实现插入、完整词查询和前缀查询。",
    "实现 Trie 类，支持 insert(word)、search(word)、startsWith(prefix)。所有输入只含小写字母。",
    ["调用次数 <= 3*10^4", "1 <= word.length <= 20"],
    [{"input": "insert('apple'),search('apple'),search('app'),startsWith('app')", "output": "true,false,true"}],
    "每个节点保存子节点映射和 is_end；插入时逐字符建立边，查询时同步走路径。",
    "每个操作 O(L)，空间 O(总字符数)。",
    ["search('app') 与 startsWith('app') 不同。", "插入相同前缀时不要覆盖子节点。", "完整词必须在 is_end 标记。"],
    "class Trie:\n    def __init__(self): self.root={}\n    def insert(self,word):\n        node=self.root\n        for ch in word: node=node.setdefault(ch,{})\n        node['#']=True\n    def search(self,word):\n        node=self._find(word); return bool(node and node.get('#'))\n    def starts_with(self,prefix): return bool(self._find(prefix))\n    def _find(self,s):\n        node=self.root\n        for ch in s:\n            if ch not in node:return None\n            node=node[ch]\n        return node")
java("p130", "class Trie {\n    private Trie[] children = new Trie[26]; private boolean end;\n    public void insert(String word) {\n        Trie node=this; for(char c:word.toCharArray()){int i=c-'a'; if(node.children[i]==null) node.children[i]=new Trie(); node=node.children[i];} node.end=true;\n    }\n    private Trie find(String s){Trie node=this;for(char c:s.toCharArray()){node=node.children[c-'a'];if(node==null)return null;}return node;}\n    public boolean search(String word){Trie n=find(word);return n!=null&&n.end;}\n    public boolean startsWith(String prefix){return find(prefix)!=null;}\n}")

add("p131", "添加与搜索单词", "medium", "trie", ["Trie", "DFS", "通配符"],
    "支持小写字母和通配符 '.' 的单词检索。",
    "实现 WordDictionary，addWord 添加单词；search 中 '.' 可匹配任意一个字母。",
    ["1 <= word.length <= 25", "addWord 只含小写字母；search 可含 '.'"],
    [{"input": "addWord('bad'),search('b..')", "output": "true"}],
    "建 Trie；遇到 '.' 递归所有子节点，否则沿字符边走。",
    "addWord O(L)；最坏 search O(26L)。",
    ["'.' 不代表零个或多个字符，只匹配一个。", "递归到词尾必须检查 is_end。", "空子树要及时剪枝。"],
    "class WordDictionary:\n    def __init__(self): self.root={}\n    def add_word(self,word):\n        node=self.root\n        for ch in word: node=node.setdefault(ch,{})\n        node['#']=True\n    def search(self,word): return self._dfs(word,0,self.root)\n    def _dfs(self,word,i,node):\n        if i==len(word): return '#' in node\n        ch=word[i]\n        if ch!='.': return ch in node and self._dfs(word,i+1,node[ch])\n        return any(self._dfs(word,i+1,node[c]) for c in node if c!='#')")
java("p131", "class WordDictionary {\n    private WordDictionary[] children=new WordDictionary[26]; private boolean end;\n    public void addWord(String word){WordDictionary node=this;for(char c:word.toCharArray()){int i=c-'a';if(node.children[i]==null)node.children[i]=new WordDictionary();node=node.children[i];}node.end=true;}\n    public boolean search(String word){return dfs(word,0,this);}\n    private boolean dfs(String word,int i,WordDictionary node){\n        if(i==word.length())return node.end;\n        char c=word.charAt(i);\n        if(c!='.') return node.children[c-'a']!=null&&dfs(word,i+1,node.children[c-'a']);\n        for(WordDictionary child:node.children) if(child!=null&&dfs(word,i+1,child)) return true;\n        return false;\n    }\n}")

add("p132", "单词搜索 II", "hard", "trie", ["Trie", "回溯", "网格"],
    "在二维网格中找出所有能由相邻单元格组成的单词。",
    "给定 board 和 words，返回所有出现在网格中的单词。同一单元格一次路径中不能重复使用。",
    ["1 <= m,n <= 12", "1 <= words.length <= 3*10^4", "字符均为小写"],
    [{"input": "board=[['o','x'],['a','t'],['x','h']], words=['oa','oath']", "output": "['oa','oath']"}],
    "把 words 建 Trie，网格 DFS 同时走 Trie；匹配到 is_end 加入答案，并逐步剪掉无子节点的分支。",
    "时间 O(mn*4*3^(L-1))，空间 O(总字符数)。",
    ["不要对每个单词单独 DFS。", "访问标记必须恢复。", "找到单词后可置 is_end=false 防重复。"],
    "def find_words(board,words):\n    root={}\n    for w in words:\n        node=root\n        for ch in w: node=node.setdefault(ch,{});\n        node['#']=w\n    ans=set(); m,n=len(board),len(board[0])\n    def dfs(i,j,node):\n        ch=board[i][j]\n        if ch not in node:return\n        node=node[ch]\n        if '#' in node: ans.add(node['#'])\n        board[i][j]='#'\n        for a,b in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):\n            if 0<=a<m and 0<=b<n: dfs(a,b,node)\n        board[i][j]=ch\n    for i in range(m):\n        for j in range(n): dfs(i,j,root)\n    return sorted(ans)")
java("p132", "import java.util.*;\nclass Solution {\n    public List<String> findWords(char[][] board, String[] words) {\n        TrieNode root=new TrieNode(); for(String w:words){TrieNode node=root;for(char c:w.toCharArray()){int i=c-'a';if(node.children[i]==null)node.children[i]=new TrieNode();node=node.children[i];}node.word=w;}\n        Set<String> ans=new HashSet<>(); int m=board.length,n=board[0].length;\n        for(int i=0;i<m;i++)for(int j=0;j<n;j++) dfs(board,i,j,root,ans);\n        return new ArrayList<>(ans);\n    }\n    private void dfs(char[][] b,int i,int j,TrieNode node,Set<String> ans){\n        char c=b[i][j]; TrieNode next=node.children[c-'a']; if(next==null)return;\n        if(next.word!=null){ans.add(next.word);next.word=null;}\n        b[i][j]='#'; int[][] d={{1,0},{-1,0},{0,1},{0,-1}};\n        for(int[] p:d){int a=i+p[0],k=j+p[1];if(a>=0&&a<b.length&&k>=0&&k<b[0].length&&b[a][k]!='#')dfs(b,a,k,next,ans);}\n        b[i][j]=c;\n    }\n    class TrieNode{String word;TrieNode[] children=new TrieNode[26];}\n}")

add("p133", "单词替换", "medium", "trie", ["Trie", "字符串", "前缀"],
    "句子中每个词替换成其最短词根。",
    "给定 dictionary roots 和 sentence，用最早匹配且最短词根替换单词；没有词根保留原词。",
    ["1 <= dictionary.length <= 1000", "1 <= sentence word count <= 1000", "字符小写"],
    [{"input": "dictionary=['cat','bat','rat'], sentence='the cattle was rattled by the battery'", "output": "'the cat was rat by the bat'"}],
    "建 Trie；对每个单词沿根向下找第一个 is_end，找到即替换。",
    "建 Trie O(总根长)；替换 O(总句长)。",
    ["优先最短根，不是字典序。", "词必须完整匹配词根，不要把 cat 匹配成 ca。", "标点和空格按题意分隔。"],
    "class Solution:\n    def replace_words(self,dictionary,sentence):\n        root={}\n        for word in dictionary:\n            node=root\n            for ch in word: node=node.setdefault(ch,{})\n            node['#']=True\n        def replace(word):\n            node=root\n            for i,ch in enumerate(word):\n                if ch not in node:return word\n                node=node[ch]\n                if '#' in node:return word[:i+1]\n            return word\n        return ' '.join(replace(w) for w in sentence.split())")
java("p133", "class Solution {\n    private Trie root=new Trie();\n    class Trie{Trie[] children=new Trie[26];boolean end;}\n    public String replaceWords(java.util.List<String> dictionary,String sentence){\n        for(String w:dictionary){Trie node=root;for(char c:w.toCharArray()){int i=c-'a';if(node.children[i]==null)node.children[i]=new Trie();node=node.children[i];}node.end=true;}\n        StringBuilder sb=new StringBuilder();\n        for(String w:sentence.split(\" \")){if(sb.length()>0)sb.append(' ');sb.append(replace(w));}\n        return sb.toString();\n    }\n    private String replace(String w){Trie node=root;\n        for(int i=0;i<w.length();i++){int c=w.charAt(i)-'a';if(node.children[c]==null)return w;node=node.children[c];if(node.end)return w.substring(0,i+1);}return w;\n    }\n}")

add("p134", "数组中两个数的最大异或值", "medium", "trie", ["位运算", "二进制 Trie", "贪心"],
    "求数组中任意两数的最大异或值。",
    "给定非负整数数组，返回任意两个元素的最大异或值。",
    ["1 <= len(nums) <= 2*10^4", "0 <= nums[i] <= 2^31-1"],
    [{"input": "[3,10,5,25,2,8]", "output": "28", "explanation": "5 ^ 25 = 28"}],
    "按高位建二进制 Trie；对每个数 x 优先选择相反位的已有数，使当前位异或为 1。",
    "时间 O(n*32)，空间 O(n*32)。",
    ["必须从最高位到最低位贪心。", "要注意允许和自己配对吗？本题需要两个不同下标，实现时应先插入 x 再查询，或查询时排除自身。", "负数按题意转换，不要直接用 Python 右移负数。"],
    "def find_maximum_xor(nums):\n    root={}; ans=0\n    def insert(x):\n        node=root\n        for i in range(31,-1,-1):\n            b=(x>>i)&1; node=node.setdefault(b,{})\n    def query(x):\n        node=root; ans=0\n        for i in range(31,-1,-1):\n            b=(x>>i)&1\n            if 1-b in node: ans|=1<<i; node=node[1-b]\n            else: node=node[b]\n        return ans\n    for x in nums:\n        if root: ans=max(ans,query(x))\n        insert(x)\n    return ans")
java("p134", "class Solution {\n    class Node{Node[] children=new Node[2];}\n    public int findMaximumXOR(int[] nums){Node root=new Node();int ans=0;\n        for(int x:nums){if(root.children[0]!=null||root.children[1]!=null)ans=Math.max(ans,query(root,x));insert(root,x);}return ans;}\n    private void insert(Node root,int x){Node node=root;for(int i=31;i>=0;i--){int b=(x>>i)&1;if(node.children[b]==null)node.children[b]=new Node();node=node.children[b];}}\n    private int query(Node root,int x){Node node=root;int ans=0;for(int i=31;i>=0;i--){int b=(x>>i)&1;int want=1-b;if(node.children[want]!=null){ans|=1<<i;node=node.children[want];}else node=node.children[b];}return ans;}\n}")

# balanced-search-trees
add("p135", "有序数组转平衡 BST", "easy", "balanced-search-trees", ["BST", "平衡树", "分治"],
    "把升序数组转换成高度平衡 BST。",
    "给定升序数组，返回任一高度平衡 BST 的根节点。",
    ["1 <= len(nums) <= 10^4", "元素互异"],
    [{"input": "[-10,-3,0,5,9]", "output": "[0,-3,9,-10,null,5]"}],
    "取中点作根，左半递归建左子树，右半递归建右子树。",
    "时间 O(n)，空间 O(log n)。",
    ["不要逐个插入，复杂度更高。", "mid 向下取整，左右区间不要重叠。", "空数组按题意处理。"],
    "def sorted_array_to_bst(nums):\n    def build(l,r):\n        if l>r:return None\n        mid=(l+r)//2; root=TreeNode(nums[mid])\n        root.left=build(l,mid-1); root.right=build(mid+1,r)\n        return root\n    return build(0,len(nums)-1)")
java("p135", "class Solution {\n    public TreeNode sortedArrayToBST(int[] nums){return build(nums,0,nums.length-1);}\n    private TreeNode build(int[] a,int l,int r){if(l>r)return null;int m=(l+r)/2;TreeNode root=new TreeNode(a[m]);root.left=build(a,l,m-1);root.right=build(a,m+1,r);return root;}\n}")

add("p136", "我的日程安排 I", "medium", "balanced-search-trees", ["有序容器", "区间冲突", "平衡树"],
    "动态插入不重叠日程，判断能否预订。",
    "实现 MyCalendar.book(start,end)：若新开区间与已有闭开区间不重叠则插入并返回 true，否则 false。",
    ["0 <= start < end <= 10^9", "调用次数 <= 1000"],
    [{"input": "book(10,20),book(15,25),book(20,30)", "output": "true,false,true"}],
    "维护按 start 有序映射；新区间只需检查前驱的 end 和后继的 start。",
    "每次 O(log n)，空间 O(n)。",
    ["端点相等视为不重叠：prev.end <= start 且 next.start >= end。", "只查相邻区间即可，无需全扫。", "先判断再插入。"],
    "from bisect import bisect_right,insort\nclass MyCalendar:\n    def __init__(self): self.starts=[]; self.ends=[]\n    def book(self,start,end):\n        i=bisect_right(self.starts,start)\n        if i and self.ends[i-1]>start:return False\n        if i<len(self.starts) and self.starts[i]<end:return False\n        self.starts.insert(i,start); self.ends.insert(i,end); return True")
java("p136", "import java.util.*;\nclass MyCalendar {\n    private TreeMap<Integer,Integer> events=new TreeMap<>();\n    public boolean book(int start,int end){\n        Map.Entry<Integer,Integer> prev=events.floorEntry(start), next=events.ceilingEntry(start);\n        if(prev!=null&&prev.getValue()>start)return false;\n        if(next!=null&&next.getKey()<end)return false;\n        events.put(start,end);return true;\n    }\n}")

add("p137", "右侧小于当前元素的个数", "hard", "balanced-search-trees", ["有序结构", "BIT", "计数"],
    "统计每个元素右侧严格小于它的元素数量。",
    "给定数组，返回 counts[i] = 右侧小于 nums[i] 的元素个数。",
    ["1 <= len(nums) <= 10^5", "-10^6 <= nums[i] <= 10^6"],
    [{"input": "[5,2,6,1]", "output": "[2,1,1,0]"}],
    "离散化后从右向左遍历，BIT 统计已出现值；对 rank-1 做前缀和。",
    "时间 O(n log n)，空间 O(n)。",
    ["离散化必须去重排序。", "严格小于用 rank-1，而不是 rank。", "从右往左，先查询再插入。"],
    "def count_smaller(nums):\n    ranks={v:i+1 for i,v in enumerate(sorted(set(nums)))}; m=len(ranks); tree=[0]*(m+1); ans=[]\n    def update(i):\n        while i<=m: tree[i]+=1; i+=i&-i\n    def query(i):\n        s=0\n        while i>0: s+=tree[i]; i-=i&-i\n        return s\n    for x in reversed(nums):\n        r=ranks[x]; ans.append(query(r-1)); update(r)\n    return ans[::-1]")
java("p137", "class Solution {\n    private int[] tree;\n    public java.util.List<Integer> countSmaller(int[] nums){\n        int[] sorted=nums.clone();java.util.Arrays.sort(sorted);java.util.Map<Integer,Integer> rank=new java.util.HashMap<>();int m=0;\n        for(int x:sorted)if(!rank.containsKey(x))rank.put(x,++m);\n        tree=new int[m+1];java.util.List<Integer> ans=new java.util.ArrayList<>();\n        for(int i=nums.length-1;i>=0;i--){int r=rank.get(nums[i]);ans.add(query(r-1));update(r);}\n        java.util.Collections.reverse(ans);return ans;\n    }\n    private void update(int i){for(;i<tree.length;i+=i&-i)tree[i]++;}\n    private int query(int i){int s=0;for(;i>0;i-=i&-i)s+=tree[i];return s;}\n}")

add("p138", "区域和检索 - 数组可修改", "medium", "balanced-search-trees", ["BIT", "线段树", "动态更新"],
    "支持数组单点更新和区间和查询。",
    "实现 NumArray：初始化数组；update(index,val) 修改元素；sumRange(left,right) 返回闭区间和。",
    ["1 <= len(nums) <= 3*10^4", "调用次数 <= 3*10^4"],
    [{"input": "NumArray([1,3,5]),sumRange(0,2),update(1,2),sumRange(0,2)", "output": "9,8"}],
    "用 BIT 存差值；update 时先把旧值减掉再加新值；sumRange 是两个前缀和之差。",
    "update/sumRange O(log n)，空间 O(n)。",
    ["update 是赋值，不是增量。", "sumRange(left,right)=prefix(right+1)-prefix(left)。", "BIT 下标从 1 开始。"],
    "class NumArray:\n    def __init__(self,nums):\n        self.n=len(nums); self.tree=[0]*(self.n+1); self.nums=nums[:]\n        for i,x in enumerate(nums,1):\n            while i<=self.n:self.tree[i]+=x;i+=i&-i\n    def update(self,index,val):\n        delta=val-self.nums[index]; self.nums[index]=val; i=index+1\n        while i<=self.n:self.tree[i]+=delta;i+=i&-i\n    def prefix(self,i):\n        s=0\n        while i>0:s+=self.tree[i];i-=i&-i\n        return s\n    def sum_range(self,left,right):return self.prefix(right+1)-self.prefix(left)")
java("p138", "class NumArray {\n    private int[] nums; private long[] tree;\n    public NumArray(int[] values){nums=values.clone();tree=new long[values.length+1];for(int i=0;i<values.length;i++)for(int j=i+1;j<=values.length;j+=j&-j)tree[j]+=values[i];}\n    public void update(int index,int val){int delta=val-nums[index];nums[index]=val;for(int i=index+1;i<tree.length;i+=i&-i)tree[i]+=delta;}\n    private long prefix(int i){long s=0;for(;i>0;i-=i&-i)s+=tree[i];return s;}\n    public int sumRange(int left,int right){return (int)(prefix(right+1)-prefix(left));}\n}")

# b-trees
add("p139", "B+ 树节点分裂", "medium", "b-trees", ["B+树", "分裂", "索引"],
    "按最小度数分裂已满叶节点。",
    "给定已满节点 keys 和最小度数 t，按 B 树分裂规则返回 [leftKeys, separator, rightKeys]。中间键上移。",
    ["keys 长度 = 2*t - 1", "2 <= t <= 100", "keys 升序互异"],
    [{"input": "keys=[1,2,3,4,5], t=3", "output": "[[1,2],3,[4,5]]"}],
    "满节点有奇数个键，取中间键 separator = keys[t-1]；左侧和右侧各 t-1 个键。",
    "时间 O(k)，空间 O(k)。",
    ["separator 必须上移，不能留在子节点。", "不要按长度一半取中间，应按 t-1 取。", "左右键数量必须相等。"],
    "def split_leaf(keys,t):\n    mid=t-1\n    return keys[:mid],keys[mid],keys[mid+1:]")
java("p139", "import java.util.*;\nclass Solution {\n    public List<List<Integer>> splitLeaf(List<Integer> keys,int t){\n        int mid=t-1;\n        return List.of(new ArrayList<>(keys.subList(0,mid)),List.of(keys.get(mid)),new ArrayList<>(keys.subList(mid+1,keys.size())));\n    }\n}")

add("p140", "B+ 树范围查询", "medium", "b-trees", ["B+树", "范围扫描", "叶子链表"],
    "在有序叶页上完成范围扫描。",
    "给定 B+ 树叶子页列表 leaves，每页 keys 升序且页间 keys 全局升序；返回 [start,end] 中的键。",
    ["1 <= len(leaves) <= 1000", "总键数 <= 10^5", "start <= end"],
    [{"input": "leaves=[[1,3],[5,7],[9]], range=[3,8]", "output": "[3,5,7]"}],
    "二分定位第一个 >= start 的位置；从那里沿叶子页顺序扫描，直到键超过 end。",
    "定位 O(log n)，扫描 O(m)，空间 O(m)。",
    ["页内和页间都有序。", "超过 end 立即停止。", "空页要跳过。"],
    "from bisect import bisect_left\ndef btree_range(leaves,start,end):\n    ans=[]\n    for page in leaves:\n        if not page or page[-1]<start: continue\n        i=bisect_left(page,start)\n        while i<len(page) and page[i]<=end: ans.append(page[i]); i+=1\n        if page[-1]>end: break\n    return ans")
java("p140", "import java.util.*;\nclass Solution {\n    public List<Integer> rangeQuery(List<List<Integer>> leaves,int start,int end){\n        List<Integer> ans=new ArrayList<>();\n        for(List<Integer> page:leaves){\n            if(page.isEmpty()||page.get(page.size()-1)<start)continue;\n            for(int x:page){if(x>end)return ans;if(x>=start)ans.add(x);}\n            if(page.get(page.size()-1)>end)break;\n        }\n        return ans;\n    }\n}")

add("p141", "合并相邻索引页", "medium", "b-trees", ["B+树", "页合并", "贪心"],
    "把相邻小页合并到不超过容量，最少化总页数。",
    "给定有序页 pages 和容量 capacity，按顺序合并相邻页；一旦加入下一页会超过容量则新建页。返回合并后页列表。",
    ["1 <= len(pages) <= 1000", "1 <= capacity <= 10^9", "每页总和 <= capacity"],
    [{"input": "pages=[[1,2],[3],[4,5]], capacity=6", "output": "[[1,2,3],[4],[5]]", "explanation": "页是不可拆分的顺序单位。"}],
    "顺序扫描；当前页能容纳则合并，否则开启新页。",
    "时间 O(总键数)，空间 O(总键数)。",
    ["必须保持页顺序，不能全局贪心重排。", "页内元素保持原顺序。", "空页输入需按题意处理。"],
    "def merge_pages(pages,capacity):\n    ans=[]; cur=[]; total=0\n    for page in pages:\n        for x in page:\n            if total+x>capacity:\n                if cur:ans.append(cur)\n                cur=[];total=0\n            cur.append(x);total+=x\n    if cur:ans.append(cur)\n    return ans")
java("p141", "import java.util.*;\nclass Solution {\n    public List<List<Integer>> mergePages(List<List<Integer>> pages,int capacity){\n        List<List<Integer>> ans=new ArrayList<>();List<Integer> cur=new ArrayList<>();long total=0;\n        for(List<Integer> page:pages)for(int x:page){if(total+x>capacity){if(!cur.isEmpty())ans.add(cur);cur=new ArrayList<>();total=0;}cur.add(x);total+=x;}\n        if(!cur.isEmpty())ans.add(cur);return ans;\n    }\n}")

# branch-and-bound
add("p142", "0/1 背包：上界剪枝", "hard", "branch-and-bound", ["分支限界", "背包", "剪枝"],
    "用分支限界求 0/1 背包最大价值。",
    "给定 items[i]=[weight,value]，选物总重不超过 capacity，返回最大价值。",
    ["1 <= len(items) <= 30", "1 <= weight,value <= 10^5", "1 <= capacity <= 10^9"],
    [{"input": "items=[[2,3],[3,4],[4,5],[5,6]], capacity=5", "output": "7"}],
    "按单位价值排序；DFS 到物品 i 时用当前价值加剩余物品分数背包上界；上界不超过已知 best 则剪枝。",
    "最坏 O(2^n)，实际剪枝后远小；排序 O(n log n)。",
    ["上界必须允许分数装入最后一个物品，否则不松弛。", "排序后索引状态要一致。", "best 初始为 0，不是负无穷。"],
    "def knapsack_bound(items,capacity):\n    items=sorted(items,key=lambda x:x[1]/x[0],reverse=True); n=len(items); best=0\n    def bound(i,value,left):\n        total=value\n        for w,v in items[i:]:\n            if w<=left:total+=v;left-=w\n            else:total+=v*left/w; break\n        return total\n    def dfs(i,value,left):\n        nonlocal best\n        if i==n or left==0:best=max(best,value);return\n        if bound(i,value,left)<=best:return\n        w,v=items[i]\n        if w<=left:dfs(i+1,value+v,left-w)\n        dfs(i+1,value,left)\n    dfs(0,0,capacity);return best")
java("p142", "import java.util.*;\nclass Solution {\n    private int best;\n    private int[][] items;\n    public int knapsack(int[][] input,int capacity){\n        items=input.clone();Arrays.sort(items,(a,b)->Double.compare((double)b[1]/b[0],(double)a[1]/a[0]));best=0;dfs(0,0,capacity);return best;\n    }\n    private double bound(int i,int value,int left){double total=value;for(;i<items.length;i++){int w=items[i][0],v=items[i][1];if(w<=left){total+=v;left-=w;}else{total+=(double)v*left/w;break;}}return total;}\n    private void dfs(int i,int value,int left){if(i==items.length||left==0){best=Math.max(best,value);return;}if(bound(i,value,left)<=best)return;int w=items[i][0],v=items[i][1];if(w<=left)dfs(i+1,value+v,left-w);dfs(i+1,value,left);}\n}")

add("p143", "旅行商路径", "hard", "branch-and-bound", ["状态压缩", "分支限界", "图"],
    "从 0 出发访问所有城市一次，返回最小路径成本。",
    "给定 n x n 成本矩阵 cost，cost[i][j] 表示从 i 到 j 的成本；从城市 0 出发访问每个城市恰好一次，返回最小总成本。",
    ["2 <= n <= 15", "0 <= cost[i][j] <= 10^6"],
    [{"input": "cost=[[0,10,15],[10,0,20],[15,20,0]]", "output": "45"}],
    "dp[mask][i] 表示已访问集合 mask 且停在 i 的最小成本；扩展未访问城市，最后回到 0。",
    "时间 O(n^2*2^n)，空间 O(n*2^n)。",
    ["mask 必须包含起点和当前城市。", "n=2 时也应完成一次返回。", "不存在路径按题意返回 -1。"],
    "def traveling_salesman(cost):\n    n=len(cost); full=(1<<n)-1; dp=[[float('inf')]*n for _ in range(1<<n)]; dp[1][0]=0\n    for mask in range(1<<n):\n        if not mask&1:continue\n        for last in range(n):\n            if not mask>>last&1 or dp[mask][last]==float('inf'):continue\n            for nxt in range(n):\n                if not mask>>nxt&1:\n                    nmask=mask|1<<nxt;dp[nmask][nxt]=min(dp[nmask][nxt],dp[mask][last]+cost[last][nxt])\n    ans=min(dp[full][i]+cost[i][0] for i in range(1,n) if dp[full][i]<float('inf'))\n    return int(ans) if ans<float('inf') else -1")
java("p143", "import java.util.*;\nclass Solution {\n    public int travelingSalesman(int[][] cost){int n=cost.length,full=(1<<n)-1;long[][] dp=new long[1<<n][n];for(long[] row:dp)Arrays.fill(row,Long.MAX_VALUE);dp[1][0]=0L;\n        for(int mask=1;mask<=full;mask++){if((mask&1)==0)continue;for(int last=0;last<n;last++){if((mask>>last&1)==0||dp[mask][last]==Long.MAX_VALUE)continue;for(int next=0;next<n;next++){if((mask>>next&1)!=0)continue;int nm=mask|1<<next;dp[nm][next]=Math.min(dp[nm][next],dp[mask][last]+cost[last][next]);}}}\n        long ans=Long.MAX_VALUE;for(int i=1;i<n;i++)if(dp[full][i]<Long.MAX_VALUE)ans=Math.min(ans,dp[full][i]+cost[i][0]);return ans==Long.MAX_VALUE?-1:(int)ans;\n    }\n}")

add("p144", "分割数组的最小最大段和", "hard", "branch-and-bound", ["二分答案", "可行性界", "分割"],
    "分割成 k 段，最小化最大段和。",
    "给定非负数组 nums，分割为 k 个非空连续子数组，返回可行的最大段和最小值。",
    ["1 <= len(nums) <= 10^5", "1 <= k <= len(nums)", "0 <= nums[i] <= 10^6"],
    [{"input": "nums=[7,2,5,10,8], k=2", "output": "18"}],
    "答案单调：限制越大越容易分割。二分 limit，贪心扫描若当前段加 x 超限则新开一段；段数 <= k 可行。",
    "时间 O(n log sum)，空间 O(1)。",
    ["每段必须非空，下界应为 max(nums)。", "可行性使用 <= k，不是 == k。", "非负数才满足贪心扫描单调性。"],
    "def split_array(nums,k):\n    lo,hi=max(nums),sum(nums)\n    def feasible(limit):\n        count=1; total=0\n        for x in nums:\n            if total+x>limit:count+=1;total=x\n            else:total+=x\n        return count<=k\n    while lo<hi:\n        mid=(lo+hi)//2\n        if feasible(mid):hi=mid\n        else:lo=mid+1\n    return lo")
java("p144", "class Solution {\n    public long splitArray(int[] nums,int k){long lo=0,hi=0;for(int x:nums){lo=Math.max(lo,x);hi+=x;}\n        while(lo<hi){long mid=lo+(hi-lo)/2;if(feasible(nums,k,mid))hi=mid;else lo=mid+1;}return lo;}\n    private boolean feasible(int[] nums,int k,long limit){int count=1;long total=0;for(int x:nums){if(total+x>limit){count++;total=x;}else total+=x;}return count<=k;}\n}")

# graph-representation
add("p145", "邻接矩阵转邻接表", "easy", "graph-representation", ["图", "邻接表", "表示法"],
    "把稠密矩阵转换成邻接表。",
    "给定 n x n 邻接矩阵 matrix，matrix[i][j] != 0 表示 i 到 j 有权边；返回节点 0..n-1 的邻接表。",
    ["1 <= n <= 1000", "-100 <= weight <= 100", "0 表示无边"],
    [{"input": "[[0,2],[0,0]]", "output": "[[[1,2]],[]]"}],
    "扫描每行，把非零项加入对应邻居列表；不建反向边。",
    "时间 O(n^2)，空间 O(E)。",
    ["0 是无边，不是权 0。", "有向图不能自动补反向边。", "负权也是合法边权。"],
    "def matrix_to_adj(matrix):\n    n=len(matrix); adj=[[] for _ in range(n)]\n    for i,row in enumerate(matrix):\n        for j,w in enumerate(row):\n            if w!=0:adj[i].append((j,w))\n    return adj")
java("p145", "import java.util.*;\nclass Solution {\n    public List<List<int[]>> matrixToAdj(int[][] matrix){int n=matrix.length;List<List<int[]>> adj=new ArrayList<>();for(int i=0;i<n;i++)adj.add(new ArrayList<>());\n        for(int i=0;i<n;i++)for(int j=0;j<n;j++)if(matrix[i][j]!=0)adj.get(i).add(new int[]{j,matrix[i][j]});return adj;\n    }\n}")

add("p146", "有向图可达性", "medium", "graph-representation", ["有向图", "DFS", "邻接表"],
    "判断 source 是否能到达 target。",
    "给定 n 个节点和有向边，返回 source 到 target 是否可达。",
    ["1 <= n <= 10^5", "0 <= edges.length <= 2*10^5"],
    [{"input": "n=3, edges=[[0,1],[1,2]], source=0, target=2", "output": "true"}],
    "建邻接表，从 source DFS/BFS；访问数组防止环导致死循环。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["有向边只加一个方向。", "不能只用递归处理极深图时忽略栈深度。", "source==target 应返回 true。"],
    "from collections import defaultdict\ndef reachable(n,edges,source,target):\n    if source==target:return True\n    g=defaultdict(list)\n    for u,v in edges:g[u].append(v)\n    seen={source}; stack=[source]\n    while stack:\n        u=stack.pop()\n        for v in g[u]:\n            if v==target:return True\n            if v not in seen:seen.add(v);stack.append(v)\n    return False")
java("p146", "import java.util.*;\nclass Solution {\n    public boolean reachable(int n,int[][] edges,int source,int target){\n        if(source==target)return true;List<List<Integer>> g=new ArrayList<>();for(int i=0;i<n;i++)g.add(new ArrayList<>());for(int[] e:edges)g.get(e[0]).add(e[1]);\n        boolean[] seen=new boolean[n];Deque<Integer> stack=new ArrayDeque<>();stack.push(source);seen[source]=true;\n        while(!stack.isEmpty()){int u=stack.pop();for(int v:g.get(u)){if(v==target)return true;if(!seen[v]){seen[v]=true;stack.push(v);}}}return false;\n    }\n}")

add("p147", "反向图可达性", "medium", "graph-representation", ["反向图", "有向图", "DFS"],
    "返回所有能到达 target 的节点。",
    "给定有向边，返回所有满足 u 可达 target 的节点，按升序返回。",
    ["1 <= n <= 10^5", "0 <= edges.length <= 2*10^5"],
    [{"input": "n=4, edges=[[0,1],[2,1],[3,1]], target=1", "output": "[0,1,2,3]"}],
    "建反向边 v->u；从 target 出发遍历，访问到的节点都能到达 target。",
    "时间 O(V+E)，空间 O(V+E)。",
    ["不要从 source 逐个 DFS，复杂度会爆炸。", "反向图方向必须取反。", "target 自己也在答案中。"],
    "from collections import defaultdict\ndef nodes_reaching(n,edges,target):\n    rg=defaultdict(list)\n    for u,v in edges:rg[v].append(u)\n    seen={target}; stack=[target]\n    while stack:\n        u=stack.pop()\n        for v in rg[u]:\n            if v not in seen:seen.add(v);stack.append(v)\n    return sorted(seen)")
java("p147", "import java.util.*;\nclass Solution {\n    public List<Integer> nodesReaching(int n,int[][] edges,int target){\n        List<List<Integer>> rg=new ArrayList<>();for(int i=0;i<n;i++)rg.add(new ArrayList<>());for(int[] e:edges)rg.get(e[1]).add(e[0]);\n        boolean[] seen=new boolean[n];Deque<Integer> stack=new ArrayDeque<>();stack.push(target);seen[target]=true;List<Integer> ans=new ArrayList<>();\n        while(!stack.isEmpty()){int u=stack.pop();ans.add(u);for(int v:rg.get(u))if(!seen[v]){seen[v]=true;stack.push(v);}}\n        java.util.Collections.sort(ans);return ans;\n    }\n}")

add("p148", "隐式网格图边数", "medium", "graph-representation", ["网格图", "隐式图", "边建模"],
    "统计陆地网格构成的隐式无向图边数。",
    "给定 0/1 矩阵，1 是陆地。相邻上下左右的陆地构成一条无向边，返回这样的边总数。",
    ["1 <= rows,cols <= 1000", "grid[i][j] 为 0 或 1"],
    [{"input": "[[1,1],[1,0]]", "output": "2"}],
    "只检查每个陆地的右邻居和下邻居，每条无向边恰好统计一次。",
    "时间 O(rows*cols)，空间 O(1)。",
    ["不要四方向重复计数。", "先判断行列边界。", "对角相邻不是边。"],
    "def grid_edge_count(grid):\n    m,n=len(grid),len(grid[0]); ans=0\n    for i in range(m):\n        for j in range(n):\n            if grid[i][j]==1:\n                if i+1<m and grid[i+1][j]==1:ans+=1\n                if j+1<n and grid[i][j+1]==1:ans+=1\n    return ans")
java("p148", "class Solution {\n    public int gridEdgeCount(int[][] grid){int m=grid.length,n=grid[0].length,ans=0;\n        for(int i=0;i<m;i++)for(int j=0;j<n;j++)if(grid[i][j]==1){if(i+1<m&&grid[i+1][j]==1)ans++;if(j+1<n&&grid[i][j+1]==1)ans++;}return ans;\n    }\n}")
