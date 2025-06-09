# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Other imports
from library.agents import Walker
from library.functions import zipCoords
import matplotlib.pyplot as plt
import time

# Currently, the performance is O(n) (1M: 3.6s, 2M: 7.4s, 4M: 13.6s). Pretty good, but I would like performance like log(n), or just faster in O(n).
# Swapping to Numpy, the performance (1M: 7.9s, 2M: 13.7s)
# Actually properly vectorizing some stuff:
#                                    (1M: 1.2s, 2M: 2.3s, 4M: 4.6s) Optimization acquired!
label_fontsize = 12
tick_fontsize = 12

start = time.time()

plt.figure()

for i in range(500):
    walker = Walker(init_position=(-25, 44.5), verticalStepSize=0.02, horizontalStepSize=0.02)
    plt.plot(*zipCoords(walker.positionJumpProcess(1000)), alpha=0.01, color='red')
plt.tight_layout() 
plt.plot(-25, 44.5, color="k", marker='.')
plt.xlabel("Longitude ($\degree$E)", fontsize=label_fontsize)
plt.ylabel("Latitude ($\degree$N)", fontsize=label_fontsize)
plt.tick_params(labelsize=tick_fontsize)

plt.axis('equal')
plt.axis('square')
end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")

plt.savefig('RRW_sample')
plt.show()