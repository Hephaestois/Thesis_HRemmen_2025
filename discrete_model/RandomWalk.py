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

plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
# Currently, the performance is O(n) (1M: 3.6s, 2M: 7.4s, 4M: 13.6s). Pretty good, but I would like performance like log(n), or just faster in O(n).
# Swapping to Numpy, the performance (1M: 7.9s, 2M: 13.7s)
# Actually properly vectorizing some stuff:
#                                    (1M: 1.2s, 2M: 2.3s, 4M: 4.6s) Optimization acquired!

start = time.time()

walker = Walker(orientationFunction=lambda x: x*2*3.1415)
plt.figure(figsize=(4,4),dpi=600)
locations = walker.positionJumpProcess(20000)
plotvals = zipCoords(locations)
# print(locations)

x_min, x_max = min(plotvals[0]), max(plotvals[0])
y_min, y_max = min(plotvals[1]), max(plotvals[1])

max_range = max(x_max, -x_min, y_max, -y_min)

plt.xlim(-max_range*1.1,+max_range*1.1)
plt.ylim(-max_range*1.1,+max_range*1.1)
for i in range(len(plotvals[0])-1):
    plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=0.5)
plt.plot([0], [0], color="k", marker='.')


end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')
