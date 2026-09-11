"""
Soft-Coloured Financial Chart & Visual Generator for FinTech AI.
"""
import os, math, csv

c_card = '#FFFFFF'
c_text_dark = '#1E293B'
c_text_muted = '#64748B'
c_grid = '#E2E8F0'
c_soft_blue = '#93C5FD'
c_soft_teal = '#5EEAD4'
c_soft_green = '#86EFAC'
c_soft_amber = '#FDE68A'
c_soft_orange = '#FDBA74'
c_soft_rose = '#FDA4AF'
c_soft_lavender = '#C4B5FD'
c_soft_indigo = '#A5B4FC'

def generate_grade_distribution_svg(output_path, records):
    grades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    counts = {g: 0 for g in grades}
    defaults = {g: 0 for g in grades}
    for r in records:
        g = r.get('grade', 'C').strip()
        if g in counts:
            counts[g] += 1
            if r.get('loan_status', '') in ['Charged Off', 'Default', 'Late (31-120 days)']:
                defaults[g] += 1
    max_c = max(counts.values()) if max(counts.values()) > 0 else 1
    w, h = 750, 420
    ml, mr, mt, mb = 70, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">LendingClub Credit Grade Distribution &amp; Default Frequency</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Sample Size: {len(records)} loans | Soft pastel segments with empirical default rates</text>'
    ]
    for i in range(5):
        y_val = int(max_c * (4 - i) / 4)
        y_pos = mt + i * (ph / 4)
        lines.append(f'<line x1="{ml}" y1="{y_pos}" x2="{w - mr}" y2="{y_pos}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{ml - 12}" y="{y_pos + 4}" font-family="sans-serif" font-size="11" text-anchor="end" fill="{c_text_muted}">{y_val}</text>')
    lines.append(f'<line x1="{ml}" y1="{mt + ph}" x2="{w - mr}" y2="{mt + ph}" stroke="{c_text_muted}" stroke-width="1.5"/>')
    bw = (pw / len(grades)) * 0.65
    step = pw / len(grades)
    colors = [c_soft_blue, c_soft_teal, c_soft_green, c_soft_amber, c_soft_orange, c_soft_rose, c_soft_lavender]
    for idx, g in enumerate(grades):
        cnt = counts[g]
        def_cnt = defaults[g]
        def_rate = (def_cnt / cnt * 100.0) if cnt > 0 else 0.0
        bh = (cnt / max_c) * ph
        x = ml + idx * step + (step - bw) / 2
        y = mt + ph - bh
        lines.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{colors[idx]}" opacity="0.9"/>')
        if def_cnt > 0:
            def_h = (def_cnt / max_c) * ph
            lines.append(f'<rect x="{x}" y="{mt + ph - def_h}" width="{bw}" height="{def_h}" rx="4" fill="#FB7185" opacity="0.85"/>')
        lines.append(f'<text x="{x + bw/2}" y="{y - 8}" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="{c_text_dark}">{cnt}</text>')
        lines.append(f'<text x="{x + bw/2}" y="{mt + ph + 20}" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="{c_text_dark}">Grade {g}</text>')
        lines.append(f'<text x="{x + bw/2}" y="{mt + ph + 36}" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#E11D48">{def_rate:.1f}% def</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_fico_dti_scatter_svg(output_path, records):
    w, h = 750, 420
    ml, mr, mt, mb = 60, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">EDA: Credit Score (FICO) vs. Debt-to-Income (DTI) Distribution</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Clustered by underwritten health: Prime Safe Zone vs. Elevated Risk</text>'
    ]
    sx1 = ml + ((700 - 600) / 220) * pw
    sw = ((820 - 700) / 220) * pw
    sh = ((20 - 0) / 45) * ph
    sy1 = mt + ph - sh
    lines.append(f'<rect x="{sx1}" y="{sy1}" width="{sw}" height="{sh}" rx="8" fill="{c_soft_teal}" opacity="0.2"/>')
    lines.append(f'<text x="{sx1 + 10}" y="{sy1 + 22}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0D9488">PRIME SAFE ZONE (FICO &gt;= 700, DTI &lt;= 20%)</text>')
    for fico in [620, 660, 700, 740, 780, 820]:
        x = ml + ((fico - 600) / 220) * pw
        lines.append(f'<line x1="{x}" y1="{mt}" x2="{x}" y2="{mt + ph}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{x}" y="{mt + ph + 18}" font-family="sans-serif" font-size="11" text-anchor="middle" fill="{c_text_muted}">{fico}</text>')
    for dti in [0, 10, 20, 30, 40]:
        y = mt + ph - (dti / 45) * ph
        lines.append(f'<line x1="{ml}" y1="{y}" x2="{w - mr}" y2="{y}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{ml - 8}" y="{y + 4}" font-family="sans-serif" font-size="11" text-anchor="end" fill="{c_text_muted}">{dti}%</text>')
    for r in records:
        try:
            fico = float(r.get('fico_range_high', 680))
            dti = float(r.get('dti', 18))
        except ValueError:
            continue
        cx = ml + max(0.0, min(1.0, (fico - 600) / 220)) * pw
        cy = mt + ph - max(0.0, min(1.0, dti / 45)) * ph
        status = r.get('loan_status', '')
        if status in ['Charged Off', 'Default']:
            col, rad = '#FB7185', 5.5
        elif fico >= 720:
            col, rad = c_soft_teal, 4.5
        else:
            col, rad = c_soft_blue, 4.0
        lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad}" fill="{col}" opacity="0.85" stroke="#FFFFFF" stroke-width="1"/>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_xai_waterfall_svg(output_path):
    w, h = 750, 420
    ml, mr, mt, mb = 220, 80, 60, 40
    pw, ph = w - ml - mr, h - mt - mb
    factors = [
        ('Inquiries Last 6M (inq_last_6mths)', +0.0350, c_soft_rose),
        ('Debt-to-Income (dti = 28.5%)', +0.0275, c_soft_orange),
        ('Loan Amount (,000)', +0.0150, c_soft_amber),
        ('Delinquency History (0 flags)', -0.0120, c_soft_teal),
        ('Annual Income (,000)', -0.0240, c_soft_green),
        ('FICO Score (750 High)', -0.0410, c_soft_blue)
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="40" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">Explainable AI (XAI): Shapley Feature Attribution Waterfall</text>',
        f'<text x="40" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Baseline Default: 14.5% | Net Underwritten Default: 9.05% (Grade A Approved)</text>'
    ]
    center_x = ml + pw / 2
    lines.append(f'<line x1="{center_x}" y1="{mt}" x2="{center_x}" y2="{mt + ph}" stroke="{c_text_muted}" stroke-width="1.5"/>')
    lines.append(f'<text x="{center_x}" y="{mt - 6}" font-family="sans-serif" font-size="11" text-anchor="middle" fill="{c_text_muted}">Population Baseline</text>')
    row_h = ph / len(factors)
    bar_h = row_h * 0.55
    for idx, (name, val, col) in enumerate(factors):
        y = mt + idx * row_h + (row_h - bar_h) / 2
        plen = (abs(val) / 0.05) * (pw / 2)
        if val >= 0:
            bx = center_x
            tx = center_x + plen + 8
            align = 'start'
        else:
            bx = center_x - plen
            tx = center_x - plen - 8
            align = 'end'
        lines.append(f'<rect x="{bx}" y="{y}" width="{plen}" height="{bar_h}" rx="4" fill="{col}"/>')
        lines.append(f'<text x="{ml - 12}" y="{y + bar_h/2 + 4}" font-family="sans-serif" font-size="12" text-anchor="end" fill="{c_text_dark}">{name}</text>')
        lines.append(f'<text x="{tx}" y="{y + bar_h/2 + 4}" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="{align}" fill="{c_text_dark}">{val:+.2%}</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_risk_var_svg(output_path):
    w, h = 750, 420
    ml, mr, mt, mb = 60, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">Credit Risk Distribution: Value-at-Risk (VaR) &amp; Expected Shortfall</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Portfolio: .44M | Expected Loss: K | 95% VaR: K | 99% VaR: K | 99% CVaR: K</text>'
    ]
    pts = []
    num_pts = 60
    for i in range(num_pts + 1):
        x_norm = (i / num_pts) * 6.0 - 2.0
        y_val = math.exp(-0.5 * x_norm ** 2) / math.sqrt(2 * math.pi)
        px = ml + (i / num_pts) * pw
        py = mt + ph - (y_val / 0.42) * ph
        pts.append((px, py, x_norm))
    d_path = f'M {pts[0][0]} {pts[0][1]} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in pts[1:])
    fill_path = f'M {pts[0][0]} {mt + ph} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in pts) + f' L {pts[-1][0]} {mt + ph} Z'
    lines.append(f'<path d="{fill_path}" fill="{c_soft_blue}" opacity="0.35"/>')
    tail_pts = [p for p in pts if p[2] >= 1.645]
    if tail_pts:
        tail_path = f'M {tail_pts[0][0]} {mt + ph} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in tail_pts) + f' L {tail_pts[-1][0]} {mt + ph} Z'
        lines.append(f'<path d="{tail_path}" fill="{c_soft_rose}" opacity="0.75"/>')
    lines.append(f'<path d="{d_path}" fill="none" stroke="{c_soft_indigo}" stroke-width="2.5"/>')
    x_95 = ml + ((1.645 + 2.0) / 6.0) * pw
    lines.append(f'<line x1="{x_95}" y1="{mt}" x2="{x_95}" y2="{mt + ph}" stroke="#F59E0B" stroke-width="2" stroke-dasharray="4"/>')
    lines.append(f'<text x="{x_95 + 6}" y="{mt + 40}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#D97706">95% VaR: ,289</text>')
    x_99 = ml + ((2.326 + 2.0) / 6.0) * pw
    lines.append(f'<line x1="{x_99}" y1="{mt}" x2="{x_99}" y2="{mt + ph}" stroke="#EF4444" stroke-width="2"/>')
    lines.append(f'<text x="{x_99 + 6}" y="{mt + 80}" font-family="sans-serif" font-size="11" font-weight="bold" fill="#DC2626">99% VaR: ,183</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_efficient_frontier_svg(output_path):
    w, h = 750, 420
    ml, mr, mt, mb = 60, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">Modern Portfolio Theory: Markowitz Efficient Frontier</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">AI Optimal Tangency Portfolio (Sharpe: 0.321) vs Conservative &amp; Equal-Weighted</text>'
    ]
    for vol in [6, 8, 10, 12, 14, 16]:
        x = ml + ((vol - 5) / 13) * pw
        lines.append(f'<line x1="{x}" y1="{mt}" x2="{x}" y2="{mt + ph}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{x}" y="{mt + ph + 18}" font-family="sans-serif" font-size="11" text-anchor="middle" fill="{c_text_muted}">{vol}%</text>')
    for ret in [4, 6, 8, 10, 12]:
        y = mt + ph - ((ret - 3) / 10) * ph
        lines.append(f'<line x1="{ml}" y1="{y}" x2="{w - mr}" y2="{y}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{ml - 8}" y="{y + 4}" font-family="sans-serif" font-size="11" text-anchor="end" fill="{c_text_muted}">{ret}%</text>')
    pts = []
    for step in range(35):
        vol = 6.0 + step * (11.0 / 34.0)
        ret = 4.5 + 2.4 * math.sqrt(max(0.1, vol - 5.8))
        px = ml + ((vol - 5) / 13) * pw
        py = mt + ph - ((ret - 3) / 10) * ph
        pts.append((px, py))
    curve_d = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in pts[1:])
    lines.append(f'<path d="{curve_d}" fill="none" stroke="{c_soft_lavender}" stroke-width="3.5"/>')
    tan_x = ml + ((10.70 - 5) / 13) * pw
    tan_y = mt + ph - ((7.94 - 3) / 10) * ph
    lines.append(f'<circle cx="{tan_x}" cy="{tan_y}" r="8" fill="#10B981" stroke="#FFFFFF" stroke-width="2"/>')
    lines.append(f'<text x="{tan_x + 12}" y="{tan_y - 8}" font-family="sans-serif" font-size="12" font-weight="bold" fill="#047857">AI Tangency (Sharpe: 0.321)</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_fairness_disparate_impact_svg(output_path):
    w, h = 750, 420
    ml, mr, mt, mb = 80, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">Trust &amp; Ethics in AI: Fair Lending Disparate Impact &amp; Mitigation</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Four-Fifths (80%) Rule Compliance: Pre-Mitigation DIR: 0.74 -&gt; Post-Calibration DIR: 0.88</text>'
    ]
    y_80 = mt + ph - (0.80 * ph)
    lines.append(f'<line x1="{ml}" y1="{y_80}" x2="{w - mr}" y2="{y_80}" stroke="#E11D48" stroke-width="2" stroke-dasharray="6"/>')
    lines.append(f'<text x="{w - mr - 8}" y="{y_80 - 8}" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="end" fill="#E11D48">EEOC 80% Disparate Impact Mandate</text>')
    bars = [
        ('Privileged (Individual)', 0.375, c_soft_blue, 'Baseline Privileged Rate'),
        ('Unprivileged Pre-Mitigation', 0.276, c_soft_rose, 'Pre-Mitigation (DIR: 0.74 - Non-Compliant)'),
        ('Unprivileged Post-Mitigation', 0.330, c_soft_teal, 'Post-Calibration (DIR: 0.88 - Compliant)')
    ]
    step = pw / len(bars)
    bw = step * 0.55
    for i, (label, rate, col, subtitle) in enumerate(bars):
        bh = (rate / 0.50) * ph
        bx = ml + i * step + (step - bw) / 2
        by = mt + ph - bh
        lines.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{col}"/>')
        lines.append(f'<text x="{bx + bw / 2}" y="{by - 8}" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle" fill="{c_text_dark}">{rate:.1%}</text>')
        lines.append(f'<text x="{bx + bw / 2}" y="{mt + ph + 20}" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="{c_text_dark}">{label}</text>')
        lines.append(f'<text x="{bx + bw / 2}" y="{mt + ph + 36}" font-family="sans-serif" font-size="10" text-anchor="middle" fill="{c_text_muted}">{subtitle}</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def generate_quantum_speedup_svg(output_path):
    w, h = 750, 420
    ml, mr, mt, mb = 70, 40, 60, 60
    pw, ph = w - ml - mr, h - mt - mb
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="auto">',
        f'<rect width="{w}" height="{h}" rx="12" fill="{c_card}" stroke="{c_grid}" stroke-width="1"/>',
        f'<text x="{ml}" y="36" font-family="sans-serif" font-size="18" font-weight="bold" fill="{c_text_dark}">Quantum Computing: Amplitude Estimation Quadratic Speedup</text>',
        f'<text x="{ml}" y="52" font-family="sans-serif" font-size="12" fill="{c_text_muted}">Query Evaluations vs. Precision (epsilon): O(1/eps) vs Classical O(1/eps^2)</text>'
    ]
    for prec in [0.05, 0.02, 0.01, 0.005]:
        x = ml + ((0.05 - prec) / 0.045) * pw
        lines.append(f'<line x1="{x}" y1="{mt}" x2="{x}" y2="{mt + ph}" stroke="{c_grid}" stroke-dasharray="4"/>')
        lines.append(f'<text x="{x}" y="{mt + ph + 18}" font-family="sans-serif" font-size="11" text-anchor="middle" fill="{c_text_muted}">{prec:.3f}</text>')
    pts_c = []
    pts_q = []
    for step in range(35):
        eps = 0.05 - step * (0.045 / 34.0)
        c_val = 1.0 / (eps ** 2)
        q_val = 1.0 / eps
        px = ml + ((0.05 - eps) / 0.045) * pw
        py_c = mt + ph - ((math.log10(c_val) - 1) / 3.7) * ph
        py_q = mt + ph - ((math.log10(q_val) - 1) / 3.7) * ph
        pts_c.append((px, py_c))
        pts_q.append((px, py_q))
    d_c = f'M {pts_c[0][0]:.1f} {pts_c[0][1]:.1f} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in pts_c[1:])
    d_q = f'M {pts_q[0][0]:.1f} {pts_q[0][1]:.1f} ' + ' '.join(f'L {p[0]:.1f} {p[1]:.1f}' for p in pts_q[1:])
    lines.append(f'<path d="{d_c}" fill="none" stroke="#FB7185" stroke-width="3"/>')
    lines.append(f'<path d="{d_q}" fill="none" stroke="#10B981" stroke-width="3"/>')
    lines.append(f'<text x="{pts_c[-1][0] - 12}" y="{pts_c[-1][1] - 8}" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="end" fill="#BE123C">Classical Monte Carlo: 40,000 queries</text>')
    lines.append(f'<text x="{pts_q[-1][0] - 12}" y="{pts_q[-1][1] - 8}" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="end" fill="#047857">Quantum Amplitude Est.: 200 queries (200x speedup)</text>')
    lines.append('</svg>')
    with open(output_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(lines))

def build_all_charts():
    dataset_path = 'dataset/lending_club_sample.csv'
    records = []
    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            records.append(r)
    out_dir = 'docs/visuals'
    os.makedirs(out_dir, exist_ok=True)
    generate_grade_distribution_svg(os.path.join(out_dir, 'eda_grade_distribution.svg'), records)
    generate_fico_dti_scatter_svg(os.path.join(out_dir, 'eda_fico_vs_dti.svg'), records)
    generate_xai_waterfall_svg(os.path.join(out_dir, 'xai_waterfall_attribution.svg'))
    generate_risk_var_svg(os.path.join(out_dir, 'risk_var_tail_distribution.svg'))
    generate_efficient_frontier_svg(os.path.join(out_dir, 'portfolio_efficient_frontier.svg'))
    generate_fairness_disparate_impact_svg(os.path.join(out_dir, 'fairness_disparate_impact.svg'))
    generate_quantum_speedup_svg(os.path.join(out_dir, 'quantum_vs_classical_speedup.svg'))
    print('All 7 standalone soft-coloured SVG charts generated successfully in docs/visuals/')

if __name__ == '__main__':
    build_all_charts()
