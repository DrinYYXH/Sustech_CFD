import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Problem 20(c)
# Fixed N = 160
# Study error vs C for 0 < C <= 1.0
# =====================================================

a = 1.0
L = 2.0
N = 160  # 固定网格数

# 生成一系列 C 的值 (0 < C <= 1.0)
# 这里取 20 个点均匀分布作为示例
C_list = np.linspace(0.05, 1.0, 20)

# Representative times
times_to_save = [0.1, 0.5, 1.0]

# =====================================================
# exact solution
# =====================================================

def exact(x, t):
    return (
        np.sin(np.pi * (x - a*t))
        + 0.6 * np.sin(3*np.pi * (x - a*t))
    )

# =====================================================
# schemes
# =====================================================

def step_upwind(u, C):
    return (
        u
        - C * (u - np.roll(u, 1))
    )

def step_Lax(u, C):
    return (
        u
        - 0.5*C*(np.roll(u,-1) - np.roll(u,1))
        + 0.5*C**2*(np.roll(u,-1) - 2*u + np.roll(u,1))
    )

def step_B(u, C):
    return (
        u
        - C*(u - np.roll(u,1))
        - 0.5*C*(1-C)
        * (u - 2*np.roll(u,1) + np.roll(u,2))
    )

schemes = {
    "Upwind": step_upwind,
    "Lax-Wendroff": step_Lax,
    "Scheme B": step_B
}

# =====================================================
# storage
# =====================================================

results_L1 = {}
results_L2 = {}

for scheme_name in schemes.keys():
    results_L1[scheme_name] = {}
    results_L2[scheme_name] = {}
    for t_save in times_to_save:
        results_L1[scheme_name][t_save] = []
        results_L2[scheme_name][t_save] = []

# =====================================================
# main loop over Courant number C
# =====================================================

# 对于固定的 N，空间步长和初始场是固定的
dx = L / N
x = np.linspace(0, L, N, endpoint=False)
u0 = (
    np.sin(np.pi*x)
    + 0.6*np.sin(3*np.pi*x)
)

Tmax = max(times_to_save)

for C in C_list:
    print(f"Running C = {C:.3f}")
    dt = C * dx / a  # 随着 C 的变化，时间步长 dt 也在改变

    # =================================================
    # loop over schemes
    # =================================================
    for scheme_name, scheme in schemes.items():
        u = u0.copy()
        t = 0.0
        target_index = 0

        while t < Tmax:
            u = scheme(u, C)
            t += dt

            # =========================================
            # save at representative times
            # 加 1e-10 是为了防止浮点数累加导致的微小误差错过目标时间
            # =========================================
            if (
                target_index < len(times_to_save)
                and abs(t - times_to_save[target_index]) <= dt/2 + 1e-10
            ):
                u_exact = exact(x, t)
                err = np.abs(u - u_exact)
                L1 = np.mean(err)
                L2 = np.sqrt(np.mean(err**2))
                
                t_save = times_to_save[target_index]
                results_L1[scheme_name][t_save].append(L1)
                results_L2[scheme_name][t_save].append(L2)
                
                target_index += 1

# =====================================================
# plotting
# =====================================================

fig1, axes1 = plt.subplots(1, 3, figsize=(18, 5))

for i, scheme_name in enumerate(schemes.keys()):
    ax = axes1[i]
    for t_save in times_to_save:
        # 这里改成了普通的 plot，因为 C 是线性变化的
        ax.plot(
            C_list,
            results_L1[scheme_name][t_save],
            marker='o',
            markersize=4,
            label=f't={t_save}'
        )
    ax.set_title(f'{scheme_name} : L1 Error vs C')
    ax.set_xlabel('Courant Number (C)')
    ax.set_ylabel('L1 Error')
    ax.grid(True)
    ax.legend()

plt.tight_layout()

# =====================================================

fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

for i, scheme_name in enumerate(schemes.keys()):
    ax = axes2[i]
    for t_save in times_to_save:
        ax.plot(
            C_list,
            results_L2[scheme_name][t_save],
            marker='o',
            markersize=4,
            label=f't={t_save}'
        )
    ax.set_title(f'{scheme_name} : L2 Error vs C')
    ax.set_xlabel('Courant Number (C)')
    ax.set_ylabel('L2 Error')
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.show()