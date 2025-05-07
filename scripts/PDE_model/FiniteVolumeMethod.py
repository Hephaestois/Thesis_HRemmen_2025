from library.structures import Grid, Edge, Node
from library.functions import progressBar
import numpy as np
import matplotlib.pyplot as plt
from time import time

grid = Grid()
end_time = 0.025
starttime = time()
dx, dy = 0.01, 0.01

grid.make_grid(2, 2, dx, dy)
grid.node_grid[(10, 10)].setValue(0.01)

dt = 0.025
N_steps = round(end_time/dt)
dt_limit = 0.25 * min(dx**2, dy**2)/max(np.linalg.eigvals(grid.node_grid[(0, 0)].D))
print(dt_limit)

if dt > dt_limit:
    print(f"dt {dt} is larger than the stability limit {dt_limit}. Rescale accordingly")

for i in range(N_steps):    
    grid.compute_fluxes(diffusive=False)
    grid.update_nodes(dt)
    grid.swap_fields()
    
    
array = grid.make_plottable()

figure=plt.figure()
axes = figure.add_subplot(111)

caxes = axes.matshow(array)
figure.colorbar(caxes)
plt.show()

    
