import numpy as np
import matplotlib.pyplot as plt

N = 160
L = 2.0
dx = L / N
a = 1.0
C = 2.5
dt = C * dx / a

x = np.linspace(0, L, N, endpoint=False)

u = np.sin(np.pi * x) + 0.6 * np.sin(3 * np.pi * x)


def exact(x, t):
    return (np.sin(np.pi * (x - a*t))
          + 0.6 * np.sin(3*np.pi * (x - a*t)))


def step(u):
    return (u
        - 0.5*C*(np.roll(u,-1) - np.roll(u,1))
        + 0.5*C**2*(np.roll(u,-1) - 2*u + np.roll(u,1)))


def step_B(u):
    return (u
        - C*(u - np.roll(u,1))
        - 0.5*C*(1-C)*(u - 2*np.roll(u,1) + np.roll(u,2)))


def step_C(u):
    return (u
        - 0.5*C*(np.roll(u,-1) - np.roll(u,1)))


t = 0
L1_list = []
L2_list = []
time_list = []

Tmax = 4.0

while t < Tmax:
    u = step(u)
    t += dt

    u_exact = exact(x, t)

    err = np.abs(u - u_exact)

    L1 = np.mean(err)
    L2 = np.sqrt(np.mean(err**2))

    L1_list.append(L1)
    L2_list.append(L2)
    time_list.append(t)

plt.figure()
plt.plot(time_list, L1_list, label="L1")
plt.plot(time_list, L2_list, label="L2")
plt.yscale('log')
plt.xlabel("Time")
plt.ylabel("Errors")
plt.legend()
plt.title("Lax-Wendroff Error Evolution")
plt.show()