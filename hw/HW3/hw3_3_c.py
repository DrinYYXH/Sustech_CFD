import numpy as np
import matplotlib.pyplot as plt

# ======================
# 读取 Fortran 输出文件
# ======================
def load_file(filename):
    data = np.loadtxt(filename)
    t = data[:,2]  # 无量纲时间 t* = nu*t/L^2
    u = data[:,3]  # 中心速度 u(y=0)
    idx = np.argsort(t)
    return t[idx], u[idx]

# ======================
# 分别绘制每个 alpha
# ======================
def plot_each_alpha():
    files = {
        0.50:  "fort.1",
        0.505: "fort.11",
        0.51:  "fort.111",
        0.52:  "fort.1111"
    }

    colors = {
        0.50: "#1f77b4",
        0.505: "#2ca02c",
        0.51: "#d62728",
        0.52: "#9467bd"
    }

    for alpha, fname in files.items():
        t, u = load_file(fname)
        mask = t <= 8.0
        t_sel = t[mask]
        u_sel = u[mask]

        plt.figure(figsize=(6,4))
        plt.plot(t_sel, u_sel, '-', color=colors[alpha], linewidth=2, label=fr'$\alpha={alpha}$')
        plt.axhline(1.0, linestyle='--', color='black', linewidth=1.2, label='Steady solution')

        plt.xlabel(r'Dimensionless time $t^* = \nu t / L^2$', fontsize=12)
        plt.ylabel(r'Centerline velocity $u(0,t)$', fontsize=12)
        plt.title(fr'Stability test at y = 0 (α = {alpha})', fontsize=14)
        plt.xlim([0,2])
        plt.ylim([0,1.2])
        plt.grid(True, linestyle='--', linewidth=0.5)
        plt.legend(fontsize=10)
        plt.tight_layout()
        plt.show()

# ======================
# 执行
# ======================
plot_each_alpha()