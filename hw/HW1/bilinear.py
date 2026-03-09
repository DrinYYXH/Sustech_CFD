import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. 读取 fort.1 数据 (处理空格分隔和 -Infinity)
df = pd.read_csv('fort.1', sep='\s+', header=None, 
                 names=['n', 'P', 'logP'], na_values=['-Infinity'])

# 2. 创建一个包含两个子图的画布
plt.figure(figsize=(10, 4))

# 左图：展示概率随 n 的演变 (线性坐标)
plt.subplot(1, 2, 1)
plt.plot(df['n'], df['P'], 'b-', label='P(n)')
plt.title('Probability Distribution $P(n)$')
plt.xlabel('n')
plt.ylabel('P')

# 右图：展示对数概率 (体现二次/抛物线性质)
plt.subplot(1, 2, 2)
valid = df.dropna()  # 过滤掉之前的 -Infinity 数据点
plt.plot(valid['n'], valid['logP'], 'r.', label='ln P(n)')
plt.title('Log-Probability (Quadratic)')
plt.xlabel('n')
plt.ylabel('ln(P)')

plt.tight_layout()
plt.show()