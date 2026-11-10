(() => {
  'use strict';

  const $ = (selector, root = document) => root.querySelector(selector);
  const content = $('#content');
  const nav = $('#nav');
  const searchInput = $('#search');
  const themeToggle = $('#theme-toggle');
  const menuButton = $('#menu-button');
  const overlay = $('#sidebar-overlay');

  const DAY_MS = 86400000;
  // 莱特纳式间隔（天）：记得 -> 下一档；忘了 -> 回到第 1 档
  const REVIEW_INTERVALS = [1, 2, 4, 7, 15, 30];
  const PLAN_DAYS = 30;
  const PLAN_STUDY_CAP = 6;
  const PLAN_REVIEW_CAP = 3;

  const state = {
    chapters: [],
    problems: [],
    solved: new Set(),
    review: {},
    graduated: 0,
    read: new Set(),
    planStart: null,
    searchIndex: null,
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

  // 与 scripts/generate_search_index.py 的 slugify/strip_inline 保持同一契约
  function stripMd(text = '') {
    return text
      .replace(/!\[([^\]]*)\]\(([^)]*)\)/g, '$1')
      .replace(/\[([^\]]+)\]\(([^)]*)\)/g, '$1')
      .replace(/`([^`]*)`/g, '$1')
      .replace(/(\*\*\*|\*\*|\*|~~)/g, '')
      .trim();
  }

  function slugify(text = '') {
    const slug = stripMd(text)
      .toLowerCase()
      .normalize('NFKC')
      .replace(/[^\p{L}\p{N}_]+/gu, '-')
      .replace(/^-+|-+$/g, '');
    return slug || 'section';
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

  function renderMarkdown(markdown = '', seen = {}) {
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

    const headingId = (text) => {
      const base = slugify(text);
      const count = seen[base] || 0;
      seen[base] = count + 1;
      return count === 0 ? base : `${base}-${count + 1}`;
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
        html.push(`<h${level} id="${escapeHtml(headingId(heading[2]))}">${inline(heading[2])}</h${level}>`);
        index += 1;
        continue;
      }

      if (/^\s*([-*_])\s*\1\s*\1[\s\-*_]*$/.test(line)) { closeList(); html.push('<hr>'); index += 1; continue; }

      if (/^\s*>\s?/.test(line)) {
        closeList();
        const quoted = [];
        while (index < lines.length && /^\s*>\s?/.test(lines[index])) quoted.push(lines[index++].replace(/^\s*>\s?/, ''));
        html.push(`<blockquote>${renderMarkdown(quoted.join('\n'), seen)}</blockquote>`);
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

  function reviewButton(problem) {
    const active = Boolean(state.review[problem.id]);
    return `<button class="link-btn toggle-review ${active ? 'reviewing' : ''}" type="button" data-action="toggle-review" data-id="${escapeHtml(problem.id)}">${active ? '⟳ 复习中' : '＋复习'}</button>`;
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
            ${reviewButton(problem)}
            <button class="link-btn mark-solved ${solved ? 'solved' : ''}" type="button" data-action="toggle-solved" data-id="${escapeHtml(problem.id)}">${solved ? '✓ 已掌握' : '标记掌握'}</button>
          </div>
        </div>
        <p>${escapeHtml(problem.summary || problem.prompt)}</p>
      </section>`;
  }

  function chapterLink(chapter) {
    return `<a href="#/chapter/${escapeHtml(chapter.id)}" data-route="#/chapter/${escapeHtml(chapter.id)}"><span>${escapeHtml(chapter.title)}</span><span class="mini">${chapter.minutes || 12} 分钟</span></a>`;
  }

  function dueCount() {
    const now = Date.now();
    return Object.values(state.review).filter(entry => entry.due <= now).length;
  }

  function planDayNumber() {
    if (!state.planStart) return null;
    return Math.min(PLAN_DAYS, Math.max(1, Math.floor((Date.now() - state.planStart) / DAY_MS) + 1));
  }

  function renderNav(activeRoute = '#/') {
    if (state.query.trim()) {
      const q = state.query.trim().toLowerCase();
      const chapters = state.chapters.filter(c => `${c.title} ${c.subtitle} ${(c.tags || []).join(' ')}`.toLowerCase().includes(q));
      const problems = state.problems.filter(p => `${p.title} ${(p.tags || []).join(' ')} ${p.summary || ''} ${p.prompt || ''}`.toLowerCase().includes(q)).slice(0, 10);
      const hits = (state.searchIndex || [])
        .filter(section => `${section.heading} ${section.chapterTitle} ${section.text}`.toLowerCase().includes(q))
        .slice(0, 8);
      nav.innerHTML = `
        <div class="nav-group">章节</div>
        ${chapters.map(chapterLink).join('') || '<a><span>无匹配章节</span></a>'}
        <div class="nav-group">题目</div>
        ${problems.map(p => `<a href="#/problem/${escapeHtml(p.id)}"><span>${escapeHtml(p.title)}</span><span class="mini">${p.difficulty}</span></a>`).join('') || '<a><span>无匹配题目</span></a>'}
        <div class="nav-group">正文命中 ${hits.length ? '' : state.searchIndex ? '' : '· 加载中'}</div>
        ${hits.map(section => `
          <a class="search-hit" href="#/chapter/${escapeHtml(section.chapter)}?h=${encodeURIComponent(section.slug)}">
            <span class="hit-title">${escapeHtml(section.heading)}</span>
            <span class="hit-snippet">${escapeHtml(snippet(section.text, q))}</span>
            <span class="mini">${escapeHtml(section.chapterTitle)}</span>
          </a>`).join('') || `<a><span>${state.searchIndex ? '正文没有匹配' : '首次搜索正在建立正文索引…'}</span></a>`}
      `;
      return;
    }

    const due = dueCount();
    const planDay = planDayNumber();
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
      <a href="#/review" data-route="#/review"><span>复习中心</span><span class="mini">${due ? `${due} 题到期` : `${Object.keys(state.review).length} 题在册`}</span></a>
      <a href="#/plan" data-route="#/plan"><span>30 天冲刺计划</span><span class="mini">${planDay ? `第 ${planDay} 天` : '未开始'}</span></a>
    `;

    [...nav.querySelectorAll('a[data-route]')].forEach(a => a.classList.toggle('active', a.dataset.route === activeRoute));
  }

  function snippet(text = '', q = '') {
    const at = text.toLowerCase().indexOf(q.toLowerCase());
    if (at < 0) return `${text.slice(0, 64)}…`;
    const start = Math.max(0, at - 24);
    return `${start > 0 ? '…' : ''}${text.slice(start, at + q.length + 56)}…`;
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

  function ensureSearchIndex() {
    if (state.searchIndex) return Promise.resolve();
    return fetchJson('./data/search-index.json')
      .then(payload => {
        state.searchIndex = payload.sections || [];
        if (state.query.trim()) renderNav(location.hash.split('?')[0]);
      })
      .catch(() => { state.searchIndex = []; });
  }

  function pagerNav(prev, next, kind) {
    if (!prev && !next) return '';
    return `
      <nav class="pager no-print" aria-label="${kind}导航">
        ${prev ? `<a class="pager-card prev" href="${escapeHtml(prev.href)}"><span class="pager-direction">← 上一${kind}</span><span class="pager-title">${escapeHtml(prev.title)}</span></a>` : '<span></span>'}
        ${next ? `<a class="pager-card next" href="${escapeHtml(next.href)}"><span class="pager-direction">下一${kind} →</span><span class="pager-title">${escapeHtml(next.title)}</span></a>` : '<span></span>'}
      </nav>`;
  }

  function homePage() {
    const solved = state.solved.size;
    const last = storageGet('dsa.last', null);
    const lastChapter = last && state.chapters.find(c => `#/chapter/${c.id}` === last);
    const due = dueCount();
    const planDay = planDayNumber();
    return `
      <h1 class="page-title">数据结构与算法</h1>
      <p class="page-subtitle">从直觉到武器库 · 一本写给工程师的在线书</p>
      ${lastChapter ? `
        <div class="continue-card no-print">
          <a href="${escapeHtml(last)}">继续阅读：${escapeHtml(lastChapter.title)}</a>
          <span class="mini">${lastChapter.minutes || 12} 分钟 · 上次读到这里</span>
        </div>` : ''}
      ${due ? `<div class="due-banner no-print"><a href="#/review">今天有 ${due} 题到期待复习</a></div>` : ''}
      <p>这本书不准备让你背题，也不假装算法只是面试魔法。它想把每个结构还原成<strong>一个承诺</strong>：数组承诺随机访问，哈希承诺快速映射，堆承诺永远先给你最紧急的事，图承诺暴露世界里的依赖关系。</p>
      <div class="meta-grid">
        <div class="meta-card"><b>${state.chapters.length + 1} 个学习单元</b><span>从复杂度、平衡树、B+ 树到分支限界、图表示和工程调试。</span></div>
        <div class="meta-card"><b>${state.problems.length} 道实战题</b><span>题面、约束、思路、复杂度、易错点完整呈现。</span></div>
        <div class="meta-card"><b>0 构建依赖</b><span>纯静态站点，适合 GitHub Pages 直接部署。</span></div>
      </div>
      <h2>怎么读这本书</h2>
      <ul>
        <li><strong>第一次学：</strong>按目录顺序读，先看直觉，再抄模板，最后做题。</li>
        <li><strong>准备面试：</strong>直接进入<a href="#/plan">30 天冲刺计划</a>或题库，按难度和主题筛选；卡住再回章节。</li>
        <li><strong>复习模式：</strong>把易错题<a href="#/review">加入复习中心</a>，按间隔重复节奏回顾；把自己当成未来的 Bug 侦探。</li>
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
      <p class="progress-note">已掌握题目：<strong>${solved}</strong> / ${state.problems.length}${state.graduated ? ` · 复习毕业 <strong>${state.graduated}</strong> 题` : ''}${planDay ? ` · 冲刺计划第 <strong>${planDay}</strong> 天（<a href="#/plan">查看</a>）` : ''}。进度保存在本地浏览器，不上传服务器。</p>
    `;
  }

  async function chapterPage(id) {
    const chapter = state.chapters.find(item => item.id === id);
    if (!chapter) return errorPanel('章节不存在', `没有找到章节 ${id}。`);
    storageSet('dsa.last', `#/chapter/${id}`);
    try {
      const markdown = await fetchText(`./chapters/${chapter.file}`);
      const related = state.problems.filter(p => p.chapter === chapter.id);
      const index = state.chapters.findIndex(item => item.id === id);
      const prev = index > 0 ? state.chapters[index - 1] : null;
      const next = index < state.chapters.length - 1 ? state.chapters[index + 1] : null;
      return `
        <h1 class="page-title">${escapeHtml(chapter.title)}</h1>
        <p class="page-subtitle">${escapeHtml(chapter.subtitle || '')}</p>
        <p class="progress-note">预计 ${chapter.minutes || 12} 分钟 · 关联题 ${related.length} 道
          <button class="link-btn no-print" type="button" data-action="print">打印本章</button>
          <button class="link-btn no-print ${state.read.has(id) ? 'solved' : ''}" type="button" data-action="toggle-read" data-id="${escapeHtml(id)}">${state.read.has(id) ? '✓ 已读' : '标记已读'}</button>
        </p>
        ${renderMarkdown(markdown)}
        ${related.length ? '<h2>本章实战题</h2>' + related.map(p => problemCard(p, true)).join('') : ''}
        ${pagerNav(prev && { href: `#/chapter/${prev.id}`, title: prev.title }, next && { href: `#/chapter/${next.id}`, title: next.title }, '章')}
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
      <div class="filters no-print">
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
      <p class="progress-note">筛选结果 ${filtered.length} 题 · 已掌握 ${state.solved.size} 题 · 复习在册 ${Object.keys(state.review).length} 题。题目为原创语义描述，可对应到任意刷题平台练习。</p>
      ${filtered.length ? filtered.map(p => problemCard(p, true)).join('') : '<div class="empty">没有匹配的题目。换个主题，或把难度放回“全部”。</div>'}
    `;
  }

  function problemPage(id) {
    const p = state.problems.find(item => item.id === id);
    if (!p) return errorPanel('题目不存在', `题库中没有 ${id}。`);
    const solved = state.solved.has(id);
    const chapter = state.chapters.find(c => c.id === p.chapter);
    const understanding = p.solution && p.solution.understanding;
    const index = state.problems.findIndex(item => item.id === id);
    const prev = index > 0 ? state.problems[index - 1] : null;
    const next = index < state.problems.length - 1 ? state.problems[index + 1] : null;
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
      <div class="problem-head no-print">
        <a class="link-btn primary" href="#/problems">返回题库</a>
        ${chapter ? `<a class="link-btn" href="#/chapter/${escapeHtml(chapter.id)}">回看 ${escapeHtml(chapter.title)}</a>` : ''}
        ${reviewButton(p)}
        <button class="link-btn mark-solved ${solved ? 'solved' : ''}" type="button" data-action="toggle-solved" data-id="${escapeHtml(id)}">${solved ? '✓ 已掌握' : '标记掌握'}</button>
      </div>
      ${pagerNav(prev && { href: `#/problem/${prev.id}`, title: prev.title }, next && { href: `#/problem/${next.id}`, title: next.title }, '题')}
    `;
  }

  function reviewEntryCard(entry, dueNow) {
    const interval = REVIEW_INTERVALS[Math.min(entry.stage, REVIEW_INTERVALS.length - 1)];
    const dayLabel = dueNow
      ? '今天到期'
      : `还有 ${Math.max(1, Math.ceil((entry.due - Date.now()) / DAY_MS))} 天`;
    return `
      <section class="problem review-card" id="review-${escapeHtml(entry.pid)}">
        <div class="problem-head">
          ${difficultyBadge(entry.problem.difficulty)}
          <h3><a href="#/problem/${escapeHtml(entry.pid)}">${escapeHtml(entry.problem.title)}</a></h3>
          <span class="tag">第 ${entry.stage + 1} 轮 · 间隔 ${interval} 天</span>
          ${entry.lapses ? `<span class="tag">忘了 ${entry.lapses} 次</span>` : ''}
          <span class="tag ${dueNow ? 'due' : ''}">${dayLabel}</span>
          <div class="problem-actions">
            ${dueNow ? `
              <button class="link-btn primary" type="button" data-action="review-remember" data-id="${escapeHtml(entry.pid)}">记得</button>
              <button class="link-btn" type="button" data-action="review-forget" data-id="${escapeHtml(entry.pid)}">忘了</button>` : ''}
            <button class="link-btn" type="button" data-action="toggle-review" data-id="${escapeHtml(entry.pid)}">移出复习</button>
          </div>
        </div>
        <p>${escapeHtml(entry.problem.summary || entry.problem.prompt)}</p>
      </section>`;
  }

  function reviewPage() {
    const now = Date.now();
    const entries = Object.entries(state.review)
      .map(([pid, entry]) => ({ pid, ...entry, problem: state.problems.find(p => p.id === pid) }))
      .filter(entry => entry.problem)
      .sort((a, b) => a.due - b.due);
    const due = entries.filter(entry => entry.due <= now);
    const upcoming = entries.filter(entry => entry.due > now).slice(0, 20);

    return `
      <h1 class="page-title">复习中心</h1>
      <p class="page-subtitle">错题不重做一遍就没用：按间隔重复节奏，直到每道题都能独立想起关键观察。</p>
      <div class="meta-grid">
        <div class="meta-card"><b>${due.length} 题今日到期</b><span>点“记得”进入更长间隔；点“忘了”回到第 1 轮。</span></div>
        <div class="meta-card"><b>${entries.length} 题在册</b><span>间隔序列：${REVIEW_INTERVALS.join(' → ')} 天。</span></div>
        <div class="meta-card"><b>${state.graduated} 题已毕业</b><span>走完全部间隔后自动移出复习队列。</span></div>
      </div>
      ${due.length ? `
        <h2>今日到期</h2>
        ${due.map(entry => reviewEntryCard(entry, true)).join('')}` : `
        <div class="empty">今天没有到期的复习题。${entries.length ? '下面的题还在间隔中，可以点开提前自测。' : '在题目页点“＋复习”，把易错题加入这里。'}</div>`}
      ${upcoming.length ? `
        <h2>间隔中</h2>
        ${upcoming.map(entry => reviewEntryCard(entry, false)).join('')}
        ${entries.length > upcoming.length ? `<p class="progress-note">还有 ${entries.length - upcoming.length} 题间隔较长，未列出。</p>` : ''}` : ''}
    `;
  }

  function buildPlan() {
    // 30 天 = [学 学 学 学 复] × 6：24 个学习日对应 24 章，6 个复习日巩固前四章
    const days = Array.from({ length: PLAN_DAYS }, (_, i) => (i % 5 === 4 ? { type: 'review', problems: [] } : { type: 'study', problems: [] }));
    const studyDays = days.map((day, i) => (day.type === 'study' ? i : -1)).filter(i => i >= 0);
    state.chapters.forEach((chapter, i) => {
      if (studyDays[i] === undefined) return;
      days[studyDays[i]].chapter = chapter;
      days[studyDays[i]].chapterIndex = i;
    });
    const load = days.map(() => 0);
    const capOf = day => (day.type === 'study' ? PLAN_STUDY_CAP : PLAN_REVIEW_CAP);
    state.chapters.forEach((chapter, i) => {
      if (studyDays[i] === undefined) return;
      let day = studyDays[i];
      for (const problem of state.problems.filter(p => p.chapter === chapter.id)) {
        while (day < days.length && load[day] >= capOf(days[day])) day += 1;
        if (day >= days.length) day = days.length - 1;
        days[day].problems.push(problem);
        load[day] += 1;
      }
    });
    days.forEach((day, i) => {
      if (day.type !== 'review') return;
      day.reviewChapters = days.filter((d, dj) => dj < i && d.chapter).map(d => d.chapter).slice(-4);
    });
    return days;
  }

  function planCompletion(days) {
    let total = 0;
    let done = 0;
    days.forEach(day => {
      if (day.chapter) {
        total += 1;
        if (state.read.has(day.chapter.id)) done += 1;
      }
      day.problems.forEach(problem => {
        total += 1;
        if (state.solved.has(problem.id)) done += 1;
      });
    });
    return { total, done };
  }

  function planPage() {
    const days = buildPlan();
    const { total, done } = planCompletion(days);
    const percent = total ? Math.round((done / total) * 100) : 0;
    const today = planDayNumber();
    const elapsed = state.planStart ? Math.max(1, Math.min(PLAN_DAYS, Math.floor((Date.now() - state.planStart) / DAY_MS) + 1)) : 0;

    const dayCard = (day, i) => {
      const number = i + 1;
      const isToday = today === number;
      const chapterBlock = day.type === 'study'
        ? (day.chapter ? `
            <div class="plan-chapter">
              <a href="#/chapter/${escapeHtml(day.chapter.id)}">${escapeHtml(day.chapter.title)}</a>
              <button class="link-btn ${state.read.has(day.chapter.id) ? 'solved' : ''}" type="button" data-action="toggle-read" data-id="${escapeHtml(day.chapter.id)}">${state.read.has(day.chapter.id) ? '✓ 已读' : '标记已读'}</button>
              <span class="mini">${day.chapter.minutes || 12} 分钟</span>
            </div>` : '')
        : `
            <div class="plan-chapter review-label">复习日：重读本周章节的陷阱清单，重做未掌握题</div>
            <div class="plan-review-links">${(day.reviewChapters || []).map(c => `<a class="tag" href="#/chapter/${escapeHtml(c.id)}">${escapeHtml(c.title)}</a>`).join('')}</div>`;
      const problems = day.problems.map(p => `
        <a class="plan-problem ${state.solved.has(p.id) ? 'done' : ''}" href="#/problem/${escapeHtml(p.id)}">
          ${difficultyBadge(p.difficulty)}<span>${escapeHtml(p.title)}</span><span class="plan-check">${state.solved.has(p.id) ? '✓' : ''}</span>
        </a>`).join('');
      const dayTotal = (day.chapter ? 1 : 0) + day.problems.length;
      const dayDone = (day.chapter && state.read.has(day.chapter.id) ? 1 : 0) + day.problems.filter(p => state.solved.has(p.id)).length;
      return `
        <section class="plan-day ${day.type} ${isToday ? 'today' : ''} ${dayDone >= dayTotal && dayTotal ? 'complete' : ''}" id="plan-day-${number}">
          <header class="plan-day-head">
            <span class="day-tag ${day.type}">${day.type === 'study' ? '学习' : '复习'}</span>
            <b>第 ${number} 天</b>
            ${isToday ? '<span class="tag due">今天</span>' : ''}
            <span class="mini">${dayTotal ? `${dayDone}/${dayTotal} 完成` : '轻量'}</span>
          </header>
          ${chapterBlock}
          ${problems ? `<div class="plan-problems">${problems}</div>` : ''}
        </section>`;
    };

    return `
      <h1 class="page-title">30 天冲刺计划</h1>
      <p class="page-subtitle">24 个学习日读完 24 章，每 5 天一个复习日；${state.problems.length} 道题按章节顺序摊进 30 天，日上限 ${PLAN_STUDY_CAP} 题（复习日 ${PLAN_REVIEW_CAP} 题）。</p>
      <div class="plan-toolbar no-print">
        ${state.planStart
          ? `<span class="progress-note">已进行 <strong>${elapsed}</strong> 天 · 总进度 <strong>${percent}%</strong>（${done}/${total} 项）</span>
             <button class="link-btn" type="button" data-action="plan-reset">重置计划进度</button>`
          : `<span class="progress-note">总进度 <strong>${percent}%</strong>（${done}/${total} 项）。点击开始后，会以今天为第 1 天高亮当前任务。</span>
             <button class="link-btn primary" type="button" data-action="plan-start">开始 30 天冲刺</button>`}
      </div>
      <div class="plan-progress" role="progressbar" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"><span style="width:${percent}%"></span></div>
      <div class="plan-grid">
        ${days.map(dayCard).join('')}
      </div>
      ${today && today < PLAN_DAYS ? '<p class="progress-note no-print">提示：每完成一项回到本页刷新进度；掌握状态与题库页共享。</p>' : ''}
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
  }

  function toggleSolved(id) {
    if (state.solved.has(id)) state.solved.delete(id); else state.solved.add(id);
    storageSet('dsa.solved', [...state.solved]);
  }

  function toggleReview(id) {
    if (state.review[id]) delete state.review[id];
    else state.review[id] = { stage: 0, due: Date.now(), lapses: 0, added: Date.now() };
    storageSet('dsa.review', state.review);
  }

  function reviewRemember(id) {
    const entry = state.review[id];
    if (!entry) return;
    entry.stage += 1;
    if (entry.stage >= REVIEW_INTERVALS.length) {
      delete state.review[id];
      state.graduated += 1;
      storageSet('dsa.graduated', state.graduated);
    } else {
      entry.due = Date.now() + REVIEW_INTERVALS[entry.stage] * DAY_MS;
    }
    storageSet('dsa.review', state.review);
  }

  function reviewForget(id) {
    const entry = state.review[id];
    if (!entry) return;
    entry.stage = 0;
    entry.lapses += 1;
    entry.due = Date.now() + REVIEW_INTERVALS[0] * DAY_MS;
    storageSet('dsa.review', state.review);
  }

  function toggleRead(id) {
    if (state.read.has(id)) state.read.delete(id); else state.read.add(id);
    storageSet('dsa.read', [...state.read]);
  }

  content.addEventListener('click', event => {
    const button = event.target.closest('[data-action]');
    if (!button) return;
    const { action, id } = button.dataset;
    if (action === 'toggle-solved') toggleSolved(id);
    else if (action === 'toggle-review') toggleReview(id);
    else if (action === 'review-remember') reviewRemember(id);
    else if (action === 'review-forget') reviewForget(id);
    else if (action === 'toggle-read') toggleRead(id);
    else if (action === 'print') { window.print(); return; }
    else if (action === 'plan-start') { state.planStart = Date.now(); storageSet('dsa.planStart', state.planStart); }
    else if (action === 'plan-reset') {
      if (!window.confirm('重置会清除开始日期；已掌握题目和已读标记保留。确定重置？')) return;
      state.planStart = null;
      storageSet('dsa.planStart', null);
    } else return;
    renderRoute({ preserveFilters: true });
  });

  function pagerTarget(direction) {
    const path = (location.hash || '#/').split('?')[0];
    const chapterMatch = path.match(/^#\/chapter\/([\w-]+)$/);
    const problemMatch = path.match(/^#\/problem\/([\w-]+)$/);
    if (chapterMatch) {
      const index = state.chapters.findIndex(c => c.id === chapterMatch[1]);
      const target = state.chapters[index + direction];
      return target ? `#/chapter/${target.id}` : null;
    }
    if (problemMatch) {
      const index = state.problems.findIndex(p => p.id === problemMatch[1]);
      const target = state.problems[index + direction];
      return target ? `#/problem/${target.id}` : null;
    }
    return null;
  }

  document.addEventListener('keydown', event => {
    const target = event.target;
    const typing = target && ((target.matches && target.matches('input, textarea, select')) || target.isContentEditable);
    if (event.key === '/' && !typing) {
      event.preventDefault();
      searchInput.focus();
      searchInput.select();
      return;
    }
    if (typing || event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    const href = pagerTarget(event.key === 'ArrowRight' ? 1 : -1);
    if (href) {
      event.preventDefault();
      location.hash = href;
    }
  });

  function renderRoute(options = {}) {
    const route = location.hash || '#/';
    const [path, queryString] = route.split('?');
    const anchor = queryString ? new URLSearchParams(queryString).get('h') : null;
    const chapterMatch = path.match(/^#\/chapter\/([\w-]+)$/);
    const problemMatch = path.match(/^#\/problem\/([\w-]+)$/);

    if (!options.preserveFilters) window.scrollTo({ top: 0, behavior: 'instant' });

    if (path === '#/' || path === '') {
      content.innerHTML = homePage();
      renderNav(path);
    } else if (chapterMatch) {
      content.innerHTML = '<div class="empty">正在加载章节…</div>';
      chapterPage(chapterMatch[1]).then(html => {
        content.innerHTML = html;
        bindPageEvents();
        renderNav(path);
        if (anchor) {
          const element = document.getElementById(anchor);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            element.classList.add('anchor-flash');
            setTimeout(() => element.classList.remove('anchor-flash'), 1800);
          }
        }
      });
    } else if (problemMatch) {
      content.innerHTML = problemPage(problemMatch[1]);
      renderNav(path);
    } else if (path === '#/problems') {
      content.innerHTML = problemsPage();
      renderNav(path);
    } else if (path === '#/review') {
      content.innerHTML = reviewPage();
      renderNav(path);
    } else if (path === '#/plan') {
      content.innerHTML = planPage();
      const today = planDayNumber();
      if (state.planStart && today) {
        const card = document.getElementById(`plan-day-${today}`);
        if (card) card.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      renderNav(path);
    } else {
      content.innerHTML = errorPanel('页面不存在', `路由 ${path} 没有对应内容。`);
      renderNav(path);
    }

    bindPageEvents();
    document.body.classList.remove('sidebar-open');
  }

  async function initialize() {
    setTheme(storageGet('dsa.theme', window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'));
    state.solved = new Set(storageGet('dsa.solved', []));
    state.review = storageGet('dsa.review', {}) || {};
    state.graduated = storageGet('dsa.graduated', 0) || 0;
    state.read = new Set(storageGet('dsa.read', []));
    state.planStart = storageGet('dsa.planStart', null);

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
      if (state.query.trim().length >= 2) ensureSearchIndex();
      renderNav(location.hash.split('?')[0]);
    });
    themeToggle.addEventListener('click', () => setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark'));
    menuButton.addEventListener('click', () => document.body.classList.toggle('sidebar-open'));
    overlay.addEventListener('click', () => document.body.classList.remove('sidebar-open'));

    renderRoute();
  }

  initialize();
})();
