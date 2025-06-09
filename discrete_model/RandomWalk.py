# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from library.agents import Walker
from library.functions import zipCoords
import matplotlib.pyplot as plt
import matplotlib
import time

# plt.rcParams['axes.edgecolor'] = 'white'
# plt.rcParams['axes.facecolor'] = 'none'
# plt.rcParams['axes.labelcolor'] = 'white'
# plt.rcParams['xtick.color'] = 'white'
# plt.rcParams['ytick.color'] = 'white'
# Currently, the performance is O(n) (1M: 3.6s, 2M: 7.4s, 4M: 13.6s). Pretty good, but I would like performance like log(n), or just faster in O(n).
# Swapping to Numpy, the performance (1M: 7.9s, 2M: 13.7s)
# Actually properly vectorizing some stuff:
#                                    (1M: 1.2s, 2M: 2.3s, 4M: 4.6s) Optimization acquired!

start = time.time()
label_fontsize = 12
tick_fontsize = 12

walker = Walker(init_position=(-25, 44.5), verticalStepSize=0.02, horizontalStepSize=0.02)
plt.figure(figsize=(6,6), dpi=100)
plt.axis('equal')
locations = walker.positionJumpProcess(20000)
print(locations)
plotvals = zipCoords(locations)
# print(locations)

x_min, x_max = min(plotvals[0]), max(plotvals[0])
y_min, y_max = min(plotvals[1]), max(plotvals[1])
plt.tight_layout() 
plt.plot(-25, 44.5, color="k", marker='.')
plt.xlabel("Longitude ($\degree$E)", fontsize=label_fontsize)
plt.ylabel("Latitude ($\degree$N)", fontsize=label_fontsize)
plt.tick_params(labelsize=tick_fontsize)

plt.axis('equal')
plt.axis('square')
# plt.xlim(1.1*x_min, 1.1*x_max)
# plt.ylim(1.1*y_min, 1.1*y_max)
for i in range(len(plotvals[0])-1):
    plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=0.333)
plt.plot([-25], [44.5], color="k", marker='.')


end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.show()
plt.savefig('randomWalk.png')
