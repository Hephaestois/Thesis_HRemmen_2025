import numpy as np
import pandas as pd
import sys
import time
import random

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