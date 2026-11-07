# 数据结构与算法：从直觉到武器库

一本可直接部署到 GitHub Pages 的在线数据结构与算法电子书。目标是把复杂度、结构、模板、证明直觉和实战题放进同一个阅读流程，让读者不仅“看懂答案”，还能自己拆题。

## 当前状态

- 可运行的静态阅读器外壳已经完成。
- 章节目录、题库数据和正文内容正在按 `docs/DESIGN.md` 继续生成。
- 当前设计、进展和交接入口如下：
  - 设计总纲与详细设计：[`docs/DESIGN.md`](docs/DESIGN.md)
  - 进展与待办：[`docs/ROADMAP.md`](docs/ROADMAP.md)
  - 会话交接：[`HANDOFF.md`](HANDOFF.md)

## 功能

- 25 个学习单元规划：24 章正文 + 题库索引，从复杂度地图到平衡树、B+ 树、分支限界和工程化调试。
- 148 道通用算法题：题面、约束、示例、思路、复杂度、易错点，以及成对的 Python/Java 参考实现。
- 核心题增加“五问法”讲解：笨办法、瓶颈、关键观察、正确性、示例跟踪与迁移；其余题先提供模型级状态图和推导脚手架，正在分批补齐。
- 24 章覆盖新增排序、Trie、AVL/红黑树、B/B+ 树、分支限界和图表示；核心章节与全部题解均含静态 SVG 状态图。
- 纯静态阅读器：目录导航、Hash 路由、题库筛选、全文搜索、暗色模式和本地进度。
- 无运行时框架、无包安装、无构建步骤。
- 响应式桌面/移动端排版，支持打印样式。

## 本地运行

站点通过 `fetch` 加载内容，必须使用静态服务器，不要直接双击 `index.html`。

```bash
python3 -m http.server 8000
```

打开：

```text
http://localhost:8000
```

## 目录结构

```text
.
├── index.html                # 应用外壳
├── assets/
│   ├── diagrams/             # 由脚本生成的静态 SVG 图示
│   ├── app.js                # 路由、Markdown 渲染、搜索、状态
│   └── style.css             # 设计 tokens、版式、组件和响应式
├── chapters/                 # 24 个章节 Markdown 正文
├── data/
│   ├── chapters.json         # 有序章节索引
│   └── problems.json         # 有序题库索引
├── scripts/
│   ├── generate_content.py    # 章节与章节索引生成器
│   ├── generate_problems.py   # 题库生成与硬校验器
│   ├── java_solutions.py     # 初始 124 题的 Java 参考实现
│   ├── new_module_problems.py # 新增模块的 24 题与 Java 实现
│   ├── teaching_notes.py     # 核心题的五问式深度讲解
│   ├── model_diagrams.py     # 模型状态图元数据
│   ├── generate_diagrams.py  # 生成章节图、手写题图与模型状态图
│   └── validate_diagrams.py  # 校验 SVG 与图引用
├── docs/
│   ├── DESIGN.md             # 产品、架构、系统与详细设计
│   └── ROADMAP.md            # 已完成、进行中和 backlog
├── HANDOFF.md                # 会话交接和最近执行点
├── robots.txt
└── sitemap.xml
```

## 部署到 GitHub Pages

推荐使用 GitHub 仓库页面手动配置“从分支部署”：

1. Repository: **Settings → Pages**。
2. Source: **Deploy from a branch**。
3. Branch: `main`。
4. Folder: `/ (root)`。
5. Save。

本项目当前遵守本地 Git 纪律：只维护本地仓库和历史，不在自动化会话中执行 push/pull/fetch 或调用远端 API。

### 关于 CI workflow

仓库不保留 `.github/workflows/python-package.yml`。它是 Python 包测试模板，会尝试安装 `pytest` 并运行测试；本项目是纯静态站点，没有包构建和 pytest 测试。部署选择 **Deploy from a branch** 时，GitHub Actions 不参与发布流程。

如果未来需要 CI 或自动部署，应新增独立的 `static.yml` / Pages workflow，而不是把 Python package workflow 改成发布器。

## 开发约定

- 修改产品行为前，先更新 `docs/DESIGN.md`。
- 新增或调整章节时，同步维护 `data/chapters.json` 和章节 Markdown。
- 新增题目必须填写难度、标签、章节、约束、示例、思路、复杂度、易错点，并同时提供 Python 与 Java 参考。
- 内容完成后更新 `docs/ROADMAP.md`、`README.md` 和 `HANDOFF.md`。
- 稳定节点执行本地 `git add` 与 `git commit`。

## 内容再生成

生成产物已入库；日常修改小段正文可直接编辑 `chapters/*.md` 或 `data/*.json`。结构性重排时使用生成器，并检查 diff：

```bash
python3 scripts/generate_content.py
python3 scripts/generate_diagrams.py
python3 scripts/generate_problems.py
python3 scripts/validate_diagrams.py
python3 scripts/validate_java.py
python3 -m py_compile scripts/*.py
node --check assets/app.js
```

## 部署排查

- 正确的项目 Pages 地址是：`https://<username>.github.io/<repo-name>/`。
- 本仓库应访问：`https://seecrazy.github.io/dsa-algorithm-book/`，不要只访问 `https://seecrazy.github.io/`。
- Pages 构建通常需要等待几十秒到几分钟；可在仓库 **Actions** 中查看自动触发的 `pages-build-deployment`。
- 仓库根目录包含 `.nojekyll`，用于跳过 Jekyll 处理，避免静态资源被误处理。
- 若 Actions 已禁用，分支部署可能不会触发；到 **Settings → Actions → General** 允许 Actions，或在 **Environments → github-pages** 查看部署状态。
