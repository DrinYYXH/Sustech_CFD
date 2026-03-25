import numpy as np
import matplotlib.pyplot as plt

# ======================
# 读取数据
# ======================
def load_file(filename):
    data = np.loadtxt(filename)
    y = data[:,1]
    t = data[:,2]
    err_pred = data[:,3]
    err_num  = data[:,4]
    return y, t, err_pred, err_num


# ======================
# 提取某一时刻
# ======================
def extract_time(y, t, e1, e2, target_t, tol=1e-2):
    mask = np.abs(t - target_t) < tol
    y_sel = y[mask]
    e1_sel = e1[mask]
    e2_sel = e2[mask]

    idx = np.argsort(y_sel)
    return y_sel[idx], e1_sel[idx], e2_sel[idx]


# ======================
# 绘图
# ======================
def plot_profile(target_t):

    files = {
        8:  "fort.8",
        16: "fort.16",
        32: "fort.32"
    }

    colors = {
        8:  "#1f77b4",
        16: "#2ca02c",
        32: "#d62728"
    }

    plt.figure(figsize=(7,5))

    for N, fname in files.items():
        y, t, e_pred, e_num = load_file(fname)

        y, e_pred, e_num = extract_time(y, t, e_pred, e_num, target_t)

        e_pred = np.maximum(e_pred, 1e-16)
        e_num  = np.maximum(e_num, 1e-16)

        color = colors[N]

        # ✅ numerical：实线（主曲线）
        plt.plot(y, e_num, '-', color=color, linewidth=2,
                 label=f'Numerical N={N}')

        # ✅ predicted：打点（不连线）
        plt.plot(y, e_pred, 'o', color=color,
                 markersize=4, fillstyle='none',
                 label=f'Predicted N={N}')

    plt.yscale('log')

    plt.xlabel('y')
    plt.ylabel('Normalized error')
    plt.title(f'Error profile at $t^* = {target_t}$')

    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.show()


# ======================
# 画图
# ======================
plot_profile(0.2)
plot_profile(10.0)