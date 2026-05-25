#!/usr/bin/env python3
"""Generate publication-quality figures for Part I PPT slides."""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    'font.size': 14,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'axes.linewidth': 1.2,
})

# ===========================================================================
# Slide 2: Square-wave initial condition
# ===========================================================================
fig, ax = plt.subplots(figsize=(8, 3.5))

x = np.linspace(-1, 1, 1000)
u = np.where((x > -0.5) & (x < 0.5), 1.0, 0.0)

ax.plot(x, u, 'b-', linewidth=2.0)
ax.fill_between(x, 0, u, alpha=0.15, color='blue')

ax.set_xlabel(r'$x$', fontsize=16)
ax.set_ylabel(r'$u(x,0)$', fontsize=16)
ax.set_title(r'Initial Condition: Square Wave', fontsize=16, fontweight='bold')
ax.set_xlim(-1, 1)
ax.set_ylim(-0.1, 1.2)
ax.set_yticks([0.0, 0.5, 1.0])

# Annotations
ax.annotate(r'$u=1$', xy=(0, 1.0), xytext=(0.3, 1.08),
            fontsize=13, ha='center', color='blue')
ax.annotate(r'$u=0$', xy=(-0.8, 0.0), xytext=(-0.8, 0.12),
            fontsize=13, ha='center', color='blue')

# Domain boundary markers
for xb in [-1, 1]:
    ax.axvline(x=xb, color='gray', linestyle=':', linewidth=0.8, alpha=0.6)

fig.tight_layout(pad=0.8)
fig.savefig(os.path.join(OUT_DIR, 'ppt_initial_condition.png'), dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_initial_condition.png')

# ===========================================================================
# Slide 2: Parameter table (clean, presentation-ready)
# ===========================================================================
fig, ax = plt.subplots(figsize=(5, 3))
ax.axis('off')

params = [
    (r'$N$', '160'),
    (r'$\Delta x$', '0.0125'),
    ('CFL', '0.5, 0.8'),
    (r'$\Delta t$ (CFL=0.8)', '0.01'),
    (r'$\Delta t$ (CFL=0.5)', '0.00625'),
]

table = ax.table(
    cellText=[[p[0], p[1]] for p in params],
    colLabels=['Parameter', 'Value'],
    cellLoc='center',
    loc='center',
    colWidths=[0.35, 0.25],
)
table.auto_set_font_size(False)
table.set_fontsize(13)
table.scale(1.0, 1.6)

# Style: header row
for j in range(2):
    cell = table[0, j]
    cell.set_facecolor('#4472C4')
    cell.set_text_props(color='white', fontweight='bold', fontsize=14)

# Style: alternating row colors
for i in range(1, len(params) + 1):
    for j in range(2):
        cell = table[i, j]
        if i % 2 == 1:
            cell.set_facecolor('#D6E4F0')
        else:
            cell.set_facecolor('white')

ax.set_title('Simulation Parameters', fontsize=15, fontweight='bold', pad=15)

fig.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT_DIR, 'ppt_parameter_table.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_parameter_table.png')

# ===========================================================================
# Computational flow diagram (linear pipeline)
# ===========================================================================
fig, ax = plt.subplots(figsize=(16, 4.0))
ax.set_xlim(0, 16)
ax.set_ylim(0, 4.0)
ax.axis('off')

arrow = dict(arrowstyle='->', color='#555555', lw=2.0)

# --- Nodes: exactly equal spacing (6 boxes, w=2.1, gap=0.5) ---
node_w, node_h = 2.1, 1.15
x_positions = [1.5, 4.1, 6.7, 9.3, 11.9, 14.5]   # np.linspace(1.5, 14.5, 6)
y_center = 2.6

nodes = [
    (x_positions[0], 'Parameters',    r'$N, \nu, \Delta x, \Delta t$',          '#E3F2FD', '#1565C0'),
    (x_positions[1], 'Grid & IC',     r'$x_i = x_{\min} + (i-1/2)\Delta x$',    '#E3F2FD', '#1565C0'),
    (x_positions[2], 'Compute Slopes', r'$\delta_j = \phi(r_j)\cdot(u_{j+1}-u_j)$', '#FFF3E0', '#E65100'),
    (x_positions[3], 'Advance',  r'$u_j^{n+1}$ from $u_j^n, \delta_j$',    '#E8F5E9', '#2E7D32'),
    (x_positions[4], 'Loop',          r'$t \to t+\Delta t$,  periodic BC',      '#F3E5F5', '#7B1FA2'),
    (x_positions[5], 'Output & Plot', r'.dat  $\to$  Python  $\to$  .png',      '#FFEBEE', '#C62828'),
]

for x, title, detail, face, edge in nodes:
    rect = mpatches.FancyBboxPatch(
        (x - node_w/2, y_center - node_h/2), node_w, node_h,
        boxstyle='round,pad=0.2', facecolor=face, edgecolor=edge, lw=1.5, alpha=0.88)
    ax.add_patch(rect)
    ax.text(x, y_center + 0.18, title, ha='center', va='center', fontsize=11,
            fontweight='bold', color=edge)
    ax.text(x, y_center - 0.30, detail, ha='center', va='center', fontsize=7.2,
            color='#555555')

# --- Arrows between nodes ---
for i in range(len(nodes) - 1):
    x0 = nodes[i][0] + node_w/2
    x1 = nodes[i+1][0] - node_w/2
    ax.annotate('', xy=(x1, y_center), xytext=(x0, y_center), arrowprops=arrow)

# --- Loop-back arc (above the nodes) ---
loop_src_x  = nodes[4][0]                     # Loop
loop_dest_x = nodes[2][0]                     # Compute Slopes
arc_y = y_center + node_h/2 + 0.3

# Draw arc path
ax.annotate('', xy=(loop_dest_x, y_center + node_h/2 + 0.08),
            xytext=(loop_src_x, y_center + node_h/2 + 0.08),
            arrowprops=dict(arrowstyle='->', color='#7B1FA2', lw=1.8,
                           connectionstyle='arc3,rad=0.4'))
ax.text((loop_src_x + loop_dest_x)/2, arc_y + 0.65, 'next time step',
        ha='center', fontsize=9, color='#7B1FA2', fontstyle='italic',
        bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.7))

# --- Stage labels (centered under each group) ---
label_y = y_center - node_h/2 - 0.45
ax.text(2.8,  label_y, 'Setup',            ha='center', fontsize=9, color='#1565C0', fontweight='bold')
ax.text(9.3,  label_y, 'Time Integration',  ha='center', fontsize=9, color='#2E7D32', fontweight='bold')
ax.text(14.5, label_y, 'Post-Process',      ha='center', fontsize=9, color='#C62828', fontweight='bold')

# --- Braces / grouping lines ---
brace_y = y_center - node_h/2 - 0.72
for xs, xe, c in [(0.45, 5.15, '#1565C0'), (5.65, 12.95, '#2E7D32'), (13.45, 15.55, '#C62828')]:
    ax.plot([xs, xe], [brace_y, brace_y], color=c, lw=1.2, marker='|', markersize=4)

# --- Title ---
ax.set_title('Computational Flow — 1D Linear Advection Solver (Part I)',
             fontsize=16, fontweight='bold', pad=15)

fig.tight_layout(pad=0.3)
fig.savefig(os.path.join(OUT_DIR, 'ppt_code_structure.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_code_structure.png')

# ===========================================================================
# Slide 3: Format equivalence — Class (flux) vs Implemented (cell-wise)
# ===========================================================================
fig, ax = plt.subplots(figsize=(14, 5.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 5.5)
ax.axis('off')

ax.set_title('Format Equivalence: From Flux Form to Cell-Wise Form',
             fontsize=16, fontweight='bold', pad=18)

# --- Box 1: Class format (flux-based conservative form) ---
y1 = 4.0
box_props = dict(boxstyle='round,pad=0.4', facecolor='#E3F2FD', edgecolor='#1565C0', lw=1.8)
ax.text(7, y1,
        r'$u_j^{n+1} = u_j^n - \frac{\Delta t}{\Delta x}\left(F_{j+1/2} - F_{j-1/2}\right)$',
        ha='center', va='center', fontsize=15,
        bbox=box_props)
ax.text(7, y1 + 0.65, 'Class Format (Conservative Flux Form)',
        ha='center', fontsize=11, fontweight='bold', color='#1565C0')

# --- Arrow 1 ---
ax.annotate('', xy=(7, 3.3), xytext=(7, y1 - 0.65),
            arrowprops=dict(arrowstyle='->', color='#555555', lw=2.2))

# --- Flux definition ---
ax.text(7, 2.9,
        r'$F_{j+1/2} = a\,u_j + \frac{a}{2}(1-\nu)\,\delta_j, \qquad '
        r'F_{j-1/2} = a\,u_{j-1} + \frac{a}{2}(1-\nu)\,\delta_{j-1}$',
        ha='center', va='center', fontsize=12,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFF8E1', edgecolor='#F9A825', lw=1.2))

ax.text(7, 2.45, r'with $\delta_j = \phi(r_j)\,(u_{j+1} - u_j),\quad \nu = a\Delta t/\Delta x$',
        ha='center', fontsize=11, color='#555555')

# --- Arrow 2 ---
ax.annotate('', xy=(7, 2.05), xytext=(7, 2.2),
            arrowprops=dict(arrowstyle='->', color='#555555', lw=2.2))

# --- Expansion ---
ax.text(7, 1.85, r'Substitute $F_{j+1/2}, F_{j-1/2}$, divide by $a$:',
        ha='center', fontsize=10, color='#555555', fontstyle='italic')

# --- Box 2: Implemented format ---
y2 = 1.1
box_props2 = dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9', edgecolor='#2E7D32', lw=1.8)
ax.text(7, y2,
        r'$u_j^{n+1} = u_j^n - \nu\,(u_j^n - u_{j-1}^n) - \frac{\nu(1-\nu)}{2}\left(\delta_j - \delta_{j-1}\right)$',
        ha='center', va='center', fontsize=15,
        bbox=box_props2)
ax.text(7, y2 + 0.7, 'Implemented Form (Cell-Wise Reconstruction)',
        ha='center', fontsize=11, fontweight='bold', color='#2E7D32')

# --- Key insight box at bottom ---
ax.text(7, 0.1,
        r'$\mathbf{Key:}\ \delta_j = 0 \Rightarrow$ 1st-order upwind;  '
        r'$\delta_j = u_{j+1}-u_j \Rightarrow$ Lax--Wendroff;  '
        r'$\delta_j$ via limiter $\Rightarrow$ van Leer / SUPERBEE',
        ha='center', fontsize=10.5, color='#333333',
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#F5F5F5', edgecolor='#999999', lw=0.8))

# --- Side annotation: δ_j mapping ---
ax.text(0.3, 3.6, r'$\delta_j$ Definition', fontsize=10, fontweight='bold', color='#333333', rotation=90, va='center')

delta_box = dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#999999', lw=0.6)
mappings = [
    (0.8, 4.8, r'LW: $\delta_j = u_{j+1}-u_j$'),
    (0.8, 4.3, r'VL: $\delta_j = \frac{r+|r|}{1+|r|}(u_{j+1}-u_j)$'),
    (0.8, 3.8, r'SB: $\delta_j = \max(0,\min(2r,1),\min(r,2))(u_{j+1}-u_j)$'),
]
for x, y, txt in mappings:
    ax.text(x, y, txt, ha='left', va='center', fontsize=9, bbox=delta_box)

fig.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT_DIR, 'ppt_format_equivalence.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_format_equivalence.png')

# ===========================================================================
# Slide 11: (c, ν) stability contour map — piecewise von Neumann analysis
# ===========================================================================
# |e^{σΔt}(c,ν,s)|² = 1 - 4ν(1-ν)(1-c)s + 4ν²(1-ν)[c²(1-ν)-2c]s²
# Unstable if max_{s∈[0,1]} |e^{σΔt}|² > 1

c_vals = np.linspace(0, 2.5, 300)
nu_vals = np.linspace(0, 1.5, 300)
C, Nu = np.meshgrid(c_vals, nu_vals)

# For each (c,ν), find max |e^{σΔt}|² over s ∈ [0,1]
s_test = np.linspace(0, 1, 200)
max_g2 = np.zeros_like(C)

for i in range(len(nu_vals)):
    for j in range(len(c_vals)):
        c = c_vals[j]
        nu = nu_vals[i]
        # |e^{σΔt}|² as a function of s
        g2 = 1.0 - 4*nu*(1-nu)*(1-c)*s_test + 4*nu**2*(1-nu)*(c**2*(1-nu) - 2*c)*s_test**2
        # Also check at s=1 (the boundaries)
        max_g2[i, j] = np.max(g2)

fig, ax = plt.subplots(figsize=(10, 7))

# Filled contour: stable (white/blue) vs unstable (red)
levels = [0, 0.99, 1.0, 1.01, 1.05, 1.1, 1.2, 1.5, 2.0, 5.0]
cmap = plt.cm.RdYlBu_r
cs = ax.contourf(C, Nu, np.log10(np.maximum(max_g2, 1e-6)), levels=20,
                  cmap='RdYlBu_r', alpha=0.85)

# Stability boundary: max_g2 = 1
ax.contour(C, Nu, max_g2, levels=[1.0], colors='black', linewidths=2.5,
           linestyles='-')

# Shade the unstable region (max_g2 > 1) lightly
ax.contourf(C, Nu, max_g2, levels=[1.0, 100], colors=['#FFE0E0'], alpha=0.3)

# CFL = 1 line
ax.axhline(y=1.0, color='#333333', linestyle='--', linewidth=1.2)
ax.text(2.35, 1.02, r'$\nu = 1$', fontsize=10, color='#333333', va='bottom')

# Mark key points
for cx, nux, label, color in [
    (0.0, 0.5, r'$c=0$ (upwind)', '#1a9641'),
    (1.0, 0.5, r'$c=1$ (LW)', '#d7191c'),
    (2.0, 0.5, r'$c=2$ (SB limit)', '#2b83ba'),
]:
    ax.plot(cx, nux, 'o', color=color, markersize=10, markeredgecolor='white', markeredgewidth=1.5)
    ax.annotate(label, xy=(cx, nux), xytext=(cx + 0.15, nux + 0.12),
                fontsize=11, fontweight='bold', color=color,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# Sweby region shading
ax.axvspan(0, 2, alpha=0.06, color='green')
ax.text(1.0, 1.35, 'Sweby\nregion', ha='center', fontsize=9, color='#2d8a2d',
        fontstyle='italic', alpha=0.7)

# Labels
ax.set_xlabel(r'Limiter output $c = \phi(r)$', fontsize=14)
ax.set_ylabel(r'CFL number $\nu$', fontsize=14)
ax.set_title(r'Stability Map: $\max_s |e^{\sigma\Delta t}(c,\nu,s)|^2$'
             '\n(Piecewise von Neumann Analysis)',
             fontsize=14, fontweight='bold')

# Colorbar
cbar = fig.colorbar(cs, ax=ax, label=r'$\log_{10}\left(\max_s |e^{\sigma\Delta t}|^2\right)$',
                    shrink=0.85, pad=0.02)
cbar.set_label(r'$\log_{10}\left(\max_s |e^{\sigma\Delta t}|^2\right)$', fontsize=11)

ax.set_xlim(0, 2.5)
ax.set_ylim(0, 1.5)

# Annotation box
ax.text(0.05, 0.05,
        r'$\mathbf{Stable:}\ \max |e^{\sigma\Delta t}|^2 \leq 1$' + '\n'
        r'$\mathbf{Unstable:}\ \max |e^{\sigma\Delta t}|^2 > 1$' + '\n'
        r'$c=0$: always stable (upwind)' + '\n'
        r'$c=1$: stable for $\nu \leq 1$' + '\n'
        r'$c=2$: unstable even at $\nu < 1$',
        transform=ax.transAxes, fontsize=9,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='gray', alpha=0.9),
        va='bottom', ha='left')

fig.tight_layout(pad=0.8)
fig.savefig(os.path.join(OUT_DIR, 'ppt_stability_contour.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_stability_contour.png')

# ===========================================================================
# Slide 7: Three-weight continuous maps in (c, ν) plane
# ===========================================================================
c_vals = np.linspace(-0.5, 3.5, 400)
nu_vals = np.linspace(0, 1.0, 300)
Cw, Nuw = np.meshgrid(c_vals, nu_vals)

# Three weights
Wm1 = Nuw * (2 - Cw + Cw*Nuw) / 2      # w_{-1}: upwind
W0  = 1 - Nuw + Cw*Nuw - Cw*Nuw**2     # w_0: center
Wp1 = -Cw * Nuw * (1 - Nuw) / 2         # w_{+1}: downwind
Wmin = np.minimum(np.minimum(Wm1, W0), Wp1)  # most negative weight

fig, axes = plt.subplots(1, 4, figsize=(22, 4.8))

titles = [
    r'$w_{-1}$ (upwind)',
    r'$w_0$ (center)',
    r'$w_{+1}$ (downwind)',
    r'$\min(w_{-1}, w_0, w_{+1})$',
]
data = [Wm1, W0, Wp1, Wmin]
cmap = plt.cm.RdBu_r

for ax, title, D in zip(axes, titles, data):
    # Symmetric color scale around 0
    vmax = max(abs(D.max()), abs(D.min()))
    levels = np.linspace(-vmax, vmax, 41)

    cs = ax.contourf(Cw, Nuw, D, levels=levels, cmap=cmap, extend='both')

    # Zero contour
    ax.contour(Cw, Nuw, D, levels=[0], colors='black', linewidths=2.0)

    ax.set_xlabel(r'$c = \phi(r)$', fontsize=12)
    ax.set_ylabel(r'$\nu$' if ax == axes[0] else '', fontsize=12)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.axhline(y=1.0, color='#333333', linestyle='--', linewidth=0.8)
    ax.set_xlim(-0.5, 3.5)

    # Mark c=0, c=1, c=2, c=3 points
    for cx, label in [(0, '0'), (1, '1'), (2, '2'), (3, '3')]:
        ax.plot(cx, 0.8, 'o', color='#333333', markersize=6, zorder=5)
        ax.annotate(r'$c=' + label + '$', xy=(cx, 0.8), xytext=(cx+0.08, 0.88),
                    fontsize=9, color='#333333')

    # Sweby boundary
    ax.axvline(x=2.0, color='#999999', linestyle=':', linewidth=0.8)

# Shared colorbar
cbar = fig.colorbar(cs, ax=axes, shrink=0.92, pad=0.015, aspect=40)
cbar.set_label('Weight value', fontsize=12)

fig.suptitle(r'Stencil Weights $w_{-1}, w_0, w_{+1}$ vs. $(c, \nu)$  —  Blue = negative,  Red = positive',
             fontsize=14, fontweight='bold', y=1.01)

fig.tight_layout(pad=0.8)
fig.savefig(os.path.join(OUT_DIR, 'ppt_weight_signs.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_weight_signs.png')

# ===========================================================================
# r_j = (u_j - u_{j-1}) / (u_{j+1} - u_j) vs x for square-wave IC
# ===========================================================================
N = 160
xmin, xmax = -1.0, 1.0
dx = (xmax - xmin) / N
x = np.linspace(xmin + dx/2, xmax - dx/2, N)

# Square wave IC
u = np.where((x > -0.5) & (x < 0.5), 1.0, 0.0)

# Compute r_j with periodic BC
r = np.zeros(N)
eps = 1e-15
for i in range(N):
    im1 = i - 1 if i > 0 else N - 1
    ip1 = i + 1 if i < N - 1 else 0
    du_back = u[i] - u[im1]
    du_forw = u[ip1] - u[i]
    if abs(du_forw) < eps:
        r[i] = np.nan
    else:
        r[i] = du_back / du_forw

# Also compute curvature sensor θ_j and c_j = 1 - θ_j
theta = np.zeros(N)
for i in range(N):
    im1 = i - 1 if i > 0 else N - 1
    ip1 = i + 1 if i < N - 1 else 0
    d2 = abs(u[ip1] - 2*u[i] + u[im1])
    d1 = abs(u[ip1] - u[i]) + abs(u[i] - u[im1]) + 1e-12
    theta[i] = min(d2 / d1, 1.0)

c_adaptive = 1.0 - theta

fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

# Top: u(x)
ax = axes[0]
ax.plot(x, u, 'b-', linewidth=1.5)
ax.fill_between(x, 0, u, alpha=0.1, color='blue')
ax.set_ylabel(r'$u(x,0)$', fontsize=13)
ax.set_ylim(-0.1, 1.3)
ax.set_yticks([0, 1])
ax.grid(True, alpha=0.3)
ax.set_title(r'Square-wave IC and the two sensors: $r_j$ vs. $\theta_j$', fontsize=14, fontweight='bold')

# Annotate flow regimes
for xpos, label, ypos in [(-0.75, 'u=0\n(constant)', 0.3), (0, 'u=1\n(constant)', 0.3),
                            (-0.5, 'left\njump', 1.1), (0.5, 'right\njump', 1.1)]:
    ax.annotate(label, xy=(xpos, ypos), ha='center', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

# Middle: r_j with logarithmic y-scale
ax = axes[1]
# Split into positive and negative for log scale
r_pos = np.where((r > 0) & np.isfinite(r), r, np.nan)
r_neg = np.where((r < 0) & np.isfinite(r), -r, np.nan)

ax.semilogy(x, r_pos, 'o', color='#2ca02c', markersize=3, alpha=0.7, label=r'$r_j > 0$')
ax.semilogy(x, r_neg, 'o', color='#d62728', markersize=3, alpha=0.7, label=r'$r_j < 0$ (as $-r_j$)')

# NaN markers for undefined r (0/0 cases)
nan_mask = np.isnan(r)
ax.scatter(x[nan_mask], np.ones(nan_mask.sum()) * 1e-3, marker='x', color='gray', s=15,
           alpha=0.5, label='undefined (0/0)')

ax.set_ylabel(r'$|r_j|$ (log)', fontsize=13)
ax.set_ylim(1e-3, 1e4)
ax.legend(fontsize=8, loc='upper right', ncol=3)
ax.grid(True, alpha=0.3)
ax.axhline(y=1.0, color='gray', linestyle=':', linewidth=0.8)

# Annotate key r values
ax.annotate(r'$r \to \infty$', xy=(-0.5, 1e4), ha='center', fontsize=9, color='#2ca02c')
ax.annotate(r'$r \to -\infty$', xy=(0.5, 1e4), ha='center', fontsize=9, color='#d62728')

# Bottom: adaptive c_j = 1 - θ_j
ax = axes[2]
ax.plot(x, c_adaptive, 'o-', color='#9467bd', markersize=3, linewidth=1.0)
ax.axhline(y=1.0, color='#2ca02c', linestyle='--', linewidth=0.8)
ax.axhline(y=0.0, color='#d62728', linestyle='--', linewidth=0.8)
ax.set_ylabel(r'$c_j = 1 - \theta_j$', fontsize=13)
ax.set_xlabel(r'$x$', fontsize=13)
ax.set_ylim(-0.1, 1.3)
ax.grid(True, alpha=0.3)

# Annotate c values
ax.annotate(r'$c \approx 0$ (upwind)', xy=(-0.52, 0.02), fontsize=9, color='#d62728')
ax.annotate(r'$c \approx 0$ (upwind)', xy=(0.52, 0.02), fontsize=9, color='#d62728')

fig.tight_layout(pad=0.5)
fig.savefig(os.path.join(OUT_DIR, 'ppt_r_sensor.png'), dpi=200,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close(fig)
print('Saved: ppt_r_sensor.png')
