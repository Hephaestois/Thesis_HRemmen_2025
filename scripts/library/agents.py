from library.functions import chooseDirection, directionsFromAngles, findClosestIndex
import numpy as np

class Grid:
    
    pass

class Walker:
    '''A walker is an object that 'walks' a 2d grid.'''
    def __init__(
            self, 
            init_position=np.array([0, 0]), 
            probs=(0.25, 0.25, 0.25, 0.25), 
            orientationFunction=lambda x: 0, 
            horizontalStepSize=1, verticalStepSize=1, 
                ):
        
        self.position = np.array(init_position)   # The coordinate where our walker is
        
        
        # related to position jump process
        self.probs = np.array(probs)              # probability of moving l, r, u, d.
        self.cumProbs = np.cumsum(self.probs)
        
        # related to velocity jump process
        self.orientationFunction = orientationFunction #A function that maps a uniform random number [0,1] to a directional statistic
        
        # Related to vector field dynamics
        self.horizontalStepSize = horizontalStepSize
        self.verticalStepSize = verticalStepSize
        
    def moveRandom(self, randomnum):
        direction = self.directionToStep(chooseDirection(self.cumProbs, randomnum)) #This is a coordinate, unit direction.
        self.position += direction
        return self.position #Might be useful later?
    
    def positionJumpProcess(self, n):
        # Precompute random directions for all steps
        randomNumbers = np.random.rand(n)
        directions = np.array([self.directionToStep(chooseDirection(self.cumProbs, randomNumbers[i])) for i in range(n)])
        
        # Calculate all positions in parallel
        positions = np.cumsum(directions, axis=0) + self.position

        # Update the final position
        self.position = positions[-1]

        return positions
    
    def velocityJumpProcess(self, n):
        #precompute random numbers for all steps
        randomNumber = np.random.rand(n)
        #convert [0,1] to [-pi, pi] to directions in 2d
        directions = np.array([self.directionToStep(directionsFromAngles(self.orientationFunction(randomNumber[i]))) for i in range(n)])
        
        positions = np.cumsum(directions, axis=0)
        positions = np.append(np.array([[0, 0]]), positions, axis=0)
        self.position = positions[-1]
        return positions
    
    def getRWBiasInField(self, vectorfield):
        lon = self.position[0]
        lat = self.position[1]
        
        # TODO: This function is horribly broken! 
        # This will always return the FIRST instance of the specific lat/lon being found. \
        # Not the actual idx being searched.
        
        closest_idx = findClosestIndex(vectorfield, lat, lon)
        # x' = x / (x+y), y' = y / (x+y), 
        # so that x'+y'=1 making it a feasible 
        # (unscaled!) prob.
        # Problem is that movement is always along vec field.
        # Negativity of field velocity is handled with logic instead math.
        
        horizontal_field_velocity = vectorfield['water_u'][closest_idx]
        vertical_field_velocity = vectorfield['water_v'][closest_idx]
        total_velocity = np.abs(horizontal_field_velocity) + np.abs(vertical_field_velocity)
        
        horiz_prob = np.abs(horizontal_field_velocity)/total_velocity
        vert_prob = np.abs(vertical_field_velocity)/total_velocity
        
        
        #now these probabilities add up to 1.
        if horizontal_field_velocity >= 0:
            if vertical_field_velocity >= 0:
                self.probs = np.array([0, horiz_prob, vert_prob, 0]) # probability of moving l, r, u, d.
            else:
                self.probs = np.array([0, horiz_prob, 0, vert_prob])
        else:
            if vertical_field_velocity >= 0:
                self.probs = np.array([horiz_prob, 0, vert_prob, 0])
            else:
                self.probs = np.array([horiz_prob, 0, 0, vert_prob])
        self.cumProbs = np.cumsum(self.probs)

    def directionToStep(self, direction):
        #Makes a step move on a grid. 
        return np.array([self.horizontalStepSize*direction[0], self.verticalStepSize*direction[1]])
    
    def traverseVectorField(self, vectorfield, n):
        # # Precompute random directions for all steps
        # directions = np.array([self.directionToStep(chooseDirection(self.cumProbs, randomNumbers[i])) for i in range(n)])
        
        # # Calculate all positions in parallel
        # positions = np.cumsum(directions, axis=0) + self.position

        # # Update the final position
        # self.position = positions[-1]

        # return positions
        
        randomNumbers = np.random.rand(n)
        positions = np.zeros([n+1,2])
        positions[0]=self.position
        for i in range(n):
            #This automatically updates the directions
            self.getRWBiasInField(vectorfield)
            newpos = self.moveRandom(randomNumbers[i])
            positions[i+1] = newpos
        
        self.position = positions[-1]
        
        return positions