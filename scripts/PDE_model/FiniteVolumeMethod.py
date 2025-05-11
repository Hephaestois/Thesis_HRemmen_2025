from library.structures import Grid
from library.functions import progressBar
import numpy as np
import matplotlib.pyplot as plt
import math
from time import time

x_range = [-29, -11]
y_range = [42, 47]
end_time = 1 #A lot?
dx = 0.036 # 18/5 x 0.1. This makes the grid square (NxN), but the domain suffers for its non-equal resolution. Not so bad at high resolutions, though.
dy = 0.01
dt = 0.005

grid = Grid(x_range, y_range, dx ,dy)
grid.setDiffusionConstants(np.array([[0.01, 0], [0, 0.01]]))
grid.setAdvectionConstant(np.array([-2, 0]))
grid.setTimestep(dt)

grid.precalculateDiffusiveMatrix(type="Neumann", direction="Horizontal")
grid.precalculateDiffusiveMatrix(type="Absorbing", direction="Vertical")
grid.precalculateAdvectiveMatrix()


## IC: Gaussian
A = 1.0
x0 = (-25)
y0 = (44.5)
sigma_x = 1
sigma_y = 1

for i in grid.x_idxs:
    for j in grid.y_idxs:
        x,y = grid.itc(i, j)
        value = A * math.exp(-((x - x0)**2) / (2 * sigma_x**2) - ((y - y0)**2) / (2 * sigma_y**2))
        grid.setValue(grid.cti(x,y), value)
## End IC

grid.setValue((0, 0), 1)



N_steps = int(end_time/dt)
start_time = time()

for i in range(N_steps):
    progressBar(i, N_steps-1, start_time, comment=grid.getTotalValue())
    grid.timeStep(diffusion=True, advection=True)

matrix = grid.getMatrix()

plt.figure(figsize=[12, 6], dpi=100)
plt.imshow(matrix, origin='lower', extent=[-29, -11, 42, 47], aspect = 1, vmin=0, vmax=1)

plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Density Field')
plt.show()






    




    
