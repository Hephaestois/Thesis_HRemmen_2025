from library.functions import chooseDirection, directionsFromAngles
import numpy as np

class Grid:
    
    pass

class Walker:
    '''A walker is an object that 'walks' a 2d grid.'''
    def __init__(self, init_position=np.array([0, 0]), probs=(0.25, 0.25, 0.25, 0.25), orientationFunction=lambda x: 0, ):
        self.position = np.array(init_position)   # The coordinate where our walker is
        
        # related to position jump process
        self.probs = np.array(probs)              # probability of moving l, r, u, d.
        self.cumProbs = np.cumsum(self.probs)
        
        # related to velocity jump process
        self.orientationFunction = orientationFunction #A function that maps a uniform random number [0,1] to a directional statistic
        
        
            
    def moveRandom(self):
        direction = chooseDirection(self.cumProbs) #This is a coordinate, unit direction.
        self.position += direction
        return self.position #Might be useful later?
    
    def positionJumpProcess(self, n):
        # Precompute random directions for all steps
        randomNumbers = np.random.rand(n)
        directions = np.array([chooseDirection(self.cumProbs, randomNumbers[i]) for i in range(n)])
        
        # Calculate all positions in parallel
        positions = np.cumsum(directions, axis=0) + self.position

        # Update the final position
        self.position = positions[-1]

        return positions
    
    def velocityJumpProcess(self, n):
        #precompute random numbers for all steps
        randomNumber = np.random.rand(n)
        #convert [0,1] to [-pi, pi] to directions in 2d
        directions = np.array([directionsFromAngles(self.orientationFunction(randomNumber[i])) for i in range(n)])
        
        positions = np.cumsum(directions, axis=0)
        positions = np.append(np.array([[0, 0]]), positions, axis=0)
        self.position = positions[-1]
        return positions
    
    

        