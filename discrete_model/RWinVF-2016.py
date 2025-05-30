# Make sure we can import from the shared library and data files
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'library')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Handle arguments
if len(sys.argv) != 3:
    print("Usage: python RWinVF-[year].py <sim_days> <n_per_day>")
    sys.exit(1)

N_simulation_days = int(sys.argv[1])
N_released_per_day = int(sys.argv[2])

# Other imports
from library.agents import Walker
from library.functions import zipCoords, progressBar, save_data
from scipy.interpolate import RegularGridInterpolator
import matplotlib.pyplot as plt
import time
import numpy as np
import netCDF4
import pickle

### Simulation options
# High level stuff
# N_tutels = 40
# N_simulation_days = simLengthDays # N days of swimming. Dont go beyond 638 fr fr, exceeds dataset bound. 
# N_released_per_day = 2   #Gamma=5 in Painter, amount of released tutels


# Turtle related stuff
startpos = np.array([-25, 44.5]) #lon(x), lat(y)
initial_probability = (0.174468, 0.28168, 0.09942134, 0.4444274) #lrud
horizontalStepSize = 0.02 # Turtle step size, in degrees lat/long
verticalStepSize = 0.02   # Turtle step size, in degrees lat/long

# Time / dataset related stuff
startTime_1 = 140_256     # This repr. 01-01-2016, Hours since 01-01-2000. End at 30-04-2016
startTime_2 = 143_184     # This repr. 01-05-2016 (May)
startTime_3 = 149_808      # This repr. 01-02-2017 (Feb)
timeResolution = 24 # This is regardless of the multiples of 3 hours 
                    # the dataset works with. 
endTime = startTime_1 + timeResolution*N_simulation_days


# Spatial dataset related stuff. #lat and #long should be the same length, delta is used to accomodate for this.
longitude_data_stepsize = 1 #Multiples of 0.04 degree
latitude_data_stepsize  = 1 #Multiples of 0.08 degree
delta = 0                   #For correcting size mismatch in latitudes/longitudes.
x_range = (-29,-11)
y_range = (42, 47)

### END of options

start = time.time()
year=2016
url1 = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3' # No spatial resolution for the dataset is necessary; it is interpolated onto the simulation grid size.
url2 = 'http://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.2'
url3 = 'https://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_92.8'

dataset1 = netCDF4.Dataset(url1)
dataset2 = netCDF4.Dataset(url2)
dataset3 = netCDF4.Dataset(url3)
e = 1e-3 #Small offset for mask boundaries

# Original arrays
time_array_1 = dataset1.variables['time'][:]
time_array_2 = dataset2.variables['time'][:]
time_array_3 = dataset3.variables['time'][:]


lon_array = dataset1.variables['lon'][:]
lat_array = dataset1.variables['lat'][:]

# Time indices and values for timeset 1
time_mask_1 = (time_array_1 >= startTime_1) & (time_array_1 <= endTime)
time_idx_1 = np.where(time_mask_1)[0]
times_1 = time_array_1[time_idx_1]
startTimeIndex_1 = list(time_array_1).index(startTime_1)

# Time indices for timeset 2
time_mask_2 = (time_array_2 >= startTime_2) & (time_array_2 <= endTime)
time_idx_2 = np.where(time_mask_2)[0]
times_2 = time_array_2[time_idx_2]
startTimeIndex_2 = list(time_array_2).index(startTime_2)

# Time indices for timeset 3
time_mask_3 = (time_array_3 >= startTime_3) & (time_array_3 <= endTime)
time_idx_3 = np.where(time_mask_3)[0]
times_3 = time_array_3[time_idx_3]
startTimeIndex_3 = list(time_array_3).index(startTime_3)

# Longitude indices and values
lon_mask = (lon_array >= min(x_range)-e) & (lon_array <= max(x_range)+e)
lon_idx = np.where(lon_mask)[0]
longitudes = lon_array[lon_idx]

# Latitude indices and values
lat_mask = (lat_array >= min(y_range)-e) & (lat_array <= max(y_range)+e)
lat_idx = np.where(lat_mask)[0]
latitudes = lat_array[lat_idx]

vectorfield = dict()
vectorfield['latitude'] = latitudes
vectorfield['longitude'] = longitudes

Tutels = []
paths = []
start_frames = []

tutel = Walker(
    init_position=startpos,
    init_probs=initial_probability,
    horizontalStepSize=horizontalStepSize, 
    verticalStepSize=verticalStepSize
)
Tutels.append(tutel)
paths.append([])
start_frames.append(0)  # Frame when this turtle starts walking
  
for i in range(N_simulation_days+1):
    if i < 366:
        for _ in range(N_released_per_day):
            tutel = Walker(
                init_position=startpos,
                init_probs=initial_probability,
                horizontalStepSize=horizontalStepSize, 
                verticalStepSize=verticalStepSize,
                lon_vals = dataset1.variables['lon'][lon_idx],
                lat_vals = dataset1.variables['lat'][lat_idx]   
            )
            Tutels.append(tutel)
            paths.append([])
            start_frames.append(i)  # Frame when this turtle starts walking

    progressBar(i, N_simulation_days, start)    

    simTime = startTime_1 + i*timeResolution #Hours since 2000
    if simTime < startTime_2:
        simulationTimeIndex = np.searchsorted(times_1, simTime) + startTimeIndex_1
        dataset = dataset1
    elif simTime < startTime_3:
        simulationTimeIndex = np.searchsorted(times_2, simTime) + startTimeIndex_2
        dataset = dataset2
    else:
        simulationTimeIndex = np.searchsorted(times_3, simTime) + startTimeIndex_3
        dataset=dataset3
    
    vectorfield['water_u']=dataset.variables['water_u'][simulationTimeIndex, 0, lat_idx, lon_idx]
    vectorfield['water_v']=dataset.variables['water_v'][simulationTimeIndex, 0, lat_idx, lon_idx]
    
    for j, tutel in enumerate(Tutels):
        if tutel.finished:
            continue
        
        tutel.probdistance = 0 
        
        while tutel.probdistance < 1:
            if tutel.finished:
                break
                        
            tutel.traverseVF(vectorfield, n=1)

        # Position is logged at the end of the day, when the turtles have finished moving. This means in the animation, the turtle step will not be equidistant!!
        # But per simulation step, this works out fine.
        paths[j].append(tutel.position)
        

print('Writing data to storage...')

exceedsTop = 0
exceedsBottom = 0 

for tutel in Tutels:
    exceedsTop += tutel.exceedsTop
    exceedsBottom += tutel.exceedsBottom

save_data([paths, start_frames], "discrete", year, N_simulation_days, f'{N_released_per_day}perday', 'allpositions')
save_data([exceedsTop, exceedsBottom], "discrete", year, N_simulation_days, f'{N_released_per_day}perday', 'exceedTopBottom')

print("Done!")

end = time.time()
print(f"{1000 * (end - start)} milliseconds elapsed")