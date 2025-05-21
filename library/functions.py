import numpy as np
import pandas as pd
import sys
import time
import random
import pickle
import os

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
        
def save_data(obj, label, year, n_days, resolution_args, day):
    """
    Save data to data/{label}/{year}_{n_days}_{resolution_args}/{day}.pkl

    Parameters:
    - obj: the Python object to pickle
    - label: subdirectory label under data/ ("PDE" or "discrete")
    - year: year of the dataset (e.g., 2020)
    - n_days: number of days total (e.g., 365)
    - resolution_args: string describing resolution params (e.g., '5min_agg')
    - day: the day number/file name (e.g., 15)
    """
    
    if label != "pde" and label != "discrete":
        print("Are you sure the save location is correct?")
    
    # Get project root (head/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Construct the path
    subfolder = f"{year}_{n_days}d_{resolution_args}"
    target_dir = os.path.join(base_dir, 'data', label, subfolder)
    os.makedirs(target_dir, exist_ok=True)

    filepath = os.path.join(target_dir, f"{day}.pkl")

    # Save using pickle
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)

    # print(f"Saved: {filepath}")
    
    
def load_data(label, year, n_days, resolution_args, day):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    subfolder = f"{year}_{n_days}d_{resolution_args}"
    filepath = os.path.join(base_dir, 'data', label, subfolder, f"{day}.pkl")

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'rb') as f:
        return pickle.load(f)
    
import os
import matplotlib.pyplot as plt

def save_figure(fig, filename, subfolder=None):
    """
    Save a matplotlib figure to the pde_figures/ directory.

    Parameters:
    - fig: the matplotlib figure object
    - filename: name of the file to save (e.g., 'solution_plot.png')
    - subfolder: optional subfolder inside pde_figures/ (e.g., '2024')
    """
    # Get the base directory (head/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Build the full path to the output folder
    out_dir = os.path.join(base_dir, 'pde_figures')
    if subfolder:
        out_dir = os.path.join(out_dir, subfolder)
    
    os.makedirs(out_dir, exist_ok=True)  # ensure the folder exists

    fig_path = os.path.join(out_dir, filename)
    fig.savefig(fig_path, bbox_inches='tight', dpi=300)
    print(f"Figure saved to: {fig_path}")
    
import os

def save_animation(anim, filename, subfolder=None, fps=30):
    """
    Save a matplotlib animation to the pde_figures/ directory.

    Parameters:
    - anim: the animation object (e.g., from FuncAnimation)
    - filename: name of the output file (e.g., 'wave.mp4' or 'wave.gif')
    - subfolder: optional subfolder inside pde_figures/
    - fps: frames per second for the animation
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    out_dir = os.path.join(base_dir, 'pde_figures')
    if subfolder:
        out_dir = os.path.join(out_dir, subfolder)
    os.makedirs(out_dir, exist_ok=True)

    filepath = os.path.join(out_dir, filename)

    # Save animation
    anim.save(filepath, writer='ffmpeg', fps=fps)
    print(f"Animation saved to: {filepath}")

