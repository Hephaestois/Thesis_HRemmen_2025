from library.functions import chooseDirection, directionsFromAngles, findClosestIndex, findClosestIndexCont
import numpy as np
import random

class Grid:
    
    pass

class Walker:
    '''A walker is an object that 'walks' a 2d grid.'''
    def __init__(
            self, 
            init_position=np.array([0, 0]), 
            init_probs=(0.25, 0.25, 0.25, 0.25), 
            orientationFunction=lambda x: 0, 
            horizontalStepSize=1, verticalStepSize=1, 
                ):
        
        self.position = np.array(init_position)   # The coordinate where our walker is
        
        # related to position jump process
        self.initProbs = np.array(init_probs)
        self.initCumProbs = np.cumsum(self.initProbs)
        self.probs = np.array(init_probs)              # probability of moving l, r, u, d.
        self.cumProbs = np.cumsum(self.probs)
        
        # related to velocity jump process
        self.orientationFunction = orientationFunction #A function that maps a uniform random number [0,1] to a directional statistic
        
        # Related to vector field dynamics
        self.horizontalStepSize = horizontalStepSize
        self.verticalStepSize = verticalStepSize
        self.localFlowSpeed = 0
        
        #Has the turtle hit a border?
        self.finished = False
        
        
    def moveRandom(self):
        # the weights for these are adapted using the flowspeed.
        weight_VF = np.divide(self.initProbs+self.localFlowSpeed, 1+self.localFlowSpeed)
        weight_self = 1 - weight_VF        
        
        weightedProbs = np.multiply(self.initProbs, weight_self) + np.multiply(self.probs, weight_VF)
        
        weightedCumProbs = np.cumsum(weightedProbs)
        direction = self.directionToStep(chooseDirection(weightedCumProbs, random.random())) #This is a coordinate, unit direction.
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
        
    def getRWBiasInContField(self, vectorfield):
        # This function updates the weights of the walker in the vector field. Strong flow means low self influence.
        # MoveRandom then uses these weights.
        lon = self.position[0]
        lat = self.position[1]
        
        closest_idx_lon, closest_idx_lat = findClosestIndexCont(vectorfield, lat, lon)
        horizontal_field_velocity = vectorfield['water_u'][closest_idx_lon, closest_idx_lat]
        vertical_field_velocity = vectorfield['water_v'][closest_idx_lon, closest_idx_lat]
        self.localFlowSpeed = np.sqrt(np.square(horizontal_field_velocity)+np.square(vertical_field_velocity))
        sum_field_velocity = horizontal_field_velocity + vertical_field_velocity

        #Only for normalization. Flow speed determines the weight
        horiz_prob = horizontal_field_velocity / sum_field_velocity
        vert_prob = vertical_field_velocity / sum_field_velocity
        
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
        positions = np.zeros([n+1,2])
        positions[0]=self.position
        for i in range(n):
            #This automatically updates the directions
            self.getRWBiasInField(vectorfield)
            newpos = self.moveRandom()
            positions[i+1] = newpos
            if self.exceeds(vectorfield):
                positions = positions[0:i+1, 0:2]
                break
        
        self.position = positions[-1]
        
        return positions
    
    def traverseContVectorField(self,vectorfield,n):
        self.exceeds(vectorfield)
        
        positions = np.zeros([n+1,2])
        positions[0]=self.position
        for i in range(n):
            #This automatically updates the directions
            self.getRWBiasInContField(vectorfield)
            newpos = self.moveRandom()
            positions[i+1] = newpos
            if self.exceeds(vectorfield):
                positions = positions[0:i+1, 0:2]
                break
        
        self.position = positions[-1]
        return positions
    
    def exceeds(self, vectorfield):
        self.finished = True
        lon = self.position[0]
        lat = self.position[1]
        
        if np.all(np.greater(lat,vectorfield['latitude'])):
            return
        if np.all(np.less(lat, vectorfield['latitude'])):
            return
        if np.all(np.greater(lon,vectorfield['longitude'])):
            return
        if np.all(np.less(lon, vectorfield['longitude'])):
            return
        self.finished = False
        