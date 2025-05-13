import numpy as np
from scipy.special import kn #Modified bessel function of order n
import netCDF4

class Grid:
    def __init__(self, x_carthesian_range, y_carthesian_range, x_stepsize, y_stepsize):
        self.x_carthesian_range = x_carthesian_range
        self.y_carthesian_range = y_carthesian_range
        self.x_stepsize = x_stepsize
        self.y_stepsize = y_stepsize
        self.x_s = np.arange(min(x_carthesian_range), max(x_carthesian_range), self.x_stepsize) # ? 
        self.y_s = np.arange(min(y_carthesian_range), max(y_carthesian_range), self.y_stepsize) #
        self.x_num = len(self.x_s)
        self.y_num = len(self.y_s)
        
        self.u_old = np.zeros(shape=(self.y_num, self.x_num))
        self.u_new = np.zeros(shape=(self.y_num, self.x_num))
        
        self.x_idxs = range(self.x_num)
        self.y_idxs = range(self.y_num)
        
        # PDE Characteristics
        self.diffusionConstants = np.zeros((2,2))
        self.advectionConstants = np.zeros(2)
    
        # d_xx, d_yy operators. x_shape by y_shape matrixes!
        self.diffusiveOperator_x = np.zeros((self.y_num, self.y_num))
        self.diffusiveOperator_y = np.zeros((self.x_num, self.x_num))
        self.advectiveOperator_x = np.zeros((self.x_num, self.y_num))
        self.advectiveOperator_y = np.zeros((self.x_num, self.y_num))
        self.advectiveOperatorVF_x = np.zeros((self.x_num, self.y_num))
        self.advectiveOperatorVF_y = np.zeros((self.x_num, self.y_num))
        
        
        # For absorbing boundaries
        self.overflow_top = 0
        self.overflow_bottom = 0
        
        self.dt = 0
    
    def setDiffusionConstants(self, D):
        self.diffusionConstants = D
        
    def setAdvectionConstant(self, A):
        # Change is necessary to make format readable for humans: necessity comes from difference between (x,y) and  (i,j) in matrix form!
        self.advectionConstants = np.array([A[1],-A[0]])
    
    def setValue(self, pos, value):
        self.u_old[pos] = value
    
    def addValue(self, pos, value):
        self.u_old[pos] += value
    
    def setTimestep(self, timestep):
        self.dt = timestep
        
    def precalculateDiffusiveOperator(self, type, direction):
        '''TODO: Code for handling boundary conditions should go here too!!!'''
        if direction == "Horizontal":
            N = self.y_num
            d2 = self.x_stepsize**2 #Stepsize squared. For use later.
        elif direction == "Vertical":
            N = self.x_num
            d2 = self.y_stepsize**2
        
        D = np.zeros((N, N)) #These need to be square for linalg reasons, preserve correct size u_new = u_old + dt*f(u_old)
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
        
        D /= d2 #Scale to appropriate axis
            
        if direction == "Horizontal":
            self.diffusiveOperator_x = D
        if direction == "Vertical":
            self.diffusiveOperator_y = D
            
    def precalculateAdvectiveOperator(self):
        N_y, N_x = self.x_num, self.y_num #These are intentionally swapped! Due to the side of u on which the operator needs to be applied. This is correct, don't worry about it Hazel

        # 1D advection operator: backward- or forward difference depending on the sign.
        def advection_operator(N, advectionDirection):
            A = np.zeros((N, N))
            
            if advectionDirection >= 0:
                np.fill_diagonal(A, 1)
                np.fill_diagonal(A[1:], -1) #below diagonal
            else:
                np.fill_diagonal(A, -1)
                np.fill_diagonal(A[:, 1:], 1) #above diagonal
            
            return A * advectionDirection

        A_x = advection_operator(N_x, self.advectionConstants[0])
        A_y = advection_operator(N_y, self.advectionConstants[1])
        
        self.advectiveOperator_x = A_x / self.x_stepsize  # operates on x (columns)
        self.advectiveOperator_y = A_y / self.y_stepsize  # operates on y (rows)
        
    def precalculateAdvectiveOperatorVF(self):
        #Similar to precalcAdvectiveOperator
        N_y, N_x = self.x_num, self.y_num #Intentionally swapped!
        
        def advection_operator(N):
            A = np.zeros((N,N))
            
            np.fill_diagonal(A[1:], 1)
            np.fill_diagonal(A[:,1:], -1)
            
            return A
        
        self.advectiveOperatorVF_x = advection_operator(N_x) / (2*self.x_stepsize)
        self.advectiveOperatorVF_y = advection_operator(N_y) / (2*self.y_stepsize)
        pass
    
    def getVectorField(self, source, simStep):
        dataset = netCDF4.Dataset(source)
        
        VF_x = np.random.rand(50, 180)
        VF_y = np.random.rand(50, 180)
        
        self.vectorfield_x = VF_x
        self.vectorfield_y = VF_y
        pass
                
    def timeStep(self, diffusion=True, constantAdvection=True, VFAdvection=True):
        self.u_new = self.u_old
        
        if diffusion:
            D_x = self.diffusiveOperator_x  # diffusion operator matrix with Neumann BCs
            D_y = self.diffusiveOperator_y  # diffusion operator matrix with absorbing BCs
            
            #Left-mul by operator for d_xx, right mul for d_yy.
            LHS_diff = self.diffusionConstants[0, 0] * np.matmul(D_x, self.u_old)
            RHS_diff = self.diffusionConstants[1, 1] * np.matmul(self.u_old, D_y)
            self.u_new += self.dt * (LHS_diff + RHS_diff)
        
        if constantAdvection:
            A_x = self.advectiveOperator_x
            A_y = self.advectiveOperator_y
            
            LHS_adv = np.matmul(A_x, self.u_old)
            RHS_adv = np.matmul(self.u_old, A_y)
            
            self.u_new -= self.dt * (LHS_adv + RHS_adv)

        if VFAdvection:
            A_x = self.advectiveOperatorVF_x
            A_y = self.advectiveOperatorVF_y
                        
            LHS_adv_VF = np.matmul(A_x, np.multiply(self.vectorfield_x, self.u_old))
            RHS_adv_VF = np.matmul(np.multiply(self.vectorfield_y, self.u_old), A_y)
            
            self.u_new -= self.dt * (LHS_adv_VF+RHS_adv_VF)
        
        #Absorbing boundaries:
        self.overflow_top += np.sum(self.u_new[-1, :])
        self.overflow_bottom += np.sum(self.u_new[0, :])
        
        #Remove value at the overflow boundary
        self.u_new[0, :] = 0
        self.u_new[-1, :] = 0
        
        self.u_old = self.u_new
        
    def getMatrix(self):
        return self.u_old
    
    def itc(self, j, i):
        '''Index (j,i) to coordinate (x,y)'''
        # For future hazel: This needs to be backwards! It is the correct way around like this!!! i and j are correct!
        x = min(self.x_carthesian_range)+i*self.x_stepsize
        y = min(self.y_carthesian_range)+j*self.y_stepsize
        return (x,y)
    
    def cti(self, x, y):
        '''Coordinate (x,y) to index (j, i)'''
        # For future hazel: This needs to be backwards! It is the correct way around like this!!! i and j are correct!
        i = int(np.searchsorted(self.x_s, x))
        j = int(np.searchsorted(self.y_s, y))
        return (j, i)
        
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
        