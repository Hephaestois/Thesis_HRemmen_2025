from lib.agents import Walker
from lib.functions import zipCoords
import matplotlib.pyplot as plt
import time

# Currently, the performance is O(n) (1M: 3.6s, 2M: 7.4s, 4M: 13.6s). Pretty good, but I would like performance like log(n), or just faster in O(n).
# Swapping to Numpy, the performance (1M: 7.9s, 2M: 13.7s)
# Actually properly vectorizing some stuff:
#                                    (1M: 1.2s, 2M: 2.3s, 4M: 4.6s) Optimization acquired!

start = time.time()
john = Walker()
locations = john.moveNStep(4000000)

plt.figure()
plt.plot(*zipCoords(locations))
end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.show()
