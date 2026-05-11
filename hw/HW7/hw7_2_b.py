import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Problem 20(b)
# Fixed C = 0.1
# Study error vs Δx
# =====================================================

a = 1.0
L = 2.0
C = 0.1

# Grid sizes
N_list = [20, 40, 80, 160, 320]

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
# main loop over grid size
# =====================================================

dx_list = []

for N in N_list:

    print(f"Running N = {N}")

    dx = L / N
    dt = C * dx / a

    dx_list.append(dx)

    x = np.linspace(0, L, N, endpoint=False)

    u0 = (
        np.sin(np.pi*x)
        + 0.6*np.sin(3*np.pi*x)
    )

    Tmax = max(times_to_save)

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
            # =========================================

            if (
                target_index < len(times_to_save)
                and abs(t - times_to_save[target_index]) < dt/2
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

        ax.loglog(
            dx_list,
            results_L1[scheme_name][t_save],
            marker='o',
            label=f't={t_save}'
        )

    ax.set_title(f'{scheme_name} : L1 Error')

    ax.set_xlabel(r'$\Delta x$')

    ax.set_ylabel('L1 Error')

    ax.grid(True)

    ax.legend()

plt.tight_layout()

# =====================================================

fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

for i, scheme_name in enumerate(schemes.keys()):

    ax = axes2[i]

    for t_save in times_to_save:

        ax.loglog(
            dx_list,
            results_L2[scheme_name][t_save],
            marker='o',
            label=f't={t_save}'
        )

    ax.set_title(f'{scheme_name} : L2 Error')

    ax.set_xlabel(r'$\Delta x$')

    ax.set_ylabel('L2 Error')

    ax.grid(True)

    ax.legend()

plt.tight_layout()

plt.show()