J = {}
J["p001"] = r'''import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (seen.containsKey(target - nums[i])) return new int[]{seen.get(target - nums[i]), i};
            seen.put(nums[i], i);
        }
        return new int[0];
    }
}'''
J["p002"] = r'''class Solution {
    public int maxSubArray(int[] nums) {
        int ans = nums[0], cur = nums[0];
        for (int i = 1; i < nums.length; i++) {
            cur = Math.max(nums[i], cur + nums[i]);
            ans = Math.max(ans, cur);
        }
        return ans;
    }
}'''
J["p003"] = r'''class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1, ans = 0;
        while (left < right) {
            ans = Math.max(ans, (right - left) * Math.min(height[left], height[right]));
            if (height[left] < height[right]) left++;
            else right--;
        }
        return ans;
    }
}'''
J["p004"] = r'''class Solution {
    public int trap(int[] h) {
        int l = 0, r = h.length - 1, lm = 0, rm = 0, ans = 0;
        while (l < r) {
            if (h[l] <= h[r]) { lm = Math.max(lm, h[l++]); ans += lm - h[l - 1]; }
            else { rm = Math.max(rm, h[r--]); ans += rm - h[r + 1]; }
        }
        return ans;
    }
}'''
J["p005"] = r'''class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int x : nums) if (x != 0) nums[slow++] = x;
        while (slow < nums.length) nums[slow++] = 0;
    }
}'''
J["p006"] = r'''class Solution {
    public void merge(int[] a, int m, int[] b, int n) {
        int i = m - 1, j = n - 1, k = m + n - 1;
        while (i >= 0 && j >= 0) a[k--] = a[i] >= b[j] ? a[i--] : b[j--];
        while (j >= 0) a[k--] = b[j--];
    }
}'''
J["p007"] = r'''class Solution {
    public int removeDuplicates(int[] nums) {
        int slow = 0;
        for (int fast = 1; fast < nums.length; fast++)
            if (nums[fast] != nums[slow]) nums[++slow] = nums[fast];
        return slow + 1;
    }
}'''
J["p008"] = r'''import java.util.*;

class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> ans = new ArrayList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum < 0) l++;
                else if (sum > 0) r--;
                else {
                    ans.add(new ArrayList<>(List.of(nums[i], nums[l++], nums[r--])));
                    while (l < r && nums[l] == nums[l - 1]) l++;
                    while (l < r && nums[r] == nums[r + 1]) r--;
                }
            }
        }
        return ans;
    }
}'''
J["p009"] = r'''class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] ans = new int[nums.length];
        ans[0] = 1;
        for (int i = 1; i < nums.length; i++) ans[i] = ans[i - 1] * nums[i - 1];
        for (int i = nums.length - 1, right = 1; i >= 0; i--) {
            ans[i] *= right;
            right *= nums[i];
        }
        return ans;
    }
}'''
J["p010"] = r'''import java.util.*;

class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> last = new HashMap<>();
        int ans = 0;
        for (int left = 0, right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            if (last.containsKey(c) && last.get(c) >= left) left = last.get(c) + 1;
            last.put(c, right);
            ans = Math.max(ans, right - left + 1);
        }
        return ans;
    }
}'''
J["p011"] = r'''import java.util.*;

class Solution {
    public boolean isValid(String s) {
        Deque<Character> st = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') st.push(')');
            else if (c == '[') st.push(']');
            else if (c == '{') st.push('}');
            else if (st.isEmpty() || st.pop() != c) return false;
        }
        return st.isEmpty();
    }
}'''
J["p012"] = r'''import java.util.*;

class MinStack {
    private Deque<Long> values = new ArrayDeque<>();
    private Deque<Long> minimums = new ArrayDeque<>();

    public void push(int val) {
        values.push((long) val);
        minimums.push(Math.min((long) val, minimums.isEmpty() ? (long) val : minimums.peek()));
    }

    public void pop() { values.pop(); minimums.pop(); }
    public int top() { return values.peek().intValue(); }
    public int getMin() { return minimums.peek().intValue(); }
}'''
J["p013"] = r'''import java.util.*;

class Solution {
    public int[] nextGreaterElements(int[] nums) {
        int[] ans = new int[nums.length];
        Arrays.fill(ans, -1);
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < nums.length; i++) {
            while (!st.isEmpty() && nums[st.peek()] < nums[i]) ans[st.pop()] = nums[i];
            st.push(i);
        }
        return ans;
    }
}'''
J["p014"] = r'''import java.util.*;

class Solution {
    public int[] dailyTemperatures(int[] t) {
        int[] ans = new int[t.length];
        Deque<Integer> st = new ArrayDeque<>();
        for (int i = 0; i < t.length; i++) {
            while (!st.isEmpty() && t[st.peek()] < t[i]) ans[st.peek()] = i - st.pop();
            st.push(i);
        }
        return ans;
    }
}'''
J["p015"] = r'''import java.util.*;

class Solution {
    public int largestRectangleArea(int[] hs) {
        Deque<Integer> st = new ArrayDeque<>();
        st.push(-1);
        int ans = 0;
        for (int i = 0; i <= hs.length; i++) {
            int h = i == hs.length ? 0 : hs[i];
            while (st.peek() != -1 && hs[st.peek()] >= h) {
                int height = hs[st.pop()];
                ans = Math.max(ans, height * (i - st.peek() - 1));
            }
            st.push(i);
        }
        return ans;
    }
}'''
J["p016"] = r'''import java.util.*;

class Solution {
    public String decodeString(String s) {
        Deque<Integer> counts = new ArrayDeque<>();
        Deque<StringBuilder> prefixes = new ArrayDeque<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 0, n = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (Character.isDigit(c)) n = n * 10 + c - '0';
            else if (c == '[') { counts.push(n); prefixes.push(cur); cur = new StringBuilder(); n = 0; }
            else if (c == ']') {
                StringBuilder next = prefixes.pop();
                for (int k = counts.pop(); k > 0; k--) next.append(cur);
                cur = next;
            } else cur.append(c);
        }
        return cur.toString();
    }
}'''
J["p017"] = r'''import java.util.*;

class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        Deque<Integer> dq = new ArrayDeque<>();
        int[] ans = new int[nums.length - k + 1];
        for (int i = 0, j = 0; i < nums.length; i++) {
            while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i]) dq.pollLast();
            dq.addLast(i);
            if (dq.peekFirst() <= i - k) dq.pollFirst();
            if (i >= k - 1) ans[j++] = nums[dq.peekFirst()];
        }
        return ans;
    }
}'''
J["p018"] = r'''import java.util.*;

class Solution {
    public int evalRPN(String[] tokens) {
        Deque<Integer> st = new ArrayDeque<>();
        for (String t : tokens) {
            switch (t) {
                case "+" -> st.push(st.pop() + st.pop());
                case "*" -> st.push(st.pop() * st.pop());
                case "-" -> { int b = st.pop(); st.push(st.pop() - b); }
                case "/" -> { int b = st.pop(); st.push(st.pop() / b); }
                default -> st.push(Integer.parseInt(t));
            }
        }
        return st.pop();
    }
}'''
J["p019"] = r'''import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();
        for (String s : strs) {
            char[] a = s.toCharArray();
            Arrays.sort(a);
            groups.computeIfAbsent(new String(a), k -> new ArrayList<>()).add(s);
        }
        return new ArrayList<>(groups.values());
    }
}'''
J["p020"] = r'''import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int x : nums) count.merge(x, 1, Integer::sum);
        return count.entrySet().stream()
            .sorted(Map.Entry.<Integer,Integer>comparingByValue().reversed())
            .limit(k).mapToInt(Map.Entry::getKey).toArray();
    }
}'''
J["p021"] = r'''import java.util.*;

class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) set.add(x);
        int ans = 0;
        for (int x : set) if (!set.contains(x - 1)) {
            int y = x;
            while (set.contains(y + 1)) y++;
            ans = Math.max(ans, y - x + 1);
        }
        return ans;
    }
}'''
J["p022"] = r'''import java.util.*;

class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> seen = new HashMap<>();
        seen.put(0, 1);
        int prefix = 0, ans = 0;
        for (int x : nums) {
            prefix += x;
            ans += seen.getOrDefault(prefix - k, 0);
            seen.merge(prefix, 1, Integer::sum);
        }
        return ans;
    }
}'''
J["p023"] = r'''import java.util.*;

class Solution {
    public int firstUniqChar(String s) {
        int[] count = new int[128];
        for (char c : s.toCharArray()) count[c]++;
        for (int i = 0; i < s.length(); i++) if (count[s.charAt(i)] == 1) return i;
        return -1;
    }
}'''
J["p024"] = r'''import java.util.*;

class Solution {
    public boolean containsNearbyDuplicate(int[] nums, int k) {
        Map<Integer, Integer> last = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (last.containsKey(nums[i]) && i - last.get(nums[i]) <= k) return true;
            last.put(nums[i], i);
        }
        return false;
    }
}'''
J["p025"] = r'''import java.util.*;

class Solution {
    public int fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        Map<Integer, Integer> ab = new HashMap<>();
        for (int x : a) for (int y : b) ab.merge(x + y, 1, Integer::sum);
        int ans = 0;
        for (int x : c) for (int y : d) ans += ab.getOrDefault(-(x + y), 0);
        return ans;
    }
}'''
J["p026"] = r'''import java.util.concurrent.ThreadLocalRandom;

class WeightPicker {
    private int[] prefix;

    public WeightPicker(int[] w) {
        prefix = new int[w.length];
        prefix[0] = w[0];
        for (int i = 1; i < w.length; i++) prefix[i] = prefix[i - 1] + w[i];
    }

    public int pick() {
        int target = ThreadLocalRandom.current().nextInt(1, prefix[prefix.length - 1] + 1);
        int lo = 0, hi = prefix.length - 1;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (prefix[mid] < target) lo = mid + 1; else hi = mid;
        }
        return lo;
    }
}'''
J["p027"] = r'''class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode prev = null;
        while (head != null) {
            ListNode next = head.next;
            head.next = prev;
            prev = head;
            head = next;
        }
        return prev;
    }
}'''
J["p028"] = r'''class Solution {
    public ListNode middleNode(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }
}'''
J["p029"] = r'''public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}'''
J["p030"] = r'''class Solution {
    public ListNode mergeTwoLists(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(), tail = dummy;
        while (a != null && b != null) {
            if (a.val <= b.val) { tail.next = a; a = a.next; }
            else { tail.next = b; b = b.next; }
            tail = tail.next;
        }
        tail.next = a != null ? a : b;
        return dummy.next;
    }
}'''
J["p031"] = r'''class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) return head;
        ListNode slow = head, fast = head.next;
        while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
        ListNode mid = slow.next;
        slow.next = null;
        return merge(sortList(head), sortList(mid));
    }

    private ListNode merge(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(), tail = dummy;
        while (a != null && b != null) {
            if (a.val <= b.val) { tail.next = a; a = a.next; }
            else { tail.next = b; b = b.next; }
            tail = tail.next;
        }
        tail.next = a != null ? a : b;
        return dummy.next;
    }
}'''
J["p032"] = r'''class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode();
        dummy.next = head;
        ListNode slow = dummy, fast = dummy;
        for (int i = 0; i <= n; i++) fast = fast.next;
        while (fast != null) { slow = slow.next; fast = fast.next; }
        slow.next = slow.next.next;
        return dummy.next;
    }
}'''
J["p033"] = r'''import java.util.*;

class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> values = new ArrayList<>();
        for (; head != null; head = head.next) values.add(head.val);
        for (int l = 0, r = values.size() - 1; l < r; l++, r--)
            if (!values.get(l).equals(values.get(r))) return false;
        return true;
    }
}'''
J["p034"] = r'''class Solution {
    public ListNode addTwoNumbers(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(), tail = dummy;
        for (int carry = 0; a != null || b != null || carry > 0; tail = tail.next) {
            int sum = carry + (a != null ? a.val : 0) + (b != null ? b.val : 0);
            carry = sum / 10;
            tail.next = new ListNode(sum % 10);
            if (a != null) a = a.next;
            if (b != null) b = b.next;
        }
        return dummy.next;
    }
}'''
J["p035"] = r'''import java.util.*;

class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) return null;
        Map<Node, Node> copied = new HashMap<>();
        for (Node cur = head; cur != null; cur = cur.next) copied.put(cur, new Node(cur.val));
        for (Node cur = head; cur != null; cur = cur.next) {
            copied.get(cur).next = copied.get(cur.next);
            copied.get(cur).random = copied.get(cur.random);
        }
        return copied.get(head);
    }
}'''
J["p036"] = r'''import java.util.*;

class LRUCache {
    private final int capacity;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(), tail = new Node();

    private static class Node {
        int key, value;
        Node prev, next;
    }

    public LRUCache(int capacity) {
        this.capacity = capacity;
        head.next = tail;
        tail.prev = head;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) return -1;
        remove(node); addFirst(node);
        return node.value;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) { node.value = value; remove(node); }
        else {
            node = new Node(); node.key = key; map.put(key, node);
        }
        node.value = value; addFirst(node);
        if (map.size() > capacity) {
            Node old = tail.prev;
            remove(old); map.remove(old.key);
        }
    }

    private void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void addFirst(Node n) {
        n.next = head.next; n.prev = head;
        head.next.prev = n; head.next = n;
    }
}'''
J["p037"] = r'''class Solution { public double myPow(double x, long n) { if (n < 0) return 1 / myPow(x, -n); double ans = 1; while (n > 0) { if ((n & 1) == 1) ans *= x; x *= x; n >>= 1; } return ans; } }'''
J["p038"] = r'''class Solution { public int mySqrt(int x) { if (x < 2) return x; int lo = 1, hi = x / 2 + 1; while (lo < hi) { int mid = lo + (hi - lo) / 2; if (mid <= x / mid) lo = mid + 1; else hi = mid; } return lo - 1; } }'''
J["p039"] = r'''class Solution { public int search(int[] nums, int target) { int lo = 0, hi = nums.length - 1; while (lo <= hi) { int mid = lo + (hi - lo) / 2; if (nums[mid] == target) return mid; if (nums[lo] <= nums[mid]) { if (nums[lo] <= target && target < nums[mid]) hi = mid - 1; else lo = mid + 1; } else { if (nums[mid] < target && target <= nums[hi]) lo = mid + 1; else hi = mid - 1; } } return -1; } }'''
J["p040"] = r'''class Solution { public int search(int[] nums, int target) { int lo = 0, hi = nums.length - 1; while (lo <= hi) { int mid = lo + (hi - lo) / 2; if (nums[mid] == target) return mid; if (nums[mid] < target) lo = mid + 1; else hi = mid - 1; } return -1; } }'''
J["p041"] = r'''public class Solution extends VersionControl { public int firstBadVersion(int n) { int lo = 1, hi = n; while (lo < hi) { int mid = lo + (hi - lo) / 2; if (isBadVersion(mid)) hi = mid; else lo = mid + 1; } return lo; } }'''
J["p042"] = r'''class Solution { public int findPeakElement(int[] nums) { int lo = 0, hi = nums.length - 1; while (lo < hi) { int mid = lo + (hi - lo) / 2; if (nums[mid] < nums[mid + 1]) lo = mid + 1; else hi = mid; } return lo; } }'''
J["p043"] = r'''import java.util.*;

class Solution { public int findKthLargest(int[] nums, int k) { PriorityQueue<Integer> pq = new PriorityQueue<>(); for (int x : nums) { pq.offer(x); if (pq.size() > k) pq.poll(); } return pq.peek(); } }'''
J["p044"] = r'''class Solution { public double findMedianSortedArrays(int[] a, int[] b) { if (a.length > b.length) return findMedianSortedArrays(b, a); int m = a.length, n = b.length, lo = 0, hi = m, half = (m + n + 1) / 2; while (lo <= hi) { int i = lo + (hi - lo) / 2, j = half - i; int la = i == 0 ? Integer.MIN_VALUE : a[i - 1], ra = i == m ? Integer.MAX_VALUE : a[i]; int lb = j == 0 ? Integer.MIN_VALUE : b[j - 1], rb = j == n ? Integer.MAX_VALUE : b[j]; if (la > rb) hi = i - 1; else if (lb > ra) lo = i + 1; else return (m + n) % 2 == 1 ? Math.max(la, lb) : (Math.max(la, lb) + Math.min(ra, rb)) / 2.0; } throw new IllegalArgumentException(); } }'''
J["p045"] = r'''class Solution { public int maxDepth(TreeNode root) { return root == null ? 0 : 1 + Math.max(maxDepth(root.left), maxDepth(root.right)); } }'''
J["p046"] = r'''class Solution { public TreeNode invertTree(TreeNode root) { if (root != null) { TreeNode left = invertTree(root.left); root.left = invertTree(root.right); root.right = left; } return root; } }'''
J["p047"] = r'''class Solution { public boolean isValidBST(TreeNode root) { return valid(root, Long.MIN_VALUE, Long.MAX_VALUE); } private boolean valid(TreeNode n, long lo, long hi) { return n == null || (lo < n.val && n.val < hi && valid(n.left, lo, n.val) && valid(n.right, n.val, hi)); } }'''
J["p048"] = r'''import java.util.*;

class Solution { public List<List<Integer>> levelOrder(TreeNode root) { List<List<Integer>> ans = new ArrayList<>(); Queue<TreeNode> q = new ArrayDeque<>(); if (root != null) q.offer(root); while (!q.isEmpty()) { int size = q.size(); List<Integer> row = new ArrayList<>(); for (int i = 0; i < size; i++) { TreeNode n = q.poll(); row.add(n.val); if (n.left != null) q.offer(n.left); if (n.right != null) q.offer(n.right); } ans.add(row); } return ans; } }'''
J["p049"] = r'''import java.util.*;

class Solution { public List<List<Integer>> zigzagLevelOrder(TreeNode root) { List<List<Integer>> ans = levelOrder(root); for (int i = 1; i < ans.size(); i += 2) Collections.reverse(ans.get(i)); return ans; } private List<List<Integer>> levelOrder(TreeNode root) { List<List<Integer>> ans = new ArrayList<>(); Queue<TreeNode> q = new ArrayDeque<>(); if (root != null) q.offer(root); while (!q.isEmpty()) { List<Integer> row = new ArrayList<>(); for (int i = q.size(); i > 0; i--) { TreeNode n = q.poll(); row.add(n.val); if (n.left != null) q.offer(n.left); if (n.right != null) q.offer(n.right); } ans.add(row); } return ans; } }'''
J["p050"] = r'''class Solution { private int ans = 0; public int diameterOfBinaryTree(TreeNode root) { depth(root); return ans; } private int depth(TreeNode n) { if (n == null) return 0; int l = depth(n.left), r = depth(n.right); ans = Math.max(ans, l + r); return 1 + Math.max(l, r); } }'''
J["p051"] = r'''class Solution { public boolean isBalanced(TreeNode root) { return height(root) >= 0; } private int height(TreeNode n) { if (n == null) return 0; int l = height(n.left), r = height(n.right); if (l < 0 || r < 0 || Math.abs(l - r) > 1) return -1; return 1 + Math.max(l, r); } }'''
J["p052"] = r'''class Solution { public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) { while (root != null) { if (p.val < root.val && q.val < root.val) root = root.left; else if (p.val > root.val && q.val > root.val) root = root.right; else return root; } return null; } }'''
J["p053"] = r'''import java.util.*;

public class Codec { public String serialize(TreeNode root) { return root == null ? "#" : root.val + "," + serialize(root.left) + "," + serialize(root.right); } public TreeNode deserialize(String data) { Queue<String> q = new LinkedList<>(Arrays.asList(data.split(","))); return build(q); } private TreeNode build(Queue<String> q) { String v = q.poll(); if (v.equals("#")) return null; TreeNode root = new TreeNode(Integer.parseInt(v)); root.left = build(q); root.right = build(q); return root; } }'''
J["p054"] = r'''import java.util.*;

class Solution { private int ans = 0; public int pathSum(TreeNode root, int target) { Map<Long,Integer> seen = new HashMap<>(); seen.put(0L, 1); dfs(root, target, 0, seen); return ans; } private void dfs(TreeNode n, int target, long cur, Map<Long,Integer> seen) { if (n == null) return; cur += n.val; ans += seen.getOrDefault(cur - target, 0); seen.merge(cur, 1, Integer::sum); dfs(n.left, target, cur, seen); dfs(n.right, target, cur, seen); seen.merge(cur, -1, Integer::sum); } }'''
J["p055"] = r'''import java.util.*;

class Solution { public List<Integer> rightSideView(TreeNode root) { List<Integer> ans = new ArrayList<>(); dfs(root, 0, ans); return ans; } private void dfs(TreeNode n, int depth, List<Integer> ans) { if (n == null) return; if (depth == ans.size()) ans.add(n.val); dfs(n.right, depth + 1, ans); dfs(n.left, depth + 1, ans); } }'''
J["p056"] = r'''import java.util.*;

class Solution { private int pos = 0; public TreeNode buildTree(int[] preorder, int[] inorder) { Map<Integer,Integer> idx = new HashMap<>(); for (int i = 0; i < inorder.length; i++) idx.put(inorder[i], i); return build(preorder, idx, 0, inorder.length - 1); } private TreeNode build(int[] pre, Map<Integer,Integer> idx, int lo, int hi) { if (lo > hi) return null; TreeNode root = new TreeNode(pre[pos++]); int mid = idx.get(root.val); root.left = build(pre, idx, lo, mid - 1); root.right = build(pre, idx, mid + 1, hi); return root; } }'''
J["p057"] = r'''import java.util.*;

class KthLargest { private final PriorityQueue<Integer> pq = new PriorityQueue<>(); private final int k; public KthLargest(int k, int[] nums) { this.k = k; for (int x : nums) add(x); } public int add(int val) { pq.offer(val); if (pq.size() > k) pq.poll(); return pq.peek(); } }'''
J["p058"] = r'''import java.util.*;

class Solution { public int[][] kClosest(int[][] points, int k) { PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> b[0] - a[0]); for (int[] p : points) { int d = p[0] * p[0] + p[1] * p[1]; if (pq.size() < k) pq.offer(new int[]{d, p[0], p[1]}); else if (d < pq.peek()[0]) { pq.poll(); pq.offer(new int[]{d, p[0], p[1]}); } } return pq.stream().map(x -> new int[]{x[1], x[2]}).toArray(int[][]::new); } }'''
J["p059"] = r'''import java.util.*;

class Solution { public ListNode mergeKLists(ListNode[] lists) { PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]); ListNode dummy = new ListNode(), tail = dummy; for (int i = 0; i < lists.length; i++) if (lists[i] != null) pq.offer(new int[]{lists[i].val, i}); while (!pq.isEmpty()) { int[] top = pq.poll(); int i = top[1]; tail.next = lists[i]; tail = tail.next; lists[i] = lists[i].next; if (lists[i] != null) pq.offer(new int[]{lists[i].val, i}); } return dummy.next; } }'''
J["p060"] = r'''import java.util.*;

class Solution { public List<String> topKFrequent(String[] words, int k) { Map<String,Integer> count = new HashMap<>(); for (String w : words) count.merge(w, 1, Integer::sum); return count.keySet().stream().sorted((a,b) -> { int d = count.get(b) - count.get(a); return d != 0 ? d : a.compareTo(b); }).limit(k).toList(); } }'''
J["p061"] = r'''import java.util.*;

class MedianFinder { private final PriorityQueue<Integer> left = new PriorityQueue<>(Collections.reverseOrder()); private final PriorityQueue<Integer> right = new PriorityQueue<>(); public void addNum(int x) { left.offer(x); right.offer(left.poll()); if (right.size() > left.size()) left.offer(right.poll()); } public double findMedian() { return left.size() > right.size() ? left.peek() : (left.peek() + right.peek()) / 2.0; } }'''
J["p062"] = r'''import java.util.*;

class Solution { public int leastInterval(char[] tasks, int n) { int[] count = new int[26]; for (char c : tasks) count[c - 'A']++; int max = Arrays.stream(count).max().orElse(0), ties = 0; for (int x : count) if (x == max) ties++; return Math.max(tasks.length, (max - 1) * (n + 1) + ties); } }'''
J["p063"] = r'''import java.util.*;

class Solution { public List<List<Integer>> kSmallestPairs(int[] a, int[] b, int k) { PriorityQueue<int[]> pq = new PriorityQueue<>((x,y) -> x[0] - y[0]); for (int i = 0; i < Math.min(k, a.length); i++) pq.offer(new int[]{a[i] + b[0], i, 0}); List<List<Integer>> ans = new ArrayList<>(); while (!pq.isEmpty() && ans.size() < k) { int[] top = pq.poll(); ans.add(List.of(a[top[1]], b[top[2]])); if (top[2] + 1 < b.length) pq.offer(new int[]{a[top[1]] + b[top[2] + 1], top[1], top[2] + 1}); } return ans; } }'''
J["p064"] = r'''class Solution { private static final int[] D = {1,0,-1,0,0,1,0,-1}; public int numIslands(char[][] grid) { int ans = 0; for (int i = 0; i < grid.length; i++) for (int j = 0; j < grid[0].length; j++) if (grid[i][j] == '1') { dfs(grid, i, j); ans++; } return ans; } private void dfs(char[][] g, int i, int j) { if (i < 0 || i >= g.length || j < 0 || j >= g[0].length || g[i][j] != '1') return; g[i][j] = '0'; for (int d = 0; d < 8; d += 2) dfs(g, i + D[d], j + D[d + 1]); } }'''
J["p065"] = r'''import java.util.*;

class Solution { public Node cloneGraph(Node node) { if (node == null) return null; Map<Node,Node> copied = new HashMap<>(); copied.put(node, new Node(node.val)); Queue<Node> q = new ArrayDeque<>(); q.offer(node); while (!q.isEmpty()) { Node cur = q.poll(); for (Node next : cur.neighbors) { if (!copied.containsKey(next)) { copied.put(next, new Node(next.val)); q.offer(next); } copied.get(cur).neighbors.add(copied.get(next)); } } return copied.get(node); } }'''
J["p066"] = r'''import java.util.*;

class Solution { public boolean canFinish(int n, int[][] edges) { List<List<Integer>> g = new ArrayList<>(); for (int i = 0; i < n; i++) g.add(new ArrayList<>()); int[] indeg = new int[n]; for (int[] e : edges) { g.get(e[1]).add(e[0]); indeg[e[0]]++; } Queue<Integer> q = new ArrayDeque<>(); for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i); int seen = 0; while (!q.isEmpty()) { int u = q.poll(); seen++; for (int v : g.get(u)) if (--indeg[v] == 0) q.offer(v); } return seen == n; } }'''
J["p067"] = r'''import java.util.*;

class Solution { public int[] findOrder(int n, int[][] edges) { List<List<Integer>> g = new ArrayList<>(); for (int i = 0; i < n; i++) g.add(new ArrayList<>()); int[] indeg = new int[n]; for (int[] e : edges) { g.get(e[1]).add(e[0]); indeg[e[0]]++; } Queue<Integer> q = new ArrayDeque<>(); for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i); int[] ans = new int[n]; int idx = 0; while (!q.isEmpty()) { int u = q.poll(); ans[idx++] = u; for (int v : g.get(u)) if (--indeg[v] == 0) q.offer(v); } return idx == n ? ans : new int[0]; } }'''
J["p068"] = r'''import java.util.*;

class Solution { public List<List<Integer>> pacificAtlantic(int[][] h) { int m = h.length, n = h[0].length; boolean[][] pac = new boolean[m][n], atl = new boolean[m][n]; for (int i = 0; i < m; i++) { dfs(h, pac, i, 0); dfs(h, atl, i, n - 1); } for (int j = 0; j < n; j++) { dfs(h, pac, 0, j); dfs(h, atl, m - 1, j); } List<List<Integer>> ans = new ArrayList<>(); for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) if (pac[i][j] && atl[i][j]) ans.add(List.of(i,j)); return ans; } private void dfs(int[][] h, boolean[][] seen, int i, int j) { if (i < 0 || i >= h.length || j < 0 || j >= h[0].length || seen[i][j]) return; seen[i][j] = true; int[][] d = {{1,0},{-1,0},{0,1},{0,-1}}; for (int[] p : d) { int a = i + p[0], b = j + p[1]; if (a >= 0 && a < h.length && b >= 0 && b < h[0].length && h[a][b] >= h[i][j]) dfs(h, seen, a, b); } } }'''
J["p069"] = r'''import java.util.*;

class Solution { public int orangesRotting(int[][] grid) { int m = grid.length, n = grid[0].length, fresh = 0, ans = 0; Queue<int[]> q = new ArrayDeque<>(); for (int i = 0; i < m; i++) for (int j = 0; j < n; j++) { if (grid[i][j] == 2) q.offer(new int[]{i,j}); if (grid[i][j] == 1) fresh++; } int[][] d = {{1,0},{-1,0},{0,1},{0,-1}}; while (!q.isEmpty() && fresh > 0) { for (int size = q.size(); size > 0; size--) { int[] cur = q.poll(); for (int[] p : d) { int a = cur[0] + p[0], b = cur[1] + p[1]; if (a >= 0 && a < m && b >= 0 && b < n && grid[a][b] == 1) { grid[a][b] = 2; fresh--; q.offer(new int[]{a,b}); } } } ans++; } return fresh == 0 ? ans : -1; } }'''
J["p070"] = r'''import java.util.*;

class Solution { public int ladderLength(String begin, String end, List<String> words) { Set<String> dict = new HashSet<>(words); if (!dict.contains(end)) return 0; Queue<String> q = new ArrayDeque<>(); q.offer(begin); dict.remove(begin); for (int depth = 1; !q.isEmpty(); depth++) for (int size = q.size(); size > 0; size--) { String cur = q.poll(); if (cur.equals(end)) return depth; char[] a = cur.toCharArray(); for (int i = 0; i < a.length; i++) for (char c = 'a'; c <= 'z'; c++) { char old = a[i]; a[i] = c; String next = new String(a); if (dict.remove(next)) q.offer(next); a[i] = old; } } return 0; } }'''
J["p071"] = r'''import java.util.*;

class Solution { public int countComponents(int n, int[][] edges) { List<List<Integer>> g = new ArrayList<>(); for (int i = 0; i < n; i++) g.add(new ArrayList<>()); for (int[] e : edges) { g.get(e[0]).add(e[1]); g.get(e[1]).add(e[0]); } boolean[] seen = new boolean[n]; int ans = 0; for (int i = 0; i < n; i++) if (!seen[i]) { dfs(g, seen, i); ans++; } return ans; } private void dfs(List<List<Integer>> g, boolean[] seen, int u) { seen[u] = true; for (int v : g.get(u)) if (!seen[v]) dfs(g, seen, v); } }'''
J["p072"] = r'''import java.util.*;

class Solution { public boolean isBipartite(int n, int[][] edges) { List<List<Integer>> g = new ArrayList<>(); for (int i = 0; i < n; i++) g.add(new ArrayList<>()); for (int[] e : edges) { g.get(e[0]).add(e[1]); g.get(e[1]).add(e[0]); } int[] color = new int[n]; Arrays.fill(color, -1); for (int start = 0; start < n; start++) if (color[start] < 0) { Queue<Integer> q = new ArrayDeque<>(); q.offer(start); color[start] = 0; while (!q.isEmpty()) { int u = q.poll(); for (int v : g.get(u)) { if (color[v] < 0) { color[v] = color[u] ^ 1; q.offer(v); } else if (color[v] == color[u]) return false; } } } return true; } }'''
J["p073"] = r'''import java.util.*;

class Solution { public int networkDelayTime(int[][] times, int n, int k) { List<int[][]> adj = new ArrayList<>(); int[] dist = new int[n + 1]; Arrays.fill(dist, Integer.MAX_VALUE); dist[k] = 0; Queue<int[]> pq = new PriorityQueue<>((a,b) -> a[0] - b[0]); pq.offer(new int[]{0,k}); while (!pq.isEmpty()) { int[] cur = pq.poll(); int u = cur[1]; if (cur[0] > dist[u]) continue; for (int[] e : adjacent(times, u)) { int v = e[0], nd = dist[u] + e[1]; if (nd < dist[v]) { dist[v] = nd; pq.offer(new int[]{nd,v}); } } } int ans = 0; for (int i = 1; i <= n; i++) ans = Math.max(ans, dist[i]); return ans == Integer.MAX_VALUE ? -1 : ans; } private List<int[]> adjacent(int[][] times, int u) { List<int[]> res = new ArrayList<>(); for (int[] e : times) if (e[0] == u) res.add(new int[]{e[1], e[2]}); return res; } }'''
J["p074"] = r'''import java.util.*;

class Solution { public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) { int[] dist = new int[n]; Arrays.fill(dist, Integer.MAX_VALUE); dist[src] = 0; for (int round = 0; round <= k; round++) { int[] next = dist.clone(); for (int[] e : flights) if (dist[e[0]] != Integer.MAX_VALUE) next[e[1]] = Math.min(next[e[1]], dist[e[0]] + e[2]); dist = next; } return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst]; } }'''
J["p075"] = r'''import java.util.*;

class Solution { public int minimumEffortPath(int[][] h) { int m = h.length, n = h[0].length, lo = 0, hi = 0; for (int[] row : h) for (int x : row) hi = Math.max(hi, x); while (lo < hi) { int mid = lo + (hi - lo) / 2; if (can(h, mid)) hi = mid; else lo = mid + 1; } return lo; } private boolean can(int[][] h, int limit) { int m = h.length, n = h[0].length; boolean[][] seen = new boolean[m][n]; Deque<int[]> q = new ArrayDeque<>(); q.offer(new int[]{0,0}); seen[0][0] = true; int[][] d = {{1,0},{-1,0},{0,1},{0,-1}}; while (!q.isEmpty()) { int[] cur = q.poll(); if (cur[0] == m - 1 && cur[1] == n - 1) return true; for (int[] p : d) { int a = cur[0] + p[0], b = cur[1] + p[1]; if (a >= 0 && a < m && b >= 0 && b < n && !seen[a][b] && Math.abs(h[a][b] - h[cur[0]][cur[1]]) <= limit) { seen[a][b] = true; q.offer(new int[]{a,b}); } } } return false; } }'''
J["p076"] = r'''import java.util.*;

class Solution { public int minCostConnectPoints(int[][] points) { int n = points.length, ans = 0; boolean[] seen = new boolean[n]; PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> a[0] - b[0]); pq.offer(new int[]{0,0}); while (!pq.isEmpty()) { int[] cur = pq.poll(); if (seen[cur[1]]) continue; seen[cur[1]] = true; ans += cur[0]; for (int i = 0; i < n; i++) if (!seen[i]) { int d = Math.abs(points[i][0] - points[cur[1]][0]) + Math.abs(points[i][1] - points[cur[1]][1]); pq.offer(new int[]{d,i}); } } return ans; } }'''
J["p077"] = r'''class Solution { public int[] findRedundantConnection(int[][] edges) { int[] parent = new int[edges.length + 1]; for (int i = 0; i <= edges.length; i++) parent[i] = i; for (int[] e : edges) if (find(parent, e[0]) == find(parent, e[1])) return e; else parent[find(parent, e[0])] = find(parent, e[1]); return new int[0]; } private int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; } }'''
J["p078"] = r'''import java.util.*;

class Solution { public int minCost(int n, int[] modules, int[][] edges) { List<int[]> all = new ArrayList<>(); for (int i = 0; i < n; i++) all.add(new int[]{modules[i], 0, i + 1}); for (int[] e : edges) all.add(new int[]{e[2], e[0], e[1]}); all.sort(Comparator.comparingInt(x -> x[0])); int[] parent = new int[n + 1]; for (int i = 0; i <= n; i++) parent[i] = i; int ans = 0, used = 0; for (int[] e : all) { int a = find(parent, e[1]), b = find(parent, e[2]); if (a != b) { parent[a] = b; ans += e[0]; if (++used == n) return ans; } } return -1; } private int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; } }'''
J["p079"] = r'''import java.util.*;

class Solution { public List<List<Integer>> permute(int[] nums) { List<List<Integer>> ans = new ArrayList<>(); dfs(nums, new boolean[nums.length], new ArrayList<>(), ans); return ans; } private void dfs(int[] nums, boolean[] used, List<Integer> path, List<List<Integer>> ans) { if (path.size() == nums.length) { ans.add(new ArrayList<>(path)); return; } for (int i = 0; i < nums.length; i++) if (!used[i]) { used[i] = true; path.add(nums[i]); dfs(nums, used, path, ans); path.remove(path.size() - 1); used[i] = false; } } }'''
J["p080"] = r'''import java.util.*;

class Solution { public List<List<Integer>> subsets(int[] nums) { List<List<Integer>> ans = new ArrayList<>(); dfs(nums, 0, new ArrayList<>(), ans); return ans; } private void dfs(int[] nums, int start, List<Integer> path, List<List<Integer>> ans) { ans.add(new ArrayList<>(path)); for (int i = start; i < nums.length; i++) { path.add(nums[i]); dfs(nums, i + 1, path, ans); path.remove(path.size() - 1); } } }'''
J["p081"] = r'''import java.util.*;

class Solution { public List<List<Integer>> combinationSum(int[] candidates, int target) { Arrays.sort(candidates); List<List<Integer>> ans = new ArrayList<>(); dfs(candidates, target, 0, new ArrayList<>(), ans); return ans; } private void dfs(int[] candidates, int rest, int start, List<Integer> path, List<List<Integer>> ans) { if (rest == 0) { ans.add(new ArrayList<>(path)); return; } for (int i = start; i < candidates.length && candidates[i] <= rest; i++) { path.add(candidates[i]); dfs(candidates, rest - candidates[i], i, path, ans); path.remove(path.size() - 1); } } }'''
J["p082"] = r'''import java.util.*;

class Solution { public List<List<String>> partition(String s) { List<List<String>> ans = new ArrayList<>(); dfs(s, 0, new ArrayList<>(), ans); return ans; } private void dfs(String s, int start, List<String> path, List<List<String>> ans) { if (start == s.length()) { ans.add(new ArrayList<>(path)); return; } for (int end = start + 1; end <= s.length(); end++) if (isPalindrome(s, start, end - 1)) { path.add(s.substring(start, end)); dfs(s, end, path, ans); path.remove(path.size() - 1); } } private boolean isPalindrome(String s, int lo, int hi) { while (lo < hi) if (s.charAt(lo++) != s.charAt(hi--)) return false; return true; } }'''
J["p083"] = r'''class Solution { public boolean exist(char[][] board, String word) { for (int i = 0; i < board.length; i++) for (int j = 0; j < board[0].length; j++) if (dfs(board, word, i, j, 0)) return true; return false; } private boolean dfs(char[][] b, String word, int i, int j, int k) { if (k == word.length()) return true; if (i < 0 || i >= b.length || j < 0 || j >= b[0].length || b[i][j] != word.charAt(k)) return false; char old = b[i][j]; b[i][j] = '#'; boolean found = dfs(b, word, i+1, j, k+1) || dfs(b, word, i-1, j, k+1) || dfs(b, word, i, j+1, k+1) || dfs(b, word, i, j-1, k+1); b[i][j] = old; return found; } }'''
J["p084"] = r'''import java.util.*;

class Solution { public List<List<String>> solveNQueens(int n) { List<List<String>> ans = new ArrayList<>(); dfs(n, 0, new HashSet<>(), new HashSet<>(), new HashSet<>(), new ArrayList<>(), ans); return ans; } private void dfs(int n, int row, Set<Integer> cols, Set<Integer> d1, Set<Integer> d2, List<Integer> queens, List<List<String>> ans) { if (row == n) { List<String> board = new ArrayList<>(); for (int c : queens) board.add(".".repeat(c) + "Q" + ".".repeat(n - c - 1)); ans.add(board); return; } for (int col = 0; col < n; col++) if (!cols.contains(col) && !d1.contains(row - col) && !d2.contains(row + col)) { cols.add(col); d1.add(row - col); d2.add(row + col); queens.add(col); dfs(n, row + 1, cols, d1, d2, queens, ans); queens.remove(queens.size() - 1); d2.remove(row + col); d1.remove(row - col); cols.remove(col); } } }'''
J["p085"] = r'''class Solution { public void solveSudoku(char[][] board) { solve(board); } private boolean solve(char[][] b) { for (int i = 0; i < 9; i++) for (int j = 0; j < 9; j++) if (b[i][j] == '.') { for (char v = '1'; v <= '9'; v++) if (valid(b, i, j, v)) { b[i][j] = v; if (solve(b)) return true; b[i][j] = '.'; } return false; } return true; } private boolean valid(char[][] b, int row, int col, char v) { for (int i = 0; i < 9; i++) if (b[row][i] == v || b[i][col] == v || b[(row/3)*3 + i/3][(col/3)*3 + i%3] == v) return false; return true; } }'''
J["p086"] = r'''import java.util.*;

class Solution { private static final String[] MAP = {"", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"}; public List<String> letterCombinations(String digits) { List<String> ans = new ArrayList<>(); if (!digits.isEmpty()) dfs(digits, 0, new StringBuilder(), ans); return ans; } private void dfs(String digits, int i, StringBuilder path, List<String> ans) { if (i == digits.length()) { ans.add(path.toString()); return; } for (char c : MAP[digits.charAt(i) - '0'].toCharArray()) { path.append(c); dfs(digits, i + 1, path, ans); path.deleteCharAt(path.length() - 1); } } }'''
J["p087"] = r'''class Solution { public boolean canJump(int[] nums) { int far = 0; for (int i = 0; i < nums.length; i++) { if (i > far) return false; far = Math.max(far, i + nums[i]); } return true; } }'''
J["p088"] = r'''class Solution { public int jump(int[] nums) { int steps = 0, end = 0, far = 0; for (int i = 0; i < nums.length - 1; i++) { far = Math.max(far, i + nums[i]); if (i == end) { steps++; end = far; } } return steps; } }'''
J["p089"] = r'''import java.util.*;

class Solution { public int[][] merge(int[][] intervals) { Arrays.sort(intervals, (a,b) -> a[0] - b[0]); List<int[]> merged = new ArrayList<>(); for (int[] interval : intervals) if (!merged.isEmpty() && interval[0] <= merged.get(merged.size() - 1)[1]) merged.get(merged.size() - 1)[1] = Math.max(merged.get(merged.size() - 1)[1], interval[1]); else merged.add(interval); return merged.toArray(int[][]::new); } }'''
J["p090"] = r'''import java.util.*;

class Solution { public int eraseOverlapIntervals(int[][] intervals) { Arrays.sort(intervals, (a,b) -> Integer.compare(a[1], b[1])); int remove = 0, end = Integer.MIN_VALUE; for (int[] interval : intervals) if (interval[0] >= end) end = interval[1]; else remove++; return remove; } }'''
J["p091"] = r'''import java.util.*;

class Solution { public int findMinArrowShots(int[][] points) { if (points.length == 0) return 0; Arrays.sort(points, (a,b) -> Integer.compare(a[1], b[1])); int arrows = 1, pos = points[0][1]; for (int[] p : points) if (p[0] > pos) { arrows++; pos = p[1]; } return arrows; } }'''
J["p092"] = r'''import java.util.*;

class Solution { public int findContentChildren(int[] g, int[] s) { Arrays.sort(g); Arrays.sort(s); int i = 0, j = 0; while (i < g.length && j < s.length) if (s[j++] >= g[i]) i++; return i; } }'''
J["p093"] = r'''import java.util.*;

class Solution { public List<Integer> partitionLabels(String s) { int[] last = new int[128]; for (int i = 0; i < s.length(); i++) last[s.charAt(i)] = i; List<Integer> ans = new ArrayList<>(); for (int i = 0, start = 0, end = 0; i < s.length(); i++) { end = Math.max(end, last[s.charAt(i)]); if (i == end) { ans.add(end - start + 1); start = end + 1; } } return ans; } }'''
J["p094"] = r'''import java.util.*;

class Solution { public int candy(int[] ratings) { int[] left = new int[ratings.length]; Arrays.fill(left, 1); for (int i = 1; i < ratings.length; i++) if (ratings[i] > ratings[i - 1]) left[i] = left[i - 1] + 1; int ans = 0, right = 1; for (int i = ratings.length - 1; i >= 0; i--) { if (i < ratings.length - 1 && ratings[i] > ratings[i + 1]) right++; else right = 1; ans += Math.max(left[i], right); } return ans; } }'''
J["p095"] = r'''class Solution { public int climbStairs(int n) { int a = 1, b = 1; for (int i = 2; i <= n; i++) { int next = a + b; a = b; b = next; } return b; } }'''
J["p096"] = r'''class Solution { public int rob(int[] nums) { int prev = 0, cur = 0; for (int x : nums) { int next = Math.max(cur, prev + x); prev = cur; cur = next; } return cur; } }'''
J["p097"] = r'''import java.util.*;

class Solution { public int coinChange(int[] coins, int amount) { int[] dp = new int[amount + 1]; Arrays.fill(dp, Integer.MAX_VALUE); dp[0] = 0; for (int coin : coins) for (int c = coin; c <= amount; c++) if (dp[c - coin] != Integer.MAX_VALUE) dp[c] = Math.min(dp[c], dp[c - coin] + 1); return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount]; } }'''
J["p098"] = r'''class Solution { public int change(int amount, int[] coins) { int[] dp = new int[amount + 1]; dp[0] = 1; for (int coin : coins) for (int c = coin; c <= amount; c++) dp[c] += dp[c - coin]; return dp[amount]; } }'''
J["p099"] = r'''class Solution { public int lengthOfLIS(int[] nums) { int[] tails = new int[nums.length]; int size = 0; for (int x : nums) { int lo = 0, hi = size; while (lo < hi) { int mid = lo + (hi - lo) / 2; if (tails[mid] < x) lo = mid + 1; else hi = mid; } tails[lo] = x; if (lo == size) size++; } return size; } }'''
J["p100"] = r'''class Solution { public int longestCommonSubsequence(String a, String b) { int[][] dp = new int[a.length() + 1][b.length() + 1]; for (int i = 1; i <= a.length(); i++) for (int j = 1; j <= b.length(); j++) dp[i][j] = a.charAt(i - 1) == b.charAt(j - 1) ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1]); return dp[a.length()][b.length()]; } }'''
J["p101"] = r'''class Solution { public int minDistance(String a, String b) { int[][] dp = new int[a.length() + 1][b.length() + 1]; for (int i = 0; i <= a.length(); i++) dp[i][0] = i; for (int j = 0; j <= b.length(); j++) dp[0][j] = j; for (int i = 1; i <= a.length(); i++) for (int j = 1; j <= b.length(); j++) dp[i][j] = a.charAt(i - 1) == b.charAt(j - 1) ? dp[i - 1][j - 1] : 1 + Math.min(dp[i - 1][j], Math.min(dp[i][j - 1], dp[i - 1][j - 1])); return dp[a.length()][b.length()]; } }'''
J["p102"] = r'''import java.util.*;

class Solution { public int uniquePaths(int m, int n) { int[] dp = new int[n]; Arrays.fill(dp, 1); for (int i = 1; i < m; i++) for (int j = 1; j < n; j++) dp[j] += dp[j - 1]; return dp[n - 1]; } }'''
J["p103"] = r'''class Solution { public int minPathSum(int[][] grid) { int m = grid.length, n = grid[0].length; int[] dp = new int[n]; dp[0] = grid[0][0]; for (int j = 1; j < n; j++) dp[j] = dp[j - 1] + grid[0][j]; for (int i = 1; i < m; i++) { dp[0] += grid[i][0]; for (int j = 1; j < n; j++) dp[j] = grid[i][j] + Math.min(dp[j], dp[j - 1]); } return dp[n - 1]; } }'''
J["p104"] = r'''import java.util.*;

class Solution { public boolean canPartition(int[] nums) { int total = Arrays.stream(nums).sum(); if (total % 2 == 1) return false; int target = total / 2; boolean[] dp = new boolean[target + 1]; dp[0] = true; for (int x : nums) for (int c = target; c >= x; c--) dp[c] |= dp[c - x]; return dp[target]; } }'''
J["p105"] = r'''import java.util.*;

class Solution { public boolean wordBreak(String s, List<String> words) { Set<String> dict = new HashSet<>(words); boolean[] dp = new boolean[s.length() + 1]; dp[0] = true; for (int i = 1; i <= s.length(); i++) for (int j = 0; j < i && !dp[i]; j++) if (dp[j] && dict.contains(s.substring(j, i))) dp[i] = true; return dp[s.length()]; } }'''
J["p106"] = r'''class Solution { public int numDecodings(String s) { if (s.charAt(0) == '0') return 0; int prev = 1, cur = 1; for (int i = 1; i < s.length(); i++) { int next = s.charAt(i) == '0' ? 0 : cur; int two = Integer.parseInt(s.substring(i - 1, i + 1)); if (two >= 10 && two <= 26) next += prev; if (next == 0) return 0; prev = cur; cur = next; } return cur; } }'''
J["p107"] = r'''class Solution { public int maximalSquare(char[][] matrix) { int m = matrix.length, n = matrix[0].length, ans = 0, prevDiag = 0; int[] dp = new int[n + 1]; for (int i = 0; i < m; i++) { prevDiag = 0; for (int j = 1; j <= n; j++) { int old = dp[j]; if (matrix[i][j - 1] == '1') { dp[j] = Math.min(prevDiag, Math.min(dp[j], dp[j - 1])) + 1; ans = Math.max(ans, dp[j]); } else dp[j] = 0; prevDiag = old; } } return ans * ans; } }'''
J["p108"] = r'''class Solution { public int maxCoins(int[] nums) { int n = nums.length + 2; int[] a = new int[n]; a[0] = a[n - 1] = 1; for (int i = 0; i < nums.length; i++) a[i + 1] = nums[i]; int[][] dp = new int[n][n]; for (int len = 2; len < n; len++) for (int l = 0, r = len; r < n; l++, r++) for (int k = l + 1; k < r; k++) dp[l][r] = Math.max(dp[l][r], dp[l][k] + a[l] * a[k] * a[r] + dp[k][r]); return dp[0][n - 1]; } }'''
J["p109"] = r'''class Solution { public boolean isPalindrome(String s) { for (int l = 0, r = s.length() - 1; l < r; l++, r--) { while (l < r && !Character.isLetterOrDigit(s.charAt(l))) l++; while (l < r && !Character.isLetterOrDigit(s.charAt(r))) r--; if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r))) return false; } return true; } }'''
J["p110"] = r'''class Solution { public int myAtoi(String s) { int i = 0, sign = 1; while (i < s.length() && s.charAt(i) == ' ') i++; if (i < s.length() && (s.charAt(i) == '+' || s.charAt(i) == '-')) sign = s.charAt(i++) == '-' ? -1 : 1; long num = 0; while (i < s.length() && Character.isDigit(s.charAt(i))) { num = num * 10 + s.charAt(i++) - '0'; if (sign == 1 && num > Integer.MAX_VALUE) return Integer.MAX_VALUE; if (sign == -1 && -num < Integer.MIN_VALUE) return Integer.MIN_VALUE; } return sign * (int) num; } }'''
J["p111"] = r'''class Solution { public String longestPalindrome(String s) { int[] best = {0, 0}; for (int i = 0; i < s.length(); i++) { for (int[] range : new int[][]{expand(s, i, i), expand(s, i, i + 1)}) if (range[1] - range[0] > best[1] - best[0]) best = range; } return s.substring(best[0], best[1]); } private int[] expand(String s, int l, int r) { while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; } return new int[]{l + 1, r}; } }'''
J["p112"] = r'''class Solution { public int strStr(String haystack, String needle) { if (needle.isEmpty()) return 0; int[] next = new int[needle.length()]; for (int i = 1, k = 0; i < needle.length(); i++) { while (k > 0 && needle.charAt(i) != needle.charAt(k)) k = next[k - 1]; if (needle.charAt(i) == needle.charAt(k)) k++; next[i] = k; } for (int i = 0, k = 0; i < haystack.length(); i++) { while (k > 0 && haystack.charAt(i) != needle.charAt(k)) k = next[k - 1]; if (haystack.charAt(i) == needle.charAt(k)) k++; if (k == needle.length()) return i - k + 1; } return -1; } }'''
J["p113"] = r'''import java.util.*;

class Solution { public String removeKdigits(String num, int k) { Deque<Character> st = new ArrayDeque<>(); for (char c : num.toCharArray()) { while (k > 0 && !st.isEmpty() && st.peekLast() > c) { st.pollLast(); k--; } st.addLast(c); } while (k-- > 0) st.pollLast(); StringBuilder sb = new StringBuilder(); boolean leading = true; for (char c : st) { if (leading && c == '0') continue; leading = false; sb.append(c); } return sb.length() == 0 ? "0" : sb.toString(); } }'''
J["p114"] = r'''class Solution { public boolean isAlienSorted(String[] words, String order) { int[] rank = new int[128]; for (int i = 0; i < order.length(); i++) rank[order.charAt(i)] = i; for (int i = 1; i < words.length; i++) if (!inOrder(words[i - 1], words[i], rank)) return false; return true; } private boolean inOrder(String a, String b, int[] rank) { int n = Math.min(a.length(), b.length()); for (int i = 0; i < n; i++) if (rank[a.charAt(i)] != rank[b.charAt(i)]) return rank[a.charAt(i)] < rank[b.charAt(i)]; return a.length() <= b.length(); } }'''
J["p115"] = r'''class Solution { public int findCircleNum(int[][] isConnected) { int n = isConnected.length; int[] parent = new int[n], size = new int[n]; for (int i = 0; i < n; i++) { parent[i] = i; size[i] = 1; } int ans = n; for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (isConnected[i][j] == 1) { int a = find(parent, i), b = find(parent, j); if (a != b) { if (size[a] < size[b]) { int t = a; a = b; b = t; } parent[b] = a; size[a] += size[b]; ans--; } } return ans; } private int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; } }'''
J["p116"] = r'''import java.util.*;

class Solution { public List<Integer> numIslands2(int m, int n, int[][] positions) { int[][] d = {{1,0},{-1,0},{0,1},{0,-1}}; Map<Long,Long> parent = new HashMap<>(); List<Integer> ans = new ArrayList<>(); int count = 0; for (int[] pos : positions) { long key = pos[0] * 1_000_00L + pos[1]; if (parent.containsKey(key)) { ans.add(count); continue; } parent.put(key, key); count++; for (int[] p : d) { int a = pos[0] + p[0], b = pos[1] + p[1]; long nk = a * 1_000_00L + b; if (a >= 0 && a < m && b >= 0 && b < n && parent.containsKey(nk)) { long ra = find(parent, key), rb = find(parent, nk); if (ra != rb) { parent.put(ra, rb); count--; } } } ans.add(count); } return ans; } private long find(Map<Long,Long> p, long x) { while (p.get(x) != x) { p.put(x, p.get(p.get(x))); x = p.get(x); } return x; } }'''
J["p117"] = r'''import java.util.*;

class Solution { public List<List<String>> accountsMerge(List<List<String>> accounts) { Map<String,Integer> id = new HashMap<>(); List<String> emails = new ArrayList<>(); for (List<String> account : accounts) for (int i = 1; i < account.size(); i++) if (!id.containsKey(account.get(i))) { id.put(account.get(i), emails.size()); emails.add(account.get(i)); } int[] parent = new int[emails.size()]; for (int i = 0; i < parent.length; i++) parent[i] = i; for (List<String> account : accounts) for (int i = 2; i < account.size(); i++) union(parent, id.get(account.get(1)), id.get(account.get(i))); Map<Integer,TreeSet<String>> groups = new HashMap<>(); for (String email : emails) groups.computeIfAbsent(find(parent, id.get(email)), k -> new TreeSet<>()).add(email); List<List<String>> ans = new ArrayList<>(); for (var entry : groups.entrySet()) { List<String> row = new ArrayList<>(); row.add(accounts.stream().filter(a -> id.containsKey(a.get(1)) && find(parent, id.get(a.get(1))) == entry.getKey()).findFirst().orElseThrow().get(0)); row.addAll(entry.getValue()); ans.add(row); } return ans; } private int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; } private void union(int[] p, int a, int b) { a = find(p,a); b = find(p,b); if (a != b) p[a] = b; } }'''
J["p118"] = r'''class Solution { public boolean equationsPossible(String[] equations) { int[] parent = new int[26]; for (int i = 0; i < 26; i++) parent[i] = i; for (String eq : equations) if (eq.charAt(1) == '=') union(parent, eq.charAt(0) - 'a', eq.charAt(3) - 'a'); for (String eq : equations) if (eq.charAt(1) == '!' && find(parent, eq.charAt(0) - 'a') == find(parent, eq.charAt(3) - 'a')) return false; return true; } private int find(int[] p, int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; } private void union(int[] p, int a, int b) { a = find(p,a); b = find(p,b); if (a != b) p[a] = b; } }'''
J["p119"] = r'''class Solution { public int singleNumber(int[] nums) { int ans = 0; for (int x : nums) ans ^= x; return ans; } }'''
J["p120"] = r'''class Solution { public int[] countBits(int num) { int[] dp = new int[num + 1]; for (int i = 1; i <= num; i++) dp[i] = dp[i >> 1] + (i & 1); return dp; } }'''
J["p121"] = r'''class Solution { public int missingNumber(int[] nums) { int ans = nums.length; for (int i = 0; i < nums.length; i++) ans ^= i ^ nums[i]; return ans; } }'''
J["p122"] = r'''import java.util.*;

class ShuffleArray { private final int[] original; private int[] values; private final Random random = new Random(); public ShuffleArray(int[] nums) { original = nums.clone(); values = nums.clone(); } public int[] reset() { values = original.clone(); return values; } public int[] shuffle() { for (int i = values.length - 1; i > 0; i--) { int j = random.nextInt(i + 1); int t = values[i]; values[i] = values[j]; values[j] = t; } return values; } }'''
J["p123"] = r'''import java.util.concurrent.locks.*;

class BoundedQueue<T> { private final Object[] items; private int count, head, tail; private final Lock lock = new ReentrantLock(); private final Condition notFull = lock.newCondition(); private final Condition notEmpty = lock.newCondition(); public BoundedQueue(int capacity) { items = new Object[capacity]; } public void put(T item) throws InterruptedException { lock.lock(); try { while (count == items.length) notFull.await(); items[tail] = item; tail = (tail + 1) % items.length; count++; notEmpty.signal(); } finally { lock.unlock(); } } @SuppressWarnings("unchecked") public T get() throws InterruptedException { lock.lock(); try { while (count == 0) notEmpty.await(); T item = (T) items[head]; items[head] = null; head = (head + 1) % items.length; count--; notFull.signal(); return item; } finally { lock.unlock(); } } }'''
J["p124"] = r'''import java.util.*;

class FairScheduler {
    private static final class Task {
        long deadline, priority, sequence;
        String user, task;
    }

    private final PriorityQueue<Task> heap = new PriorityQueue<>((a,b) -> {
        if (a.deadline != b.deadline) return Long.compare(a.deadline, b.deadline);
        if (a.priority != b.priority) return Long.compare(a.priority, b.priority);
        return Long.compare(a.sequence, b.sequence);
    });
    private long sequence;
    private final Map<String,Long> usage = new HashMap<>();

    public void submit(String task, long deadline, String user, int basePriority) {
        Task item = new Task();
        item.deadline = deadline;
        item.priority = basePriority + usage.getOrDefault(user, 0L) * 1_000L;
        item.sequence = ++sequence;
        item.user = user;
        item.task = task;
        heap.offer(item);
    }

    public String nextTask() {
        Task item = heap.poll();
        if (item == null) return null;
        usage.merge(item.user, 1L, Long::sum);
        return item.task;
    }
}'''
JAVA_SOLUTIONS = J
