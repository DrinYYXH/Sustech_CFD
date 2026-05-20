import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 基础配置与学术级画布规范
# =================================================================
BASE_DIR = "/home/u12310744/hw/project1/"

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# 独立构建连续的高分辨率真实解析解（方波）
x_dense = np.linspace(-1.0, 1.0, 2500)
u_analytical = np.where((x_dense > -0.5) & (x_dense < 0.5), 1.0, 0.0)

# 文件路径自动拼接（同时兼容你目录下的全小写命名规范）
files_t2 = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, 'lw_result_t2.txt')],
    'van Leer': [os.path.join(BASE_DIR, 'vanleer_result_t2.txt')],
    'SUPERBEE': [os.path.join(BASE_DIR, 'superbee_result_t2.txt')]
}

files_t8 = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, 'lw_result_t8.txt')],
    'van Leer': [os.path.join(BASE_DIR, 'vanleer_result_t8.txt')],
    'SUPERBEE': [os.path.join(BASE_DIR, 'superbee_result_t8.txt')]
}

files_tv = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, 'lw_tv_history.txt')],
    'van Leer': [os.path.join(BASE_DIR, 'vanleer_tv_history.txt')],
    'SUPERBEE': [os.path.join(BASE_DIR, 'superbee_tv_history.txt')]
}

# 统一样式字典：通过 markevery=5 降低点密度，让连续曲线与散点交相辉映
styles = {
    'Lax-Wendroff': dict(color='blue', linestyle='--', marker='o', label='Lax-Wendroff'),
    'van Leer': dict(color='green', linestyle='-', marker='s', label='van Leer'),
    'SUPERBEE': dict(color='red', linestyle='-', marker='^', label='SUPERBEE')
}

def helper_load(file_list):
    """安全读取函数"""
    for f in file_list:
        if os.path.exists(f):
            print(f"Successfully loaded: {os.path.basename(f)}")
            return np.loadtxt(f, skiprows=1)
    return None

# =================================================================
# 2. 绘图一：t = 2.0 (流场剖面图，完美解决图例遮挡)
# =================================================================
fig, ax = plt.subplots(figsize=(6.8, 5))
ax.plot(x_dense, u_analytical, 'k-', linewidth=2.0, label='Analytical')

for scheme, paths in files_t2.items():
    data = helper_load(paths)
    if data is not None:
        ax.plot(data[:, 0], data[:, 1], linestyle=styles[scheme]['linestyle'], 
                marker=styles[scheme]['marker'], markevery=5, markersize=4.5,
                color=styles[scheme]['color'], label=styles[scheme]['label'])

ax.set_xlabel('Dimensionless Coordinate $x$', fontsize=12)
ax.set_ylabel('Dimensionless Variable $u$', fontsize=12)
ax.set_title('Profiles Comparison at Non-dimensional Time $t = 2.0$', fontsize=11, fontweight='bold')
ax.set_xlim([-1.0, 1.0])
ax.set_ylim([-0.3, 1.4])  # 留足空间显示 LW 格式跌落到负数的振荡
ax.grid(True, linestyle=':', alpha=0.5)

# 图例优雅地挂在左上角 (upper left)，彻底移开右侧波头，防遮挡
ax.legend(loc='upper left', edgecolor='black', framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'solution_comparison_t2.png'), dpi=300)
plt.show()

# =================================================================
# 3. 绘图二：t = 8.0 (流场剖面图)
# =================================================================
fig, ax = plt.subplots(figsize=(6.8, 5))
ax.plot(x_dense, u_analytical, 'k-', linewidth=2.0, label='Analytical')

for scheme, paths in files_t8.items():
    data = helper_load(paths)
    if data is not None:
        ax.plot(data[:, 0], data[:, 1], linestyle=styles[scheme]['linestyle'], 
                marker=styles[scheme]['marker'], markevery=5, markersize=4.5,
                color=styles[scheme]['color'], label=styles[scheme]['label'])

ax.set_xlabel('Dimensionless Coordinate $x$', fontsize=12)
ax.set_ylabel('Dimensionless Variable $u$', fontsize=12)
ax.set_title('Profiles Comparison at Non-dimensional Time $t = 8.0$', fontsize=11, fontweight='bold')
ax.set_xlim([-1.0, 1.0])
ax.set_ylim([-0.3, 1.4])
ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='upper left', edgecolor='black', framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'solution_comparison_t8.png'), dpi=300)
plt.show()

# =================================================================
# 4. 绘图三：TV Evolution (全变差演化图，拓宽坐标轴记录发散)
# =================================================================
fig, ax = plt.subplots(figsize=(6.8, 5))

for scheme, paths in files_tv.items():
    data = helper_load(paths)
    if data is not None:
        ax.plot(data[:, 0], data[:, 1], color=styles[scheme]['color'], 
                linestyle=styles[scheme]['linestyle'], linewidth=1.8, label=styles[scheme]['label'])

ax.set_xlabel('Dimensionless Time $t$', fontsize=12)
ax.set_ylabel('Total Variation ($TV$)', fontsize=12)
ax.set_title('Evolution of Total Variation ($TV$)', fontsize=12, fontweight='bold')
ax.set_xlim([0.0, 8.0])

# 【关键改动】纵坐标范围从原先的 3.5 扩展到 12.0。
# 限制器将稳定躺在 2.0 地平线，而你可以亲眼目睹非 TVD 格式（LW）的数据垂直飙升向上的发散全貌！
ax.set_ylim([0.0, 12.0]) 
ax.grid(True, linestyle=':', alpha=0.5)
ax.legend(loc='upper right', edgecolor='black')
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'tv_evolution_comparison.png'), dpi=300)
plt.show()

print(">>> [成功] 无量纲高品相学术图表已全部重新生成完毕！")