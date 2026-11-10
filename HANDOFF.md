# 会话交接

## 当前状态

项目已经具备可部署的静态电子书骨架：

- 入口：`index.html`
- 样式：`assets/style.css`
- 阅读器逻辑：`assets/app.js`
- 章节正文：`chapters/*.md`
- 目录：`data/chapters.json`
- 题库：`data/problems.json`
- 设计依据：`docs/DESIGN.md`
- 进展：`docs/ROADMAP.md`
- 运行与部署：`README.md`

## 继续工作入口

1. 改章节内容：编辑 `chapters/` 下对应 Markdown。
2. 新增题目：编辑 `data/problems.json`，保持 `id` 唯一。
3. 调整目录：同步更新 `data/chapters.json` 和侧边栏数据。
4. 改阅读体验：优先改 `assets/app.js` 与 `assets/style.css`。
5. 发布：将仓库推送到 GitHub，在 Pages 设置中选择 `main` 分支根目录。

## 约定

- 不引入运行时框架和构建依赖。
- Markdown 只使用设计文档中声明支持的语法。
- 题目必须包含思路、复杂度和易错点。
- 改产品行为前，先更新 `docs/DESIGN.md`。
- 图不是装饰，必须表达状态迁移、指针移动、查询关系或递归/DP 转移。
- 题解必须逐步升级为“五问法”：笨办法、瓶颈、关键观察、正确性、示例跟踪；只有方法名不算合格题解。
- 不保留 `python-package.yml`；Pages 当前采用分支部署模型，不需要 Python package CI。

## 最近执行点

1. 已完成本地静态站点外壳：`index.html`、`assets/style.css`、`assets/app.js`。
2. 已生成 24 个章节 Markdown 与 `data/chapters.json`，新增排序、Trie、AVL/红黑树、B/B+ 树、分支限界和图表示。
3. 已生成 `data/problems.json`，固定 148 题；每题包含约束、示例、思路、复杂度、至少三个易错点。每题已同时包含 Python 和 Java 两个参考实现；148 个 Java 片段已通过 javac 编译检查。
4. 已通过 `py_compile`、`node --check`、JSON 数量、ID 唯一性和章节引用校验。
5. 设计文档已覆盖运行时文件、生成器、核心方法、路由和错误契约。
6. 视觉学习层已迁移到 Pillow 渲染管线：169 张图 = 21 张章节 PNG + 25 张手写题解 PNG + 123 张 trace 题解动画 GIF（约 15MB）；所有定位基于实测字宽，148 题全部有题解专用图；引用可通过 `scripts/validate_diagrams.py` 校验。
7. 24 章正文完成全量体检与深化（2026-11-08）：动态规划补背包倒序不变量与 LIS tails 论证；排序换原地分区快排 + 三路分区 + 稳定计数排序；字符串补 KMP 匹配主循环与 next 示例；平衡树补左旋与红黑两倍界推导；B 树补键-指针关系与 I/O 实例；Trie 补删除代码与压缩 Trie；图搜索补 Tarjan 直觉与二分图染色；并查集补 BIT 模板；分支限界补主循环伪码与下界合法性；复杂度补 Θ/Ω 与递归树展开；how-to-use 按 24 章口径重写快速路线；另补贪心反例、最小栈、BST LCA、O(n) 建堆、子集型辨析、快速幂、LFU 结构。改动全部落在 `scripts/generate_content.py` 与 `scripts/new_modules.py`。
8. 新增 p125-p148 共 24 题，总题库 148；新增 `scripts/validate_java.py`，148 个 Java 片段编译通过。
9. M7 已完成：`scripts/remaining_teaching_notes.py` 补齐剩余 107 题五问法；`scripts/trace_diagrams.py` 用五问法 trace 生成 123 张题解动画 GIF；全部旧 SVG（含 `problem-*-model.svg` 占位图）已删除，校验器拒绝回潮。
10. 本地渲染依赖：`python3 -m pip install --user pillow fonttools`（仅生成器需要）。
11. 生成器重跑哈希一致（幂等）；`py_compile`、`node --check`、`validate_diagrams.py`、`validate_java.py` 全部通过；169 个被引用资源 HTTP 200。
12. 浏览器端人工冒烟（2026-11-10，M8 收口完成）：首页、章节、题库、题目、搜索、主题、双语言代码块、GIF 动画播放、移动端与掌握状态。
13. M8 学习闭环升级（2026-11-10）：新增 `scripts/generate_search_index.py` 与 `data/search-index.json`（24 章 197 小节，幂等）；`assets/app.js` 升级——复习中心 `#/review`（莱特纳间隔 1/2/4/7/15/30 天）、30 天冲刺计划 `#/plan`（24 学习日 + 6 复习日、题目确定性摊排）、全文搜索（惰性加载索引、片段预览、`?h=` 锚点高亮）、章节/题目上下页、首页继续阅读（启用 `dsa.last`）、`/` 与 `←`/`→` 快捷键、打印本章。
14. M8 文档同步：DESIGN.md 修复顶层结构编号错乱并新增 13.6 生成器契约与 14.3 数据模型；index.html 修 124→148 过时 meta；ROADMAP/README 对齐口径。
15. 下一件事：backlog 剩余项——每章可视化/可交互演示、章节模板 Java 版、UI 自动化冒烟、错题原因笔记。

## Git 纪律

- 本项目所有 GitHub 操作只在本地 Git 仓库执行。
- 禁止 `git push`、`git pull`、`git fetch` 或调用远端服务。
- 每个稳定节点必须本地 commit，保证新会话可从提交历史和 HANDOFF 恢复上下文。
