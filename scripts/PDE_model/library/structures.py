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
        self.diffusiveMatrix_x = np.zeros((self.x_num, self.y_num))
        self.diffusiveMatrix_y = np.zeros((self.x_num, self.y_num))
        self.advectiveMatrix_x = np.zeros((self.x_num, self.y_num))
        self.advectiveMatrix_y = np.zeros((self.x_num, self.y_num))
        
        
        # For absorbing boundaries
        self.overflow_top = 0
        self.overflow_bottom = 0
        
        self.dt = 0
    
    def setDiffusionConstants(self, D):
        self.diffusionConstants = D
        
    def setAdvectionConstant(self, A):
        print(A[0], A[1])
        self.advectionConstants = A
    
    def setValue(self, pos, value):
        self.u_old[pos] = value
    
    def setTimestep(self, timestep):
        self.dt = timestep
        
    def precalculateDiffusiveMatrix(self, type, direction):
        '''TODO: Code for handling boundary conditions should go here too!!!'''
        D = np.zeros((self.x_num, self.y_num))
        np.fill_diagonal(D, -2)
        np.fill_diagonal(D[1:], 1)    # sub-diagonal
        np.fill_diagonal(D[:,1:], 1)  # super-diagonal
        
        if type == "Neumann":
            D[0,0] = -1
            D[-1, -1] = -1
        if type == "Absorbing":
            D[0,0] = 0
            D[0,1] = 0
            D[-1,-1] = 0
            D[-1,-2] = 0
            
        if direction == "Horizontal":
            self.diffusiveMatrix_x = D
        if direction == "Vertical":
            self.diffusiveMatrix_y = D
            
    def precalculateAdvectiveMatrix(self):
        Ax = np.zeros((self.x_num, self.x_num))
        np.fill_diagonal(Ax, -1)
        np.fill_diagonal(Ax[:,1:], 1)
        self.advectiveMatrix_x = Ax * self.advectionConstants[0]
        
        Ay = np.zeros((self.y_num, self.y_num))
        np.fill_diagonal(Ay, -1)
        np.fill_diagonal(Ay[:,1:], 1)
        self.advectiveMatrix_y = Ay * self.advectionConstants[1]
                
    def timeStep(self, diffusion=True, advection=True):
        self.u_new = self.u_old
        
        if diffusion:
            D_x = self.diffusiveMatrix_x  # diffusion operator matrix with Neumann BCs
            D_y = self.diffusiveMatrix_y  # diffusion operator matrix with absorbing BCs
            
            
            #Left-mul by operator for d_xx, right mul for d_yy.
            LHS_diff = self.diffusionConstants[0, 0] * np.matmul(D_x, self.u_old)
            RHS_diff = self.diffusionConstants[1, 1] * np.matmul(self.u_old, D_y)
            self.u_new += self.dt * (LHS_diff + RHS_diff)
        
        if advection:
            A_x = self.advectiveMatrix_x
            A_y = self.advectiveMatrix_y
            
            LHS_adv = np.matmul(A_x, self.u_old)
            RHS_adv = np.matmul(self.u_old, A_y)
            self.u_new += self.dt * (LHS_adv + RHS_adv)
            
            
        #Absorbing boundaries:
        self.overflow_top += self.u_new[:, -1].sum()
        self.overflow_bottom += self.u_new[:, 0].sum()
        
        #Remove value at the overflow boundary
        self.u_new[:, 0] = 0
        self.u_new[:, -1] = 0
        
        self.u_old = self.u_new
        
        
        
    def getMatrix(self):
        return self.u_old
    
    def itc(self, i, j):
        '''Index (i,j) to coordinate (x,y)'''
        # For future hazel: This needs to be backwards! It is the correct way around like this!!! i and j are correct!
        x = min(self.x_carthesian_range)+j*self.x_stepsize
        y = min(self.y_carthesian_range)+i*self.y_stepsize
        return (x,y)
    
    def cti(self, x, y):
        '''Coordinate (x,y) to index (i, j)'''
        # For future hazel: This needs to be backwards! It is the correct way around like this!!! i and j are correct!
        j = int(np.searchsorted(self.x_s, x))
        i = int(np.searchsorted(self.y_s, y))
        return (i, j)
        
    def getTotalValue(self):
        return np.sum(self.u_old)
    
    def getOverflowBottom(self):
        return self.overflow_bottom
    
    def getOverflowRatio(self):
        '''Ratio between bottom overflow and total overflow'''
        try:
            return self.overflow_bottom / (self.overflow_bottom+self.overflow_top)
        except:
            return None
        
    def getOverflowTop(self):
        return self.overflow_top
    
    def getOverflow(self):
        return self.overflow_bottom + self.overflow_top
        