import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 配置参数
# =================================================================
N_list = [20, 40, 80, 160, 320]
L = 2.0
schemes = {1: 'Lax-Wendroff', 2: 'van Leer', 3: 'SUPERBEE'}

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
# 2. 自动化运行并收集数据
# =================================================================
print(">>> 启动全自动化测试 (t=2.0 & t=8.0)...")
for stype, sname in schemes.items():
    for N in N_list:
        dx = L / N
        print(f"正在计算: {sname:<15} | N = {N:<4}", end='\r')
        
        # 运行 Fortran
        cmd = f"./cfd_solver {N} {stype}"
        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 处理 t=2.0 (根据 Fortran 命名的文件读取)
        prefix = {1:'lw', 2:'vanleer', 3:'superbee'}[stype]
        f2 = f"{prefix}_result_t2_N{N}.txt"
        l1_2, l2_2 = calculate_errors_from_file(f2)
        if l1_2 is not None and np.isfinite(l1_2):
            results[sname][2.0]['dx'].append(dx)
            results[sname][2.0]['l1'].append(l1_2)
            results[sname][2.0]['l2'].append(l2_2)

        # 处理 t=8.0
        f8 = f"{prefix}_result_t8_N{N}.txt"
        l1_8, l2_8 = calculate_errors_from_file(f8)
        if l1_8 is not None and np.isfinite(l1_8) and l1_8 < 100: # 过滤掉 LW 发散的巨大误差
            results[sname][8.0]['dx'].append(dx)
            results[sname][8.0]['l1'].append(l1_8)
            results[sname][8.0]['l2'].append(l2_8)

# =================================================================
# 3. 绘图：2x2 学术级双对数图
# =================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 11))
plt.subplots_adjust(hspace=0.3, wspace=0.25)

colors = {'Lax-Wendroff': 'red', 'van Leer': 'blue', 'SUPERBEE': 'green'}
markers = {'Lax-Wendroff': 'o', 'van Leer': 's', 'SUPERBEE': '^'}

time_list = [2.0, 8.0]
norm_list = ['l1', 'l2']
norm_titles = {'l1': '$L_1$ Error Norm', 'l2': '$L_2$ Error Norm'}

for r, t in enumerate(time_list):
    for c, norm in enumerate(norm_list):
        ax = axes[r, c]
        
        # 画各格式的误差线
        for sname in schemes.values():
            dx_vals = results[sname][t]['dx']
            err_vals = results[sname][t][norm]
            if dx_vals:
                ax.loglog(dx_vals, err_vals, color=colors[sname], marker=markers[sname], 
                          label=sname, linewidth=1.5, markersize=7)
        
        # 叠加参考斜率线 (Slope 1.0 和 2.0)
        if results['van Leer'][t]['dx']:
            ref_dx = np.array(results['van Leer'][t]['dx'])
            # 以 van Leer 的最大误差作为起点平移参考线
            y0 = results['van Leer'][t][norm][0]
            x0 = ref_dx[0]
            
            line1 = y0 * (ref_dx / x0)**1.0
            line2 = y0 * (ref_dx / x0)**2.0
            
            ax.loglog(ref_dx, line1, color='gray', linestyle='--', alpha=0.7, label='Slope 1.0')
            ax.loglog(ref_dx, line2, color='black', linestyle=':', alpha=0.7, label='Slope 2.0')

        ax.set_title(f"{norm_titles[norm]} at $t = {t}$", fontsize=13, fontweight='bold')
        ax.set_xlabel('Grid Spacing $\Delta x$')
        ax.set_ylabel('Error Value')
        ax.grid(True, which="both", ls="--", alpha=0.5)
        ax.legend(fontsize=9)

plt.savefig('full_convergence_report.png', dpi=300)
print("\n>>> [成功] 2x2 全量精度报告图片已保存为 'full_convergence_report.png'")