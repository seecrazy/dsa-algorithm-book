#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate static SVG visual explanations for chapters and core problems."""
from html import escape
from pathlib import Path
import json

from model_diagrams import diagram_key, model_diagram

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "diagrams"

CSS = """
.panel{fill:#fff;stroke:#cbd5e1;stroke-width:2}
.box{stroke-width:2}
.plain{fill:#f8fafc;stroke:#94a3b8}
.blue{fill:#dbeafe;stroke:#2563eb}
.green{fill:#dcfce7;stroke:#059669}
.orange{fill:#ffedd5;stroke:#d97706}
.red{fill:#fee2e2;stroke:#dc2626}
.purple{fill:#ede9fe;stroke:#7c3aed}
.line{stroke:#64748b;stroke-width:2;fill:none}
.arrow{stroke:#334155;stroke-width:2;fill:none;marker-end:url(#arrow)}
.flow{stroke:#2563eb;stroke-width:3;fill:none;marker-end:url(#blue-arrow)}
.bad{stroke:#dc2626;stroke-width:3;fill:none;marker-end:url(#red-arrow)}
.good{stroke:#059669;stroke-width:3;fill:none;marker-end:url(#green-arrow)}
.t{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC','PingFang SC',sans-serif;font-size:17px;fill:#111827;text-anchor:middle;font-weight:650}
.s{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC','PingFang SC',sans-serif;font-size:14px;fill:#475569;text-anchor:middle}
.small{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC','PingFang SC',sans-serif;font-size:13px;fill:#64748b;text-anchor:middle}
.axis{stroke:#94a3b8;stroke-width:2}
.title{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif;font-size:21px;fill:#0f172a;text-anchor:start;font-weight:800}
"""

def svg(width, height, body):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">
<title id="t">算法状态图</title><desc id="d">可视化算法状态迁移</desc>
<defs>
<marker id="arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#334155"/></marker>
<marker id="blue-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#2563eb"/></marker>
<marker id="green-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#059669"/></marker>
<marker id="red-arrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 Z" fill="#dc2626"/></marker>
</defs>
<style>{CSS}</style>
<rect class="panel" x="10" y="10" width="{width-20}" height="{height-20}" rx="18"/>
{body}
</svg>
'''

def rect(x, y, w, h, cls="plain", rx=12):
    return f'<rect class="box {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'

def node(x, y, w, h, label, cls="plain", sub=None):
    parts = [rect(x, y, w, h, cls)]
    if sub:
        parts += [f'<text class="t" x="{x+w/2}" y="{y+h/2-2}">{escape(str(label), quote=False)}</text>',
                  f'<text class="small" x="{x+w/2}" y="{y+h/2+19}">{escape(str(sub), quote=False)}</text>']
    else:
        parts += [f'<text class="t" x="{x+w/2}" y="{y+h/2+6}">{escape(str(label), quote=False)}</text>']
    return ''.join(parts)

def text(x, y, label, cls="s"):
    return f'<text class="{cls}" x="{x}" y="{y}">{escape(str(label), quote=False)}</text>'

def path(points, cls="arrow"):
    points = [p if isinstance(p, tuple) else (p, p) for p in points]
    return f'<path class="{cls}" d="M' + ' L'.join(f'{x},{y}' for x,y in points) + '"/>'

def chapter_complexity():
    body = [text(34,52,'为什么 O(log n) 比 O(n²) 更像“地图”','title'),
            '<path class="axis" d="M72,350 L680,350"/><path class="axis" d="M72,350 L72,72"/>']
    body += [text(680,375,'n'), text(50,78,'工作量')]
    body += ['<path class="flow" d="M82,330 C220,330 420,322 668,310"/>']
    body += ['<path class="line" d="M82,330 C300,310 520,245 668,175" marker-end="url(#arrow)"/>']
    body += ['<path class="line" d="M82,330 L668,120" marker-end="url(#arrow)"/>']
    body += ['<path class="bad" d="M82,330 C160,295 240,170 335,82"/>']
    body += [text(390,318,'O(n)'), text(490,232,'O(n log n)'), text(552,116,'O(n)'),
             text(262,110,'O(n²)'), text(322,322,'O(log n)')]
    body += [text(358,410,'横轴看输入规模，纵轴看增长形状：曲线越陡，规模放大后越危险')]
    return svg(720,440,''.join(body))

def chapter_two_pointers():
    nums=[1,8,6,2,5,4,8,3,7]
    body=[text(32,50,'对撞双指针：只移动“较弱的一侧”','title')]
    x=64
    for i,v in enumerate(nums):
        cls='blue' if i in (1,8) else ('gray' if i in (0,2,3,4,5,6,7) else 'plain')
        body.append(node(x,105,56,64,str(v),cls)); body.append(text(x+28,190,str(i))); x+=60
    body += [path([92,85,92,58]), path([500,85,500,58])]
    body += [text(92,48,'left'), text(500,48,'right')]
    body += [rect(58,230,604,64,'green')]
    body += [text(360,258,'面积 = (right-left) × min(height[left], height[right])'),
             text(360,281,'短边决定水面；移动长边不可能变大，所以短边可安全淘汰')]
    body += [text(360,340,'蓝色是当前候选；灰色是已检查或当前区间内的其他柱子')]
    return svg(720,380,''.join(body))

def chapter_sliding_window():
    chars=list('abcabcbb')
    body=[text(32,50,'滑动窗口：right 探索，left 修复非法状态','title')]
    x=70
    for i,ch in enumerate(chars):
        cls='blue' if i in (0,1,2) else ('red' if i==3 else 'plain')
        body.append(node(x,95,52,58,ch,cls)); body.append(text(x+26,174,str(i))); x+=56
    body += [rect(62,88,164,72,'purple',18)]
    body += [text(146,236,'right 新读字符'), path([354,124,212,124])]
    body += [text(146,292,'left 只能前进'), path([354,292,172,292])]
    body += [rect(52,330,616,58,'green')]
    body += [text(360,357,'不变量：窗口内没有重复字符；right 前进扩大答案，left 跳到冲突位置之后')]
    return svg(720,410,''.join(body))

def chapter_monotonic_stack():
    hs=[3,1,4,2,5]
    body=[text(32,50,'单调栈：新证据到来，旧候选立刻退场','title')]
    x=88
    for v in hs:
        h=v*34; body.append(rect(x,255-h,48,h,'blue' if v==5 else 'plain')); body.append(text(x+24,280,str(v))); x+=64
    st=[(500,196,'i=3 · h=2','blue'),(500,250,'i=2 · h=4','orange'),(500,304,'i=0 · h=3','plain')]
    body += [rect(464,160,170,180,'purple')]
    body += [text(549,148,'栈：下标 + 未解决')]
    body += [node(486,188,128,38,'2（下标3）','blue'), node(486,238,128,38,'4（下标2）','orange'), node(486,288,128,38,'3（下标0）','plain')]
    body += [path([240,215,462,212])]
    body += [text(360,390,'新高度 5 到来：比栈顶小的候选可被弹出并确定“下一个更大值”')]
    return svg(720,430,''.join(body))

def chapter_hash_prefix():
    nums=[1,1,1]; body=[text(32,50,'前缀和 + 哈希：把重复求和变成一次查询','title')]
    body += [node(70,90,90,54,'nums','plain'), node(190,90,100,54,'prefix','blue'), node(320,90,140,54,'prefix - k','orange'), node(490,90,180,54,'哈希表查询','green')]
    body += [path([160,117,186,117]), path([290,117,316,117]), path([460,117,486,117])]
    body += [rect(62,180,598,82,'purple')]
    body += [text(360,209,'prefix=1，prefix=2，prefix=3 都记录出现次数'),
             text(360,237,'扫描到 prefix=3 时查 prefix-k=1；查询结果就是和为 k 的子数组数量')]
    body += [rect(62,290,598,72,'green')]
    body += [text(360,318,'不重新枚举 [i,j]；空间换时间，把“历史是否存在”降为 O(1)'),
             text(360,346,'注意：数组含负数时不能改成滑动窗口')]
    return svg(720,390,''.join(body))

def chapter_cycle():
    body=[text(32,50,'快慢指针：环内相对距离每步缩短 1','title')]
    body += [node(80,120,76,50,'1','plain'), node(230,105,76,50,'2','blue'), node(390,130,76,50,'3','plain'), node(500,210,76,50,'4','orange'), node(330,245,76,50,'-4','plain')]
    body += [path([156,145,226,130]), path([306,130,386,155]), path([466,180,502,205]), path([500,260,410,260]), path([330,245,150,175])]
    body += [text(266,80,'fast：每次 2 格'), text(150,300,'slow：每次 1 格')]
    body += [rect(58,350,604,62,'green')]
    body += [text(360,376,'fast 和 fast.next 非空才移动；只要两者指向同一节点，就证明存在环')]
    body += [text(360,400,'slow == fast 是同一对象判断，不是值相等')]
    return svg(720,440,''.join(body))

def chapter_binary_search():
    vals=[1,3,5,7,9,11,13]; body=[text(32,50,'二分：维持两个“已确定区域”','title')]
    x=74
    for i,v in enumerate(vals):
        cls='blue' if i==3 else ('green' if i<3 else 'plain')
        body.append(node(x,95,64,58,str(v),cls)); body.append(text(x+32,174,str(i))); x+=70
    body += [rect(66,225,452,56,'green'), rect(530,225,130,56,'orange')]
    body += [text(292,250,'[0, lo)：一定不满足'), text(595,250,'[hi, n)：可能满足')]
    body += [path([368,160,368,218])]
    body += [text(368,210,'mid')]
    body += [rect(62,315,598,64,'purple')]
    body += [text(360,342,'ok(mid) 后 hi=mid；不满足后 lo=mid+1'),
             text(360,368,'循环结束时 lo==hi，这就是第一个满足条件的边界')]
    return svg(720,410,''.join(body))

def chapter_tree_recursion():
    body=[text(32,50,'树的后序：先问子树要答案，再合并自己','title')]
    body += [node(300,80,120,58,'根 1','blue'), node(140,190,110,56,'左 2','orange'), node(450,190,110,56,'右 3','orange'), node(75,300,95,52,'空','green'), node(230,300,95,52,'空','green'), node(395,300,95,52,'空','green'), node(545,300,95,52,'空','green')]
    body += [path([315,138,195,186]), path([405,138,505,186])]
    body += [text(105,250,'depth=0'), text(277,250,'depth=0'), text(442,250,'depth=0'), text(592,250,'depth=0')]
    body += [rect(58,390,604,62,'green')]
    body += [text(360,416,'depth(n)=1+max(depth(left), depth(right))'),
             text(360,440,'父节点不关心子树内部形状，只接收“子问题已解决”的值')]
    return svg(720,470,''.join(body))

def chapter_heap():
    body=[text(32,50,'堆：只保证最优先者在顶部','title')]
    body += [node(300,85,120,58,'最小 2','blue'), node(170,185,100,54,'5','orange'), node(430,185,100,54,'4','orange'), node(95,285,90,50,'8','plain'), node(240,285,90,50,'7','plain'), node(380,285,90,50,'6','plain'), node(510,285,90,50,'9','plain')]
    body += [path([295,143,220,181]), path([365,143,480,181]), path([200,239,145,281]), path([238,239,272,281]), path([460,239,418,281]), path([500,239,548,281])]
    body += [rect(58,380,280,56,'purple'), rect(390,380,272,56,'green')]
    body += [text(198,405,'插入/弹出：O(log n)'), text(526,405,'查看堆顶：O(1)')]
    body += [text(360,352,'数组 [2,5,4,8,7,6,9]；父子有顺序，兄弟不比较')]
    return svg(720,460,''.join(body))

def chapter_graph_bfs():
    body=[text(32,50,'BFS：按层扩散，所以无权图第一到达即最短','title')]
    body += [node(300,85,120,58,'起点','blue')]
    body += [node(130,190,100,54,'A','orange'), node(470,190,100,54,'B','orange')]
    body += [node(80,300,100,54,'C','green'), node(240,300,100,54,'D','green'), node(430,300,100,54,'E','green')]
    body += [path([300,143,190,186]), path([360,143,470,186]), path([160,244,135,296]), path([210,244,278,296]), path([450,244,478,296])]
    body += [text(360,395,'第 0 层：起点；第 1 层：A、B；第 2 层：C、D、E')]
    body += [rect(58,420,604,56,'green')]
    body += [text(360,446,'入队时立刻标记访问，避免同一层重复加入')]
    return svg(720,500,''.join(body))

def chapter_topological():
    body=[text(32,50,'拓扑排序：先处理没有未完成前置的节点','title')]
    body += [node(95,90,110,58,'0 · 入度0','green'), node(310,90,110,58,'1 · 入度1','orange'), node(520,90,110,58,'2 · 入度1','orange'), node(215,230,110,58,'3 · 入度2','red'), node(430,230,110,58,'4 · 入度2','red')]
    body += [path([205,119,306,119]), path([420,119,516,119]), path([150,148,240,226]), path([365,148,455,226]), path([325,119,430,226])]
    body += [text(360,340,'0 学完后，依赖 0 的课程入度减 1；入度变 0 才能进入队列')]
    body += [rect(58,380,604,60,'green')]
    body += [text(360,404,'若最终输出的节点数 < 总节点数，说明剩余依赖形成环')]
    return svg(720,470,''.join(body))

def chapter_dp_grid():
    body=[text(32,50,'DP：先定义状态，再看格子来自哪里','title')]
    body += [rect(90,90,76,52,'plain'), rect(170,90,76,52,'plain'), rect(250,90,76,52,'blue'), rect(330,90,76,52,'plain')]
    body += [rect(90,146,76,52,'plain'), rect(170,146,76,52,'blue'), rect(250,146,76,52,'plain'), rect(330,146,76,52,'plain')]
    body += [text(128,121,'dp0'), text(208,121,'dp1'), text(288,121,'dp2'), text(368,121,'dp3'),
             text(128,177,'dp4'), text(208,177,'dp5'), text(288,177,'dp6'), text(368,177,'dp7')]
    body += [path([250,160,211,160]), path([288,146,288,142]), path([250,146,211,146])]
    body += [text(220,250,'左 / 上 / 左上：当前状态的历史来源')]
    body += [rect(58,290,604,82,'purple')]
    body += [text(360,318,'状态是什么？状态值表示什么？转移从哪些子问题来？'),
             text(360,346,'边界是递推的“地基”；顺序错，整个表格会依赖还没算出的格子')]
    return svg(720,400,''.join(body))

def chapter_backtracking():
    body=[text(32,50,'回溯：选择 → 探索 → 撤销','title')]
    body += [node(300,80,120,54,'[]','blue'), node(140,180,110,54,'[1]','orange'), node(450,180,110,54,'[2]','orange'), node(70,290,95,52,'[1,2]','green'), node(230,290,95,52,'[1,3]','green'), node(400,290,95,52,'[2,1]','green'), node(540,290,95,52,'[2,3]','green')]
    body += [path([295,134,195,176]), path([365,134,495,176]), path([165,234,115,286]), path([210,234,272,286]), path([465,234,442,286]), path([510,234,580,286])]
    body += [text(360,395,'绿色是记录点；回到父节点必须删除刚做的选择，否则状态污染')]
    body += [rect(58,420,604,56,'purple')]
    body += [text(360,446,'红色剪枝用于整棵子树都不可能满足约束的情况')]
    return svg(720,500,''.join(body))

def chapter_union_find():
    body=[text(32,50,'并查集：不关心路径，只关心“谁和谁同根”','title')]
    body += [node(250,90,110,54,'A 根','blue'), node(430,90,110,54,'B 根','red')]
    body += [node(130,200,100,52,'C','orange'), node(360,200,100,52,'D','orange'), node(520,200,100,52,'E','plain')]
    body += [path([220,144,185,196]), path([295,144,400,196]), path([455,144,545,196])]
    body += [path([180,226,425,130],'good')]
    body += [text(300,290,'union(C,B)：找到 A 根和 B 根，再把一个根挂到另一个根下面')]
    body += [rect(58,325,604,68,'purple')]
    body += [text(360,352,'路径压缩：find 时把沿途节点直接挂到根'),
             text(360,380,'按大小合并：小树挂到大树，避免变成长链')]
    return svg(720,420,''.join(body))

def problem_two_sum():
    body=[text(32,50,'两数之和：把“找同伴”变成一次历史查询','title')]
    body += [node(70,95,95,56,'x = 7','blue'), node(215,95,145,56,'需要 2','orange'), node(410,95,180,56,'seen[2]=0','green')]
    body += [path([165,123,211,123]), path([360,123,406,123])]
    body += [rect(62,190,598,88,'purple')]
    body += [text(360,218,'seen 记录历史值 → 下标：{2:0}'),
             text(360,247,'扫描到 7 时，同伴 target-x=2 已经出现过；不需要回头再扫')]
    body += [rect(62,305,598,56,'green')]
    body += [text(360,331,'答案返回 [seen[2], 当前下标1] = [0,1]')]
    return svg(720,390,''.join(body))

def problem_max_subarray():
    body=[text(32,50,'最大子数组和：负前缀不值得携带','title')]
    nums=[-2,1,-3,4,-1,2,1]
    x=70
    for i,v in enumerate(nums):
        cls='red' if i==0 else ('blue' if i==3 else 'plain')
        body.append(node(x,100,58,56,str(v),cls)); body.append(text(x+29,176,str(i))); x+=64
    body += [path([100,90,210,90],'bad'), path([230,90,312,90])]
    body += [text(145,78,'cur<0：丢弃'), text(280,78,'从 4 重新开始')]
    body += [rect(58,220,604,88,'purple')]
    body += [text(360,248,'cur = 以 i 结尾的最大和'),
             text(360,276,'cur = max(nums[i], cur + nums[i])；ans 记录历史最大值')]
    body += [rect(58,335,604,56,'green')]
    body += [text(360,361,'后续 4,-1,2,1 形成最大连续和 6')]
    return svg(720,420,''.join(body))

def problem_container():
    body=[text(32,50,'盛水容器：面积由短边和宽度共同决定','title')]
    hs=[1,8,6,2,5,4,8,3,7]; x=75; ybase=260
    for i,h in enumerate(hs):
        hh=h*22; cls='blue' if i in (1,8) else 'plain'
        body.append(rect(x,ybase-hh,48,hh,cls)); body.append(text(x+24,285,str(h))); x+=55
    body += ['<path class="line" d="M88,238 L463,238" stroke-dasharray="8 8"/>']
    body += [text(120,226,'left=1 · 高8'), text(430,226,'right=8 · 高7')]
    body += [rect(58,325,604,66,'green')]
    body += [text(360,350,'宽 = 8 - 1 = 7；高 = min(8,7) = 7；面积 = 49'),
             text(360,378,'移动较长右边不会增加上限，因此右指针可安全左移')]
    return svg(720,420,''.join(body))

def problem_three_sum():
    body=[text(32,50,'三数之和：固定一个，剩下的变成对撞搜索','title')]
    vals=[-1,0,1,2]
    x=85
    for i,v in enumerate(vals):
        cls='blue' if i==0 else ('green' if i==1 else ('orange' if i==3 else 'plain'))
        body.append(node(x,100,62,56,str(v),cls)); body.append(text(x+31,176,str(i))); x+=68
    body += [text(116,80,'固定 i'), text(177,222,'l：小则右移'), text(450,222,'r：大则左移')]
    body += [rect(58,255,604,72,'purple')]
    body += [text(360,281,'sum = nums[i] + nums[l] + nums[r]'),
             text(360,310,'sum<0 右移 l；sum>0 左移 r；sum=0 记录并同步跳过重复值')]
    body += [rect(58,355,604,56,'green')]
    body += [text(360,381,'排序不仅提供单调方向，也让重复三元组相邻可见')]
    return svg(720,440,''.join(body))

def problem_next_greater():
    body=[text(32,50,'下一个更大元素：新值淘汰无法获胜的旧候选','title')]
    nums=[1,2,1]
    body += [node(80,95,74,56,'1','blue'), node(190,95,74,56,'2','green'), node(300,95,74,56,'1','orange')]
    body += [path([154,123,186,123])]
    body += [text(120,78,'新到 2'), text(227,78,'1 出栈')]
    body += [rect(420,95,180,116,'purple')]
    body += [text(510,125,'栈保存下标'), text(510,155,'值保持递减')]
    body += [rect(58,245,604,82,'green')]
    body += [text(360,272,'2 大于栈内 1，因此下标 0 的答案确定为 2'),
             text(360,301,'被弹出的元素已解决；仍留在栈中的元素继续等待更大的数')]
    body += [text(360,365,'答案 [2,-1,-1]')]
    return svg(720,400,''.join(body))

def problem_histogram():
    body=[text(32,50,'柱状图最大矩形：低柱变成左右边界的分界','title')]
    hs=[2,5,6,2]
    x=82; ybase=270
    for i,h in enumerate(hs):
        hh=h*40; cls='blue' if i in (1,2) else 'plain'
        body.append(rect(x,ybase-hh,50,hh,cls)); body.append(text(x+25,295,str(h))); x+=60
    body += ['<path class="line" d="M142,110 L262,110" stroke-dasharray="7 7"/>']
    body += [rect(136,103,132,14,'blue',3)]
    body += [text(202,85,'高度 5 的最大矩形')]
    body += [rect(58,330,604,70,'purple')]
    body += [text(360,356,'弹出 6 时：右边界是更低柱 2，左边界来自新栈顶'),
             text(360,385,'宽度 = i - stack[-1] - 1')]
    return svg(720,430,''.join(body))

def problem_prefix_sum():
    body=[text(32,50,'和为 k 的子数组：把区间差转成前缀差','title')]
    body += [node(70,95,130,56,'prefix[j]','blue'), node(280,95,125,56,'prefix[i]','orange'), node(465,95,120,56,'= k','green')]
    body += [path([200,123,276,123]), path([405,123,461,123])]
    body += [rect(58,190,604,80,'purple')]
    body += [text(360,218,'prefix[i] = prefix[j] - k'),
             text(360,246,'所以只查这个值出现过几次，就得到几个以 j 结尾的子数组')]
    body += [rect(58,298,604,56,'green')]
    body += [text(360,324,'seen[0]=1 是边界：从头开始的合法子数组也要被计数')]
    return svg(720,380,''.join(body))

def problem_cycle():
    body=[text(32,50,'环检测：追上即证明绕圈','title')]
    body += [node(80,115,80,52,'A','plain'), node(250,100,80,52,'B','blue'), node(410,125,80,52,'C','orange'), node(470,230,80,52,'D','plain'), node(250,250,80,52,'E','plain')]
    body += [path([160,141,246,120]), path([330,120,406,140]), path([450,177,495,226]), path([470,282,334,267]), path([250,250,120,190])]
    body += [text(160,80,'slow · +1'), text(360,80,'fast · +2')]
    body += [rect(58,330,604,66,'green')]
    body += [text(360,355,'进入环后 fast 每步比 slow 多走 1 格'),
             text(360,383,'相对距离不断缩小，最终 slow == fast')]
    return svg(720,420,''.join(body))

def problem_remove_nth():
    body=[text(32,50,'删除倒数第 n 个：用固定距离找前驱','title')]
    vals=['d',1,2,3,4,5]; x=62
    for i,v in enumerate(vals):
        cls='blue' if i in (0,1) else ('orange' if i==4 else 'plain')
        body.append(node(x,100,56,54,str(v),cls)); body.append(text(x+28,174,str(i))); x+=62
    body += [text(90,80,'slow'), text(335,80,'fast 提前')]
    body += [rect(58,225,604,82,'purple')]
    body += [text(360,252,'dummy 使头节点也有前驱；fast 从 dummy 先走 n+1 步'),
             text(360,281,'fast 到 null 时，slow 停在待删节点的前一个节点')]
    body += [rect(58,335,604,56,'green')]
    body += [text(360,361,'slow.next = slow.next.next，一趟完成删除')]
    return svg(720,420,''.join(body))

def problem_bst_range():
    body=[text(32,50,'验证 BST：祖先约束传给整棵子树','title')]
    body += [node(300,80,120,58,'2 · (-∞,+∞)','blue'), node(140,190,120,58,'1 · (-∞,2)','green'), node(450,190,120,58,'3 · (2,+∞)','green')]
    body += [path([315,138,195,186]), path([405,138,505,186])]
    body += [text(200,160,'左子树上界变2'), text(465,160,'右子树下界变2')]
    body += [rect(58,285,604,78,'purple')]
    body += [text(360,312,'不是只比较左右孩子；整棵左子树都必须小于根'),
             text(360,341,'区间继承让祖先约束一直传播到底')]
    return svg(720,395,''.join(body))

def problem_topological():
    body=[text(32,50,'课程表：入度 0 表示可以立刻学习','title')]
    body += [node(90,95,125,58,'0 · 入度0','green'), node(300,95,125,58,'1 · 入度1','orange'), node(510,95,125,58,'2 · 入度1','orange')]
    body += [path([215,124,296,124]), path([425,124,506,124])]
    body += [path([152,153,245,240],'good'), path([362,153,435,240],'good')]
    body += [node(205,245,105,54,'3 · 入度2','red'), node(400,245,105,54,'2 · 入度2','red')]
    body += [rect(58,335,604,66,'purple')]
    body += [text(360,360,'学完 0 后，1、2、3 的入度减 1'),
             text(360,389,'输出数量小于课程总数，等价于存在环')]
    return svg(720,430,''.join(body))

def problem_dijkstra():
    body=[text(32,50,'Dijkstra：每次固定当前最近的未确定节点','title')]
    body += [node(80,100,110,56,'S · 0','green'), node(320,80,120,56,'A · 1','orange'), node(520,100,115,56,'B · 4','plain'), node(320,225,120,56,'T · ?','plain')]
    body += [path([190,128,316,104],'good'), path([440,100,516,124]), path([380,136,380,221])]
    body += [text(252,85,'1'), text(483,80,'3'), text(398,180,'7')]
    body += [rect(58,315,604,76,'purple')]
    body += [text(360,342,'堆弹出 (1,A)；边权非负，A 的 1 不可能再被更长路径改善'),
             text(360,371,'如果堆里出现过期距离，必须跳过')]
    return svg(720,420,''.join(body))

def problem_coin_change():
    body=[text(32,50,'零钱兑换：最后一枚硬币决定转移来源','title')]
    body += [node(70,95,110,56,'dp[c-5]','blue'), node(230,95,110,56,'+1','orange'), node(390,95,110,56,'dp[c]','green')]
    body += [path([180,123,226,123]), path([340,123,386,123])]
    body += [rect(58,185,604,88,'purple')]
    body += [text(360,213,'dp[c] = min(dp[c-1], dp[c-2], dp[c-5]) + 1'),
             text(360,242,'dp[c] 的含义是：凑出金额 c 的最少硬币数')]
    body += [rect(58,300,604,62,'green')]
    body += [text(360,326,'11 = 5 + 5 + 1；状态只关心剩余金额，不关心硬币顺序')]
    return svg(720,390,''.join(body))

def problem_lis_tails():
    body=[text(32,50,'LIS：tail[k] 是长度 k+1 的最小可行尾值','title')]
    nums=[10,9,2,5,3,7]
    x=72
    for i,v in enumerate(nums):
        cls='blue' if i==3 else ('plain' if i not in (4,5) else 'orange')
        body.append(node(x,95,62,54,str(v),cls)); body.append(text(x+31,168,str(i))); x+=68
    body += [rect(58,210,180,120,'green'), rect(270,210,180,120,'orange')]
    body += [text(148,238,'tails=[2,3]'), text(148,266,'长度2'), text(148,300,'3 是最小尾值')]
    body += [text(360,238,'读入 7'), text(360,266,'比所有尾值大')]
    body += [text(360,300,'LIS 长度变为 3')]
    body += [rect(58,355,604,56,'purple')]
    body += [text(360,381,'tails 不一定是真实 LIS，但长度是正确答案')]
    return svg(720,440,''.join(body))

def problem_edit_distance():
    body=[text(32,50,'编辑距离：每个格子表示前缀之间的最小代价','title')]
    rows=[['dp[1][1]','h→r','替换1'],['dp[2][1]','ho→r','删除1'],['dp[1][2]','h→ro','插入1']]
    positions=[(80,95),(260,95),(440,95)]
    for (x,y),vals in zip(positions,rows):
        body.append(rect(x,y,180,118,'blue' if vals[0]=='dp[1][1]' else 'plain'))
        body += [text(x+90,y+34,vals[0]), text(x+90,y+66,vals[1]), text(x+90,y+96,vals[2])]
    body += [rect(58,255,604,92,'purple')]
    body += [text(360,282,'dp[i][j] = min(删除，插入，替换) + 1'),
             text(360,311,'字符相等时继承 dp[i-1][j-1]，不需要再花一次代价')]
    body += [rect(58,375,604,56,'green')]
    body += [text(360,401,'horse → ros 的答案在右下角：3')]
    return svg(720,460,''.join(body))

def problem_palindrome():
    body=[text(32,50,'最长回文子串：奇偶中心都要检查','title')]
    body += [node(85,95,64,54,'b','plain'), node(165,95,64,54,'a','blue'), node(245,95,64,54,'b','blue'), node(325,95,64,54,'a','orange'), node(405,95,64,54,'d','plain')]
    body += ['<path class="line" d="M197,178 L277,178" stroke-dasharray="7 7"/>']
    body += [text(237,205,'中心 1：字符 a，扩展得到 aba')]
    body += ['<path class="line" d="M237,265 L317,265" stroke-dasharray="7 7"/>']
    body += [text(277,292,'中心 2：a/b 之间，偶数长度候选')]
    body += [rect(58,325,604,66,'green')]
    body += [text(360,350,'每个奇中心 + 每个偶中心都向两侧扩展'),
             text(360,378,'遇到不相等立即停止，记录最大长度')]
    return svg(720,420,''.join(body))

def chapter_sorting_models():
    body=[text(32,50,'排序选型：先看值域和顺序要求','title')]
    body += [node(70,95,150,58,'比较排序','blue'), node(300,95,180,58,'值域/位数受限？','orange'), node(545,95,120,58,'非比较','green')]
    body += [path([220,124,296,124]), path([480,124,541,124])]
    body += [rect(58,190,286,128,'blue'), rect(376,190,286,128,'purple')]
    body += [text(201,217,'快排 / 归并 / 堆排'), text(201,245,'平均 O(n log n)'), text(201,281,'按稳定性与原地性选择')]
    body += [text(519,217,'计数 / 基数 / 桶'), text(519,245,'利用值域或位数'), text(519,281,'可突破比较下界')]
    body += [rect(58,350,604,66,'green')]
    body += [text(360,375,'稳定排序能保持相等元素原序；基数排序的每一位必须稳定'),
             text(360,403,'通用数组常选快排；链表/外部排序常用归并；小整数用计数')]
    return svg(720,440,''.join(body))

def chapter_trie_prefix():
    body=[text(32,50,'Trie：共享前缀只走一次','title')]
    body += [node(300,80,95,50,'root','blue'), node(145,180,85,50,'a','green'), node(305,180,85,50,'b','plain'), node(145,280,85,50,'p','green'), node(145,375,95,50,'p · end','blue')]
    body += [path([300,130,190,176]), path([330,130,345,176]), path([187,230,187,276]), path([187,330,192,371])]
    body += [text(355,210,'b 分支与其他词共享根'), text(345,340,'apple 的唯一路径')]
    body += [rect(58,445,604,70,'purple')]
    body += [text(360,470,'插入/查找/前缀判断都是 O(L)'),
             text(360,500,'is_end 标记“到此是一个完整词”；子节点保存下一字符')]
    return svg(720,540,''.join(body))

def chapter_avl_rotation():
    body=[text(32,50,'AVL 旋转：恢复高度，不破坏中序','title')]
    body += [text(180,78,'失衡：左左'), text(520,78,'右旋后')]
    body += [node(190,95,100,54,'y','red'), node(115,205,95,54,'x','blue'), node(280,205,95,54,'C','plain'), node(70,315,90,52,'A','green'), node(165,315,90,52,'B','orange')]
    body += [path([205,149,165,201]), path([285,149,315,201]), path([130,259,112,311]), path([182,259,197,311])]
    body += [node(480,160,100,54,'x','blue'), node(390,270,95,54,'A','green'), node(575,270,95,54,'y','orange'), node(535,375,90,52,'B','green'), node(630,375,90,52,'C','plain')]
    body += [path([510,214,430,266]), path([560,214,592,266]), path([425,324,525,371]), path([598,324,646,371])]
    body += [text(360,450,'中序仍是 A < x < B < y < C；只有父子关系被旋转')]
    body += [rect(58,475,604,60,'purple')]
    body += [text(360,500,'更新高度顺序：先孩子，再父节点')]
    return svg(720,560,''.join(body))

def chapter_btree_split():
    body=[text(32,50,'B+ 树：满节点分裂，中间键上移','title')]
    body += [node(80,95,170,58,'[10,20,30,40]','red'), path([250,124,330,124]), node(335,95,170,58,'分裂','orange')]
    body += [node(160,215,105,54,'[10,20]','green'), node(330,215,105,54,'[30,40]','green'), node(240,95,0,0,'', 'plain')]
    body += [node(245,330,110,54,'20 上移','blue')]
    body += [path([185,215,285,158]), path([385,215,300,158])]
    body += ['<path class="line" d="M265,269 L265,326" stroke-dasharray="7 7"/>']
    body += [rect(58,420,604,90,'purple')]
    body += [text(360,446,'内部节点只放索引键；真实数据在叶子'),
             text(360,475,'叶子链表支持范围扫描：定位起点后顺序读'),
             text(360,498,'一次节点读取对应一次磁盘页，而不是一个二叉节点')]
    return svg(720,535,''.join(body))

def chapter_branch_bound():
    body=[text(32,50,'分支限界：用界剪掉注定更差的子树','title')]
    body += [node(300,80,120,54,'部分解','blue'), node(130,185,120,54,'分支 A','orange'), node(450,185,120,54,'分支 B','orange')]
    body += [path([295,134,195,181]), path([365,134,495,181])]
    body += [node(80,300,150,54,'界 12','green'), node(300,300,150,54,'界 17','red'), node(500,300,150,54,'界 19','plain')]
    body += [path([160,239,120,296]), path([230,239,340,296]), path([490,239,545,296])]
    body += [text(155,390,'已知最优 ≥17'), text(375,390,'12 不可能更优，剪掉'), text(575,390,'继续扩展')]
    body += [rect(58,420,604,64,'purple')]
    body += [text(360,445,'最小化问题用下界；最大化问题用上界'),
             text(360,472,'bound 不可能优于 best 时，整棵子树都可剪掉')]
    return svg(720,510,''.join(body))

def chapter_graph_representation():
    body=[text(32,50,'图表示法：空间、查边和遍历都不同','title')]
    body += [rect(58,90,300,130,'blue'), rect(362,90,300,130,'orange')]
    body += [text(208,118,'邻接表 O(V+E)'), text(208,150,'遍历稀疏边最省'), text(208,184,'查边要看度数')]
    body += [text(512,118,'矩阵 O(V²)'), text(512,150,'O(1) 判断 u-v'), text(512,184,'密集图/Floyd')]
    body += [rect(58,245,300,130,'purple'), rect(362,245,300,130,'green')]
    body += [text(208,273,'边数组 O(E)'), text(208,305,'Kruskal/Bellman'), text(208,338,'不适合查邻居')]
    body += [text(512,273,'隐式图'), text(512,305,'按状态生成邻居'), text(512,338,'控制状态爆炸')]
    body += [rect(58,405,604,64,'plain')]
    body += [text(360,430,'建模四问：点是什么？边是什么？权是什么？方向如何？'),
             text(360,456,'选错容器，算法仍正确，但时间或空间可能不可承受')]
    return svg(720,495,''.join(body))

DIAGRAMS = {
    "chapter-complexity-growth": chapter_complexity,
    "chapter-array-two-pointers": chapter_two_pointers,
    "chapter-sliding-window": chapter_sliding_window,
    "chapter-monotonic-stack": chapter_monotonic_stack,
    "chapter-hash-prefix-sum": chapter_hash_prefix,
    "chapter-linked-list-cycle": chapter_cycle,
    "chapter-binary-search-boundary": chapter_binary_search,
    "chapter-tree-recursion": chapter_tree_recursion,
    "chapter-heap-shape": chapter_heap,
    "chapter-graph-bfs-layers": chapter_graph_bfs,
    "chapter-topological-order": chapter_topological,
    "chapter-dp-state-grid": chapter_dp_grid,
    "chapter-backtracking-tree": chapter_backtracking,
    "chapter-union-find": chapter_union_find,
    "chapter-sorting-models": chapter_sorting_models,
    "chapter-trie-prefix": chapter_trie_prefix,
    "chapter-avl-rotation": chapter_avl_rotation,
    "chapter-btree-split": chapter_btree_split,
    "chapter-branch-bound": chapter_branch_bound,
    "chapter-graph-representation": chapter_graph_representation,
    "problem-p001-two-sum": problem_two_sum,
    "problem-p002-max-subarray": problem_max_subarray,
    "problem-p003-container": problem_container,
    "problem-p008-three-sum": problem_three_sum,
    "problem-p010-sliding-window": chapter_sliding_window,
    "problem-p013-next-greater": problem_next_greater,
    "problem-p015-histogram": problem_histogram,
    "problem-p022-prefix-sum": problem_prefix_sum,
    "problem-p029-cycle": problem_cycle,
    "problem-p032-remove-nth": problem_remove_nth,
    "problem-p047-bst-range": problem_bst_range,
    "problem-p066-topological": problem_topological,
    "problem-p073-dijkstra": problem_dijkstra,
    "problem-p097-coin-change": problem_coin_change,
    "problem-p099-lis-tails": problem_lis_tails,
    "problem-p101-edit-distance": problem_edit_distance,
    "problem-p111-palindrome": problem_palindrome,
}

def model_state_svg(problem, chapter_lookup):
    model = model_diagram(problem, chapter_lookup)
    body = [
        text(32, 52, model["title"], "title"),
        text(34, 80, model["subtitle"], "small"),
        node(58, 112, 190, 82, model["kind"], "blue", "当前状态"),
        node(270, 112, 190, 82, model["action"], "orange", "操作"),
        node(482, 112, 190, 82, model["result"], "green", "目标"),
        path([248, 153], "arrow"),
        path([460, 153], "arrow"),
    ]
    body += [rect(58, 225, 614, 76, "purple")]
    body += [text(360, 252, "本题 focus"), text(360, 281, model["focus"])]
    body += [rect(58, 325, 614, 76, "green")]
    body += [text(360, 352, "不变量"), text(360, 381, model["invariant"])]
    body += [rect(58, 425, 614, 56, "plain")]
    body += [text(360, 450, "模型图先展示状态迁移骨架；五问法内容仍按批次深化")]
    return svg(720, 505, "".join(body))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chapter_lookup = {
        chapter["id"]: chapter
        for chapter in json.loads((ROOT / "data" / "chapters.json").read_text(encoding="utf-8"))
    }
    problems = json.loads((ROOT / "data" / "problems.json").read_text(encoding="utf-8"))
    custom_problem_ids = {
        name.split("-")[1]
        for name in DIAGRAMS
        if name.startswith("problem-")
    }
    model_count = 0
    for problem in problems:
        if problem["id"] in custom_problem_ids:
            continue
        target = OUT / diagram_key(problem["id"])
        target.write_text(model_state_svg(problem, chapter_lookup), encoding="utf-8")
        model_count += 1

    for name, builder in DIAGRAMS.items():
        target = OUT / f"{name}.svg"
        target.write_text(builder(), encoding="utf-8")
    print(f"generated {len(DIAGRAMS)} hand-made diagrams and {model_count} model diagrams")


def chapter_interval_schedule():
    body=[text(32,50,'区间调度：按结束时间排序，保留最早结束者','title')]
    intervals=[('A',70,220,'blue',True),('B',190,160,'red',False),('C',300,220,'blue',True),('D',430,160,'plain',False)]
    y=100
    for name,x,w,cls,selected in intervals:
        body += [rect(x,y,w,56,cls), text(x+w/2,y+34,name)]
        if selected: body += [text(x+45,y+190,'选中')]
        y += 68
    body += [text(360,345,'A 结束最早，不会减少后续机会；B 与 A 重叠，可安全淘汰')]
    body += [rect(58,370,604,66,'green')]
    body += [text(360,395,'蓝色区间互不重叠；红色区间与已选集合冲突')]
    body += [text(360,423,'证明思路：任何最优解都可以把第一个区间换成结束最早的 A')]
    return svg(720,450,''.join(body))

DIAGRAMS["chapter-interval-scheduling"] = chapter_interval_schedule


def problem_sort_colors():
    body=[text(32,50,'颜色分类：三个边界把数组切成四个区','title')]
    vals=['0','0','1','1','2','2']
    x=78
    for i,v in enumerate(vals):
        cls='green' if i<2 else ('blue' if i<4 else ('red' if i>4 else 'orange'))
        body.append(node(x,100,64,58,v,cls)); body.append(text(x+32,178,str(i))); x+=68
    body += [text(110,84,'[0,left)'), text(310,84,'[left,i)'), text(478,84,'(i,right]'), text(640,84,'(right,n)')]
    body += [rect(58,225,614,76,'purple')]
    body += [text(360,252,'遇 0：与 left 交换，left++，i++'),
             text(360,281,'遇 2：与 right 交换，right--，i 不前进')]
    body += [rect(58,325,614,62,'green')]
    body += [text(360,350,'[0,left) 全 0；(right,n) 全 2；i 到 right 只剩 1 和未处理状态')]
    body += [text(360,398,'换回的 2 或 0 必须重新判断')]
    return svg(720,430,''.join(body))

def problem_inversions():
    body=[text(32,50,'逆序对：在归并跨越处批量计数','title')]
    body += [node(65,95,140,58,'左半 [5,7]','blue'), node(300,95,140,58,'右半 [4,6]','orange')]
    body += [path([205,124,296,124])]
    body += [node(105,205,80,52,'取 4','red'), node(310,205,90,52,'剩 5,7','green')]
    body += [path([240,153,150,201])]
    body += [text(250,290,'左半剩余 2 个，都大于 4：一次性计 2')]
    body += [rect(58,325,614,76,'purple')]
    body += [text(360,351,'左半和右半各自有序'),
             text(360,380,'当前右值 < 当前左值时，跨半逆序数 = m - i + 1')]
    body += [rect(58,425,614,52,'green')]
    body += [text(360,449,'相等用 <=，避免把相等元素算成逆序')]
    return svg(720,500,''.join(body))

def problem_trie_path():
    body=[text(32,50,'Trie：前缀路径与完整词标记','title')]
    body += [node(300,80,100,52,'root','blue'), node(180,180,90,52,'a','plain'), node(430,180,90,52,'b','plain'), node(180,285,90,52,'p','orange'), node(180,390,110,56,'p · end','green')]
    body += [path([315,132,195,176]), path([345,132,465,176]), path([225,232,225,281]), path([225,337,235,386])]
    body += [text(385,236,'b 分支不共享 apple'), text(340,375,'apple 到达 end')]
    body += [rect(58,475,614,66,'purple')]
    body += [text(360,500,'search(app) 走到 p，但 end=false'),
             text(360,528,'startsWith(app) 只要求路径存在')]
    return svg(720,570,''.join(body))

def problem_trie_dfs():
    body=[text(32,50,'单词搜索 II：网格路径与 Trie 同步走','title')]
    body += [node(95,100,70,56,'o','blue'), node(235,100,70,56,'a','green'), node(375,100,70,56,'t','green'), node(515,100,70,56,'h','green')]
    body += [path([165,128,235,128]), path([305,128,375,128]), path([445,128,515,128])]
    body += [text(65,185,'网格起点'), text(185,185,'匹配 oa'), text(325,185,'匹配 oat'), text(465,185,'匹配 oath')]
    body += [rect(58,225,614,80,'purple')]
    body += [text(360,252,'Trie 无边 => 当前网格子树整体剪枝'),
             text(360,281,'匹配完整词后加入答案，并清除 end 标记避免重复')]
    body += [rect(58,330,614,72,'green')]
    body += [text(360,356,'DFS 进入时临时标记格子'),
             text(360,386,'四个方向返回后恢复字符')]
    body += [text(360,435,'共享前缀只搜索一次')]
    return svg(720,465,''.join(body))

def problem_calendar():
    body=[text(32,50,'日程安排：只看前驱与后继','title')]
    body += [rect(85,110,240,58,'green'), rect(385,110,220,58,'orange')]
    body += [text(205,139,'前驱 [10,20]'), text(495,139,'后继不存在')]
    body += [rect(295,210,220,58,'blue')]
    body += [text(405,239,'新区间 [20,30)')]
    body += ['<path class="line" d="M325,200 L350,168" stroke-dasharray="7 7"/>']
    body += [text(170,305,'prev.end=20 <= start=20：不冲突')]
    body += [rect(58,340,614,76,'purple')]
    body += [text(360,366,'prev.end <= start 且 next.start >= end'),
             text(360,394,'有序结构只需检查两个相邻候选')]
    body += [rect(58,440,614,52,'green')]
    body += [text(360,464,'端点相接视为不重叠')]
    return svg(720,515,''.join(body))

def problem_bit_query():
    body=[text(32,50,'BIT：从右往左先查询再插入','title')]
    body += [node(70,100,120,58,'nums[i]','blue'), node(240,100,150,58,'rank-1','orange'), node(440,100,180,58,'query(r-1)','green')]
    body += [path([190,129,236,129]), path([390,129,436,129])]
    body += [rect(58,190,614,80,'purple')]
    body += [text(360,217,'BIT 中只包含右侧已处理元素'),
             text(360,245,'query(r-1) 返回严格小于当前 rank 的数量')]
    body += [rect(58,295,614,76,'green')]
    body += [text(360,321,'随后 update(r)，把当前数加入右侧集合'),
             text(360,350,'顺序颠倒会把自身或左侧元素算进去')]
    body += [text(360,410,'最后反转答案数组')]
    return svg(720,435,''.join(body))

def problem_bplus_split():
    body=[text(32,50,'B+ 树节点分裂：中间键上移','title')]
    body += [node(80,110,190,58,'[1,2,3,4,5]','red'), path([270,139,330,139])]
    body += [node(335,110,70,58,'3','blue')]
    body += [node(105,230,125,58,'[1,2]','green'), node(345,230,125,58,'[4,5]','green')]
    body += [path([150,168,160,226]), path([310,168,380,226])]
    body += [text(240,330,'separator=keys[t-1]')]
    body += [rect(58,370,614,86,'purple')]
    body += [text(360,396,'左、右各 t-1 个键'),
             text(360,424,'separator 不能留在子节点'),
             text(360,446,'键升序保证左右范围不重叠')]
    return svg(720,480,''.join(body))

def problem_knapsack_bound():
    body=[text(32,50,'0/1 背包分支限界：用松弛上界剪枝','title')]
    body += [node(75,100,170,64,'部分解 i','blue'), node(300,100,170,64,'分数背包','orange'), node(520,100,150,64,'上界 bound','green')]
    body += [path([245,132,296,132]), path([470,132,516,132])]
    body += [rect(58,195,614,86,'purple')]
    body += [text(360,221,'剩余物品能装则整装；装不下按比例计入'),
             text(360,250,'这是 0/1 背包的松弛解，不会低估真实可达价值')]
    body += [rect(58,305,614,80,'red')]
    body += [text(360,331,'若 bound <= best，整棵子树不可能改善答案'),
             text(360,360,'立即剪枝，不再枚举剩余选择')]
    body += [text(360,415,'方向必须正确：最大化问题用上界')]
    return svg(720,440,''.join(body))

DIAGRAMS["problem-p125-sort-colors"] = problem_sort_colors
DIAGRAMS["problem-p126-inversions"] = problem_inversions
DIAGRAMS["problem-p130-trie-path"] = problem_trie_path
DIAGRAMS["problem-p132-trie-dfs"] = problem_trie_dfs
DIAGRAMS["problem-p136-calendar"] = problem_calendar
DIAGRAMS["problem-p137-bit-query"] = problem_bit_query
DIAGRAMS["problem-p139-bplus-split"] = problem_bplus_split
DIAGRAMS["problem-p142-knapsack-bound"] = problem_knapsack_bound


if __name__ == "__main__":
    main()
