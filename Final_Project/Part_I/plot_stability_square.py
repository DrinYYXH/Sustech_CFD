"""Plot square-wave stability study: L1 vs time for each scheme and CFL."""
import numpy as np
import matplotlib.pyplot as plt

with open('stability_square.dat', 'r') as f:
    lines = f.readlines()

records = []
for line in lines:
    if line.startswith('#'):
        continue
    parts = line.split()
    cfl = float(parts[0])
    scheme = parts[1]
    t = float(parts[2])
    l1 = float(parts[3])
    records.append((cfl, scheme, t, l1))

records_by_scheme = {}
for cfl, scheme, t, l1 in records:
    key = (scheme, cfl)
    if key not in records_by_scheme:
        records_by_scheme[key] = ([], [])
    records_by_scheme[key][0].append(t)
    records_by_scheme[key][1].append(l1)

colors = {0.50: '#1b9e77', 0.80: '#7570b3', 1.00: '#d95f02',
          1.05: '#e7298a', 1.10: '#e41a1c'}
scheme_labels = {'LW': 'Lax-Wendroff', 'VL': 'van Leer', 'SB': 'SUPERBEE'}

fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

for ax, scheme in zip(axes, ['LW', 'VL', 'SB']):
    for cfl in [0.50, 0.80, 1.00, 1.05, 1.10]:
        key = (scheme, cfl)
        if key in records_by_scheme:
            t_arr = np.array(records_by_scheme[key][0])
            l1_arr = np.array(records_by_scheme[key][1])
            valid = l1_arr < 1e9
            ax.semilogy(t_arr[valid], l1_arr[valid],
                       color=colors[cfl], lw=1.0,
                       label=f'CFL={cfl}')
    ax.set_title(scheme_labels[scheme])
    ax.set_xlabel('t')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7, loc='upper left')

axes[0].set_ylabel(r'$L_1$ norm')

fig.suptitle('Square-wave stability: $L_1$ vs time', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig('stability_square.png', dpi=150, bbox_inches='tight')
print('Saved: stability_square.png')
