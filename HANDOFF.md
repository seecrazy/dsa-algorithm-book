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

## 最近执行点

1. 已完成本地静态站点外壳：`index.html`、`assets/style.css`、`assets/app.js`。
2. 已把架构、文件、方法、数据模型、路由、Markdown 子集和错误契约写入 `docs/DESIGN.md`。
3. 待继续：生成 `data/chapters.json`、`data/problems.json` 和 `chapters/*.md`。
4. 生成内容后必须执行 JSON/题目引用/UI 冒烟检查，再更新 ROADMAP、README 并本地提交。

## Git 纪律

- 本项目所有 GitHub 操作只在本地 Git 仓库执行。
- 禁止 `git push`、`git pull`、`git fetch` 或调用远端服务。
- 每个稳定节点必须本地 commit，保证新会话可从提交历史和 HANDOFF 恢复上下文。
