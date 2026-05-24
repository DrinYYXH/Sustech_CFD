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
