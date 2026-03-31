import numpy as np
import matplotlib.pyplot as plt

# ======================
# 读取 Fortran 输出数据
# ======================
data = np.loadtxt('fort.1')   # 改成你的文件名

t = data[:, 0]          # 时间
u_num = data[:, 1]      # 数值解
u_theory = data[:, 2]   # 差分理论解

# ======================
# 绘图
# ======================
plt.figure()

plt.plot(t, u_num, 'o-', label='Numerical solution')
plt.plot(t, u_theory, '-', label='Theory solution')

plt.xlabel('Time')
plt.ylabel('u(y=0.5L)')
plt.title('Problem 12(a): Numerical vs Theory')
plt.legend()
plt.grid()

plt.show()