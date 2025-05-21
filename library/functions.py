import numpy as np
import pandas as pd
import sys
import time
import random

def zipCoords(steps):
    '''A function to convert a list of steps into a list of x and y coordinates for plotting'''
    return np.transpose(np.array(steps))

def chooseDirection(cumProbs):
    '''Converts from a cumulative probability list lrud to a direction chosen according to those probabilities.'''
    randomNumber = random.random()
    e = 1e-4
    
    for v in cumProbs:
        if v>1 or v<0:
            raise("Impossible probability was found!!!!!")
    if cumProbs[3] < 1-e or cumProbs[3] > 1+e:
        raise(f"invalid sum of probs found!!!! {cumProbs[3]}")
    
    if randomNumber <= cumProbs[0]:
        return np.array([-1, 0])
    
    if randomNumber <= cumProbs[1]:
        return np.array([1, 0])
    
    if randomNumber <= cumProbs[2]:
        return np.array([0, 1])
    
    # randomNumber <= cumProbs[3] = 1: always happens. Due to rounding errors (somewhere a prob. gets created with division), this function uses exceeds.
    return np.array([0, -1])

def directionsFromAngles(angle):
    return np.array([np.cos(angle), np.sin(angle)])
    
def findClosestIndex(vectorfield, lat, lon):
    closestLatIdx = np.argmin(np.abs(vectorfield['latitude']-lat))
    closestLonIdx = np.argmin(np.abs(vectorfield['longitude']-lon))
    return [closestLonIdx, closestLatIdx]
    
def positionToIndex(vectorfield, lon, lat):
    """Interpolates a decimal grid index from a geographic position (lat, lon),
    using the known lat/lon values from the NetCDF dataset.

    Parameters:
        vectorfield (dict): Contains 'latitude' and 'longitude' arrays.
        lat (float): Latitude of the walker.
        lon (float): Longitude of the walker.

    Returns:
        (float, float): (lon_index, lat_index) as decimal values.
    """
    lat_vals = vectorfield['latitude']
    lon_vals = vectorfield['longitude']
    
    # Check bounds
    # if not (lat_vals[0] <= lat <= lat_vals[-1]):
    #     raise ValueError(f"Latitude {lat} is out of bounds.")
    # if not (lon_vals[0] <= lon <= lon_vals[-1]):
    #     raise ValueError(f"Longitude {lon} is out of bounds.")

    # Interpolate lat index
    lat_idx = np.interp(lat, lat_vals, np.arange(len(lat_vals)))
    lon_idx = np.interp(lon, lon_vals, np.arange(len(lon_vals)))

    return lon_idx, lat_idx 

def progressBar(progress, max, start_time, bar_length=40, comment=False, commentMessage=''):
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
    if comment:
        text += f" | {commentMessage}: {str(comment)[:10]}"
    
    sys.stdout.write(text)
    sys.stdout.flush()

    if progress == max:
        print()  # Move to next line on completion