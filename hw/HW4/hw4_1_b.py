import numpy as np
import matplotlib.pyplot as plt

# ======================
# 读取数据
# ======================
data = np.loadtxt('fort.2')

t = data[:, 0]
err_num = data[:, 1]
err_trunc = data[:, 2]
err_mod = data[:, 3]

# ======================
# 绘图
# ======================
plt.figure()

plt.plot(t, err_num, 'o-', label='Numerical error')
plt.plot(t, err_trunc, '-', label='Truncation error')
plt.plot(t, err_mod, '--', label='Modified eq error')

plt.xlabel('Time')
plt.ylabel('Normalized error')
plt.title('Problem 12(b): Error comparison at y=0.5L')
plt.legend()
plt.grid()

plt.show()