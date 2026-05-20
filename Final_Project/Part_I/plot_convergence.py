#!/usr/bin/env python3
"""Task 3: Order of accuracy — log-log error vs dx plots."""

import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('convergence.dat', skiprows=1)
N    = data[:, 0].astype(int)
dx   = data[:, 1]
l1_lw, linf_lw = data[:, 2], data[:, 3]
l1_vl, linf_vl = data[:, 4], data[:, 5]
l1_sb, linf_sb = data[:, 6], data[:, 7]

plt.rcParams.update({'font.size': 12, 'axes.grid': True, 'grid.alpha': 0.4})

def slope_str(dx, err):
    """Fit log10(err) vs log10(dx) and return slope."""
    m, _ = np.polyfit(np.log10(dx), np.log10(err), 1)
    return m

def plot_errors(title, dx, errs, labels, colors, filename):
    fig, ax = plt.subplots(figsize=(8, 6))
    for err, label, color in zip(errs, labels, colors):
        ax.loglog(dx, err, 'o-', color=color, label=label)
        m = slope_str(dx, err)
        ax.loglog(dx, err[0] * (dx / dx[0])**m, '--', color=color, alpha=0.5,
                  label=f'{label} slope = {m:.2f}')
    # Reference slopes
    ref = dx**2 * errs[0][0] / dx[0]**2
    ax.loglog(dx, ref, ':', color='gray', alpha=0.5, label=r'$O(\Delta x^2)$')
    ax.set_xlabel(r'$\Delta x$')
    ax.set_ylabel('Error')
    ax.set_title(title)
    ax.legend(fontsize=10)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)

# L1 plot
plot_errors(r'$L_1$ Error Convergence (smooth IC, $t=1.0$, CFL=0.8)',
            dx,
            [l1_lw, l1_vl, l1_sb],
            ['Lax-Wendroff', 'van Leer', 'SUPERBEE'],
            ['#d62728', '#2ca02c', '#1f77b4'],
            'convergence_l1.png')

# Linf plot
plot_errors(r'$L_\infty$ Error Convergence (smooth IC, $t=1.0$, CFL=0.8)',
            dx,
            [linf_lw, linf_vl, linf_sb],
            ['Lax-Wendroff', 'van Leer', 'SUPERBEE'],
            ['#d62728', '#2ca02c', '#1f77b4'],
            'convergence_linf.png')

print('Plot convergence_l1.png:')
for name, err in [('LW', l1_lw), ('VL', l1_vl), ('SB', l1_sb)]:
    print(f'  {name} L1 slope = {slope_str(dx, err):.2f}')
print('Plot convergence_linf.png:')
for name, err in [('LW', linf_lw), ('VL', linf_vl), ('SB', linf_sb)]:
    print(f'  {name} Linf slope = {slope_str(dx, err):.2f}')
print('Done.')
