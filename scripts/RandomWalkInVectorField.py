from library.agents import Walker
from library.functions import zipCoords, getVectorFieldFromExcel
import matplotlib.pyplot as plt
import matplotlib
import time
import pandas as pd
import numpy as np

start = time.time()
vectorfield = getVectorFieldFromExcel('data/2014-5by6-oneday.csv')

Tutel = Walker(init_position=np.array([44.4, -25.6]), horizontalStepSize=0.2, verticalStepSize=0.47998)

locations = Tutel.traverseVectorField(vectorfield, 20)
#Math ends here, only plotting below.
latitude = vectorfield['latitude'].to_numpy() #not important now, but later this being numpy will be convenient :)
longitude = vectorfield['longitude'].to_numpy()
water_u = vectorfield['water_u'].to_numpy()
water_v = vectorfield['water_v'].to_numpy()



plotvals = zipCoords(locations)

plt.quiver(longitude, latitude, water_u, water_v, angles='xy', scale_units='xy', scale=1)
for i in range(len(plotvals[0])-1):
    plt.plot(plotvals[1][i:i+2], plotvals[0][i:i+2], color='red', alpha=0.5)
plt.plot(plotvals[1][0], plotvals[0][0], color="k", marker='.')


end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')