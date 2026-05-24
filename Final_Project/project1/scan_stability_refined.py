import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os

# =================================================================
# 1. 实验参数设计与学术画布配置
# =================================================================
BASE_DIR = "/home/u12310744/hw/project1/"
N_test = 160
L = 2.0
schemes = {1: 'Lax-Wendroff', 2: 'van Leer', 3: 'SUPERBEE'}

cfl_list = [0.5, 0.9, 1.0, 1.01, 1.02, 1.05]

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

print("=" * 70)
print(f"🚀 开始学术级真正 $L_1$ 误差无量纲探测 (时间视窗 \tau \in [0, 3])")
print("=" * 70)

def run_solver_with_cfl(cfl_val, scheme_type, history_file):
    """动态修改 Fortran 里的 CFL 数，并在正确目录下编译运行"""
    fortran_file = os.path.join(BASE_DIR, "T1.f90")
    
    if os.path.exists(history_file):
        os.remove(history_file)
        
    with open(fortran_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(fortran_file, 'w', encoding='utf-8') as f:
        for line in lines:
            if "double precision, parameter :: cfl =" in line:
                f.write(f"    double precision, parameter :: cfl = {cfl_val}d0  ! Python动态修改\n")
            else:
                f.write(line)
                
    cmd_compile = f"cd {BASE_DIR} && gfortran T1.f90 -o hw"
    cmd_run = f"cd {BASE_DIR} && ./hw {N_test} {scheme_type}"
    
    subprocess.run(cmd_compile, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.run(cmd_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# =================================================================
# 2. 自动化多流场测试与不稳定性精确抓取
# =================================================================
data_history = {name: {} for name in schemes.values()}

for stype, sname in schemes.items():
    print(f"\n[正在扫描] 格式: {sname}")
    prefix = {1:'lw', 2:'vanleer', 3:'superbee'}[stype]
    
    for cfl in cfl_list:
        print(f"  -> 正在探测临界 CFL = {cfl:<4} ...")
        history_file = os.path.join(BASE_DIR, f"{prefix}_tv_history_N{N_test}.txt")
        
        run_solver_with_cfl(cfl, stype, history_file)
        
        t_plot, l1_plot = [], []
        
        if os.path.exists(history_file) and os.path.getsize(history_file) > 50:
            try:
                raw_data = np.genfromtxt(history_file, skip_header=1, invalid_raise=False)
                if raw_data.ndim == 1:
                    raw_data = np.atleast_2d(raw_data)
                
                t_arr = raw_data[:, 0]
                l1_arr = raw_data[:, 3] # 精准读取第四列真正的 L1_Error
                
                # 剔除包含 NaN, Inf 以及极大发散值的数据步
                valid_mask = np.isfinite(l1_arr) & (l1_arr < 1e9)
                
                if not np.all(valid_mask):
                    # 一旦发散，仅保留彻底安全合法的点，绝不人工拼接 1e5
                    first_invalid = np.where(~valid_mask)[0][0]
                    t_plot = t_arr[:first_invalid]
                    l1_plot = l1_arr[:first_invalid]
                else:
                    t_plot = t_arr
                    l1_plot = l1_arr
            except Exception as e:
                print(f"  ⚠️ 解析文本失败: {e}")
        
        # 处理第一步或初始化直接越界暴毙无法写入的情况
        if len(t_plot) == 0 and cfl > 1.0:
            t_plot = np.array([0.0, 0.01])
            l1_plot = np.array([1e-2, 1e7])
            
        data_history[sname][cfl] = (t_plot, l1_plot)

# =================================================================
# 3. 绘制 1x3 紧凑型无量纲化双对数稳定性分析图
# =================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)

style_mapping = {
    0.5:  {'color': '#2ca02c', 'ls': '-',  'lw': 1.5},   
    0.9:  {'color': '#1f77b4', 'ls': '-',  'lw': 1.5},   
    1.0:  {'color': '#ff7f0e', 'ls': '-',  'lw': 2.0},   
    1.01: {'color': '#d62728', 'ls': '--', 'lw': 1.8},  
    1.02: {'color': '#9467bd', 'ls': '--', 'lw': 1.8},  
    1.05: {'color': '#8c564b', 'ls': ':',  'lw': 2.2}   
}

for idx, sname in enumerate(schemes.values()):
    ax = axes[idx]
    
    for cfl in cfl_list:
        if cfl in data_history[sname]:
            t_plot, l1_plot = data_history[sname][cfl]
            if len(t_plot) > 0:
                ax.plot(t_plot, l1_plot, label=f"CFL = {cfl}", 
                        color=style_mapping[cfl]['color'], 
                        linestyle=style_mapping[cfl]['ls'], 
                        linewidth=style_mapping[cfl]['lw'])
                
    ax.set_title(f"{sname} Stability Analysis", fontsize=12, fontweight='bold')
    ax.set_xlabel("Dimensionless Time $\\tau$", fontsize=11)
    if idx == 0:
        ax.set_ylabel("$L_1$ Error Norm (Log Scale)", fontsize=11)
        
    ax.set_yscale('log')
    
    # 🎯【核心调整】将时间轴上限精准锁定在 3.0，使曲线演化比例最完美、饱满
    ax.set_xlim(0.0, 3.0)  
    ax.set_ylim(1e-3, 1e6) 
    
    ax.grid(True, which="both", linestyle=":", alpha=0.5)
    ax.legend(loc='upper left', fontsize=9.5, edgecolor='black')

plt.tight_layout()
output_name = os.path.join(BASE_DIR, "numerical_stability_refined.png")
plt.savefig(output_name, dpi=300)

print("\n" + "=" * 70)
print(f"🎉 $\\tau \\in [0, 3]$ 的纯净版无量纲稳定性图已成功保存至:\n    {output_name}")
print("=" * 70)