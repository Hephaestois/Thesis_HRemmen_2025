from library.functions import chooseDirection
import numpy as np

class Grid:
    
    pass

class Walker:
    '''A walker is an object that 'walks' a 2d grid.'''
    def __init__(self, init_position=np.array([0, 0]), probs=(0.25, 0.25, 0.25, 0.25), grid=None):
        #self.grid = grid                # The grid on which the walker exists. Currently unused.
        self.position = np.array(init_position)   # The coordinate where our walker is
        self.probs = np.array(probs)              # probability of moving l, r, u, d.
        self.cumProbs = np.cumsum(self.probs)
            
    def moveRandom(self):
        direction = chooseDirection(self.cumProbs) #This is a coordinate, unit direction.
        self.position += direction
        return self.position #Might be useful later?
    
    def moveNStep(self, n):
        # Precompute random directions for all steps
        randomNumbers = np.random.rand(n)
        directions = np.array([chooseDirection(self.cumProbs, randomNumbers[i]) for i in range(n)])
        
        # Calculate all positions in parallel
        positions = np.cumsum(directions, axis=0) + self.position

        # Update the final position
        self.position = positions[-1]

        return positions
    

        