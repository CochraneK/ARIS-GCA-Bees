#!/usr/bin/env python3
"""Regenerate ARIS4C001 SVG figures from committed machine-readable results."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "figures"

STYLE = '''<style>
text{font-family:Inter,Arial,sans-serif;fill:#17201f}.title{font-size:28px;font-weight:700}.sub{font-size:15px;fill:#6f7773}.axis{stroke:#9aa09c;stroke-width:1}.grid{stroke:#e5e7e5;stroke-width:1}.label{font-size:16px}.small{font-size:13px;fill:#6f7773}.value{font-size:14px;font-weight:700}.mark{fill:#1f8c82}.mark2{fill:#5d62c9}.mark3{fill:#a46c18}
</style>'''

def wrap(title: str, subtitle: str, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="640" viewBox="0 0 1000 640" role="img">
<rect width="1000" height="640" fill="#ffffff"/>{STYLE}
<text x="60" y="55" class="title">{title}</text>
<text x="60" y="82" class="sub">{subtitle}</text>{body}</svg>'''

def fig1(summary: dict) -> str:
    vals = summary['descriptive_pooled_correlations']
    rows = [('AL–RL', vals['AL_RL']), ('AL–NP', vals['AL_NP']), ('RL–NP', vals['RL_NP'])]
    xmin, xmax, x0, x1 = -0.1, 0.8, 250, 920
    sx = lambda v: x0 + (v-xmin)/(xmax-xmin)*(x1-x0)
    b=[]
    for i in range(10):
        v=-0.1+i*0.1; x=sx(v)
        b.append(f'<line x1="{x}" y1="130" x2="{x}" y2="520" class="grid"/><text x="{x}" y="548" text-anchor="middle" class="small">{v:.1f}</text>')
    b.append(f'<line x1="{sx(0)}" y1="125" x2="{sx(0)}" y2="525" stroke="#555" stroke-width="1.5"/>')
    for i,(name,r) in enumerate(rows):
        y=200+i*120; lo=r['ci95_low']; hi=r['ci95_high']; est=r['r']
        b.append(f'<text x="60" y="{y+6}" class="label">{name}</text><line x1="{sx(lo)}" y1="{y}" x2="{sx(hi)}" y2="{y}" stroke="#1f8c82" stroke-width="5" stroke-linecap="round"/><circle cx="{sx(est)}" cy="{y}" r="9" class="mark"/><text x="930" y="{y+5}" class="value">{est:.3f} [{lo:.3f}, {hi:.3f}]</text>')
    b.append('<text x="585" y="595" text-anchor="middle" class="label">Descriptive pooled correlation (r), Fisher-z synthesis</text>')
    return wrap('Figure 1 · Published learning covariance','Published-summary synthesis; not a population meta-analysis.',''.join(b))

def fig2(summary: dict) -> str:
    loads=summary['inputs']['factor_loadings']; names=['AL','RL','NP']
    b=['<line x1="110" y1="520" x2="900" y2="520" class="axis"/><line x1="110" y1="130" x2="110" y2="520" class="axis"/>']
    for i in range(6):
        v=i*0.2; y=520-v*360; b.append(f'<line x1="110" y1="{y}" x2="900" y2="{y}" class="grid"/><text x="90" y="{y+5}" text-anchor="end" class="small">{v:.1f}</text>')
    for i,name in enumerate(names):
        cx=260+i*240; v=loads['visual'][name]; o=loads['olfactory'][name]; yv=520-v*360; yo=520-o*360
        b.append(f'<rect x="{cx-65}" y="{yv}" width="55" height="{520-yv}" rx="5" class="mark"/><rect x="{cx+10}" y="{yo}" width="55" height="{520-yo}" rx="5" class="mark2"/><text x="{cx}" y="552" text-anchor="middle" class="label">{name}</text><text x="{cx-38}" y="{yv-8}" text-anchor="middle" class="value">{v:.3f}</text><text x="{cx+37}" y="{yo-8}" text-anchor="middle" class="value">{o:.3f}</text>')
    b.append(f'<text x="505" y="600" text-anchor="middle" class="small">Tucker congruence = {summary["tucker_congruence_visual_vs_olfactory"]:.5f}; variance = {loads["visual"]["variance"]*100:.1f}% visual, {loads["olfactory"]["variance"]*100:.1f}% olfactory.</text>')
    return wrap('Figure 2 · Cross-modality factor loading structure','Published one-factor loadings reported by Peñaherrera-Aguirre et al. (2024).',''.join(b))

def fig3(model: dict) -> str:
    Ns=[60,90,120,160]; xs=[220,410,600,790]; y=lambda v:520-v*360
    cor=[model['sample_sizes'][str(n)]['selection_rate']['two_factor_correlated'] for n in Ns]
    ind=[model['sample_sizes'][str(n)]['selection_rate']['two_factor_independent'] for n in Ns]
    one=[model['sample_sizes'][str(n)]['selection_rate']['one_factor'] for n in Ns]
    path=lambda vals:' '.join(('M' if i==0 else 'L')+f'{xs[i]} {y(v)}' for i,v in enumerate(vals))
    b=['<line x1="120" y1="520" x2="900" y2="520" class="axis"/><line x1="120" y1="130" x2="120" y2="520" class="axis"/>']
    for i in range(6):
        v=i*0.2; yy=y(v); b.append(f'<line x1="120" y1="{yy}" x2="900" y2="{yy}" class="grid"/><text x="98" y="{yy+5}" text-anchor="end" class="small">{round(v*100)}%</text>')
    b.append(f'<path d="{path(cor)}" fill="none" stroke="#1f8c82" stroke-width="5"/><path d="{path(ind)}" fill="none" stroke="#5d62c9" stroke-width="5"/><path d="{path(one)}" fill="none" stroke="#a46c18" stroke-width="4" stroke-dasharray="8 7"/>')
    for i,n in enumerate(Ns):
        b.append(f'<text x="{xs[i]}" y="550" text-anchor="middle" class="label">N={n}</text><circle cx="{xs[i]}" cy="{y(cor[i])}" r="7" class="mark"/><circle cx="{xs[i]}" cy="{y(ind[i])}" r="7" class="mark2"/><circle cx="{xs[i]}" cy="{y(one[i])}" r="6" class="mark3"/>')
    b.append('<text x="510" y="600" text-anchor="middle" class="small">Synthetic diagnostic only: 200 replications; loading=.65; factor correlation=.35. Not empirical evidence about bees.</text>')
    return wrap('Figure 3 · Synthetic model-recovery diagnostic','BIC selection under a two-correlated-factor data-generating model.',''.join(b))

def main() -> None:
    OUT.mkdir(exist_ok=True)
    summary=json.loads((DATA/'published_summary_synthesis.json').read_text())
    model=json.loads((DATA/'model_recovery_synthetic.json').read_text())
    (OUT/'figure1_published_learning_covariance.svg').write_text(fig1(summary),encoding='utf-8')
    (OUT/'figure2_factor_loading_congruence.svg').write_text(fig2(summary),encoding='utf-8')
    (OUT/'figure3_model_recovery.svg').write_text(fig3(model),encoding='utf-8')
    print('Regenerated 3 ARIS4C001 SVG figures')

if __name__ == '__main__':
    main()
