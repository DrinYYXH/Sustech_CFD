import numpy as np
import matplotlib.pyplot as plt

N = 160
L = 2.0
dx = L / N
a = 1.0
C = 2.5
dt = C * dx / a

x = np.linspace(0, L, N, endpoint=False)

u0 = np.sin(np.pi * x) + 0.6 * np.sin(3 * np.pi * x)

# ======================
# exact solution
# ======================

def exact(x, t):
    return (np.sin(np.pi * (x - a*t))
          + 0.6 * np.sin(3*np.pi * (x - a*t)))

# ======================
# schemes
# ======================

def step_Lax(u):
    return (u
        - 0.5*C*(np.roll(u,-1) - np.roll(u,1))
        + 0.5*C**2*(np.roll(u,-1) - 2*u + np.roll(u,1)))

def step_B(u):
    return (u
        - C*(u - np.roll(u,1))
        - 0.5*C*(1-C)*(u - 2*np.roll(u,1) + np.roll(u,2)))

def step_center(u):
    return (u
        - 0.5*C*(np.roll(u,-1) - np.roll(u,1)))

def step_upwind(u):
    return (u
        - C*(u - np.roll(u,1)))

def step_downwind(u):
    return (u
        - C*(np.roll(u,-1) - u))

schemes = {
    "Lax-Wendroff": step_Lax,
    "Beam-Warming": step_B,
    "Center": step_center,
    "Upwind": step_upwind,
    "Downwind": step_downwind
}

# ======================
# onset + σ（最终稳定版）
# ======================

def detect_sigma(time_arr, data):

    t = np.array(time_arr)
    y = np.array(data)

    logy = np.log(y + 1e-16)

    # ======================
    # ✔ 全局最优分段点检测
    # ======================

    best_i = 5
    best_err = 1e30

    for i in range(5, len(t)-5):

        # 左段拟合
        t1 = t[:i]
        y1 = logy[:i]

        k1, b1 = np.polyfit(t1, y1, 1)
        err1 = np.mean((y1 - (k1*t1 + b1))**2)

        # 右段拟合
        t2 = t[i:]
        y2 = logy[i:]

        k2, b2 = np.polyfit(t2, y2, 1)
        err2 = np.mean((y2 - (k2*t2 + b2))**2)

        total_err = err1 + err2

        if total_err < best_err:
            best_err = total_err
            best_i = i

    onset_time = t[best_i]

    # ======================
    # σ：用后段指数增长率
    # ======================

    t_fit = t[best_i:]
    y_fit = y[best_i:]

    mask = y_fit > 1e-16

    sigma, _ = np.polyfit(
        t_fit[mask],
        np.log(y_fit[mask] + 1e-16),
        1
    )

    return sigma, onset_time

# ======================
# plotting
# ======================

fig, axes = plt.subplots(2, 5, figsize=(20, 8))

Tmax = 4.0

# ======================
# main loop
# ======================

for col, (name, scheme) in enumerate(schemes.items()):

    u = u0.copy()
    t = 0

    L1_list = []
    L2_list = []
    time_list = []

    while t < Tmax:

        u = scheme(u)
        t += dt

        u_exact = exact(x, t)
        err = np.abs(u - u_exact)

        L1_list.append(np.mean(err))
        L2_list.append(np.sqrt(np.mean(err**2)))
        time_list.append(t)

    # ======================
    # L1
    # ======================

    sigma_L1, onset_L1 = detect_sigma(time_list, L1_list)

    axes[0, col].plot(time_list, L1_list)
    axes[0, col].set_yscale("log")
    axes[0, col].set_title(name)
    axes[0, col].set_xlabel("Time")
    axes[0, col].set_ylabel("L1 Error")

    axes[0, col].axvline(onset_L1, linestyle="--")
    axes[0, col].text(
        0.5, 0.9,
        rf"$\sigma={sigma_L1:.3f}$",
        transform=axes[0, col].transAxes,
        ha="center"
    )

    # ======================
    # L2
    # ======================

    sigma_L2, onset_L2 = detect_sigma(time_list, L2_list)

    axes[1, col].plot(time_list, L2_list)
    axes[1, col].set_yscale("log")
    axes[1, col].set_title(name)
    axes[1, col].set_xlabel("Time")
    axes[1, col].set_ylabel("L2 Error")

    axes[1, col].axvline(onset_L2, linestyle="--")
    axes[1, col].text(
        0.5, 0.9,
        rf"$\sigma={sigma_L2:.3f}$",
        transform=axes[1, col].transAxes,
        ha="center"
    )

plt.tight_layout()
plt.show()