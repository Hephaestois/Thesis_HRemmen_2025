from library.agents import Walker
from library.functions import zipCoords
import matplotlib.pyplot as plt
import time

# Currently, the performance is O(n) (1M: 3.6s, 2M: 7.4s, 4M: 13.6s). Pretty good, but I would like performance like log(n), or just faster in O(n).
# Swapping to Numpy, the performance (1M: 7.9s, 2M: 13.7s)
# Actually properly vectorizing some stuff:
#                                    (1M: 1.2s, 2M: 2.3s, 4M: 4.6s) Optimization acquired!
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'none'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

start = time.time()

walkers = 50
steps = 1000

plt.figure(figsize=(4,4),dpi=600)
for i in range(walkers):
    walker = Walker(probs=(0.23, 0.27, 0.25, 0.25))
    plt.plot(*zipCoords(walker.moveNStep(steps)), alpha=0.1, color='red')
plt.axis('equal')
plt.axis('square')
end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig(f'RRW{walkers}-{steps}MoreRightward.png', transparent=True)
plt.savefig('randomWalkNontrans.png')
