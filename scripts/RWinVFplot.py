# NOTE The time for doing RRW in VF's became significant (>1m), 
# so I decided to make the plotting part standalone.
# That is what this file is.

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pickle
from library.functions import zipCoords
from time import time

walk_opacity = 0.2

start = time()
# Load the data from the file into the variable 'paths'
with open('createdData.pkl', 'rb') as file:
    paths = pickle.load(file)

print(len(paths[0]))
    
# for path in paths:
#     plotvals = zipCoords(path)
#     for i in range(len(plotvals[0])-1):
#         plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=walk_opacity)   
#plt.plot(paths[0][0][0], paths[0][1][0], color="k", marker='.')


plt.figure(figsize=[10, 4], dpi=600)
plt.xlim(-29, -11)
plt.ylim(42, 47)

for path in paths:
    plotvals = zipCoords(path)
    for i in range(0, 200):
        print(i)
        plt.plot(plotvals[0][i:i+2], plotvals[1][i:i+2], color='red', alpha=0.2)
    plt.plot(plotvals[0][-1], plotvals[1][-1], color='g', marker='.', alpha=1)

# fig = plt.figure()
# def updateFig(i):
#     fig.clear()
#     plotvals = zipCoords(paths[i])

#     p = plt.plot(plotvals[0], plotvals[1], color='r', marker='.')
#     plt.draw()
    
# # Create animation
# ani = FuncAnimation(fig, updateFig, interval=200, blit=False)

# # Save animation using FFMpegWriter
# writer = FFMpegWriter(fps=5, bitrate=1800)
# ani.save('test.mp4', writer=writer, dpi=200)



end = time()
plt.savefig('randomWalk.png')

