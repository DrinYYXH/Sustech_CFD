import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 基础配置与学术级画布规范
# =================================================================
BASE_DIR = "/home/u12310744/hw/project1/"
N_plot = 160  # 标准网格点数

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

schemes = {1: 'Lax-Wendroff', 2: 'van Leer', 3: 'SUPERBEE'}

# =================================================================
# 2. 全自动后台编译与运行 (保持与 Fortran 结果同步)
# =================================================================
print("=" * 70)
print(f"🚀 开始编译与运行流场解算器 (Grid N = {N_plot})")
print("=" * 70)

fortran_file = os.path.join(BASE_DIR, "T1.f90")
executable = os.path.join(BASE_DIR, "cfd_solver")

compile_cmd = f"gfortran {fortran_file} -o {executable}"
comp_res = subprocess.run(compile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if comp_res.returncode != 0:
    print("❌ 编译失败！错误信息：")
    print(comp_res.stderr.decode('utf-8'))
    exit(1)

for stype, sname in schemes.items():
    run_cmd = f"{executable} {N_plot} {stype}"
    subprocess.run(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print("\n🎉 流场数据计算就绪，开始进行高学术品相微调绘图...\n" + "-" * 70)

# =================================================================
# 3. 路径映射与独立解析解构建
# =================================================================
files_t2 = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, f'lw_result_t2_N{N_plot}.txt')],
    'van Leer':     [os.path.join(BASE_DIR, f'vanleer_result_t2_N{N_plot}.txt')],
    'SUPERBEE':     [os.path.join(BASE_DIR, f'superbee_result_t2_N{N_plot}.txt')]
}

files_t8 = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, f'lw_result_t8_N{N_plot}.txt')],
    'van Leer':     [os.path.join(BASE_DIR, f'vanleer_result_t8_N{N_plot}.txt')],
    'SUPERBEE':     [os.path.join(BASE_DIR, f'superbee_result_t8_N{N_plot}.txt')]
}

files_tv = {
    'Lax-Wendroff': [os.path.join(BASE_DIR, f'lw_tv_history_N{N_plot}.txt')],
    'van Leer':     [os.path.join(BASE_DIR, f'vanleer_tv_history_N{N_plot}.txt')],
    'SUPERBEE':     [os.path.join(BASE_DIR, f'superbee_tv_history_N{N_plot}.txt')]
}

styles = {
    'Lax-Wendroff': dict(color='blue', linestyle='--', marker='o', label='Lax-Wendroff'),
    'van Leer':     dict(color='green', linestyle='-', marker='s', label='van Leer'),
    'SUPERBEE':     dict(color='red', linestyle='-', marker='^', label='SUPERBEE')
}

x_dense = np.linspace(-1.0, 1.0, 2500)
u_analytical = np.where((x_dense > -0.5) & (x_dense < 0.5), 1.0, 0.0)

def helper_load(file_list):
    for f in file_list:
        if os.path.exists(f):
            return np.loadtxt(f, skiprows=1)
    return None

# =================================================================
# 4. 绘图一：t = 2.0 (微调缩小图例，杜绝遮挡)
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
ax.set_title(f'Profiles Comparison at Non-dimensional Time $t = 2.0$ ($N={N_plot}$)', fontsize=11, fontweight='bold')
ax.set_xlim([-1.0, 1.0])
ax.set_ylim([-0.3, 1.4])
ax.grid(True, linestyle=':', alpha=0.5)

ax.legend(loc='upper left', edgecolor='black', framealpha=0.9,
          prop={'size': 9.5}, labelspacing=0.3, handlelength=1.5, handletextpad=0.4)

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'solution_comparison_t2.png'), dpi=300)
print("💾 已优化保存: solution_comparison_t2.png")

# =================================================================
# 5. 绘图二：t = 8.0 (微调缩小图例)
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
ax.set_title(f'Profiles Comparison at Non-dimensional Time $t = 8.0$ ($N={N_plot}$)', fontsize=11, fontweight='bold')
ax.set_xlim([-1.0, 1.0])
ax.set_ylim([-0.3, 1.4])
ax.grid(True, linestyle=':', alpha=0.5)

ax.legend(loc='upper left', edgecolor='black', framealpha=0.9,
          prop={'size': 9.5}, labelspacing=0.3, handlelength=1.5, handletextpad=0.4)

plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'solution_comparison_t8.png'), dpi=300)
print("💾 已优化保存: solution_comparison_t8.png")

# =================================================================
# 6. 绘图三：TV Evolution (改变图例位置，微扩纵坐标，解决遮挡与重合)
# =================================================================
fig, ax = plt.subplots(figsize=(6.8, 5))

for scheme, paths in files_tv.items():
    data = helper_load(paths)
    if data is not None:
        if scheme == 'van Leer':
            ax.plot(data[:, 0], data[:, 1], color=styles[scheme]['color'], 
                    linestyle='-', linewidth=3.5, label=styles[scheme]['label'])
        elif scheme == 'SUPERBEE':
            ax.plot(data[:, 0], data[:, 1], color=styles[scheme]['color'], 
                    linestyle='-.', linewidth=1.8, label=styles[scheme]['label'])
        else:
            ax.plot(data[:, 0], data[:, 1], color=styles[scheme]['color'], 
                    linestyle=styles[scheme]['linestyle'], linewidth=1.8, label=styles[scheme]['label'])

ax.set_xlabel('Dimensionless Time $t$', fontsize=12)
ax.set_ylabel('Total Variation ($TV$)', fontsize=12)
ax.set_title('Evolution of Total Variation ($TV$)', fontsize=12, fontweight='bold')
ax.set_xlim([0.0, 8.0])

# 【关键改进】纵坐标稍微扩大至 [0.0, 6.0]，留出上方空间
ax.set_ylim([0.0, 6.0]) 
ax.grid(True, linestyle=':', alpha=0.5)

# 【关键改进】将位置移到左上方 'upper left'，利用初期的空白区域，完美避免遮挡尾部曲线
ax.legend(loc='upper left', edgecolor='black', prop={'size': 9.5}, labelspacing=0.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, 'tv_evolution_comparison.png'), dpi=300)
print("💾 已优化保存: tv_evolution_comparison.png")

print("\n" + "=" * 70)
print(">>> [完美微调] 更加精确、绝无遮挡的图表已全部重新生成完毕！")
print("=" * 70)