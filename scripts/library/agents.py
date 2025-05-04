from library.functions import chooseDirection, directionsFromAngles, findClosestIndexCont
import numpy as np
import random

class Grid:
    
    pass

class Walker:
    '''Our swimming turtles are defined under the Walker class, as they perform a random walk.
    
    
    '''
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
        '''This function is responsible for handling the end-decision of where a turtle moves. 
        
        It relies on the local Flow Speed, and the local and global probabilities of movement.
        I use Viktoria's proposal for the determination of the flow speed, so that we still
        acquire valid probabilities (SUM=1), and are able to factor in the weight of the vector field.
        
        TODO: Study how the parameter localFlowSpeed should be multiplied so that 
        '''
        # Correction factor for the localFlowSpeed, because of unit conversions. Currently unused (=1)
        flowSpeedMultiplier = 1
        
        # the weights for these are adapted using the flowspeed.
        weight_VF = np.divide(self.initProbs+self.localFlowSpeed*flowSpeedMultiplier, 1+self.localFlowSpeed*flowSpeedMultiplier)
        weight_self = 1 - weight_VF        
        
        # These are 4-vectors (lrud) containing the final local movement probability
        weightedProbs = np.multiply(self.initProbs, weight_self) + np.multiply(self.probs, weight_VF)
        weightedCumProbs = np.cumsum(weightedProbs)
        
        # This function chooses a direction based on the probabilities. The outer makes it respect the specified grid size.
        direction = self.directionToStep(chooseDirection(weightedCumProbs, random.random())) #This is a coordinate, unit direction.
        self.position += direction
        return self.position
    
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
        self.localFlowSpeed = np.sqrt(np.square(horizontal_field_velocity)+np.square(vertical_field_velocity))
        sum_field_velocity = np.abs(horizontal_field_velocity) + np.abs(vertical_field_velocity)

        #Only for normalization. Flow speed determines the weight
        horiz_prob = horizontal_field_velocity / sum_field_velocity
        vert_prob = vertical_field_velocity / sum_field_velocity
        
        
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

    def getRWBiasInVF(self, vectorfield):
        lon = self.position[0]
        lat = self.position[1]
        
        closest_idx_lon, closest_idx_lat = findClosestIndexCont(vectorfield, lat, lon)
        horizontal_field_velocity = vectorfield['water_u'][closest_idx_lon, closest_idx_lat]
        vertical_field_velocity = vectorfield['water_v'][closest_idx_lon, closest_idx_lat]
        self.localFlowSpeed = np.sqrt(np.square(horizontal_field_velocity)+np.square(vertical_field_velocity))
        sum_field_velocity = np.abs(horizontal_field_velocity) + np.abs(vertical_field_velocity)

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
    
    def traverseVF(self, vectorfield, n=1):
        '''Traversal of a vector field. Irregarless of time-variable, this is managed in the level above!!
        The vector field here is a snapshot in time, and should be used for small time- and space-steps.
        '''
        self.exceeds(vectorfield)
        
        # n=1 always now
        positions = np.zeros([2,2])
        positions[0]=self.position
        
        # Update the probabilities based on the local position
        self.getRWBiasInVF(vectorfield)
        
        # Take a random step and save it here. moveRandom returns the new position.
        newpos = self.moveRandom()
        positions[1] = newpos
    
        self.position = positions[-1]
        return positions
    
    def exceeds(self, vectorfield):
        '''Function to check if turtle exceeds the simulation range. 
        Called form traverse[Cont]VF. 
        
        When the VF is exceeded, for plotting purposes set position to the boundary.
        '''
        
        # Programming trick Only when all if's are false (so the turtle doesn't exceed) is this going to return True: 
        self.finished = True
        
        lon = self.position[0]
        lat = self.position[1]
        
        # These boundaries are according to Painter, page 27:
        # Stop sim when latitude exceeding 46.5 or 42.5 horizontal. The vertical boundaries are far enough so that they are not reached. 
        if np.all(np.greater(lat, 46.5)):
            # Force latitude to this value.
            self.position[1]=46.5
            return
        if np.all(np.less(lat, 42.5)):
            self.position[1]=42.5
            return
        
        if np.all(np.greater(lon,vectorfield['longitude'])):
            #We don't really care for the longitudinal exceeding, that doesn't really happen.
            return
        if np.all(np.less(lon, vectorfield['longitude'])):
            return
        self.finished = False
        