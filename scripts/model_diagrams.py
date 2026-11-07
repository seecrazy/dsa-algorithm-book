# -*- coding: utf-8 -*-
"""Model-level visual explanations for problems without hand-made diagrams."""
from html import escape


CHAPTER_MODELS = {
    "complexity": {
        "kind": "规模状态", "action": "把输入规模代入增长曲线", "result": "选择可承受复杂度",
        "invariant": "约束规模决定了哪些算法数量级可行。", "focus": "n 的量级是第一约束。",
    },
    "array-two-pointers": {
        "kind": "数组区间", "action": "移动 left / right 或写入 slow", "result": "保留有效前缀或答案区间",
        "invariant": "指针外区域已被证明不需要再考虑。", "focus": "明确每个指针边界含义。",
    },
    "stack-queue-monotonic": {
        "kind": "栈/队列状态", "action": "入栈、弹出或过期出队", "result": "保留仍可能产生答案的候选",
        "invariant": "结构内的候选都还未完成处理。", "focus": "淘汰不可能再优的旧候选。",
    },
    "hash-and-counting": {
        "kind": "哈希状态", "action": "写入键值或查询历史键", "result": "用 O(1) 查询替代重复扫描",
        "invariant": "键定义了对象等价关系。", "focus": "先设计 key，再设计容器。",
    },
    "linked-list": {
        "kind": "链表引用", "action": "改写 next / prev，移动指针", "result": "dummy 与快慢指针覆盖边界",
        "invariant": "已处理链段和新链段不断裂。", "focus": "先保存会被覆盖的引用。",
    },
    "recursion-divide-binary-search": {
        "kind": "搜索边界", "action": "缩小子问题或收缩 lo/hi", "result": "边界收敛到目标",
        "invariant": "两侧区域的可满足性已经确定。", "focus": "单调性比“取中间”更重要。",
    },
    "sorting": {
        "kind": "有序状态", "action": "分区、合并或按位分桶", "result": "全局顺序逐步确定",
        "invariant": "已完成部分与未处理部分边界清晰。", "focus": "稳定性和数据分布决定算法。",
    },
    "trees": {
        "kind": "子树答案", "action": "递归左子树和右子树", "result": "父节点合并两个子问题",
        "invariant": "子函数返回值覆盖整棵子树。", "focus": "先定义子树返回什么。",
    },
    "balanced-search-trees": {
        "kind": "平衡状态", "action": "旋转或重染色", "result": "恢复高度/黑高约束",
        "invariant": "中序顺序不因旋转改变。", "focus": "平衡是局部旋转换来的全局高度。",
    },
    "b-trees": {
        "kind": "节点页", "action": "查找节点、分裂或合并", "result": "树高稳定且叶子可顺序扫描",
        "invariant": "节点键数处于上下界之间。", "focus": "磁盘页大小决定分支因子。",
    },
    "trie": {
        "kind": "前缀路径", "action": "沿字符边移动", "result": "定位完整词或公共前缀",
        "invariant": "从根到节点是一条真实前缀。", "focus": "共享前缀只存一次。",
    },
    "heaps": {
        "kind": "优先级状态", "action": "插入、弹出或替换堆顶", "result": "堆顶始终是当前最优先项",
        "invariant": "父子优先级保持堆序。", "focus": "Top K 只维护最必要的 K 个候选。",
    },
    "graph-search": {
        "kind": "访问状态", "action": "扩散邻居或递归深入", "result": "连通性、层次或依赖顺序确定",
        "invariant": "已访问节点不会重复入队。", "focus": "先确认点、边、方向和权。",
    },
    "graph-shortest-mst": {
        "kind": "候选边集", "action": "松弛节点或选择安全边", "result": "最短距离/生成树逐步固定",
        "invariant": "已固定节点距离或生成树不被破坏。", "focus": "非负边权才能贪心固定。",
    },
    "graph-representation": {
        "kind": "图容器", "action": "添加点边或生成邻居", "result": "按查询模式选择容器",
        "invariant": "点、边、权与方向一致。", "focus": "先看空间，再看查询频率。",
    },
    "backtracking": {
        "kind": "选择路径", "action": "做选择、递归、撤销选择", "result": "合法解被完整枚举",
        "invariant": "撤销后状态与进入分支前一致。", "focus": "剪枝必须排除整棵不可能子树。",
    },
    "branch-and-bound": {
        "kind": "部分解界", "action": "估计上下界并扩展节点", "result": "不可能更优的子树被剪掉",
        "invariant": "界必须松弛且方向正确。", "focus": "尽早得到强上界，剪枝才有威力。",
    },
    "greedy": {
        "kind": "候选顺序", "action": "按排序键逐个选择", "result": "局部安全选择合并为全局解",
        "invariant": "选择后剩余子问题仍独立。", "focus": "贪心需要交换论证或反例检验。",
    },
    "dynamic-programming": {
        "kind": "DP 状态", "action": "从历史状态转移", "result": "目标状态包含最优值",
        "invariant": "状态定义覆盖子问题完整信息。", "focus": "先写状态，再看转移来源。",
    },
    "strings": {
        "kind": "匹配状态", "action": "扩展中心、移动索引或跳转前缀", "result": "重复结构被有效利用",
        "invariant": "已匹配前后缀关系保持一致。", "focus": "把文本看成状态转移。",
    },
    "union-find-advanced": {
        "kind": "连通分量", "action": "find 根节点并 union 合并", "result": "同根即同集合",
        "invariant": "每个节点只保存当前父引用。", "focus": "路径压缩与按大小合并缺一不可。",
    },
    "math-bit-probability": {
        "kind": "数值/位状态", "action": "异或、移位、模运算或抽样", "result": "利用奇偶与不变量求解",
        "invariant": "关键奇偶、总和或模值保持稳定。", "focus": "寻找操作中不变的量。",
    },
    "engineering-interview": {
        "kind": "系统状态", "action": "并发读写、缓存或调度", "result": "接口在约束内保持正确",
        "invariant": "共享状态修改受锁或顺序约束保护。", "focus": "先定义失败、超时和重入行为。",
    },
}

DEFAULT_MODEL = {
    "kind": "问题状态", "action": "维护状态并做出安全决策", "result": "在约束内得到答案",
    "invariant": "每一步都保持可验证的局部性质。", "focus": "先从小例子确认状态迁移。",
}


def diagram_key(problem_id: str) -> str:
    return f"problem-{problem_id}-model.svg"


def model_diagram(problem: dict, chapter_lookup=None) -> dict:
    chapter_id = problem.get("chapter", "")
    model = CHAPTER_MODELS.get(chapter_id, DEFAULT_MODEL)
    chapter_title = chapter_id
    if chapter_lookup:
        chapter = chapter_lookup.get(chapter_id)
        if chapter:
            chapter_title = chapter.get("title", chapter_id)
    focus = problem.get("summary") or problem.get("prompt", "")
    if len(focus) > 90:
        focus = focus[:88].rstrip() + "…"
    title = f"{problem.get('title', problem['id'])} · {model['kind']}"
    return {
        "src": f"./assets/diagrams/{diagram_key(problem['id'])}",
        "alt": f"{problem.get('title', problem['id'])} 的模型级状态图",
        "caption": f"{model['focus']} 不变量：{model['invariant']}",
        "title": title,
        "subtitle": f"模型：{chapter_title}",
        "kind": model["kind"],
        "action": model["action"],
        "result": model["result"],
        "focus": focus,
        "invariant": model["invariant"],
    }
