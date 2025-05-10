import numpy as np
from scipy.special import kn #Modified bessel function of order n


class Grid:
    def __init__(self, x_carthesian_range, y_carthesian_range, x_stepsize, y_stepsize):
        self.x_carthesian_range = x_carthesian_range
        self.y_carthesian_range = y_carthesian_range
        self.x_stepsize = x_stepsize
        self.y_stepsize = y_stepsize
        
        self.x_num = int((max(x_carthesian_range)-min(x_carthesian_range))/x_stepsize)
        self.y_num = int((max(y_carthesian_range)-min(y_carthesian_range))/y_stepsize)
        self.u_old = np.zeros(shape=(self.x_num, self.y_num))
        self.u_new = np.zeros(shape=(self.x_num, self.y_num))
        
        self.x_idxs = range(self.x_num)
        self.y_idxs = range(self.y_num)
        self.x_s = np.linspace(min(x_carthesian_range), max(x_carthesian_range), self.x_num)
        self.y_s = np.linspace(min(y_carthesian_range), max(y_carthesian_range), self.y_num)

        # PDE Characteristics
        self.diffusionConstants = np.zeros((2,2))
        self.advectionConstants = np.zeros(2)
    
        # d_xx, d_yy operators. x_shape by y_shape matrixes!
        self.diffusiveMatrix = np.zeros((self.x_num, self.y_num))
        self.advectiveMatrix = np.zeros((self.x_num, self.y_num))
        
        self.dt = 0
    
    def setDiffusionConstants(self, D):
        self.diffusionConstants = D
        print(self.diffusionConstants)
    
    def setValue(self, pos, value):
        self.u_old[pos] = value
    
    
    def setTimestep(self, timestep):
        self.dt = timestep
        
    def precalculateDiffusiveMatrix(self):
        '''TODO: Code for handling boundary conditions should go here too!!!'''
        np.fill_diagonal(self.diffusiveMatrix, -2)
        np.fill_diagonal(self.diffusiveMatrix[1:], 1)    # sub-diagonal
        np.fill_diagonal(self.diffusiveMatrix[:,1:], 1)  # super-diagonal
        
        self.diffusiveMatrix[0,0] = -1
        self.diffusiveMatrix[-1, -1] = -1
        print(self.diffusiveMatrix)
        
        
    
    
    def timeStep(self):
        #Left-mul by operator for d_xx, right mul for d_yy.
        LHS = self.diffusionConstants[0, 0] * np.matmul(self.diffusiveMatrix, self.u_old)
        RHS = self.diffusionConstants[1, 1] * np.matmul(self.u_old, self.diffusiveMatrix)
        self.u_new = self.u_old + self.dt * (LHS + RHS)
        self.u_old = self.u_new
        
    def getMatrix(self):
        return self.u_old
    
    def itc(self, i, j):
        '''Index (i,j) to coordinate (x,y)'''
        x = min(self.x_carthesian_range)+i*self.x_stepsize
        y = min(self.y_carthesian_range)+j*self.y_stepsize
        return (x,y)
    
    def cti(self, x, y):
        '''Coordinate (x,y) to index (i, j)'''
        i = int(np.searchsorted(self.x_s, x))
        j = int(np.searchsorted(self.y_s, y))
        return (i, j)
        
    def getTotalValue(self):
        return np.sum(self.u_old)
        
        