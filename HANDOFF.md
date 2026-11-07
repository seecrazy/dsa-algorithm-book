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
6. 已实现视觉学习层：169 个静态 SVG；14 个核心章节含 16 个引用，148 题全部有题解图（25 张手写专用题图 + 123 张模型状态图；另有 20 个章节图，共 169 个 SVG）；引用可通过 `scripts/validate_diagrams.py` 校验。
7. 已完成核心模块覆盖审计，并补齐排序、Trie、AVL/红黑树、B/B+ 树、分支限界和图表示章。
8. 新增 p125-p148 共 24 题，总题库 148；新增 `scripts/validate_java.py`，148 个 Java 片段编译通过。
9. 已抽查 p125-p148 的 Python 实现示例，修复了 B+ 树页合并、Trie 回溯示例和分支限界溢出问题。
10. 已为 p125-p148 全部补齐五问法；为 p125/p126/p130/p132/p136/p137/p139/p142 升级手写图。
11. 下一件事是浏览器端人工冒烟：首页、章节、题库、题目、搜索、主题、双语言代码块、移动端与掌握状态。：首页、章节、题库、题目、搜索、主题、双语言代码块、移动端与掌握状态。

## Git 纪律

- 本项目所有 GitHub 操作只在本地 Git 仓库执行。
- 禁止 `git push`、`git pull`、`git fetch` 或调用远端服务。
- 每个稳定节点必须本地 commit，保证新会话可从提交历史和 HANDOFF 恢复上下文。
