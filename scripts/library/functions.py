import numpy as np
import pandas as pd

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
    
    
    