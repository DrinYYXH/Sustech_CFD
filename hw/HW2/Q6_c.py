import matplotlib.pyplot as plt
import numpy as np

# --- 基础配置 ---
file_configs = [
    {'name': 'fort.8',  'N': 8,  'dt': 0.2,    'ntime': 2},
    {'name': 'fort.16', 'N': 16, 'dt': 0.05,   'ntime': 8},
    {'name': 'fort.32', 'N': 32, 'dt': 0.0125, 'ntime': 32}
]
nu = 0.1
aL = 1.0

def plot_6c_standard():
    plt.figure(figsize=(10, 6))
    
    ana_t_stars = None
    ana_stresses = None

    for cfg in file_configs:
        fname, N = cfg['name'], cfg['N']
        dt, ntime = cfg['dt'], cfg['ntime']
        dy = 2.0 * aL / N
        t_star_factor = (ntime * dt) * nu / (aL**2)
        
        try:
            data = np.loadtxt(fname)
        except:
            continue

        labels = np.unique(data[:, 0])
        t_stars = []
        stresses_num = []
        stresses_ana = []

        for lab in labels:
            block = data[data[:, 0] == lab]
            if len(block) < 2: continue
            
            t_curr = lab * t_star_factor
            t_stars.append(t_curr)
            
            # 数值解壁面剪切应力
            u2_num = block[1, 3] 
            stresses_num.append(nu * (u2_num / dy))
            
            # 提取解析解数据（受限于离散误差）
            u2_ana = block[1, 2] 
            stresses_ana.append(nu * (u2_ana / dy))

        plt.plot(t_stars, stresses_num, '--', label=f'Numerical N={N}')
        
        # 始终用最高精度的解析数据作为参考
        if N == 32:
            ana_t_stars = t_stars
            ana_stresses = stresses_ana

    # 1. 绘制解析解参考线 (由级数算出，带有 N=32 的离散误差)
    if ana_stresses is not None:
        plt.plot(ana_t_stars, ana_stresses, 'k-', linewidth=1.5, label='Analytical Series (N=32)', zorder=2)

    # 2. 绘制标准的物理稳态线 (2 * nu = 0.2)
    # 这条线是绝对真理，不随网格改变
    plt.axhline(y=0.2, color='gray', linestyle=':', linewidth=2, label='Steady-State Limit (0.2)', zorder=1)

    plt.xlabel('Dimensionless Time $t^* = \\nu t / L^2$')
    plt.ylabel('Normalized Wall Stress $\\tau_w / (u_0/L)$')
    plt.title('6(c) Comparison of Wall Viscous Stress Evolution')
    
    # 限制 y 轴范围，让对比更清晰
    plt.ylim(0, 0.25)
    
    plt.legend(loc='lower right', fontsize='small')
    plt.grid(True, linestyle=':')
    plt.savefig('6c_wall_stress_final.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    plot_6c_standard()