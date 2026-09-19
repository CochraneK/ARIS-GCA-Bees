#!/usr/bin/env python3
"""Generate bilingual README visuals from canonical ARIS4C portfolio metadata.

All README graphics are repository-native SVGs so they stay crisp, editable,
Git-friendly, and automatically refreshable.
"""
from __future__ import annotations
import html, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAPERS=ROOT/"papers"
ASSET_DIR=ROOT/"docs"/"assets"/"readme"
BG="#07162b"; PANEL="#0d2442"; PANEL2="#102c50"; GRID="#245d95"
TEXT="#f8fafc"; MUTED="#a9bfe0"; ACTIVE="#48e996"; GATED="#f2c14e"; QUIET="#8aa0b8"; BLOCKED="#ef6a6a"; ACCENT="#54a9ff"

ZH_TITLES={
"001":"蜜蜂 GCA × 不确定性","002":"语言周期性检验","003":"殖民遗产 × 学科优势",
"004":"排斥的反事实知识网络成本","005":"坏科学的全球隐性负担","006":"中国姓名字母顺序暴露",
"007":"跨物种年龄等价","008":"人类高级智力演化","009":"现象学保持型计算精神病学",
"010":"Universal Concept Identification","011":"Research Forensics","012":"Oppositional Causal Inversion",
"013":"出生—死亡时间耦合","014":"Public Integrity Forensics","015":"Sleeping Beauty Miner",
"016":"全球脏话 / 禁忌语言语法"}

def esc(x): return html.escape(str(x),quote=True)

def load():
    dash=json.loads((PAPERS/"dashboard.json").read_text(encoding="utf-8"))
    rows=[]
    for mf in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        p=json.loads(mf.read_text(encoding="utf-8")); d=dash["projects"].get(p["id"],{})
        handoff=mf.parent/"handoff"
        rows.append({"id":p["id"],"short":p.get("short_title") or p["title"],"progress":int(d.get("progress",0)),
                     "activity":d.get("activity","active"),"handoff":handoff.is_dir() and len(list(handoff.glob("*.md")))>=8,
                     "pdf":bool(p.get("links",{}).get("paper_en_pdf") and p.get("links",{}).get("paper_zh_pdf"))})
    return rows

def head(title,subtitle,w=1600,h=900):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">',
    f'<title>{esc(title)}</title>',f'<rect width="{w}" height="{h}" rx="28" fill="{BG}"/>',
    '<style>text{font-family:Inter,"Noto Sans SC","Microsoft YaHei","PingFang SC",system-ui,sans-serif}.t{font-size:48px;font-weight:800;fill:#f8fafc}.s{font-size:23px;fill:#a9bfe0}.h{font-size:25px;font-weight:750;fill:#f8fafc}.b{font-size:17px;fill:#c8d7ec}.m{font-size:14px;fill:#8da9ce}.k{font-size:16px;font-weight:700;fill:#66e7a4}.n{font-size:17px;font-weight:800;fill:#54a9ff}.metric{font-size:38px;font-weight:800;fill:#f8fafc}</style>',
    '<text x="58" y="62" class="n">ARIS<tspan fill="#f8fafc">4C</tspan></text>',
    f'<text x="{w/2}" y="72" text-anchor="middle" class="t">{esc(title)}</text>',
    f'<text x="{w/2}" y="112" text-anchor="middle" class="s">{esc(subtitle)}</text>']

def lines(s,x,y,items,klass="b",step=28):
    for i,t in enumerate(items): s.append(f'<text x="{x}" y="{y+i*step}" class="{klass}">{esc(t)}</text>')

def hero(rows,lang):
    zh=lang=="zh"; counts={k:sum(r["activity"]==k for r in rows) for k in ("active","gated","quiet","blocked")}
    avg=round(sum(r["progress"] for r in rows)/max(1,len(rows))); continuity=sum(r["handoff"] for r in rows); pdf=sum(r["pdf"] for r in rows)
    title="让研究成为一个可持续运行的系统" if zh else "Research as a living system."
    subtitle="论文 · 证据 · 双语输出 · 审查门 · 跨 Agent 连续性" if zh else "Papers · evidence · bilingual outputs · review gates · cross-agent continuity"
    s=head(title,subtitle,1600,500)
    s += ['<path d="M0 370 C320 300 520 510 820 390 S1320 260 1600 360 V500 H0 Z" fill="#0b2748"/>']
    labels=(["论文项目","平均成熟度","Active","At gate","handoff ready"] if zh else ["tracked papers","mean maturity","Active","At gate","handoff ready"])
    vals=[len(rows),f"{avg}%",counts["active"],counts["gated"],f"{continuity}/{len(rows)}"]
    for i,(v,l) in enumerate(zip(vals,labels)):
        x=70+i*300; s += [f'<rect x="{x}" y="205" width="255" height="110" rx="20" fill="{PANEL}" stroke="{GRID}"/>',
        f'<text x="{x+22}" y="255" class="metric">{v}</text>',f'<text x="{x+22}" y="288" class="b">{esc(l)}</text>']
    note=(f"当前 {pdf} 个项目已提供 EN + ZH PDF · continuity {continuity}/{len(rows)}"
          if zh else f"{pdf} project(s) expose EN + ZH PDFs · continuity {continuity}/{len(rows)}")
    s += [f'<text x="70" y="455" class="m">{esc(note)}</text>','</svg>']; return "\n".join(s)

def status(rows,lang):
    zh=lang=="zh"; counts={k:sum(r["activity"]==k for r in rows) for k in ("active","gated","quiet","blocked")}
    labels={"active":"Active","gated":"At gate","quiet":"Quiet","blocked":"Blocked"}; colors={"active":ACTIVE,"gated":GATED,"quiet":QUIET,"blocked":BLOCKED}
    title="Portfolio 当前状态" if zh else "Portfolio state"; subtitle="来自 papers/dashboard.json 的 MECE 管理状态" if zh else "MECE management states from papers/dashboard.json"
    s=head(title,subtitle,1600,420); x=80; total=len(rows); bar=1440
    for k in ("active","gated","quiet","blocked"):
        w=bar*counts[k]/max(1,total)
        if w: s.append(f'<rect x="{x:.1f}" y="185" width="{w:.1f}" height="58" fill="{colors[k]}"/>'); x+=w
    for i,k in enumerate(("active","gated","quiet","blocked")):
        xx=90+i*360; s += [f'<circle cx="{xx}" cy="320" r="10" fill="{colors[k]}"/>',
        f'<text x="{xx+22}" y="327" class="h">{labels[k]} · {counts[k]}</text>']
    s += [f'<text x="1510" y="327" text-anchor="end" class="m">Total {total}</text>','</svg>']; return "\n".join(s)

def maturity(rows,lang):
    zh=lang=="zh"; title="16 个 Paper 的成熟度" if zh else "Portfolio maturity by paper"
    subtitle="项目管理估计，不是科学结果；100% 表示仓库层最终输出契约满足" if zh else "Management estimate, not a scientific result; 100% means the repository-level final output contract is satisfied"
    colors={"active":ACTIVE,"gated":GATED,"quiet":QUIET,"blocked":BLOCKED}; s=head(title,subtitle,1600,880)
    for i,r in enumerate(rows):
        col=0 if i<8 else 1; row=i if i<8 else i-8; x=70+col*785; y=165+row*82
        name=ZH_TITLES.get(r["id"],r["short"]) if zh else r["short"]; label=f'{r["id"]} · {name}'
        if len(label)>38: label=label[:36]+"…"
        s += [f'<text x="{x}" y="{y}" class="h" font-size="20">{esc(label)}</text>',
        f'<text x="{x+660}" y="{y}" text-anchor="end" class="b">{r["progress"]}%</text>',
        f'<rect x="{x}" y="{y+18}" width="660" height="16" rx="8" fill="#1b385a"/>',
        f'<rect x="{x}" y="{y+18}" width="{6.6*r["progress"]}" height="16" rx="8" fill="{colors.get(r["activity"],ACTIVE)}"/>']
    s += ['</svg>']; return "\n".join(s)

def readiness(rows,lang):
    zh=lang=="zh"; total=len(rows); continuity=sum(r["handoff"] for r in rows); pdf=sum(r["pdf"] for r in rows); avg=round(sum(r["progress"] for r in rows)/max(1,total))
    title="交付与连续性" if zh else "Delivery & continuity"; subtitle="仓库不仅保存论文，也保存让下一位执行者继续研究所需的状态与上下文" if zh else "The repository preserves both research outputs and enough context for the next executor to continue"
    s=head(title,subtitle,1600,480)
    cards=([("项目",total,"canonical paper.json"),("可接管",continuity,f"{continuity}/{total} handoff"),("双语 PDF",pdf,f"{pdf}/{total} EN + ZH"),("平均成熟度",f"{avg}%","portfolio estimate")]
           if zh else [("Tracked projects",total,"canonical paper.json"),("Continuity-ready",continuity,f"{continuity}/{total} handoffs"),("Bilingual PDF-ready",pdf,f"{pdf}/{total} EN + ZH"),("Mean maturity",f"{avg}%","portfolio estimate")])
    for i,(lab,val,note) in enumerate(cards):
        x=70+i*380; s += [f'<rect x="{x}" y="180" width="330" height="180" rx="24" fill="{PANEL}" stroke="{GRID}"/>',
        f'<text x="{x+24}" y="235" class="metric">{esc(val)}</text>',f'<text x="{x+24}" y="278" class="h">{esc(lab)}</text>',f'<text x="{x+24}" y="318" class="m">{esc(note)}</text>']
    s += ['</svg>']; return "\n".join(s)

def architecture(rows,lang):
    zh=lang=="zh"; title="ARIS4C 研究系统架构" if zh else "ARIS4C research system architecture"
    subtitle="科学工作向前流动；handoff 上下文形成回路，让下一位执行者安全继续" if zh else "Scientific work flows forward; handoff context loops back so another executor can safely continue"
    s=head(title,subtitle,1600,780)
    cards=(["研究问题","ARIS 引擎","Paper 工作空间","Review gates","公开输出"] if zh else ["Research question","ARIS engine","Paper workspace","Review gates","Public output"])
    notes=(["想法 · 假设 · scope","检索 · 设计 · critique","canonical evidence hub","科学 · 复现 · 独立审查","EN + ZH PDF"] if zh else ["idea · hypothesis · scope","search · design · critique","canonical evidence hub","science · reproducibility","EN + ZH PDF"])
    xs=[60,360,660,1000,1300]; widths=[240,240,280,240,240]
    for i,(x,w) in enumerate(zip(xs,widths)):
        y=180 if i!=2 else 155; h=150 if i!=2 else 200
        s += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{PANEL2}" stroke="{ACCENT if i==2 else GRID}" stroke-width="2"/>',
        f'<text x="{x+20}" y="{y+38}" class="n">0{i+1}</text>',f'<text x="{x+20}" y="{y+82}" class="h">{esc(cards[i])}</text>',f'<text x="{x+20}" y="{y+118}" class="m">{esc(notes[i])}</text>']
        if i<4: s += [f'<line x1="{x+w+10}" y1="255" x2="{xs[i+1]-18}" y2="255" stroke="#54a9ff" stroke-width="4"/>',f'<path d="M{xs[i+1]-20} 246 L{xs[i+1]-5} 255 L{xs[i+1]-20} 264 Z" fill="#54a9ff"/>']
    subs=(["Evidence","双语论文","Visual narrative","handoff/"] if zh else ["Evidence","Bilingual paper","Visual narrative","handoff/"])
    subnotes=(["data · code · provenance","EN + ZH","figures · tables","8-file continuity pack"] if zh else ["data · code · provenance","EN + ZH","figures · tables","8-file continuity pack"])
    for i in range(4):
        x=310+i*315; s += [f'<rect x="{x}" y="450" width="270" height="120" rx="20" fill="{PANEL}" stroke="{GRID}"/>',
        f'<text x="{x+20}" y="495" class="h">{esc(subs[i])}</text>',f'<text x="{x+20}" y="535" class="m">{esc(subnotes[i])}</text>']
    loop=("Git → handoff/ → 下一台电脑 / 账号 / Agent → 同一个 canonical Paper 工作空间" if zh else "Git → handoff/ → next computer / account / agent → the same canonical paper workspace")
    s += ['<rect x="80" y="650" width="1440" height="64" rx="18" fill="#0b213c" stroke="#245d95"/>',
    f'<text x="110" y="691" class="k">{esc("跨 Agent continuity" if zh else "Cross-agent continuity")}</text>',
    f'<text x="360" y="691" class="b">{esc(loop)}</text>','</svg>']; return "\n".join(s)

def paper_structure(lang):
    zh=lang=="zh"; title="单篇 Paper 项目的通用结构" if zh else "Common structure of an ARIS4C paper project"
    subtitle="每个编号项目都遵循同一套可复现、可审计、可接管的工作空间" if zh else "A reproducible, auditable, resumable workspace for every numbered paper"
    s=head(title,subtitle,1600,900)
    s += ['<rect x="80" y="155" width="1440" height="590" rx="28" fill="#091f39" stroke="#245d95" stroke-width="2"/>',
    '<text x="120" y="210" class="h" font-size="32">papers/<tspan fill="#54a9ff">00X-project/</tspan></text>']
    cards=([
      ("paper.json","元数据 · 链接 · 状态",["标题、作者、状态、公开入口","与 ARIS provenance"]),
      ("manuscript/","中英文论文",["English / 中文源稿","以及公开/编译版本"]),
      ("figures/ + tables/","视觉叙事",["图表按问题与信息增益设计","不固定数量和图型"]),
      ("code/ + data/","分析 · 数据 · 溯源",["代码、处理数据、来源链接","与可复现分析资产"]),
      ("process/","设计 · gate · 冻结决策",["研究计划、审查门","预注册/冻结决策与状态"]),
      ("handoff/","跨 Agent 连续性",["STATUS · TODO · DECISIONS","CHATLOG · AGENT_HANDOFF · SESSION_LOG"])
    ] if zh else [
      ("paper.json","metadata · links · status",["title, authors, status, public entry","and ARIS provenance"]),
      ("manuscript/","English + Chinese papers",["source manuscripts","and compiled/public versions"]),
      ("figures/ + tables/","visual narrative",["visuals follow information gain","no fixed figure quota"]),
      ("code/ + data/","analysis · provenance",["code, processed data, source links","and reproducibility assets"]),
      ("process/","design · gates · frozen decisions",["study plan, review gates","preregistration and state"]),
      ("handoff/","cross-agent continuity",["STATUS · TODO · DECISIONS","CHATLOG · AGENT_HANDOFF · SESSION_LOG"])
    ])
    xs=[120,575,1030]; ys=[270,500]
    for i,c in enumerate(cards):
        x=xs[i%3]; y=ys[i//3]; s += [f'<rect x="{x}" y="{y}" width="390" height="185" rx="22" fill="{PANEL}" stroke="{GRID}"/>',
        f'<circle cx="{x+42}" cy="{y+42}" r="24" fill="#0f7ee8"/><text x="{x+42}" y="{y+49}" text-anchor="middle" class="h" font-size="18">{i+1}</text>',
        f'<text x="{x+82}" y="{y+48}" class="h">{esc(c[0])}</text>',f'<text x="{x+82}" y="{y+80}" class="s" font-size="18">{esc(c[1])}</text>']
        lines(s,x+28,y+118,c[2],"b",27)
    rule=("证据可追踪 · 完成时双语 · 图表按信息增益 · 可跨设备/账号/Agent 接管" if zh else "traceable evidence · bilingual at completion · adaptive visuals · resumable across devices/accounts/agents")
    s += ['<rect x="80" y="785" width="1440" height="62" rx="18" fill="#0b213c" stroke="#245d95"/>',f'<text x="120" y="825" class="k">{esc(rule)}</text>','</svg>']; return "\n".join(s)

def lifecycle(lang):
    zh=lang=="zh"; title="单篇 Paper 的生命周期" if zh else "Lifecycle of an ARIS4C paper"
    subtitle="从想法，到证据，到双语公开输出" if zh else "From idea, to evidence, to bilingual public output"
    s=head(title,subtitle,1600,900)
    steps=([
      ("问题 / 想法",["明确可研究的问题","及其现实或理论价值"]),
      ("界定范围与检索",["系统检索、定位 gap","确认可行性与新颖性"]),
      ("研究设计",["方法、数据、指标、对照","与 falsifier 先行"]),
      ("证据 / 代码 / 数据",["执行分析并保留","完整 provenance"]),
      ("论文撰写",["方法、结果、讨论","图表、引用与局限"]),
      ("Review gates",["科学、复现、独立审查","与质量门"]),
      ("公开输出",["EN + ZH PDF","代码、数据、图表与 handoff"])
    ] if zh else [
      ("Question / idea",["define the problem","and why it matters"]),
      ("Scope & search",["search prior art and the gap","test feasibility and novelty"]),
      ("Study design",["methods, data, metrics, controls","and falsifiers upfront"]),
      ("Evidence / code / data",["run analyses and preserve","complete provenance"]),
      ("Drafting",["methods, results, discussion","visuals, references, limits"]),
      ("Review gates",["science, reproducibility","independent review, quality"]),
      ("Public outputs",["EN + ZH PDFs","code, data, visuals, handoff"])
    ])
    w=205; gap=18; x0=35
    for i,(name,desc) in enumerate(steps):
        x=x0+i*(w+gap); s += [f'<rect x="{x}" y="190" width="{w}" height="470" rx="22" fill="{PANEL}" stroke="{GRID}"/>',
        f'<circle cx="{x+31}" cy="226" r="24" fill="#0f7ee8"/><text x="{x+31}" y="233" text-anchor="middle" class="h" font-size="18">{i+1}</text>',
        f'<text x="{x+18}" y="310" class="h" font-size="20">{esc(name)}</text>']; lines(s,x+18,365,desc,"b",32)
        if i<6: s += [f'<path d="M{x+w+3} 420 L{x+w+18} 420" stroke="#54a9ff" stroke-width="4"/>',f'<path d="M{x+w+14} 411 L{x+w+28} 420 L{x+w+14} 429 Z" fill="#54a9ff"/>']
    rules=("贯穿全程：证据可追踪 · 图表按信息增益自适应 · 完成时 EN + ZH · continuity 持续更新" if zh else "Cross-cutting: traceable evidence · adaptive visuals · EN + ZH at completion · continuity kept current")
    s += ['<rect x="35" y="720" width="1530" height="88" rx="22" fill="#0b213c" stroke="#245d95"/>',f'<text x="70" y="775" class="k" font-size="19">{esc(rules)}</text>','</svg>']; return "\n".join(s)

def handoff(lang):
    zh=lang=="zh"; title="跨 Agent 接管包" if zh else "Cross-agent handoff package"
    subtitle="让同一篇 Paper 在不同对话、账号、电脑和 Agent 之间持续推进" if zh else "Keep one paper resumable across conversations, accounts, computers, and agents"
    s=head(title,subtitle,1600,900)
    files=( [
      ("README.md","快速上手与读取顺序"),("STATUS.md","当前状态、进度、gate、blocker"),("TODO.md","开放任务、优先级与下一步"),
      ("DECISIONS.md","关键决策、理由与替代方案"),("CONTEXT.md","研究背景、scope 与关键上下文"),("CHATLOG.md","重要对话的 public-safe 摘要"),
      ("AGENT_HANDOFF.md","下一位 Agent 的明确接管说明"),("SESSION_LOG.md","每次执行、验证与 commit 记录")
    ] if zh else [
      ("README.md","cold-start guide and read order"),("STATUS.md","current state, progress, gate, blocker"),("TODO.md","open tasks, priorities, next actions"),
      ("DECISIONS.md","key decisions, rationale, alternatives"),("CONTEXT.md","research background, scope, context"),("CHATLOG.md","public-safe summaries of material conversations"),
      ("AGENT_HANDOFF.md","explicit takeover brief for the next agent"),("SESSION_LOG.md","execution, validation, and commit history")
    ])
    xs=[80,455,830,1205]; ys=[190,410]
    for i,(name,note) in enumerate(files):
        x=xs[i%4]; y=ys[i//4]; s += [f'<rect x="{x}" y="{y}" width="315" height="170" rx="22" fill="{PANEL}" stroke="{GRID}"/>',
        f'<circle cx="{x+38}" cy="{y+40}" r="22" fill="#0f7ee8"/><text x="{x+38}" y="{y+47}" text-anchor="middle" class="h" font-size="16">{i+1}</text>',
        f'<text x="{x+76}" y="{y+47}" class="h" font-size="22">{esc(name)}</text>']; lines(s,x+24,y+102,[note],"b",28)
    flow=("当前执行者 → 更新 handoff/ → Git 仓库 → 下一位执行者读取 handoff/ → 继续推进" if zh else "current executor → update handoff/ → Git repository → next executor reads handoff/ → continue")
    s += ['<rect x="80" y="675" width="1440" height="76" rx="20" fill="#0b213c" stroke="#245d95"/>',f'<text x="120" y="722" class="h">{esc(flow)}</text>',
    f'<text x="800" y="825" text-anchor="middle" class="k">{esc("continuity 是 final output contract 的组成部分，不是可选附加项" if zh else "continuity is part of the final output contract, not an optional extra")}</text>','</svg>']; return "\n".join(s)

def main():
    rows=load()
    funcs={"hero":hero,"portfolio-status":status,"portfolio-maturity":maturity,"delivery-readiness":readiness,"architecture":architecture}
    for lang in ("en","zh"):
        out=ASSET_DIR/lang; out.mkdir(parents=True,exist_ok=True)
        for name,fn in funcs.items(): (out/f"{name}.svg").write_text(fn(rows,lang)+"\n",encoding="utf-8")
        (out/"paper-structure.svg").write_text(paper_structure(lang)+"\n",encoding="utf-8")
        (out/"paper-lifecycle.svg").write_text(lifecycle(lang)+"\n",encoding="utf-8")
        (out/"handoff-package.svg").write_text(handoff(lang)+"\n",encoding="utf-8")
    print("Generated bilingual README assets: 16 SVGs")
    return 0
if __name__=="__main__": raise SystemExit(main())
