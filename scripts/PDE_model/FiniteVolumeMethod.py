from library.structures import Grid, Edge, Node
import numpy as np
import matplotlib.pyplot as plt

grid = Grid()
N_steps = 10

grid.make_grid(100, 100, 1, 1)
grid.node_grid[(50, 50)].setValue(100)

for _ in range(N_steps):    
    grid.compute_fluxes()
    grid.update_nodes(1)
    grid.swap_fields()
    
    
array = grid.make_plottable()

plt.matshow(array)
plt.show()
