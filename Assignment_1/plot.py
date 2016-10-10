"""
Demo using fontdict to control style of text and labels.
"""
import numpy as np
import matplotlib.pyplot as plt


font = {
    'fontname': 'Arial',
    # 'fontname': 'Helvetica',
    # 'color':  'darkred',
    'weight': 'normal',
    'size': 20,
}

plt.figure(figsize=(10, 10))
x = np.linspace(-40.0, 40.0, 200)
y1 = 1 / (1 + np.exp(-4*x))
y2 = 1 / (1 + np.exp(-2*x))
y3 = 1 / (1 + np.exp(-x))
y4 = 1 / (1 + np.exp(-0.5*x))
y5 = 1 / (1 + np.exp(-0.25*x))

plt.plot(x, y1, label=r"$\frac{1}{1 + e^{-4x}}$", color="magenta", linewidth=1.5)
plt.plot(x, y2, label=r"$\frac{1}{1 + e^{-2x}}$", color="green", linewidth=2)
plt.plot(x, y3, label=r"$\frac{1}{1 + e^{-x}}$", color="red", linewidth=3)
plt.plot(x, y4, label=r"$\frac{1}{1 + e^{- \frac{1}{2} x}}$", color="purple", linewidth=2)
plt.plot(x, y5, label=r"$\frac{1}{1 + e^{- \frac{1}{4} x}}$", color="blue", linewidth=1.5)

plt.title(u'Sigmoid Function with Different \u03b1 Value', fontdict=font)
# plt.xlabel('time (s)', fontdict=font)
# plt.ylabel('voltage (mV)', fontdict=font)
plt.xlim(-25.0, 25.0)

# Tweak spacing to prevent clipping of ylabel
# plt.subplots_adjust(left=0.15)
plt.legend(loc=4, fontsize=18)
plt.show()
