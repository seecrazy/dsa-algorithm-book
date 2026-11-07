(() => {
  'use strict';

  const $ = (selector, root = document) => root.querySelector(selector);
  const content = $('#content');
  const nav = $('#nav');
  const searchInput = $('#search');
  const themeToggle = $('#theme-toggle');
  const menuButton = $('#menu-button');
  const overlay = $('#sidebar-overlay');

  const state = {
    chapters: [],
    problems: [],
    searchIndex: [],
    solved: new Set(),
    query: '',
    difficulty: 'all',
    tag: 'all'
  };

  function storageGet(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key)) ?? fallback; }
    catch (_) { return fallback; }
  }

  function storageSet(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) { /* ignore */ }
  }

  function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    storageSet('dsa.theme', theme);
  }

  function escapeHtml(value = '') {
    return value
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function inline(value = '') {
    let out = escapeHtml(value);
    out = out.replace(/`([^`]+)`/g, (_, code) => `<code>${code}</code>`);
    out = out.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (_, alt, src) => {
      const safeSrc = escapeHtml(src);
      const external = /^https?:/i.test(src);
      return `<img src="${safeSrc}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async"${external ? ' referrerpolicy="no-referrer"' : ''}>`;
    });
    out = out.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    out = out.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');
    out = out.replace(/~~(.+?)~~/g, '<del>$1</del>');
    out = out.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (_, text, href) => {
      const safeHref = escapeHtml(href);
      const external = /^https?:/i.test(href);
      return `<a href="${safeHref}"${external ? ' target="_blank" rel="noopener noreferrer"' : ''}>${text}</a>`;
    });
    return out;
  }

  function renderMarkdown(markdown = '') {
    const lines = markdown.replace(/\r\n?/g, '\n').split('\n');
    let html = [];
    let index = 0;
    let inUnordered = false;
    let inOrdered = false;
    let tableBuffer = [];

    const closeList = () => {
      if (inUnordered) { html.push('</ul>'); inUnordered = false; }
      if (inOrdered) { html.push('</ol>'); inOrdered = false; }
    };

    const flushTable = () => {
      if (!tableBuffer.length) return;
      const rows = tableBuffer.map(line => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(cell => cell.trim()));
      const header = rows.shift();
      if (rows.length && /^:?-{2,}:?$/.test(rows[0][0] || '')) rows.shift();
      html.push('<table><thead><tr>');
      header.forEach(cell => html.push(`<th>${inline(cell)}</th>`));
      html.push('</tr></thead><tbody>');
      rows.forEach(row => {
        html.push('<tr>');
        row.forEach(cell => html.push(`<td>${inline(cell)}</td>`));
        html.push('</tr>');
      });
      html.push('</tbody></table>');
      tableBuffer = [];
    };

    while (index < lines.length) {
      const line = lines[index];

      if (/^\s*```/.test(line)) {
        closeList(); flushTable();
        const language = line.replace(/^\s*```/, '').trim();
        const source = [];
        index += 1;
        while (index < lines.length && !/^\s*```/.test(lines[index])) source.push(lines[index++]);
        index += 1;
        const encoded = escapeHtml(source.join('\n'));
        html.push(`<pre><button class="code-copy" type="button" data-copy="${encodeURIComponent(source.join('\n'))}">复制</button><code data-language="${escapeHtml(language)}">${encoded}</code></pre>`);
        continue;
      }

      if (/^\s*\|.*\|\s*$/.test(line)) {
        closeList();
        tableBuffer.push(line);
        index += 1;
        continue;
      }

      flushTable();

      if (!line.trim()) { closeList(); index += 1; continue; }

      const heading = line.match(/^(#{1,6})\s+(.+)$/);
      if (heading) {
        closeList();
        const level = Math.min(heading[1].length + 1, 6);
        html.push(`<h${level}>${inline(heading[2])}</h${level}>`);
        index += 1;
        continue;
      }

      if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) { closeList(); html.push('<hr>'); index += 1; continue; }

      if (/^\s*>\s?/.test(line)) {
        closeList();
        const quoted = [];
        while (index < lines.length && /^\s*>\s?/.test(lines[index])) quoted.push(lines[index++].replace(/^\s*>\s?/, ''));
        html.push(`<blockquote>${renderMarkdown(quoted.join('\n'))}</blockquote>`);
        continue;
      }

      const task = line.match(/^\s*[-*]\s+\[([ xX])\]\s+(.+)$/);
      if (task) {
        if (!inUnordered) { closeList(); html.push('<ul class="task-list">'); inUnordered = true; }
        html.push(`<li><input type="checkbox" disabled ${task[1].toLowerCase() === 'x' ? 'checked' : ''}> ${inline(task[2])}</li>`);
        index += 1;
        continue;
      }

      const unordered = line.match(/^\s*[-*+]\s+(.+)$/);
      if (unordered) {
        if (inOrdered) { html.push('</ol>'); inOrdered = false; }
        if (!inUnordered) { html.push('<ul>'); inUnordered = true; }
        html.push(`<li>${inline(unordered[1])}</li>`);
        index += 1;
        continue;
      }

      const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
      if (ordered) {
        if (inUnordered) { html.push('</ul>'); inUnordered = false; }
        if (!inOrdered) { html.push('<ol>'); inOrdered = true; }
        html.push(`<li>${inline(ordered[1])}</li>`);
        index += 1;
        continue;
      }

      closeList();
      const paragraph = [];
      while (index < lines.length && lines[index].trim() && !/^(#{1,6}\s|\s*```|\s*[-*+]\s|\s*\d+[.)]\s|\s*>\s?|\s*\|)/.test(lines[index])) paragraph.push(lines[index++]);
      if (paragraph.length) html.push(`<p>${inline(paragraph.join(' '))}</p>`);
      else index += 1;
    }

    closeList(); flushTable();
    return html.join('');
  }

  function difficultyBadge(difficulty) {
    const label = { easy: '简单', medium: '中等', hard: '困难' }[difficulty] || difficulty;
    return `<span class="badge ${escapeHtml(difficulty)}">${label}</span>`;
  }

  function problemCard(problem, compact = false) {
    const solved = state.solved.has(problem.id);
    return `
      <section class="problem" id="${escapeHtml(problem.id)}">
        <div class="problem-head">
          ${difficultyBadge(problem.difficulty)}
          <h3><a href="#/problem/${escapeHtml(problem.id)}">${escapeHtml(problem.title)}</a></h3>
          ${(problem.tags || []).slice(0, compact ? 2 : 4).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join('')}
          <div class="problem-actions">
            <a class="link-btn primary" href="#/problem/${escapeHtml(problem.id)}">打开</a>
            <button class="link-btn mark-solved ${solved ? 'solved' : ''}" type="button" data-id="${escapeHtml(problem.id)}">${solved ? '✓ 已掌握' : '标记掌握'}</button>
          </div>
        </div>
        <p>${escapeHtml(problem.summary || problem.prompt)}</p>
      </section>`;
  }

  function chapterLink(chapter) {
    return `<a href="#/chapter/${escapeHtml(chapter.id)}" data-route="#/chapter/${escapeHtml(chapter.id)}"><span>${escapeHtml(chapter.title)}</span><span class="mini">${chapter.minutes || 12} 分钟</span></a>`;
  }

  function renderNav(activeRoute = '#/') {
    if (state.query.trim()) {
      const q = state.query.toLowerCase();
      const chapters = state.chapters.filter(c => `${c.title} ${c.subtitle}`.toLowerCase().includes(q));
      const problems = state.problems.filter(p => `${p.title} ${(p.tags || []).join(' ')}`.toLowerCase().includes(q)).slice(0, 12);
      nav.innerHTML = `
        <div class="nav-group">章节</div>
        ${chapters.map(chapterLink).join('') || '<a><span>无匹配章节</span></a>'}
        <div class="nav-group">题目</div>
        ${problems.map(p => `<a href="#/problem/${escapeHtml(p.id)}"><span>${escapeHtml(p.title)}</span><span class="mini">${p.difficulty}</span></a>`).join('') || '<a><span>无匹配题目</span></a>'}
      `;
      return;
    }

    nav.innerHTML = `
      <div class="nav-group">开始阅读</div>
      <a href="#/" data-route="#/"><span>首页</span></a>
      ${state.chapters.filter(c => c.section === 'start').map(chapterLink).join('')}
      <div class="nav-group">核心结构</div>
      ${state.chapters.filter(c => c.section === 'structures').map(chapterLink).join('')}
      <div class="nav-group">核心思想</div>
      ${state.chapters.filter(c => c.section === 'techniques').map(chapterLink).join('')}
      <div class="nav-group">进阶与实战</div>
      ${state.chapters.filter(c => c.section === 'advanced').map(chapterLink).join('')}
      <div class="nav-group">练习</div>
      <a href="#/problems" data-route="#/problems"><span>${state.problems.length} 道题库索引</span><span class="mini">${state.solved.size} 已掌握</span></a>
    `;

    [...nav.querySelectorAll('a[data-route]')].forEach(a => a.classList.toggle('active', a.dataset.route === activeRoute));
  }

  function errorPanel(title, detail) {
    return `<div class="error-panel"><h2>${escapeHtml(title)}</h2><p>${escapeHtml(detail)}</p><p><a href="#/">返回首页</a></p></div>`;
  }

  async function fetchJson(path) {
    const response = await fetch(path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`${path} 加载失败：${response.status}`);
    return response.json();
  }

  async function fetchText(path) {
    const response = await fetch(path, { cache: 'no-cache' });
    if (!response.ok) throw new Error(`${path} 加载失败：${response.status}`);
    return response.text();
  }

  function homePage() {
    const solved = state.solved.size;
    return `
      <h1 class="page-title">数据结构与算法</h1>
      <p class="page-subtitle">从直觉到武器库 · 一本写给工程师的在线书</p>
      <p>这本书不准备让你背题，也不假装算法只是面试魔法。它想把每个结构还原成<strong>一个承诺</strong>：数组承诺随机访问，哈希承诺快速映射，堆承诺永远先给你最紧急的事，图承诺暴露世界里的依赖关系。</p>
      <div class="meta-grid">
        <div class="meta-card"><b>${state.chapters.length + 1} 个学习单元</b><span>从复杂度、平衡树、B+ 树到分支限界、图表示和工程调试。</span></div>
        <div class="meta-card"><b>${state.problems.length} 道实战题</b><span>题面、约束、思路、复杂度、易错点完整呈现。</span></div>
        <div class="meta-card"><b>0 构建依赖</b><span>纯静态站点，适合 GitHub Pages 直接部署。</span></div>
      </div>
      <h2>怎么读这本书</h2>
      <ul>
        <li><strong>第一次学：</strong>按目录顺序读，先看直觉，再抄模板，最后做题。</li>
        <li><strong>准备面试：</strong>直接进入题库，按难度和主题筛选；卡住再回章节。</li>
        <li><strong>复习模式：</strong>标记已掌握题，重点看“易错点”，把自己当成未来的 Bug 侦探。</li>
        <li><strong>读完目标：</strong>不是记住答案，而是看到新题时能问：状态是什么？顺序是什么？不变量是什么？代价在哪？</li>
      </ul>
      <h2>三条原则</h2>
      <ol>
        <li><strong>先说清问题，再谈解法。</strong>没有约束的最优解是玄学。</li>
        <li><strong>结构不是名词，是策略。</strong>选择结构就是选择访问、更新和删除的代价。</li>
        <li><strong>答案会过时，直觉会繁殖。</strong>一个模板后面应该站着一类题。</li>
      </ol>
      <blockquote><p>算法题的爽点不是写出巧技，而是在混乱约束中找到那个简单、可证明、可维护的秩序。</p></blockquote>
      <h2>当前进度</h2>
      <p class="progress-note">已掌握题目：<strong>${solved}</strong> / ${state.problems.length}。进度保存在本地浏览器，不上传服务器。</p>
    `;
  }

  async function chapterPage(id) {
    const chapter = state.chapters.find(item => item.id === id);
    if (!chapter) return errorPanel('章节不存在', `没有找到章节 ${id}。`);
    storageSet('dsa.last', `#/chapter/${id}`);
    try {
      const markdown = await fetchText(`./chapters/${chapter.file}`);
      const related = state.problems.filter(p => p.chapter === chapter.id);
      return `
        <h1 class="page-title">${escapeHtml(chapter.title)}</h1>
        <p class="page-subtitle">${escapeHtml(chapter.subtitle || '')}</p>
        <p class="progress-note">预计 ${chapter.minutes || 12} 分钟 · 关联题 ${related.length} 道</p>
        ${renderMarkdown(markdown)}
        ${related.length ? '<h2>本章实战题</h2>' + related.map(p => problemCard(p, true)).join('') : ''}
      `;
    } catch (error) {
      return errorPanel('章节加载失败', error.message);
    }
  }

  function problemsPage() {
    const tags = [...new Set(state.problems.flatMap(p => p.tags || []))].sort((a, b) => a.localeCompare(b, 'zh-CN'));
    const filtered = state.problems.filter(p => {
      const okDifficulty = state.difficulty === 'all' || p.difficulty === state.difficulty;
      const okTag = state.tag === 'all' || (p.tags || []).includes(state.tag);
      const q = state.query.trim().toLowerCase();
      const okQuery = !q || `${p.title} ${(p.tags || []).join(' ')} ${p.summary || ''}`.toLowerCase().includes(q);
      return okDifficulty && okTag && okQuery;
    });
    return `
      <h1 class="page-title">题库索引</h1>
      <p class="page-subtitle">${state.problems.length} 道通用算法题 · 每题都有思路、复杂度和陷阱</p>
      <div class="filters">
        <input id="problem-search" type="search" placeholder="搜索题名或标签" value="${escapeHtml(state.query)}">
        <select id="difficulty-filter">
          <option value="all">全部难度</option>
          <option value="easy" ${state.difficulty === 'easy' ? 'selected' : ''}>简单</option>
          <option value="medium" ${state.difficulty === 'medium' ? 'selected' : ''}>中等</option>
          <option value="hard" ${state.difficulty === 'hard' ? 'selected' : ''}>困难</option>
        </select>
        <select id="tag-filter">
          <option value="all">全部主题</option>
          ${tags.map(tag => `<option value="${escapeHtml(tag)}" ${state.tag === tag ? 'selected' : ''}>${escapeHtml(tag)}</option>`).join('')}
        </select>
      </div>
      <p class="progress-note">筛选结果 ${filtered.length} 题 · 已掌握 ${state.solved.size} 题。题目为原创语义描述，可对应到任意刷题平台练习。</p>
      ${filtered.length ? filtered.map(p => problemCard(p, true)).join('') : '<div class="empty">没有匹配的题目。换个主题，或把难度放回“全部”。</div>'}
    `;
  }

  function problemPage(id) {
    const p = state.problems.find(item => item.id === id);
    if (!p) return errorPanel('题目不存在', `题库中没有 ${id}。`);
    const solved = state.solved.has(id);
    const chapter = state.chapters.find(c => c.id === p.chapter);
    const understanding = p.solution && p.solution.understanding;
    const modelDiagram = p.solution && p.solution.diagram;
    const deepExplanation = understanding ? `
      <h2>从“看答案”到“知其所以然”</h2>
      ${understanding.diagram ? `
        <figure class="diagram">
          <img src="${escapeHtml(understanding.diagram.src)}" alt="${escapeHtml(understanding.diagram.alt)}" loading="lazy" decoding="async">
          <figcaption>${escapeHtml(understanding.diagram.caption)}</figcaption>
        </figure>` : ''}
      <div class="problem">
        <h3>第 1 问：笨办法是什么？</h3>
        <p>${escapeHtml(understanding.brute_force)}</p>
        <h3>第 2 问：瓶颈在哪里？</h3>
        <p>${escapeHtml(understanding.bottleneck)}</p>
        <h3>第 3 问：关键观察是什么？</h3>
        <p>${escapeHtml(understanding.key_observation)}</p>
        <h3>第 4 问：为什么这样是对的？</h3>
        <p>${escapeHtml(understanding.why_correct)}</p>
        <h3>第 5 问：示例怎么一步步走？</h3>
        <ol>${(understanding.trace || []).map(step => `<li>${escapeHtml(step)}</li>`).join('')}</ol>
        <h3>换一道题时怎么迁移？</h3>
        <ul>${(understanding.transfer || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
      </div>` : `
      <h2>从“看答案”到“知其所以然”</h2>
      ${modelDiagram ? `
        <figure class="diagram">
          <img src="${escapeHtml(modelDiagram.src)}" alt="${escapeHtml(modelDiagram.alt)}" loading="lazy" decoding="async">
          <figcaption>${escapeHtml(modelDiagram.caption)}</figcaption>
        </figure>` : ''}
      <div class="problem">
        <p>这题的完整五问讲解还在分批撰写中。先按下面的脚手架自己推导，比直接抄模板更有效：</p>
        <ol>
          <li><b>先写笨办法：</b>不用任何“技巧”，写一个正确但可能慢的做法。</li>
          <li><b>找出瓶颈：</b>哪里在重复计算？哪些组合注定不合法？</li>
          <li><b>找关键观察：</b>数据是否有序？是否需要记录历史？是否有依赖或单调性？</li>
          <li><b>检查不变量：</b>每次循环/递归前后，哪个性质必须保持？</li>
          <li><b>走小例子：</b>用规模 0、1、2 的输入手动追踪状态。</li>
        </ol>
      </div>`;
    return `
      <h1 class="page-title">${escapeHtml(p.title)}</h1>
      <p class="page-subtitle">${difficultyBadge(p.difficulty)} ${(p.tags || []).map(tag => `<span class="tag">${escapeHtml(tag)}</span>`).join(' ')}</p>
      <h2>题面</h2>
      <p>${escapeHtml(p.prompt)}</p>
      <h3>约束</h3>
      <ul>${(p.constraints || []).map(x => `<li>${escapeHtml(x)}</li>`).join('')}</ul>
      <h3>示例</h3>
      ${(p.examples || []).map((ex, i) => `
        <div class="problem">
          <b>示例 ${i + 1}</b>
          <pre><code>输入：${escapeHtml(ex.input)}
输出：${escapeHtml(ex.output)}${ex.explanation ? `\n解释：${escapeHtml(ex.explanation)}` : ''}</code></pre>
        </div>`).join('')}
      <details>
        <summary>思路、复杂度与易错点</summary>
        <h3>核心思路</h3><p>${escapeHtml(p.solution.idea)}</p>
        <h3>复杂度</h3><p>${escapeHtml(p.solution.complexity)}</p>
        <h3>易错点</h3><ul>${(p.solution.pitfalls || []).map(x => `<li>${escapeHtml(x)}</li>`).join('')}</ul>
      </details>
      ${deepExplanation}
      ${(p.solution.code || []).map(item => `<h3>${escapeHtml(item.language)} 参考</h3><pre><button class="code-copy" type="button" data-copy="${encodeURIComponent(item.source)}">复制</button><code>${escapeHtml(item.source)}</code></pre>`).join('')}
      <div class="problem-head">
        <a class="link-btn primary" href="#/problems">返回题库</a>
        ${chapter ? `<a class="link-btn" href="#/chapter/${escapeHtml(chapter.id)}">回看 ${escapeHtml(chapter.title)}</a>` : ''}
        <button class="link-btn mark-solved ${solved ? 'solved' : ''}" type="button" data-id="${escapeHtml(id)}">${solved ? '✓ 已掌握' : '标记掌握'}</button>
      </div>
    `;
  }

  function bindPageEvents() {
    const problemSearch = $('#problem-search');
    if (problemSearch) {
      problemSearch.addEventListener('input', event => {
        state.query = event.target.value;
        renderRoute({ preserveFilters: true });
      });
    }
    const difficultyFilter = $('#difficulty-filter');
    if (difficultyFilter) difficultyFilter.addEventListener('change', e => { state.difficulty = e.target.value; renderRoute({ preserveFilters: true }); });
    const tagFilter = $('#tag-filter');
    if (tagFilter) tagFilter.addEventListener('change', e => { state.tag = e.target.value; renderRoute({ preserveFilters: true }); });

    document.querySelectorAll('.code-copy').forEach(button => {
      button.addEventListener('click', async () => {
        const source = decodeURIComponent(button.dataset.copy || '');
        try {
          await navigator.clipboard.writeText(source);
          button.textContent = '已复制';
        } catch (_) {
          button.textContent = '无法复制';
        }
        setTimeout(() => { button.textContent = '复制'; }, 1400);
      });
    });

    document.querySelectorAll('.mark-solved').forEach(button => {
      button.addEventListener('click', () => {
        const id = button.dataset.id;
        if (state.solved.has(id)) state.solved.delete(id); else state.solved.add(id);
        storageSet('dsa.solved', [...state.solved]);
        renderRoute({ preserveFilters: true });
      });
    });
  }

  function renderRoute(options = {}) {
    const route = location.hash || '#/';
    const match = route.match(/^#\/chapter\/([\w-]+)$/);
    const problemMatch = route.match(/^#\/problem\/([\w-]+)$/);

    if (!options.preserveFilters) window.scrollTo({ top: 0, behavior: 'instant' });

    if (route === '#/' || route === '') {
      content.innerHTML = homePage();
    } else if (match) {
      content.innerHTML = '<div class="empty">正在加载章节…</div>';
      chapterPage(match[1]).then(html => {
        content.innerHTML = html;
        bindPageEvents();
        renderNav(route);
      });
    } else if (problemMatch) {
      content.innerHTML = problemPage(problemMatch[1]);
    } else if (route === '#/problems') {
      content.innerHTML = problemsPage();
    } else {
      content.innerHTML = errorPanel('页面不存在', `路由 ${route} 没有对应内容。`);
    }

    if (route !== '#/chapter/' + match?.[1]) renderNav(route);
    bindPageEvents();
    document.body.classList.remove('sidebar-open');
  }

  async function initialize() {
    setTheme(storageGet('dsa.theme', window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
    state.solved = new Set(storageGet('dsa.solved', []));

    try {
      const [chapters, problems] = await Promise.all([
        fetchJson('./data/chapters.json'),
        fetchJson('./data/problems.json')
      ]);
      state.chapters = chapters;
      state.problems = problems;
    } catch (error) {
      content.innerHTML = errorPanel('站点数据初始化失败', `${error.message}。请通过静态服务器访问，不要用 file:// 打开。`);
      return;
    }

    renderNav();
    window.addEventListener('hashchange', () => renderRoute());
    searchInput.addEventListener('input', event => {
      state.query = event.target.value;
      renderNav(location.hash);
    });
    themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));
    menuButton.addEventListener('click', () => document.body.classList.toggle('sidebar-open'));
    overlay.addEventListener('click', () => document.body.classList.remove('sidebar-open'));

    renderRoute();
  }

  initialize();
})();
