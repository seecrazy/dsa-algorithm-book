# 《数据结构与算法：从直觉到武器库》设计文档

## 1. 目标与非目标

### 目标

- 做一本可以部署到 GitHub Pages 的在线电子书。
- 讲清数据结构与算法的“是什么、为什么、何时用、怎么写错、怎么变强”。
- 内容覆盖线性结构、树、图、动态规划、贪心、分治、回溯、字符串、数学、并发/系统题型与工程化调试。
- 提供大量真实风格算法题，每题包含：难度、考点、题面、约束、示例、思路、复杂度、易错点、参考实现。
- 阅读体验专业但不僵硬：允许比喻、吐槽、生活化类比，但不牺牲精确性。
- 支持目录导航、全文搜索、阅读进度、暗色模式、代码块复制、移动端阅读。

### 非目标

- 第一版不做账号登录、云同步、评论系统和付费墙。
- 不承诺覆盖所有竞赛高级专题，如多项式乘法优化 DP、可持久化平衡树、高级群论构造题。
- 不绑定某个刷题平台；题目保留通用语义，不抓取或复制受版权保护的题库原文。
- 不把本书做成代码库生成器或在线评测系统；只做学习、检索和练习材料。

## 2. 目标读者

- 想系统补齐数据结构与算法的工程师。
- 准备技术面试，希望从模板走向举一反三的候选人。
- 有基础编程能力，但容易“看懂答案、自己写崩”的学习者。
- 希望把算法从考试知识转成工程直觉的读者。

## 3. 产品形态

- 纯静态站点，可托管在 GitHub Pages。
- 默认入口为 `index.html`。
- 章节正文使用 Markdown，存放于 `chapters/`。
- 题库索引和章节清单使用 JSON，存放于 `data/`。
- 前端使用原生 HTML/CSS/JavaScript，不引入运行时框架。
- 阅读器在浏览器内解析 Markdown；部署产物不需要 Node 构建。
- 本地开发使用任意静态服务器，例如 `python3 -m http.server 8000`。

## 4. 信息架构

### 顶层结构

1. 开篇：如何使用本书
2. 复杂度：性能的地图
3. 数组与双指针
4. 栈、队列与单调结构
5. 哈希表与计数
6. 链表与边界控制
7. 递归、分治与二分
8. 树与递归思维
9. 堆与优先队列
10. 图论：搜索、拓扑与连通性
11. 最短路、最小生成树与图建模
12. 回溯：排列、组合与搜索剪枝
13. 贪心：局部决策与全局证明
14. 动态规划：状态、转移与记忆
15. 字符串算法
16. 并查集与高级结构
17. 数学、位运算与概率思维
18. 工程化调试与面试作战手册
8. 排序：从比较到分桶
9. 树与递归思维
10. AVL 与红黑树
11. 堆与优先队列
12. B 树与 B+ 树
13. 图论：搜索、拓扑与连通性
14. 图的表示与建模选型
15. 最短路、最小生成树与图建模
16. 回溯：排列、组合与搜索剪枝
17. 分支限界
18. 贪心：局部决策与全局证明
19. 动态规划：状态、转移与记忆
20. Trie：前缀就是路径
21. 字符串算法
22. 并查集与高级结构
23. 数学、位运算与概率思维
24. 工程化调试与面试作战手册
25. 题库索引

### 章节正文约定

每章尽量包含：

- 一句直觉解释。
- 适合场景与反例场景。
- 核心不变量或证明要点。
- 常见模板。
- 陷阱清单。
- 若干道题。
- “举一反三”提示。

### 题目数据模型

```text
Problem {
  id: string
  title: string
  difficulty: easy | medium | hard
  tags: string[]
  chapter: string
  prompt: string
  constraints: string[]
  examples: { input: string, output: string, explanation?: string }[]
  solution: {
    idea: string
    complexity: string
    pitfalls: string[]
    code: { language: string, source: string }[]
  }
}
```

## 5. 用户流程

### 阅读流程

1. 用户访问站点首页。
2. 侧边栏展示章节目录与题库入口。
3. 点击章节后，前端加载对应 Markdown。
4. 页面记录最近章节和滚动进度。
5. 用户可切换亮暗主题。
6. 用户可通过搜索框查找章节标题、标签、题目和正文关键词。

### 练习流程

1. 用户进入章节，先看直觉和陷阱。
2. 点击题目卡片，题面默认可见。
3. 思路、复杂度、代码默认折叠，避免一眼看答案。
4. 用户自行尝试后展开参考解。
5. 题库页可按难度和主题筛选。
6. 已完成题目标记保存在浏览器本地。

## 6. 前端架构

- `index.html`：应用外壳、侧边栏、内容区、搜索控件。
- `assets/style.css`：版式、排版、暗色模式、响应式规则。
- `assets/app.js`：路由、数据加载、Markdown 渲染、搜索、状态管理。
- `data/chapters.json`：章节顺序与元数据。
- `data/problems.json`：题库与筛选索引。
- `chapters/*.md`：章节内容。
- 状态保存使用 `localStorage`，包括主题、最近章节、已完成题目标记。

### Markdown 支持范围

第一版渲染器支持：

- 标题、段落、有序/无序列表。
- 代码块与行内代码。
- 粗体、斜体、删除线和链接。
- 表格。
- 引用块。
- 分隔线。
- 任务清单。

不追求完整 CommonMark；遇到复杂 HTML 会转义，防止布局和注入问题。

## 7. 视觉与语气

- 版式偏书籍：较大正文行高、清晰标题层级、适度留白。
- 亮暗双主题。
- 代码块保持等宽字体和高对比。
- 标题采用“专业但不板正”的风格。
- 正文规则：比喻必须服务理解；关键结论用定义、复杂度和反例兜底。
- 避免炫技式名词堆砌；每个新概念给出动机。

## 8. 边界与错误处理

- Markdown 文件加载失败时显示可读错误，并提供返回目录。
- JSON 解析失败时显示配置错误，不白屏。
- 搜索输入为空时恢复默认目录。
- 未知路由回退到首页。
- 用户浏览器禁用 `localStorage` 时，阅读体验仍可用，只是不保存进度。
- 题库筛选条件组合为空时显示空态提示。
- 代码只用于展示；前端不执行用户输入代码。

## 9. SEO 与部署

- 提供 `robots.txt` 和 `sitemap.xml`。
- GitHub Pages 可通过“从分支部署”直接发布根目录。
- 推荐部署分支为 `main`，推荐发布目录为 `/ (root)`。
- 不依赖 GitHub Actions。
- 不使用 `.github/workflows/python-package.yml`；那是 Python 包测试模板，与纯静态站点无关。
- 如果未来改用 GitHub Actions 部署，应新增独立的 Pages workflow，而不是修改 Python package workflow。
- 站点内部链接使用相对路径，避免 project page 子路径问题。

## 10. 验收清单

- [x] 设计文档存在并解释目标、流程、状态、边界与部署。
- [x] 进展文档存在，反映已完成与未完成事项。
- [x] README 说明产品状态、本地运行、部署和文档入口。
- [x] 站点可在静态服务器中加载首页、章节和题库。
- [x] 固定 148 道通用算法题，且带有思路、复杂度和陷阱。
- [x] 章节目录、题库目录、正文链接一致。
- [x] 全文搜索可用。
- [x] 亮暗模式可用且状态保存。
- [x] 代码块可复制。
- [x] 移动端可读，侧边栏可开合。
- [x] GitHub Pages 相对路径访问无资源 404。

## 11. 协作与版本控制约束

- 项目必须使用本地 Git 仓库管理。
- 每个稳定交付节点都要本地提交；提交信息应说明设计、内容或运行时变化。
- 所有 GitHub 相关操作只允许停留在本地仓库层面；禁止执行 `git push`、`git pull`、`git fetch`、`gh repo create`、GitHub API 或任何远端写操作。
- `origin` 不是必需配置。若本地存在旧 remote，不得在本任务中主动使用或同步。
- 交付前的提交检查包括：代码与设计一致、ROADMAP 更新、README 可复现、无未暂存的临时产物。

## 12. 系统架构设计

### 12.1 上下文视图

```text
读者浏览器
  -> index.html 应用外壳
  -> assets/app.js 阅读器控制器
  -> data/chapters.json / data/problems.json 内容索引
  -> chapters/*.md 章节正文
  -> localStorage 主题、最近路由、掌握进度
GitHub Pages 静态文件服务只负责返回文件；不提供服务端计算。
```

### 12.2 运行时架构

- 形态：Hash Router + 内容加载器 + 本地渲染器 + 本地状态层。
- 不使用框架、包管理器和构建步骤。
- 部署单位是仓库根目录。
- 所有跨页面路由使用 `#/`，保证 GitHub Pages 子路径下无需服务器重写规则。
- 所有资源链接使用 `./` 相对路径。
- 站点启动时并发加载两个 JSON；章节正文按路由懒加载。
- 首页、题库页、题目页由内存数据同步渲染；章节页异步渲染。
- 用户输入 Markdown 或 JSON 不在前端执行，只做文本渲染。

### 12.3 模块边界

```text
Presentation  : index.html、assets/style.css
Controller    : assets/app.js 初始化与路由
Renderer      : assets/app.js Markdown 渲染器
Content Model : data/*.json
Source Text   : chapters/*.md
Persistence   : localStorage（可失败降级）
```

## 13. 详细文件设计

### 13.1 `/index.html`

职责：定义应用外壳和固定 DOM 锚点。

| 元素 / ID | 职责 |
|---|---|
| `#sidebar` | 桌面固定侧边栏，移动端通过 `body.sidebar-open` 抽屉显示 |
| `#theme-toggle` | 在 light/dark 间切换，并写入 localStorage |
| `#search` | 输入时过滤侧边栏章节与题目，不直接替换主内容 |
| `#nav` | 由 `renderNav()` 渲染分组目录和搜索结果 |
| `#sidebar-overlay` | 移动端遮罩，点击关闭抽屉 |
| `#menu-button` | 移动端打开抽屉 |
| `#content` | 主内容区域，所有路由 HTML 输出到这里 |

SEO 契约：静态 `title`、`description` 和 Book JSON-LD 必须存在；动态正文不做 SSR。

### 13.2 `/assets/style.css`

样式分为五层：

1. Design tokens：`--bg`、`--surface`、`--text`、`--primary` 等，dark 主题通过 `html[data-theme="dark"]` 覆盖。
2. Base reset 与排版：body 字体、行高、滚动行为。
3. Layout：`.app`、`.sidebar`、`.main`、`.content`。
4. Components：按钮、徽章、题目卡片、表格、代码块、筛选器。
5. Responsive/print：900px 以下抽屉化；打印隐藏交互元素。

关键类契约：

- `.badge.easy|medium|hard`：难度语义色。
- `.problem`：题目卡片。
- `.task-list`：Markdown 任务清单样式。
- `.sidebar-overlay`：仅在 `body.sidebar-open` 且移动端可见。
- `.code-copy`：必须出现在 `pre` 内，并携带 `data-copy`。

### 13.3 `/assets/app.js`

#### 全局状态

```ts
AppState {
  chapters: Chapter[]
  problems: Problem[]
  solved: Set<string>
  query: string
  difficulty: 'all' | 'easy' | 'medium' | 'hard'
  tag: string
}
```

localStorage keys：

| Key | 类型 | 说明 |
|---|---|---|
| `dsa.theme` | `"light" | "dark"` | 主题 |
| `dsa.solved` | `string[]` | 已掌握题目 ID |
| `dsa.last` | `string` | 最近章节路由 |

#### 方法清单

| 方法 | 输入 | 输出 / 副作用 | 错误契约 |
|---|---|---|---|
| `$` | selector、root | 返回第一个元素 | 无 |
| `storageGet` | key、fallback | JSON 解析值 | 解析失败返回 fallback |
| `storageSet` | key、value | 写入 localStorage | 配额或权限失败静默降级 |
| `setTheme` | theme | 设置 `data-theme` 并持久化 | 无 |
| `escapeHtml` | 任意文本 | HTML 实体转义 | 无 |
| `inline` | Markdown 行内文本 | 行内 HTML | 不允许执行 raw HTML |
| `renderMarkdown` | 多行 Markdown | block-level HTML | 支持声明子集，复杂 HTML 转义 |
| `difficultyBadge` | difficulty | 难度徽章 | 未知难度原样显示 |
| `problemCard` | Problem、compact | 题目摘要卡片 | 摘要缺失时回退题面 |
| `renderNav` | activeRoute | 渲染目录或搜索结果 | 查询为空恢复目录 |
| `fetchJson` | 相对路径 | JSON Promise | HTTP 非 2xx 抛错 |
| `fetchText` | 相对路径 | 文本 Promise | HTTP 非 2xx 抛错 |
| `homePage` | state | 首页 HTML | 无 |
| `chapterPage` | id | 异步章节 HTML | 章节缺失或文件加载失败显示错误面板 |
| `problemsPage` | state | 筛选后的题库 HTML | 空结果显示 `.empty` |
| `problemPage` | id | 题目详情 HTML | 未知 ID 显示错误面板 |
| `bindPageEvents` | 当前 DOM | 绑定复制、筛选、掌握按钮 | 每次渲染后只绑定当前节点 |
| `renderRoute` | 当前 hash | 主内容渲染 | 未知 hash 回退错误面板 |
| `initialize` | 无 | 加载数据、恢复状态、绑定全局事件 | JSON 初始化失败不白屏 |

#### Hash 路由契约

| Route | 页面 |
|---|---|
| `#/` | 首页 |
| `#/chapter/:id` | 章节页 |
| `#/problem/:id` | 题目详情 |
| `#/problems` | 题库筛选页 |
| 其他 | 错误面板 |

路由规则：

- `:id` 仅允许 `[\w-]+`，防止路径拼接歧义。
- 章节异步加载期间先显示 `.empty`。
- 题库筛选器变化时调用 `renderRoute({ preserveFilters: true })`，不重置滚动位置。
- 最近章节在进入 `#/chapter/:id` 成功发起读取前写入 `dsa.last`。

#### Markdown 渲染契约

按行解析，优先级从高到低：

1. fenced code：` ``` `
2. table：以 `|` 开头并以 `|` 结尾
3. heading：1-6 个 `#`
4. horizontal rule
5. blockquote：`>`
6. task list：`- [x]` / `- [ ]`
7. unordered list：`-`、`*`、`+`
8. ordered list：数字加 `.` 或 `)`
9. paragraph

行内解析顺序：HTML escape -> inline code -> bold/italic -> delete -> link。链接协议是 `http/https` 时加 `target="_blank" rel="noopener noreferrer"`。

#### 状态与事件生命周期

1. `initialize()` 恢复主题和 solved。
2. 并发加载 `chapters.json`、`problems.json`。
3. 渲染侧边栏，绑定 hash/search/theme/menu/overlay。
4. `renderRoute()` 根据 hash 生成页面。
5. `bindPageEvents()` 只绑定本次渲染生成的节点，避免全局委托重复绑定。
6. 掌握状态变化后重新渲染当前路由，并同步 localStorage。

### 13.4 `/scripts/generate_content.py`

职责：章节 Markdown 与 `data/chapters.json` 的可重放生成器。生成产物必须入库，不能要求部署环境执行 Python。

| 常量 / 方法 | 契约 |
|---|---|
| `ROOT` | 解析为仓库根目录，不依赖当前 shell 工作目录 |
| `CHAPTERS` | 有序章节元数据，顺序即学习顺序 |
| `CONTENT` | 章节正文源文本，key 必须是 `Chapter.id` |
| `build_chapter_metadata()` | 返回章节元数据副本/引用的有序数组 |
| `write_chapters()` | 合并 `NEW_CHAPTERS`、追加“一图看懂”、写入 24 个 Markdown、重写 `chapters.json` |
| `validate()` | 检查 ID 唯一、section 合法、正文齐全，孤儿文件仅警告 |
| `main()` | 写入、校验并输出生成数量 |

运行方式：`python3 scripts/generate_content.py`。生成后必须检查 `git diff`；不要把自动重排或无关换行混入提交。

### 13.5 `/scripts/generate_problems.py`

职责：生成并校验 `data/problems.json`。同样地，生成产物入库，脚本只用于本地维护。

| 常量 / 方法 | 契约 |
|---|---|
| `CHAPTER_IDS` | 与 `data/chapters.json` 当前章节集合一致的硬校验集合 |
| `add()` | 组装题目，必填 13 个字段；先写入 Python 参考实现 |
| `P` | 内存中的有序题库 |
| `validate(problems)` | 校验固定 148 题、ID 唯一、章节引用、难度、约束、示例、>=3 个陷阱和代码 |
| `main()` | 合并 `java_solutions.JAVA_SOLUTIONS`、校验双语言、写 JSON、输出按章节统计 |
| `scripts/java_solutions.py` | 以 `problem.id` 为键保存 Java 参考实现；`main()` 重跑时不得丢失 |
| `scripts/trace_diagrams.py` | `diagram_key()` 生成 `problem-<id>-trace.gif` 文件名；`trace_diagram_meta()` 返回题解图元数据；`trace_state_gif()` 渲染逐步动画 GIF |
| `scripts/generate_diagrams.py:main()` | 先为无手写图的题目生成 trace 动画 GIF，再重建手写章节/题解 PNG；当前为 123 张 GIF 和 46 张 PNG |
| `scripts/new_module_problems.py` | 定义 p125-p148 题目、Python 实现和 `NEW_JAVA`；不含前端运行时逻辑 |
| `scripts/validate_java.py` | 为 148 个 Java 片段注入共享类型并在唯一 package 中编译 |
| `scripts/validate_diagrams.py` | 校验 PNG/GIF 完整性（GIF 至少 2 帧）、章节引用、148 题图引用、五问法全覆盖和无未引用文件；拒绝任何残留 SVG 或 `-model` 占位图回潮 |
| `scripts/validate_java.py` | 为 148 个 Java 片段注入共享类型并在唯一 package 中编译 |

内容不变量补充：

- 当前题库固定为 148 题。
- 难度分布不是硬约束，但生成日志会输出，便于检查内容倾斜。
- 调整题库数量时，必须同步更新本节、README、首页文案、侧边栏文案和校验器预期值。

## 14. 数据模型与校验

### 14.1 `Chapter`

```ts
type ChapterSection = 'start' | 'structures' | 'techniques' | 'advanced';

interface Chapter {
  id: string;          // 语义化 slug，唯一
  title: string;       // 目录和 H1
  subtitle: string;    // 页面副标题
  section: ChapterSection;
  file: string;        // chapters/ 下文件名
  minutes: number;     // 预计阅读分钟
  tags: string[];
}
```

### 14.2 `Problem`

```ts
type Difficulty = 'easy' | 'medium' | 'hard';

interface ProblemExample {
  input: string;
  output: string;
  explanation?: string;
}

interface ProblemSolution {
  idea: string;
  complexity: string;
  pitfalls: string[];
  code: { language: string; source: string }[];
}

interface Problem {
  id: string;
  title: string;
  difficulty: Difficulty;
  tags: string[];
  chapter: string;      // 必须指向 Chapter.id
  summary?: string;     // 题库卡片一句话
  prompt: string;
  constraints: string[];
  examples: ProblemExample[];
  solution: ProblemSolution;
}
```

内容不变量：

- `Problem.id` 全局唯一。
- `Problem.chapter` 必须存在于 `Chapter.id`。
- 题目至少一个示例和三个易错点。
- 每题必须同时提供 Python 和 Java 两个参考实现。
- `summary` 若缺失，前端回退显示 `prompt`。

### 14.1a 视觉学习层

“一图胜千言”不是加装饰图，而是把抽象过程画成可追踪的状态图。项目由 Pillow 渲染 PNG/GIF，运行时零依赖，由 `scripts/generate_diagrams.py` 统一生成。

目标：

- 让读者先看到状态如何移动，再看代码如何实现。
- 把复杂度、指针、栈、哈希映射、递归树、DP 网格等抽象过程变成可见对象。
- 保持无构建部署：PNG/GIF 是最终产物，GitHub Pages 直接托管；浏览器 `<img>` 原生播放 GIF 动画。

视觉语言约定：

- 蓝色：当前重点/主指针。
- 绿色：已确定或安全的区域。
- 橙色：待处理状态。
- 红色：冲突、淘汰或非法路径。
- 灰色：背景/已处理过但不再重要的状态。
- 图内文字使用中文短句，图下使用说明字幕。
- 图必须表达“变化前后”或“查询/转移关系”，不接受只有标题的示意图。

实现约定：

- 章节图通过 Markdown 图片语法插入：`![说明](./assets/diagrams/xxx.png)`。
- 题解图存放在 `Problem.solution.understanding.diagram`：

```ts
interface ProblemDiagram {
  src: string;
  alt: string;
  caption: string;
}
```

- 前端在五问法块内渲染 `understanding.diagram`。
- 前端使用 `figure.diagram` 渲染，`img` 使用 `loading="lazy"`。
- Markdown 行内解析支持图片语法，但不允许用户输入执行 SVG/HTML。
- 当前生成 169 张图：46 张手写 PNG（21 张章节图 + 25 张题解图）和 123 张 trace 题解动画 GIF；148 题全部有题解专用图。

### 14.1b 图示渲染管线（Pillow）

图示由 Pillow 渲染，不再手写 SVG。管线分三层：

| 模块 | 职责 |
|---|---|
| `scripts/imdraw.py` | 绘图工具包：圆角盒、箭头、步骤圆片、多行注释框；所有坐标基于实测字宽（Hiragino Sans GB，缺字形自动回退 Arial Unicode），2x 超采样后缩输出；GIF 共享调色板防闪烁 |
| `scripts/static_diagrams.py` | 46 个手写图 builder（21 章节 + 25 题解），返回 `Diagram`，统一保存为 PNG |
| `scripts/trace_diagrams.py` | 题解动画：每个 trace 步骤一帧，当前步高亮、未来步幽灵占位、进度条 + 步骤计数，末帧加粗不变量框，导出 GIF |

约定：

- 语义配色沿用视觉语言：蓝=当前重点、绿=确定/安全、橙=待处理、红=冲突、紫=不变量。
- 盒内文字垂直居中、行高按字号 + 9px 计算；标题行加粗；正文色 `#475569`。
- `note_h()` 与 `note()` 必须传同一组参数，保证“先量高度再画布”不裁切。
- 本地渲染依赖：`python3 -m pip install --user pillow fonttools`（仅生成器需要，站点运行时零依赖）。

### 14.2a 题解理解层

题解不能只回答“用什么算法”。为了让一般读者达到“知其所以然”，题库逐步增加 `understanding` 字段：

```ts
interface ProblemUnderstanding {
  brute_force: string;        // 最直接的合法做法
  bottleneck: string;         // 慢在哪、重复在哪
  key_observation: string;    // 为什么可以换结构或剪枝
  why_correct: string;        // 正确性来自什么不变量或证明
  trace: string[];            // 示例逐步跟踪
  transfer: string[];         // 怎样迁移到同类题
}

Problem.solution.understanding?: ProblemUnderstanding;
```

题解渲染顺序固定为“五问法”：

1. **笨办法是什么？**先写一个正确但可能慢的解法。
2. **瓶颈在哪里？**指出重复计算、无意义枚举或错误搜索方向。
3. **关键观察是什么？**把约束转换成单调性、等价类、状态、依赖关系或不变量。
4. **为什么是对的？**说明每个循环/递归步骤维持什么不变量。
5. **怎么走一遍例子？**用小规模输入逐步追踪状态。

内容规则：

- 不允许只写“使用哈希表优化”这类结论，必须说明“记录什么、之后查什么、为什么查得到”。
- 不允许只写“动态规划”，必须说明状态含义和转移来源。
- 已升级题的 `trace` 至少 3 步，并使用示例中的具体值。
- 148 题已全部具备五问法；若未来新增题暂时缺失字段，前端显示通用五问脚手架，不允许伪装成已完整讲解。

### 14.3 内容索引

- `data/chapters.json` 是有序数组；数组顺序就是首页学习顺序。
- `data/problems.json` 是有序数组；数组顺序是题库默认展示顺序。
- 章节页自动按 `Problem.chapter` 注入“本章实战题”。
- 不需要额外双向索引文件；运行时从题库数组派生，避免索引漂移。

## 14.4 补充模块设计

为补齐教科书式覆盖，新增 6 个学习模块：

| id | 模块 | 必须覆盖 |
|---|---|---|
| `sorting` | 排序与选型 | 快排、归并、堆排、计数、基数、桶、稳定性、原地性、比较下界、工程选型 |
| `trie` | Trie 与前缀结构 | 节点模型、插入/查找/前缀统计、删除、Trie + DFS、压缩 Trie |
| `balanced-search-trees` | 自平衡搜索树 | BST 退化、AVL 四种旋转、红黑树五性质、插入重染色直觉、工程取舍 |
| `b-trees` | B 树 / B+ 树 | 阶/度、节点分裂、键与子指针、叶子链表、磁盘页与范围扫描 |
| `branch-and-bound` | 分支限界 | 状态空间、上界/下界、优先队列扩展、最优性剪枝、与回溯差异 |
| `graph-representation` | 图表示与建模 | 邻接表、矩阵、边数组、隐式图、空间/查询/遍历代价、反向图与网格图 |

这些模块先提供原理、模板、复杂度、陷阱和章节图；题库问题暂不强行迁移。后续若新增题目，必须沿用 Python/Java、五问法和题解图约定。

### 14.4d 全量五问法与 trace 驱动图（已完成）

剩余题已按统一批次补齐：

1. `p004-p124` 中尚无五问法的 107 题已补齐完整 `understanding`（`scripts/remaining_teaching_notes.py`）。
2. 五问法的 `trace` 不只用于文字说明，还作为题解专用图的输入。
3. 无手写专用图的题自动生成“trace 状态图”：标题来自题目，节点来自示例状态，边来自操作，底部展示不变量。
4. 该图与旧模型级图不同：内容引用该题的示例、状态和迁移，而不是只展示章节模型。
5. 完成后 148 题全部具备五问法与题解专用图；123 张旧 `problem-<id>-model.svg` 已删除，校验器拒绝模型占位图回潮。

### 14.4c 新增模块讲解批次 2

新增 p125-p148 的 24 题全部补齐 `understanding` 五问法，确保新模块不只停留在 API 和模板层面。同时将 8 个代表性题升级为手写专用图：

| id | 题目 | 视觉重点 |
|---|---|---|
| p125 | 颜色分类 | 三路分区边界移动 |
| p126 | 逆序对 | 归并跨越计数 |
| p130 | Trie | 前缀路径与 is_end |
| p132 | 单词搜索 II | Trie 与网格 DFS 同步 |
| p136 | 日程安排 | 有序区间前驱/后继冲突 |
| p137 | 右侧更小计数 | 离散化 BIT 查询/更新顺序 |
| p139 | B+ 树节点分裂 | 中间键上移与左右页 |
| p142 | 0/1 背包上界剪枝 | 分数背包上界与剪枝 |

### 14.4b 新增模块专属题库

为避免新章只讲概念，新增 24 题，总题库从 124 题扩到 148 题：

| 模块 | 题数 | 覆盖点 |
|---|---:|---|
| `sorting` | 5 | 三路分区、逆序对、桶排序、自定义稳定排序、字典序比较器 |
| `trie` | 5 | Trie API、通配符匹配、Trie + DFS、最短根替换、二进制 Trie |
| `balanced-search-trees` | 4 | 平衡 BST 构建、区间冲突、动态计数、BIT/Segment Tree 更新 |
| `b-trees` | 3 | 节点分裂、叶子范围扫描、相邻页合并 |
| `branch-and-bound` | 3 | 0/1 背包上界剪枝、TSP 状态空间、最小化最大段 |
| `graph-representation` | 4 | 容器转换、可达性、反向图、隐式网格图 |

新增题必须满足既有不变量：

- `id` 从 `p125` 到 `p148`，全局唯一。
- 每题有 Python 与 Java 参考。
- 每题至少一个约束、一个示例、三个易错点。
- 每题挂 `understanding.diagram` 题解专用图（手写图或 trace 图）。
- `validate()` 预期数量改为 148。

### 14.4a 新增模块图示

新增 6 章均有章节级 PNG：

- `sorting`：比较排序与非比较排序选型。
- `trie`：共享前缀路径。
- `balanced-search-trees`：AVL 旋转与中序不变量。
- `b-trees`：节点分裂与 B+ 树叶子链表。
- `branch-and-bound`：界剪枝。
- `graph-representation`：四种图容器对比。

## 14.5 题解图示策略（已升级为 trace 驱动）

首批 17 题与 8 个新模块代表题使用手写专用 PNG。其余题由 `scripts/trace_diagrams.py` 生成“题解跟踪动画”：

- 每题至少一个 GIF，文件名为 `problem-<id>-trace.gif`。
- 标题来自题目；副标题标注章节与“示例驱动”。
- 节点来自该题 `understanding.trace` 的每一步示例状态，按“初始（蓝）→ 中间（橙）→ 答案（绿）”着色。
- 边表示相邻步骤之间的操作；底部紫色块展示 `why_correct` 的不变量。
- 中文按实测字宽换行，图内文字不越界；校验器要求：148 题全部有题解图、五问法全覆盖、无残留 SVG、无未引用图片。

## 15. 错误处理矩阵

| 场景 | 行为 |
|---|---|
| JSON HTTP 失败 | `#content` 显示初始化失败面板 |
| 章节文件 HTTP 失败 | 只替换当前章节区域为错误面板 |
| 未知章节/题目 | 显示可返回首页的错误面板 |
| `localStorage` 被禁用 | 静默跳过保存，页面功能可用 |
| clipboard API 失败 | 按钮短暂显示“无法复制” |
| Markdown 不支持语法 | 按普通段落转义显示 |
| 搜索无结果 | 侧边栏显示无匹配；题库显示空态 |
| 移动端路由切换 | 自动关闭侧边栏 |

## 16. 可测试验收

### 数据验收

- 所有 JSON 可被 `JSON.parse`。
- 题目数量固定为 148。
- 每题 `chapter` 均有效。
- 题目 ID 无重复，目录文件无重复。
- 所有题目都有 Python 与 Java 两个参考实现，且 Java 片段可通过编译检查。
- `python3 -m py_compile scripts/*.py` 通过。
- `node --check assets/app.js` 通过。

### UI 冒烟

- 首页加载后侧边栏出现所有章节。
- 点击章节、题目、题库、首页均无路由错误。
- 搜索“动态规划”能命中相关章节与题目。
- 难度筛选、主题筛选和关键词组合可用。
- 代码复制按钮在安全上下文可用；失败有提示。
- 切换主题并刷新后主题保持。
- 标记掌握并刷新后状态保持。

### 部署验收

- `python3 -m http.server 8000` 下所有资源 200。
- GitHub Pages project page 子路径下相对资源不 404。
- 仓库根目录可直接作为 Pages 发布目录。

## 17. Pages 部署排障

- 根目录必须有 `index.html`。
- 根目录添加 `.nojekyll`，显式禁用 Jekyll 处理。
- 项目 Pages 地址必须包含仓库名：`https://<owner>.github.io/<repo>/`。
- 分支部署依赖 GitHub 自动运行的 `pages-build-deployment`；若 Actions 被禁用，需要启用 Actions。
- 若仓库为 private 且账户/组织套餐不支持 Pages，Pages 不能公开发布。
- 检查顺序：仓库根文件 → Settings → Pages URL → Actions 构建日志 → Environments 部署状态 → 浏览器无缓存访问。
