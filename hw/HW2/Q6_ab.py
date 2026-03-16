import matplotlib.pyplot as plt
import numpy as np

# --- 基础配置：ntime 已除以 5 ---
file_configs = [
    {'name': 'fort.8',  'N': 8,  'dt': 0.2,    'ntime': 2},   # 原 10 -> 2
    {'name': 'fort.16', 'N': 16, 'dt': 0.05,   'ntime': 8},   # 原 40 -> 8
    {'name': 'fort.32', 'N': 32, 'dt': 0.0125, 'ntime': 32}   # 原 160 -> 32
]
nu = 0.1
L = 1.0

# 修正后的目标 Label (由于采样频率提高5倍，序号也乘以5)
# 对应 t* = 0.2, 1.0, 5.0 
target_labels = [5.0, 25.0, 125.0] 
t_star_names = ['0.2', '1.0', '5.0']
colors = ['red', 'green', 'blue']

def process_homework_results():
    for cfg in file_configs:
        fname, N = cfg['name'], cfg['N']
        dt, ntime = cfg['dt'], cfg['ntime']
        
        # 物理时间计算因子: t* = (Label * ntime * dt) * nu / L^2 [cite: 11, 15]
        t_star_factor = (ntime * dt) * nu / (L**2)
        
        try:
            # 数据列: [Label, ycc, theory1, u/u0, error] [cite: 43]
            data = np.loadtxt(fname)
        except:
            print(f"无法读取文件: {fname}")
            continue

        # --- 自动寻找“第一次达到速度要求”的时刻 (0.97 u0) ---
        # 寻找中心点 y=0 对应的数据行 
        center_mask = np.isclose(data[:, 1], 0.0)
        center_data = data[center_mask]
        
        steady_label = None
        steady_t_star = 0.0
        # 遍历中心点速度，寻找第一个 u/u0 >= 0.97 的时刻 
        for row in center_data:
            if row[3] >= 0.97:
                steady_label = row[0]
                steady_t_star = steady_label * t_star_factor
                break

        print(f"N={N}: 捕捉到稳态时刻 t* ≈ {steady_t_star:.4f} (Label {steady_label})")

        # --- 6(a) 速度剖面图：增加稳态曲线 ---
        plt.figure(figsize=(7, 6))
        for i, label in enumerate(target_labels):
            block = data[data[:, 0] == label]
            if len(block) > 0:
                # 绘制数值解 (散点虚线) 
                plt.plot(block[:, 3], block[:, 1], 'o--', color=colors[i], 
                         markersize=4, label=f'Numerical $t^*={t_star_names[i]}$')
                # 绘制解析解 (浅色实线) 
                plt.plot(block[:, 2], block[:, 1], '-', color=colors[i], alpha=0.2)

        # 重点展示：绘制捕捉到的稳态时刻 (黑实线加粗)
        if steady_label is not None:
            steady_block = data[data[:, 0] == steady_label]
            plt.plot(steady_block[:, 3], steady_block[:, 1], 'k-', linewidth=2.5, 
                     label=f'STEADY REACHED ($t^* \\approx {steady_t_star:.2f}$)')

        plt.xlabel('$u/u_0$')
        plt.ylabel('$y/L$')
        plt.title(f'6(a) Velocity Profiles with Steady Capture (N={N})')
        plt.legend(fontsize='small', loc='lower right')
        plt.grid(True, linestyle=':')
        plt.savefig(f'6a_velocity_N{N}.png', dpi=300)
        plt.close()

        # --- 6(b) 误差图：增加稳态误差 ---
        plt.figure(figsize=(7, 6))
        for i, label in enumerate(target_labels):
            block = data[data[:, 0] == label]
            if len(block) > 0:
                # 归一化误差定义: |u_num - u_ana| / u0 [cite: 21]
                norm_error = np.abs(block[:, 3] - block[:, 2]) 
                plt.plot(block[:, 1], norm_error, 's-', color=colors[i],
                         label=f'Error at $t^*={t_star_names[i]}$')

        # 同时展示稳态时刻的误差表现
        if steady_label is not None:
            steady_block = data[data[:, 0] == steady_label]
            steady_err = np.abs(steady_block[:, 3] - steady_block[:, 2])
            plt.plot(steady_block[:, 1], steady_err, 'k--', linewidth=1.5, 
                     label=f'Error at Steady Time')

        plt.xlabel('$y/L$')
        plt.ylabel('Normalized Error $|u_{num} - u_{ana}|/u_0$')
        plt.yscale('log') # 使用对数坐标观察误差量级
        plt.title(f'6(b) Error Distribution (N={N})')
        plt.legend(fontsize='small')
        plt.grid(True, which='both', linestyle=':')
        plt.savefig(f'6b_error_N{N}.png', dpi=300)
        plt.close()

if __name__ == "__main__":
    process_homework_results()