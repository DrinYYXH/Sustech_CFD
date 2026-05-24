import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 配置参数与学术画布
# =================================================================
BASE_DIR = "/home/u12310744/hw/project1/"
N_list = [20, 40, 80, 160, 320]
L = 2.0
schemes = {1: 'Lax-Wendroff', 2: 'van Leer', 3: 'SUPERBEE'}

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

# 存储结构：results[scheme][time][norm] = []
results = {sname: {t: {'dx': [], 'l1': [], 'l2': []} for t in [2.0, 8.0]} for sname in schemes.values()}

def calculate_errors_from_file(filepath):
    """从导出的 txt 文件中读取并计算 L1 和 L2 误差"""
    if not os.path.exists(filepath): return None, None
    try:
        data = np.loadtxt(filepath, skiprows=1)
        u_num = data[:, 1]
        u_ana = data[:, 2]
        l1 = np.mean(np.abs(u_num - u_ana))
        l2 = np.sqrt(np.mean((u_num - u_ana)**2))
        return l1, l2
    except:
        return None, None

# =================================================================
# 2. 【核心修复】先将最新的 Fortran 源码强行编译，消灭 Bug
# =================================================================
print("=" * 70)
print("🚀 正在强行编译最新的 Fortran 代码以消灭虚节点 Bug...")
fortran_file = os.path.join(BASE_DIR, "T1.f90")
executable = os.path.join(BASE_DIR, "cfd_solver")

compile_cmd = f"gfortran {fortran_file} -o {executable}"
comp_res = subprocess.run(compile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if comp_res.returncode != 0:
    print("❌ Fortran 编译失败！错误信息：")
    print(comp_res.stderr.decode('utf-8'))
    exit(1)
print("✨ 编译成功！新 cfd_solver 已整装待发。")
print("=" * 70)

# =================================================================
# 3. 自动化多网格扫网格数据收集
# =================================================================
print(">>> 启动全自动化多网格收敛性测试 (t=2.0 & t=8.0)...")
for stype, sname in schemes.items():
    for N in N_list:
        dx = L / N
        print(f"正在计算: {sname:<15} | N = {N:<4}")
        
        # 运行最新的流场解算器
        cmd = f"{executable} {N} {stype}"
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 文件名前缀映射
        prefix = {1:'lw', 2:'vanleer', 3:'superbee'}[stype]
        
        # 处理 t=2.0
        f2 = os.path.join(BASE_DIR, f"{prefix}_result_t2_N{N}.txt")
        l1_2, l2_2 = calculate_errors_from_file(f2)
        if l1_2 is not None and np.isfinite(l1_2):
            results[sname][2.0]['dx'].append(dx)
            results[sname][2.0]['l1'].append(l1_2)
            results[sname][2.0]['l2'].append(l2_2)

        # 处理 t=8.0
        f8 = os.path.join(BASE_DIR, f"{prefix}_result_t8_N{N}.txt")
        l1_8, l2_8 = calculate_errors_from_file(f8)
        if l1_8 is not None and np.isfinite(l1_8) and l1_8 < 100:  # 过滤发散的 LW
            results[sname][8.0]['dx'].append(dx)
            results[sname][8.0]['l1'].append(l1_8)
            results[sname][8.0]['l2'].append(l2_8)

# =================================================================
# 4. 绘图：2x2 学术级双对数收敛图
# =================================================================
fig, axes = plt.subplots(2, 2, figsize=(13, 10.5))
plt.subplots_adjust(hspace=0.28, wspace=0.25)

colors = {'Lax-Wendroff': 'red', 'van Leer': 'blue', 'SUPERBEE': 'green'}
markers = {'Lax-Wendroff': 'o', 'van Leer': 's', 'SUPERBEE': '^'}

time_list = [2.0, 8.0]
norm_list = ['l1', 'l2']
norm_titles = {'l1': '$L_1$ Error Norm', 'l2': '$L_2$ Error Norm'}

for r, t in enumerate(time_list):
    for c, norm in enumerate(norm_list):
        ax = axes[r, c]
        
        # 画各格式的误差收敛线
        for sname in schemes.values():
            dx_vals = results[sname][t]['dx']
            err_vals = results[sname][t][norm]
            if dx_vals:
                ax.loglog(dx_vals, err_vals, color=colors[sname], marker=markers[sname], 
                          label=sname, linewidth=1.5, markersize=6.5)
        
        # 叠加标准的渐近参考斜率线 (Slope 1.0 和 2.0)
        if results['van Leer'][t]['dx']:
            ref_dx = np.array(results['van Leer'][t]['dx'])
            y0 = results['van Leer'][t][norm][0]
            x0 = ref_dx[0]
            
            line1 = y0 * (ref_dx / x0)**1.0
            line2 = y0 * (ref_dx / x0)**2.0
            
            ax.loglog(ref_dx, line1, color='gray', linestyle='--', alpha=0.6, label='Slope 1.0 (Ref)')
            ax.loglog(ref_dx, line2, color='black', linestyle=':', alpha=0.6, label='Slope 2.0 (Ref)')

        ax.set_title(f"{norm_titles[norm]} Convergence at $t = {t}$", fontsize=12, fontweight='bold')
        ax.set_xlabel('Grid Spacing $\Delta x$', fontsize=10)
        ax.set_ylabel('Numerical Error', fontsize=10)
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(fontsize=9, edgecolor='black', loc='lower right')

output_img = os.path.join(BASE_DIR, 'full_convergence_report.png')
plt.savefig(output_img, dpi=300, bbox_inches='tight')
print("\n" + "=" * 70)
print(f">>> [完美成功] 2x2 全量高品相精度收敛报告已保存至:\n    {output_img}")
print("=" * 70)