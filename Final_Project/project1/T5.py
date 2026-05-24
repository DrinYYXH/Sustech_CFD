import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 实验参数与大作业规范学术画布配置
# =================================================================
BASE_DIR = "/home/u12310744/hw/project1/"
N = 160
L = 2.0
Target_Time = 1.0  # 与 Fortran 内部的 max_t 严格对齐

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

print("=" * 70)
print(f"🚀 开始执行第五问：改进型 Lax-Wendroff 空间波形对比验证")
print("=" * 70)

# =================================================================
# 2. 准确构造该特定时间下的解析解 (基于周期性方波平移)
# =================================================================
x_exact = np.linspace(0, L, 1000, endpoint=False) # 细腻的解析解线
u_exact = np.zeros_like(x_exact)
for i, xi in enumerate(x_exact):
    # 考虑对流速度为 1.0 的周期性位移
    pos = (xi - 1.0 * Target_Time) % L  
    if 0.5 <= pos <= 1.0:
        u_exact[i] = 1.0
    else:
        u_exact[i] = 0.0

# =================================================================
# 3. 自动化调度 Fortran 获取两组数值快照
# =================================================================
def run_and_load(scheme_type):
    """编译、运行 Fortran 并回载数据"""
    cmd_compile = f"cd {BASE_DIR} && gfortran T5.f90 -o hw"
    cmd_run = f"cd {BASE_DIR} && ./hw {N} {scheme_type}"
    
    # 编译并运行
    subprocess.run(cmd_compile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(cmd_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    file_name = "lw_snapshot.txt" if scheme_type == 1 else "clw_snapshot.txt"
    data_path = os.path.join(BASE_DIR, file_name)
    
    if os.path.exists(data_path):
        raw = np.loadtxt(data_path)
        return raw[:, 0], raw[:, 1]
    else:
        raise FileNotFoundError(f"未能正常读取 Fortran 导出的数据文件: {file_name}")

print(" -> 正在运行原始 Lax-Wendroff 格式...")
x_lw, u_lw = run_and_load(1)

print(" -> 正在运行改进型 (Artificial Viscosity) Lax-Wendroff 格式...")
x_clw, u_clw = run_and_load(4)

# =================================================================
# 4. 绘制用于报告提交的高分辨率对比图像
# =================================================================
plt.figure(figsize=(8.5, 5.8), dpi=300)

# 1. 绘制完美解析解（黑色实线）
plt.plot(x_exact, u_exact, label="Exact Solution", color="black", linestyle="-", linewidth=1.5)

# 2. 绘制标准 LW 结果（红色虚线，突出 Gibbs 现象毛刺）
plt.plot(x_lw, u_lw, label="Standard Lax-Wendroff", color="#d62728", linestyle="--", linewidth=1.5)

# 3. 绘制改进版 LW 结果（绿色实线，展示完美平滑台阶）
plt.plot(x_clw, u_clw, label="Improved LW (Artificial Viscosity)", color="#2ca02c", linestyle="-", linewidth=2.0)

# 学术润色
plt.title(f"Solution Comparison at $\\tau = {Target_Time}$ (Grid N = {N})", fontsize=12, fontweight='bold')
plt.xlabel("Spatial Coordinate $x$", fontsize=11)
plt.ylabel("Field Variable $u$", fontsize=11)

plt.xlim(0.0, L)
plt.ylim(-0.2, 1.3) # 预留空间以便清晰展示标准 LW 的上下冲振荡

plt.grid(True, linestyle=":", alpha=0.5)
plt.legend(loc="upper right", fontsize=10.5, edgecolor="black", framealpha=1.0)

plt.tight_layout()
output_image = os.path.join(BASE_DIR, "improved_lw_snapshot_comparison.png")
plt.savefig(output_image, dpi=300)

print("=" * 70)
print(f"🎉 验证图像已完美生成！请查看大作业配图：\n    {output_image}")
print("=" * 70)