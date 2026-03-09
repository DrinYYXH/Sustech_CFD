import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取数据
# 第一列是 n (1-300), 第二列是概率 y, 第三列是 log(y)
df = pd.read_csv('fort.1', sep='\s+', header=None, 
                 names=['n', 'Prob', 'LogProb'], 
                 na_values=['-Infinity'])

# 将 -Infinity 替换为 NaN 以便绘图，或保留 valid 数据用于分析
valid_df = df.dropna(subset=['LogProb'])

# 2. 创建画布
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# 图 A: 概率分布演变 (Linear Scale)
# 展示从 n=245 开始的概率显著增长，直到均值 n=300
ax1.plot(df['n'], df['Prob'], color='blue', linewidth=2, label='Binomial P(n)')
ax1.fill_between(df['n'], df['Prob'], color='blue', alpha=0.2)
ax1.set_title('Probability Distribution $P(n)$ ($m=600, p=0.5$)', fontsize=14)
ax1.set_xlabel('State $n$', fontsize=12)
ax1.set_ylabel('Probability', fontsize=12)
ax1.grid(True, linestyle=':', alpha=0.7)

# 图 B: 对数概率的二次特性分析 (Quadratic Analysis)
# 在此处我们可以看到 ln(P) 随 n 的变化
ax2.scatter(valid_df['n'], valid_df['LogProb'], color='red', s=10, label='Data from Fortran')

# 执行二次多项式拟合，验证“二次分布”特性
z = np.polyfit(valid_df['n'], valid_df['LogProb'], 2)
p = np.poly1d(z)
n_fit = np.linspace(valid_df['n'].min(), valid_df['n'].max(), 100)
ax2.plot(n_fit, p(n_fit), 'k--', alpha=0.8, label=f'Quadratic Fit')

ax2.set_title('Log-Probability Quadratic Trend', fontsize=14)
ax2.set_xlabel('State $n$', fontsize=12)
ax2.set_ylabel('$\ln(P(n))$', fontsize=12)
ax2.legend()
ax2.grid(True, linestyle=':', alpha=0.7)

plt.tight_layout()
plt.show()

# 打印拟合参数以供 CFD 分析参考
print(f"拟合方程: ln(P) = {z[0]:.6f}*n^2 + {z[1]:.6f}*n + {z[2]:.6f}")