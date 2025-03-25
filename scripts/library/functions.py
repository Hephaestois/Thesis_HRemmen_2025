import numpy as np

def zipCoords(steps):
    '''A function to convert a list of steps into a list of x and y coordinates for plotting'''
    return np.array(steps).T

def chooseDirection(cumProbs, randomNumber):
    if randomNumber <= cumProbs[0]:
        return np.array([-1, 0])
    if randomNumber <= cumProbs[1]:
        return np.array([1, 0])
    if randomNumber <= cumProbs[2]:
        return np.array([0, 1])
    # randomNumber <= cumProbs[3] = 1: always happens
    return np.array([0, -1])
