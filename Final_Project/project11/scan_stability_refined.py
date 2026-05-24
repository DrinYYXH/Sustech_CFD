import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 实验参数设计 (临界区细化扫描)
# =================================================================
N_test = 160
L = 2.0
schemes = {1: 'Lax-Wendroff', 2: 'van Leer', 3: 'SUPERBEE'}

# 细化 1.0 附近的采样点，精准捕捉发散形态
cfl_list = [0.5, 0.9, 1.0, 1.01, 1.02, 1.05]

print("=" * 70)
print(f"  开始数值稳定性临界区细化探测 (Grid N = {N_test})")
print("=" * 70)

def run_solver_with_cfl(cfl_val, scheme_type):
    """动态修改 Fortran 里的 CFL 数，编译并运行"""
    fortran_file = "T1.f90"
    if not os.path.exists(fortran_file):
        if os.path.exists("main.f90"): fortran_file = "main.f90"
    
    with open(fortran_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(fortran_file, 'w', encoding='utf-8') as f:
        for line in lines:
            if "double precision, parameter :: cfl =" in line:
                f.write(f"    double precision, parameter :: cfl = {cfl_val}d0  ! Python动态修改\n")
            else:
                f.write(line)
                
    subprocess.run(f"gfortran {fortran_file} -o cfd_solver", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(f"./cfd_solver {N_test} {scheme_type}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

data_history = {name: {} for name in schemes.values()}

for stype, sname in schemes.items():
    print(f"\n[正在扫描] 格式: {sname}")
    prefix = {1:'lw', 2:'vanleer', 3:'superbee'}[stype]
    
    for cfl in cfl_list:
        print(f"  -> 正在探测临界 CFL = {cfl:<4} ...", end='\r')
        run_solver_with_cfl(cfl, stype)
        
        history_file = f"{prefix}_tv_history_N{N_test}.txt"
        
        if os.path.exists(history_file):
            try:
                raw_data = np.loadtxt(history_file, skiprows=1)
                if raw_data.ndim == 1:
                    raw_data = np.atleast_2d(raw_data)
                    
                t_arr = raw_data[:, 0]
                l2_arr = raw_data[:, 2]
                
                # 过滤无效值
                valid_mask = np.isfinite(l2_arr) & (l2_arr < 1e12)
                
                if not np.all(valid_mask):
                    first_invalid = np.where(~valid_mask)[0][0]
                    t_plot = t_arr[:first_invalid+1]
                    l2_plot = l2_arr[:first_invalid+1]
                    if len(l2_plot) > 0:
                        l2_plot[-1] = 1e6  # 强行拉高终点以作发散视觉呈现
                else:
                    t_plot = t_arr
                    l2_plot = l2_arr
                    
                data_history[sname][cfl] = (t_plot, l2_plot)
            except Exception as e:
                print(f"  ⚠️ 读取 CFL={cfl} 历史失败: {e}")

# =================================================================
# 3. 绘制 1x3 细化品鉴图
# =================================================================
fig, axes = plt.subplots(1, 3, figsize=(19, 6), sharey=True)

# 为不同的 CFL 匹配专门的颜色和线型，凸显临界区
style_mapping = {
    0.5:  {'color': '#2ca02c', 'ls': '-',  'lw': 1.2},   # 安全区（绿）
    0.9:  {'color': '#1f77b4', 'ls': '-',  'lw': 1.2},   # 接近区（蓝）
    1.0:  {'color': '#ff7f0e', 'ls': '-',  'lw': 1.8},   # 理论边界（橙）
    1.01: {'color': '#d62728', 'ls': '--', 'lw': 1.8},  # 超出1%（浅红虚线）
    1.02: {'color': '#9467bd', 'ls': '--', 'lw': 2.0},  # 超出2%（紫虚线）
    1.05: {'color': '#8c564b', 'ls': ':',  'lw': 2.5}   # 暴恐区（棕点线）
}

for idx, sname in enumerate(schemes.values()):
    ax = axes[idx]
    
    for cfl in cfl_list:
        if cfl in data_history[sname]:
            t_plot, l2_plot = data_history[sname][cfl]
            if len(t_plot) > 0:
                ax.plot(t_plot, l2_plot, label=f"CFL = {cfl}", 
                        color=style_mapping[cfl]['color'], 
                        linestyle=style_mapping[cfl]['ls'], 
                        linewidth=style_mapping[cfl]['lw'])
                
    ax.set_title(f"{sname} Stability Analysis", fontsize=13, fontweight='bold')
    ax.set_xlabel("Physical Time $t$", fontsize=11)
    if idx == 0:
        ax.set_ylabel("$L_2$ Error Norm (Log Scale)", fontsize=11)
        
    ax.set_yscale('log')
    ax.set_ylim(1e-3, 1e6) 
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(loc='upper left', fontsize=9.5)

plt.tight_layout()
output_name = "numerical_stability_refined.png"
plt.savefig(output_name, dpi=300)

print("\n" + "=" * 70)
print(f"🎉 临界细化探测试验圆满结束！高清图已保存为: '{output_name}'")
print("=" * 70)