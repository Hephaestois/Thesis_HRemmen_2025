import pandas as pd
import matplotlib.pyplot as plt
from time import time

start = time()
# Read the CSV file
data = pd.read_csv('data/2014-5by6-oneday.csv')

# Extract the necessary columns
latitude = data['latitude']
longitude = data['longitude']
water_u = data['water_u']
water_v = data['water_v']

print(f'Elapsed time after reading data: {time()-start}')
# Create a plot
plt.figure(figsize=(10, 8))
plt.quiver(longitude, latitude, water_u, water_v, angles='xy', scale_units='xy', scale=1)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Water Vectors (water_u, water_v)')
print(f'Elapsed time after plotting: {time()-start}')
plt.show()
