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

- 19 个学习单元规划：从复杂度地图到工程化调试。
- 124 道通用算法题：题面、约束、示例、思路、复杂度、易错点和参考实现。
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
│   ├── app.js                # 路由、Markdown 渲染、搜索、状态
│   └── style.css             # 设计 tokens、版式、组件和响应式
├── chapters/                 # 章节 Markdown 正文
├── data/
│   ├── chapters.json         # 有序章节索引
│   └── problems.json         # 有序题库索引
├── scripts/
│   ├── generate_content.py    # 章节与章节索引生成器
│   └── generate_problems.py   # 题库生成与硬校验器
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
- 新增题目必须填写难度、标签、章节、约束、示例、思路、复杂度、易错点和参考实现。
- 内容完成后更新 `docs/ROADMAP.md`、`README.md` 和 `HANDOFF.md`。
- 稳定节点执行本地 `git add` 与 `git commit`。

## 内容再生成

生成产物已入库；日常修改小段正文可直接编辑 `chapters/*.md` 或 `data/*.json`。结构性重排时使用生成器，并检查 diff：

```bash
python3 scripts/generate_content.py
python3 scripts/generate_problems.py
python3 -m py_compile scripts/*.py
node --check assets/app.js
```

## 部署排查

- 正确的项目 Pages 地址是：`https://<username>.github.io/<repo-name>/`。
- 本仓库应访问：`https://seecrazy.github.io/dsa-algorithm-book/`，不要只访问 `https://seecrazy.github.io/`。
- Pages 构建通常需要等待几十秒到几分钟；可在仓库 **Actions** 中查看自动触发的 `pages-build-deployment`。
- 仓库根目录包含 `.nojekyll`，用于跳过 Jekyll 处理，避免静态资源被误处理。
- 若 Actions 已禁用，分支部署可能不会触发；到 **Settings → Actions → General** 允许 Actions，或在 **Environments → github-pages** 查看部署状态。
