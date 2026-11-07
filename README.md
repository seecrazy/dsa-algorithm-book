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
- 120 道通用算法题：题面、约束、示例、思路、复杂度、易错点和参考实现。
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

## 开发约定

- 修改产品行为前，先更新 `docs/DESIGN.md`。
- 新增或调整章节时，同步维护 `data/chapters.json` 和章节 Markdown。
- 新增题目必须填写难度、标签、章节、约束、示例、思路、复杂度、易错点和参考实现。
- 内容完成后更新 `docs/ROADMAP.md`、`README.md` 和 `HANDOFF.md`。
- 稳定节点执行本地 `git add` 与 `git commit`。
