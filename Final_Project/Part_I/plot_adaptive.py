#!/usr/bin/env python3
"""Task 5: Adaptive Lax-Wendroff — comparison with LW, VL, SB."""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12, 'axes.grid': True, 'grid.alpha': 0.4})

# --- Read solution data ---
def read_sol(fname):
    d = np.loadtxt(fname, skiprows=2)
    return d[:, 0], d[:, 1], d[:, 2]

x, lw_t2, ana2 = read_sol('lax_wendroff_t2.dat')
_, vl_t2, _     = read_sol('van_leer_t2.dat')
_, sb_t2, _     = read_sol('superbee_t2.dat')
_, alw_t2, _    = read_sol('adaptive_lw_t2.dat')

_, lw_t8, _  = read_sol('lax_wendroff_t8.dat')
_, vl_t8, _  = read_sol('van_leer_t8.dat')
_, sb_t8, _  = read_sol('superbee_t8.dat')
_, alw_t8, _ = read_sol('adaptive_lw_t8.dat')

# --- Read TV data ---
tv_main = np.loadtxt('total_variation.dat', skiprows=1)
tv_alw  = np.loadtxt('adaptive_tv.dat', skiprows=1)

colors = {'ana': 'black', 'lw': '#d62728', 'vl': '#2ca02c',
          'sb': '#1f77b4', 'alw': '#ff7f0e'}

# =====================================================================
# Figure 1: Solutions at t=2.0 (full domain)
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, ana2,  '--', color=colors['ana'], linewidth=2.0, label='Analytical')
ax.plot(x, lw_t2, '-', color=colors['lw'], label='Lax-Wendroff')
ax.plot(x, vl_t2, '-', color=colors['vl'], label='van Leer')
ax.plot(x, sb_t2, '-', color=colors['sb'], label='SUPERBEE')
ax.plot(x, alw_t2,'-', color=colors['alw'], label='Adaptive LW')
ax.set_xlabel(r'$x$'); ax.set_ylabel(r'$u$')
ax.set_title(r'Solution at $t=2.0$ (CFL=0.8, N=160)')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlim(-1, 1); ax.set_ylim(-0.3, 1.5)
fig.tight_layout(); fig.savefig('adaptive_solution_t2.png', dpi=150)
plt.close(fig)

# =====================================================================
# Figure 2: Solutions at t=8.0 (full domain)
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, ana2,  '--', color=colors['ana'], linewidth=2.0, label='Analytical')
ax.plot(x, lw_t8, '-', color=colors['lw'], label='Lax-Wendroff')
ax.plot(x, vl_t8, '-', color=colors['vl'], label='van Leer')
ax.plot(x, sb_t8, '-', color=colors['sb'], label='SUPERBEE')
ax.plot(x, alw_t8,'-', color=colors['alw'], label='Adaptive LW')
ax.set_xlabel(r'$x$'); ax.set_ylabel(r'$u$')
ax.set_title(r'Solution at $t=8.0$ (CFL=0.8, N=160)')
ax.legend(loc='upper right', fontsize=10)
ax.set_xlim(-1, 1); ax.set_ylim(-0.3, 1.5)
fig.tight_layout(); fig.savefig('adaptive_solution_t8.png', dpi=150)
plt.close(fig)

# =====================================================================
# Figure 3: TV history
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tv_main[:, 0], tv_main[:, 1], color=colors['lw'], label='Lax-Wendroff')
ax.plot(tv_main[:, 0], tv_main[:, 2], color=colors['vl'], label='van Leer')
ax.plot(tv_main[:, 0], tv_main[:, 3], color=colors['sb'], label='SUPERBEE')
ax.plot(tv_alw[:, 0],  tv_alw[:, 1],  color=colors['alw'], label='Adaptive LW')
ax.axhline(y=2.0, color='gray', linestyle=':', alpha=0.5)
ax.set_xlabel(r'$t$'); ax.set_ylabel(r'$TV$')
ax.set_title(r'Total Variation vs. Time (CFL=0.8, N=160)')
ax.legend(fontsize=10)
fig.tight_layout(); fig.savefig('adaptive_tv.png', dpi=150)
plt.close(fig)

# =====================================================================
# Figure 4: Zoom near left discontinuity at t=2.0
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5))
mask = (x > -0.7) & (x < -0.3)
ax.plot(x[mask], ana2[mask],  '--', color=colors['ana'], linewidth=2.0, label='Analytical')
ax.plot(x[mask], lw_t2[mask], '-', color=colors['lw'], label='Lax-Wendroff')
ax.plot(x[mask], vl_t2[mask], '-', color=colors['vl'], label='van Leer')
ax.plot(x[mask], sb_t2[mask], '-', color=colors['sb'], label='SUPERBEE')
ax.plot(x[mask], alw_t2[mask],'-', color=colors['alw'], label='Adaptive LW')
ax.set_xlabel(r'$x$'); ax.set_ylabel(r'$u$')
ax.set_title(r'Zoom near left discontinuity at $t=2.0$')
ax.legend(fontsize=10)
fig.tight_layout(); fig.savefig('adaptive_zoom_t2.png', dpi=150)
plt.close(fig)

# --- Summary stats ---
print('ALW at t=2.0: min={:.4f}  max={:.4f}'.format(alw_t2.min(), alw_t2.max()))
print('ALW at t=8.0: min={:.4f}  max={:.4f}'.format(alw_t8.min(), alw_t8.max()))
print('LW  at t=2.0: min={:.4f}  max={:.4f}'.format(lw_t2.min(), lw_t2.max()))
print('LW  at t=8.0: min={:.4f}  max={:.4f}'.format(lw_t8.min(), lw_t8.max()))
print('ALW TV at t=2.0: {:.4f}'.format(tv_alw[np.argmin(np.abs(tv_alw[:,0]-2.0)), 1]))
print('ALW TV at t=8.0: {:.4f}'.format(tv_alw[-1, 1]))
print('Plots saved.')
