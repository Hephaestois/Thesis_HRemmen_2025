# NOTE The time for doing RRW in VF's became significant (>1m), 
# so I decided to make the plotting part standalone.
# That is what this file is.

import matplotlib.pyplot as plt
import pickle
from library.functions import zipCoords
from time import time

walk_opacity = 0.03

plt.figure(figsize=(6,2), dpi=600)
start = time()
# Load the data from the file into the variable 'paths'
with open('createdData.pkl', 'rb') as file:
    paths = pickle.load(file)
    
for path in paths:
    plotvals = zipCoords(path)
    for i in range(len(plotvals[0])-1):
        plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=walk_opacity)   
#plt.plot(paths[0][0][0], paths[0][1][0], color="k", marker='.')
end = time()
print(f"{1000 * (end - start)} milliseconds elapsed")
plt.savefig('randomWalk.png')