from library.structures import Grid, Edge, Node
from library.functions import progressBar
import numpy as np
import matplotlib.pyplot as plt
from time import time
import netCDF4

grid = Grid([-29,-11], [42,47])
end_time = 0.025
starttime = time()
dx, dy = 0.1, 0.1 #generally, dy = 3.6dx for a square grid.

print("Starting process")
grid.make_grid(dx, dy)
print("Finished making grid")
grid.add_value(*grid.cti(-25, 44.5), 1)

dt = 0.001
N_steps = round(end_time/dt)
dt_limit = 0.25 * min(dx**2, dy**2)/max(np.linalg.eigvals(grid.node_grid[(0, 0)].D))

print(grid.cti(*grid.itc(10, 10)))


if dt > dt_limit:
    print(f"dt {dt} is larger than the stability limit {dt_limit}. Rescale accordingly")

for i in range(N_steps):
    progressBar(i, N_steps-1, starttime)
    grid.compute_fluxes(diffusive=False)
    grid.update_nodes(dt)
    grid.swap_fields()
    grid.add_value(*grid.cti(-25, 44.5), 1)
    
    
array = grid.make_plottable()

plt.figure(figsize=[10, 4], dpi=100)
plt.imshow(array.T, origin='lower', extent=[-29, -11, 42, 47], aspect  = dx/dy)

plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Density Field')
plt.show()
    
