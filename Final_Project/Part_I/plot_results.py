#!/usr/bin/env python3
"""
Plotting script for Part I: 1D Linear Advection Equation
Generates:
  1. Solution comparison at t = 2.0
  2. Solution comparison at t = 8.0
  3. Total Variation history for all three schemes
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Read data files ---
def read_solution(filename):
    """Read x, u_numerical, u_analytical from data file."""
    data = np.loadtxt(filename, skiprows=2)
    x = data[:, 0]
    u_num = data[:, 1]
    u_ana = data[:, 2]
    return x, u_num, u_ana

def read_tv(filename):
    """Read time, TV_LW, TV_VL, TV_SB from TV file."""
    data = np.loadtxt(filename, skiprows=1)
    t = data[:, 0]
    tv_lw = data[:, 1]
    tv_vl = data[:, 2]
    tv_sb = data[:, 3]
    return t, tv_lw, tv_vl, tv_sb

# --- Load all data ---
x, lw_t2, _ = read_solution('lax_wendroff_t2.dat')
_, vl_t2, ana = read_solution('van_leer_t2.dat')
_, sb_t2, _   = read_solution('superbee_t2.dat')

_, lw_t8, _  = read_solution('lax_wendroff_t8.dat')
_, vl_t8, _  = read_solution('van_leer_t8.dat')
_, sb_t8, _  = read_solution('superbee_t8.dat')

t_tv, tv_lw, tv_vl, tv_sb = read_tv('total_variation.dat')

# --- Plot settings ---
plt.rcParams.update({
    'font.size': 12,
    'figure.figsize': (10, 6),
    'lines.linewidth': 1.5,
    'axes.grid': True,
    'grid.alpha': 0.4,
})

colors = {
    'ana': 'black',
    'lw':  '#d62728',  # red
    'vl':  '#2ca02c',  # green
    'sb':  '#1f77b4',  # blue
}

# =====================================================================
# Figure 1: Solutions at t = 2.0
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, ana,  color=colors['ana'], linestyle='--', linewidth=2.0, label='Analytical')
ax.plot(x, lw_t2, color=colors['lw'], label='Lax-Wendroff')
ax.plot(x, vl_t2, color=colors['vl'], label='van Leer')
ax.plot(x, sb_t2, color=colors['sb'], label='SUPERBEE')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$u$')
ax.set_title(r'Solution at $t = 2.0$ (CFL = 0.8, $N = 160$)')
ax.legend(loc='upper right')
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-0.3, 1.5)
fig.tight_layout()
fig.savefig('solution_t2.png', dpi=150)
plt.close(fig)

# =====================================================================
# Figure 2: Solutions at t = 8.0
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, ana,  color=colors['ana'], linestyle='--', linewidth=2.0, label='Analytical')
ax.plot(x, lw_t8, color=colors['lw'], label='Lax-Wendroff')
ax.plot(x, vl_t8, color=colors['vl'], label='van Leer')
ax.plot(x, sb_t8, color=colors['sb'], label='SUPERBEE')

ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$u$')
ax.set_title(r'Solution at $t = 8.0$ (CFL = 0.8, $N = 160$)')
ax.legend(loc='upper right')
ax.set_xlim(-1.0, 1.0)
ax.set_ylim(-0.3, 1.5)
fig.tight_layout()
fig.savefig('solution_t8.png', dpi=150)
plt.close(fig)

# =====================================================================
# Figure 3: Total Variation history
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t_tv, tv_lw, color=colors['lw'], label='Lax-Wendroff')
ax.plot(t_tv, tv_vl, color=colors['vl'], label='van Leer')
ax.plot(t_tv, tv_sb, color=colors['sb'], label='SUPERBEE')

ax.axhline(y=2.0, color='gray', linestyle=':', linewidth=1.0, alpha=0.7)

ax.set_xlabel(r'$t$')
ax.set_ylabel(r'$TV = \sum |u_{i+1} - u_i|$')
ax.set_title(r'Total Variation vs. Time (CFL = 0.8, $N = 160$)')
ax.legend(loc='best')
fig.tight_layout()
fig.savefig('total_variation.png', dpi=150)
plt.close(fig)

print('Plots saved:')
print('  solution_t2.png')
print('  solution_t8.png')
print('  total_variation.png')
