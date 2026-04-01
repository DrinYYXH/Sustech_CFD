import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. 读文件
# =========================
data = np.loadtxt("output13.dat")

# =========================
# 2. 拆列（按你的 Fortran 顺序）
# =========================
t_col = data[:, 0]
x_col = data[:, 1]
u_up = data[:, 2]
u_down = data[:, 3]
u_cen = data[:, 4]
u_exact = data[:, 5]

# =========================
# 3. 选定某个时间（比如 t = 1.5）
# =========================
t_target = 0.5
mask = np.isclose(t_col, t_target)

x = x_col[mask]
up = u_up[mask]
down = u_down[mask]
cen = u_cen[mask]
exact = u_exact[mask]

# =========================
# 4. 排序（防止 x 乱序）
# =========================
idx = np.argsort(x)
x = x[idx]
up = up[idx]
down = down[idx]
cen = cen[idx]
exact = exact[idx]

# =========================
# 5. 画图
# =========================
plt.figure(figsize=(10,6))

plt.plot(x, exact, 'k-', linewidth=2, label='Exact')
plt.plot(x, up, 'b-o', markersize=3, label='Upwind')
plt.plot(x, cen, 'r--', label='Central')
plt.plot(x, down, 'g-.', label='Downwind')

# 防止爆炸值影响显示
plt.ylim(-3, 3)

plt.title(f"t = {t_target}")
plt.xlabel("x")
plt.ylabel("u")
plt.grid(True)
plt.legend()

plt.show()