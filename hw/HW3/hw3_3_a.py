import numpy as np
import matplotlib.pyplot as plt

# ======================
# 全局风格设置（关键）
# ======================
plt.rcParams.update({
    "font.size": 12,
    "font.family": "serif",
    "mathtext.fontset": "stix",
    "axes.linewidth": 1.0,
    "lines.linewidth": 2.0,
})

# ======================
# 读取数据
# ======================
data = np.loadtxt('fort.2')

t = data[:, 2]
err_pred = data[:, 3]
err_num  = data[:, 4]

# 排序（非常重要）
idx = np.argsort(t)
t = t[idx]
err_pred = err_pred[idx]
err_num  = err_num[idx]

# 防止 log 问题
err_pred = np.maximum(err_pred, 1e-16)
err_num  = np.maximum(err_num, 1e-16)

# ======================
# 开始绘图
# ======================
fig, ax = plt.subplots(figsize=(7,5))

# 专业配色（类似论文风格）
color1 = "#1f77b4"   # 深蓝
color2 = "#d62728"   # 深红

# --- 主曲线（无marker，干净）---
line1, = ax.plot(t, err_pred, '-', color=color1, label=r'Predicted $|u_m - u|/u_0$')
line2, = ax.plot(t, err_num,  '--', color=color2, label=r'Numerical $|u_N - u|/u_0$')

# --- 稀疏 marker（点缀，不干扰）---
step = max(len(t)//25, 1)

ax.plot(t[::step], err_pred[::step], 'o',
        color=color1, markersize=4)

ax.plot(t[::step], err_num[::step], 's',
        color=color2, markersize=4)

# ======================
# 坐标 & 标注
# ======================
ax.set_yscale('log')

ax.set_xlabel(r'Dimensionless time $t^* = \nu t / a_L^2$')
ax.set_ylabel('Normalized error')

ax.set_title('Error comparison at channel center ($y=0$)')

# 网格（细而不抢）
ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)

# 图例（干净）
ax.legend(frameon=False)

# 边框优化
for spine in ax.spines.values():
    spine.set_linewidth(1.0)

plt.tight_layout()
plt.show()