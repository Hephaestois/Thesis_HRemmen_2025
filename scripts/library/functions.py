import numpy as np
import pandas as pd
import sys
import time

def zipCoords(steps):
    '''A function to convert a list of steps into a list of x and y coordinates for plotting'''
    return np.transpose(np.array(steps))

def chooseDirection(cumProbs, randomNumber):
    if randomNumber <= cumProbs[0]:
        return np.array([-1, 0])
    if randomNumber <= cumProbs[1]:
        return np.array([1, 0])
    if randomNumber <= cumProbs[2]:
        return np.array([0, 1])
    # randomNumber <= cumProbs[3] = 1: always happens
    return np.array([0, -1])

def directionsFromAngles(angle):
    return np.array([np.cos(angle), np.sin(angle)])

def getVectorFieldFromExcel(filename):
    #This is currently dependent on deleting line 2 in the CSV. This should be fixed.
    data = pd.read_csv(f'{filename}')
    return data
    
def findClosestIndex(vectorfield, lat, lon): 
    latts = np.power(vectorfield['latitude']-lat, 2)
    longs = np.power(vectorfield['longitude']-lon, 2)
    distance = np.sqrt(latts+longs)
    index = np.argmin(distance)
    return index

def findClosestIndexCont(vectorfield, lat, lon):
    closestLatIdx = np.argmin(np.abs(vectorfield['latitude']-lat))
    closestLonIdx = np.argmin(np.abs(vectorfield['longitude']-lon))
    return [closestLonIdx, closestLatIdx]
    
def progressBar(progress, max, start_time, bar_length=40):
    """
    Prints a dynamic progress bar with estimated time remaining.

    Parameters:
        progress (int): Current progress value (0 to max).
        max (int): Total or maximum value.
        start_time (float): The time when the operation started (time.time()).
        bar_length (int): Length of the progress bar in characters.
    """
    if max == 0:
        percent = 1
    else:
        percent = progress / max

    block = int(round(bar_length * percent))
    elapsed = time.time() - start_time
    if percent > 0:
        estimated_total = elapsed / percent
        remaining = estimated_total - elapsed
    else:
        remaining = 0

    elapsed_str = time.strftime("%H:%M:%S", time.gmtime(elapsed))
    remaining_str = time.strftime("%H:%M:%S", time.gmtime(remaining))

    text = (
        f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] "
        f"{percent * 100:.1f}% | Elapsed: {elapsed_str} | ETA: {remaining_str}"
    )
    sys.stdout.write(text)
    sys.stdout.flush()

    if progress == max:
        print()  # Move to next line on completion
