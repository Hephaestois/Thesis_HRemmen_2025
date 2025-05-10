from library.structures import Grid
from library.functions import progressBar
import numpy as np
import matplotlib.pyplot as plt
import math
from time import time

start_time = time()
x_range = [-29, -11]
y_range = [42, 47]
end_time = 10 #A lot?
dx = 0.36 #0.36x0.1. This makes the grid square, but the domain suffers for its non-equal resolution.
dy = 0.1
dt = 0.01



grid = Grid(x_range, y_range, dx ,dy)
grid.setDiffusionConstants(np.eye(2,2))
grid.setTimestep(dt)

grid.precalculateDiffusiveMatrix()

A = 1.0
x0 = (-20)
y0 = (44.5)
sigma_x = (-18) / 6  # or any scale you prefer
sigma_y = (-5) / 6

for i in grid.x_idxs:
    for j in grid.y_idxs:
        x,y = grid.itc(i, j)
        value = A * math.exp(-((x - x0)**2) / (2 * sigma_x**2) - ((y - y0)**2) / (2 * sigma_y**2))
        grid.setValue(grid.cti(x,y), value)

matrix = grid.getMatrix()

plt.figure(figsize=[10, 4], dpi=100)
plt.imshow(matrix.T, origin='lower', extent=[-29, -11, 42, 47], aspect  = dx/dy, vmin=0, vmax=1)

plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Density Field')
plt.show()


N_steps = int(end_time/dt)

print(grid.getTotalValue())
for i in range(N_steps):
    progressBar(i, N_steps-1, start_time, comment=grid.getTotalValue())
    grid.timeStep()
    
matrix = grid.getMatrix()

plt.figure(figsize=[10, 4], dpi=100)
plt.imshow(matrix.T, origin='lower', extent=[-29, -11, 42, 47], aspect  = dx/dy, vmin=0, vmax=1)

plt.colorbar()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Density Field')
plt.show()



    




    
