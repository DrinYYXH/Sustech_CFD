#!/usr/bin/env python3
"""Task 4: Numerical stability — semi-log max|u| vs time."""

import numpy as np
import matplotlib.pyplot as plt

# Read data: # CFL  scheme  time  max|u|
with open('stability_maxval.dat') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

data = {'LW': {}, 'VL': {}, 'SB': {}}
for line in lines:
    parts = line.split()
    cfl = float(parts[0])
    scheme = parts[1]
    t = float(parts[2])
    umax = float(parts[3])
    if cfl not in data[scheme]:
        data[scheme][cfl] = {'t': [], 'umax': []}
    data[scheme][cfl]['t'].append(t)
    data[scheme][cfl]['umax'].append(umax)

cfl_vals = sorted(data['LW'].keys())
schemes = ['LW', 'VL', 'SB']
scheme_labels = ['Lax-Wendroff', 'van Leer', 'SUPERBEE']
colors_s = {'LW': '#d62728', 'VL': '#2ca02c', 'SB': '#1f77b4'}

plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': 0.4})

fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for ax, scheme, label in zip(axes, schemes, scheme_labels):
    for cfl in cfl_vals:
        t = np.array(data[scheme][cfl]['t'])
        umax = np.array(data[scheme][cfl]['umax'])
        ax.semilogy(t, umax, label=f'CFL={cfl:.2f}')
    ax.set_title(label)
    ax.set_xlabel(r'$t$')
    ax.set_ylabel(r'$\max|u|$' if scheme == 'LW' else '')
    ax.legend(fontsize=8, loc='upper right')
    ax.set_ylim(1e-1, 1e12)

fig.suptitle('Numerical Stability: max|u| vs. Time (smooth IC, N=80)',
             fontsize=13)
fig.tight_layout()
fig.savefig('stability.png', dpi=150)
plt.close(fig)
print('stability.png saved')
