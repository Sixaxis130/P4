import numpy as np
import matplotlib.pyplot as plt

p = 1

if p == 0:
    param = 'lp'
    color = 'green'
elif p == 1:
    param = 'lpcc'
    color = 'red'
else:
    param = 'mfcc'
    color = 'blue'

coefs = np.loadtxt(param + '_2_3.txt')

coef_2 = coefs[:, 0]
coef_3 = coefs[:, 1]

plt.title(param.upper())
plt.xlabel("2nd Coefficient")
plt.ylabel("3rd Coefficient")
plt.scatter(coef_2, coef_3, s=1, c=color)
plt.show()