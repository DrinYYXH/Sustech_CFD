import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('prob_N600.dat')
M = data[:,0]
P = data[:,1]

plt.plot(M, P, 'o-', markersize=2)
plt.xlabel('M')
plt.ylabel('Probability')
plt.title('N=600 Binomial Distribution')
plt.grid(True)
plt.show()