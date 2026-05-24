#!/usr/bin/env python3
"""Task 4: Numerical stability — semi-log L1 norm vs time.

L1 = (1/N) * sum_i |u_i|
For sin(pi*x) exact solution: L1 = 2/pi ≈ 0.6366 (constant in time).
Deviation from this constant signals numerical instability.
"""

import numpy as np
import matplotlib.pyplot as plt

# Read data: # CFL  scheme  time  L1
with open('stability_l1.dat') as f:
    lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]

data = {'LW': {}, 'VL': {}, 'SB': {}}
for line in lines:
    parts = line.split()
    cfl = float(parts[0])
    scheme = parts[1]
    t = float(parts[2])
    l1norm = float(parts[3])
    if cfl not in data[scheme]:
        data[scheme][cfl] = {'t': [], 'l1norm': []}
    data[scheme][cfl]['t'].append(t)
    data[scheme][cfl]['l1norm'].append(l1norm)

cfl_vals = sorted(data['LW'].keys())
schemes = ['LW', 'VL', 'SB']
scheme_labels = ['Lax-Wendroff', 'van Leer', 'SUPERBEE']
colors_s = {'LW': '#d62728', 'VL': '#2ca02c', 'SB': '#1f77b4'}

# Reference L1 for sin(pi*x): 2/pi ≈ 0.6366
l1_ref = 2.0 / np.pi

plt.rcParams.update({'font.size': 11, 'axes.grid': True, 'grid.alpha': 0.4})

fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for ax, scheme, label in zip(axes, schemes, scheme_labels):
    for cfl in cfl_vals:
        t = np.array(data[scheme][cfl]['t'])
        l1norm = np.array(data[scheme][cfl]['l1norm'])
        ax.semilogy(t, l1norm, label=f'CFL={cfl:.2f}')
    # Reference line at L1_exact = 2/pi
    ax.axhline(y=l1_ref, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.set_title(label)
    ax.set_xlabel(r'$t$')
    ax.set_ylabel(r'$L_1 = \frac{1}{N}\sum |u_i|$' if scheme == 'LW' else '')
    ax.legend(fontsize=8, loc='upper right')
    ax.set_ylim(5e-1, 1e12)

fig.suptitle('Numerical Stability: $L_1$ Norm vs. Time (smooth IC, $N=80$, '
             r'$L_1^{\mathrm{exact}} = 2/\pi \approx 0.637$)',
             fontsize=13)
fig.tight_layout()
fig.savefig('stability_l1.png', dpi=150)
plt.close(fig)
print('stability_l1.png saved')
