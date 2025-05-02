from library.agents import Walker
from library.functions import zipCoords, getVectorFieldFromExcel, progressBar
import matplotlib.pyplot as plt
import time
import pandas as pd
import numpy as np


### Simulation options
# High level stuff
N_swims = 40
swim_length = 600

# Turtle related stuff
startpos = np.array([-25.6, 44.4])
initial_probability = (0.25, 0.25, 0.25, 0.25) #lrud
horizontalStepSize = 0.05 # Turtle step size
verticalStepSize = 0.05   # Turtle step size


### Plotting options
walk_opacity = 0.2


###

start = time.time()
vectorfield = getVectorFieldFromExcel('data/2014-5by6-oneday.csv')


#Math ends here, only plotting below.
plt.figure(figsize=[10, 4], dpi=400)
plt.quiver(vectorfield['longitude'].to_numpy(), vectorfield['latitude'].to_numpy(), vectorfield['water_u'].to_numpy(), vectorfield['water_v'].to_numpy(), angles='xy', scale_units='xy', scale=2)
points = []


for i in range(N_swims):
    progressBar(i, N_swims-1, start)
    Tutel = Walker(
        init_position=startpos,
        init_probs = initial_probability,
        horizontalStepSize=horizontalStepSize, 
        verticalStepSize=verticalStepSize
        )
    locations = Tutel.traverseVectorField(vectorfield, swim_length) #swim_length
    plotvals = zipCoords(locations)
    points.append([plotvals[0][-1], plotvals[1][-1]])
    
    if walk_opacity == 0:
        continue
    
    for j in range(len(plotvals[0])-1):
        plt.plot(plotvals[0][j:j+2], plotvals[1][j:j+2], color='red', alpha=walk_opacity)
    
plt.scatter(zipCoords(points)[0], zipCoords(points)[1], color='g', marker='.', zorder=10)        
plt.plot(startpos[0], startpos[1], color="k", marker='.')

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')