import numpy as np
import matplotlib.pyplot as plt

# 定义计算放大因子模长的函数
def calc_G_mag(C, theta):
    G_R = 0.5 * C * (C - 1) * np.cos(2*theta) + C * (2 - C) * np.cos(theta) + 0.5 * (C - 1) * (C - 2)
    # 修正了 np.np.sin 的笔误
    G_I = -0.5 * C * (C - 1) * np.sin(2*theta) - C * (2 - C) * np.sin(theta)
    return np.sqrt(G_R**2 + G_I**2)

# 创建网格数据
C_vals = np.linspace(0, 3.0, 300)
theta_vals = np.linspace(-np.pi, np.pi, 300)
C_grid, theta_grid = np.meshgrid(C_vals, theta_vals)

# 计算 |G|
G_mag_grid = calc_G_mag(C_grid, theta_grid)

# 绘制 Contour Plot
plt.figure(figsize=(10, 6))
# 画等值线图
cp = plt.contourf(theta_grid, C_grid, G_mag_grid, levels=np.linspace(0, 2, 21), cmap='viridis', extend='max')
plt.colorbar(cp, label=r'Amplification Factor $|G|$')

# 添加 |G| = 1 的加粗红线作为稳定性边界
plt.contour(theta_grid, C_grid, G_mag_grid, levels=[1.0], colors='red', linewidths=2)

# 设置标题和标签（字符串前加 r 消除 SyntaxWarning）
plt.title(r'Von Neumann Stability Analysis: $|G|$ Contour Plot')
plt.xlabel(r'Phase Angle $k\Delta x$ ($\theta$)')
plt.ylabel(r'CFL Number ($C$)')

# 标记稳定区域（字符串前加 r 消除 SyntaxWarning）
plt.text(0, 1.0, r'Stable Area ($|G| \leq 1$)', color='white', ha='center', va='center', fontsize=12, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.5)
plt.show()