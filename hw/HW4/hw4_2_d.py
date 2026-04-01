import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("fort.20")

t = data[:,0]

l1_up = data[:,1]
l1_cen = data[:,2]
l1_down = data[:,3]

l2_up = data[:,4]
l2_cen = data[:,5]
l2_down = data[:,6]

# =========================
# L1 plot
# =========================
plt.figure(figsize=(8,5))

plt.plot(t, l1_up,
         color='blue',
         linestyle='-',
         marker='o',
         markersize=4,
         linewidth=2,
         label='Upwind L1')

plt.plot(t, l1_cen,
         color='red',
         linestyle='--',
         marker='s',
         markersize=4,
         linewidth=2,
         label='Central L1')

plt.plot(t, l1_down,
         color='green',
         linestyle='-.',
         marker='^',
         markersize=4,
         linewidth=2,
         label='Downwind L1')

plt.yscale('log')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.title("L1 Error vs Time")
plt.xlabel("time")
plt.ylabel("L1 error")
plt.ylim(0, 10)
plt.show()

# =========================
# L2 plot
# =========================
plt.figure(figsize=(8,5))

plt.plot(t, l2_up,
         color='blue',
         linestyle='-',
         marker='o',
         markersize=4,
         linewidth=2,
         label='Upwind L2')

plt.plot(t, l2_cen,
         color='red',
         linestyle='--',
         marker='s',
         markersize=4,
         linewidth=2,
         label='Central L2')

plt.plot(t, l2_down,
         color='green',
         linestyle='-.',
         marker='^',
         markersize=4,
         linewidth=2,
         label='Downwind L2')

plt.yscale('log')
plt.grid(True, which='both', alpha=0.3)
plt.legend()
plt.title("L2 Error vs Time")
plt.xlabel("time")
plt.ylabel("L2 error")
plt.ylim(0, 10)
plt.show()