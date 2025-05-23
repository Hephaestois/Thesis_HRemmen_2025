import numpy as np
from scipy.special import kn #Modified bessel function of order n
from scipy.interpolate import RegularGridInterpolator
import netCDF4
import math

class Grid:
    def __init__(self, x_carthesian_range, y_carthesian_range, x_stepsize, y_stepsize):
        self.x_carthesian_range = x_carthesian_range
        self.y_carthesian_range = y_carthesian_range
        self.x_stepsize = x_stepsize
        self.y_stepsize = y_stepsize
        self.x_s = np.arange(min(x_carthesian_range), max(x_carthesian_range), self.x_stepsize) # ? max(x_carthesian_range), int(round((max(x_carthesian_range) - min(x_carthesian_range)) / self.x_stepsize)) + 1
        self.y_s = np.arange(min(y_carthesian_range), max(y_carthesian_range), self.y_stepsize) #   max(y_carthesian_range), int(round((max(y_carthesian_range) - min(y_carthesian_range)) / self.y_stepsize)) + 1
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
        self.advectiveOperatorVF_x = np.zeros((self.x_num, self.y_num))
        self.advectiveOperatorVF_y = np.zeros((self.x_num, self.y_num))
        self.advectiveUpwindOperator_x = np.zeros((self.x_num, self.y_num))
        self.advectiveDownwindOperator_x = np.zeros((self.x_num, self.y_num))
        self.advectiveUpwindOperator_y = np.zeros((self.x_num, self.y_num))
        self.advectiveDownwindOperator_y = np.zeros((self.x_num, self.y_num))
        
        # For absorbing boundaries
        self.overflow_top = 0
        self.overflow_bottom = 0
        
        self.dt = 0
    
    def setDiffusionConstants(self, D):
        self.diffusionConstants = D
        
    def setAdvectionConstant(self, A):
        # Change is necessary to make format readable for humans: necessity comes from difference between (x,y) and  (i,j) in matrix form!
        self.advectionConstants = np.array([-A[0],A[1]])
    
    def setValue(self, pos, value):
        self.u_old[pos] = value/(self.x_stepsize*self.y_stepsize)
    
    def addValue(self, pos, value):
        self.u_old[pos] += value/(self.x_stepsize*self.y_stepsize)
    
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
        N_x, N_y = self.x_num, self.y_num #These are intentionally swapped! Due to the side of u on which the operator needs to be applied. This is correct, don't worry about it Hazel

        # 1D advection operator: backward- or forward difference depending on the sign.
        def advection_operator(N, advectionDirection):
            A = np.zeros((N,N))
            #advectiondirection >0: upwind, <0: downwind
            if advectionDirection >= 0:
                np.fill_diagonal(A, 1)
                np.fill_diagonal(A[1:], -1) #below diagonal
            else:
                np.fill_diagonal(A, -1)
                np.fill_diagonal(A[:, 1:], 1) #above diagonal
            
            return A
        
        self.advectiveUpwindOperator_x = advection_operator(N_x, 1) / self.x_stepsize  # operates on x (columns)
        self.advectiveDownwindOperator_x = advection_operator(N_x, -1) / self.x_stepsize
        self.advectiveUpwindOperator_y = advection_operator(N_y, 1) / self.y_stepsize
        self.advectiveDownwindOperator_y = advection_operator(N_y, -1) / self.y_stepsize
    
    def setLonLatVals(self, dataset, lons_idx, lats_idx):
        self.lon_vals = dataset.variables['lon'][lons_idx]
        self.lat_vals = dataset.variables['lat'][lats_idx]
    
    def getVectorField(self, dataset, lons_idx, lats_idx, timeIndex):
        u_data = dataset.variables['water_u'][timeIndex, 0, lats_idx, lons_idx]
        v_data = dataset.variables['water_v'][timeIndex, 0, lats_idx, lons_idx]

        
        self.vectorfield_x = np.zeros((self.y_num, self.x_num))
        self.vectorfield_y = np.zeros((self.y_num, self.x_num))
        
        for i in range(self.x_num):
            for j in range(self.y_num):
                pos_x, pos_y = self.itc(j, i)
                idx_data_lon = np.clip(np.searchsorted(self.lon_vals, pos_x), 0, len(self.lon_vals)-1)
                idx_data_lat = np.clip(np.searchsorted(self.lat_vals, pos_y), 0, len(self.lat_vals)-1)
                x_val = u_data[idx_data_lat, idx_data_lon]
                y_val = v_data[idx_data_lat, idx_data_lon]
                
                if x_val==-30000 or y_val==-30000:
                    print('misread')
                # Convert from mm/s to m/day
                # These constants are debatable, and so they will be!
                self.vectorfield_x[j, i] = 0.864*x_val
                self.vectorfield_y[j, i] = 0.864*y_val

        return self.vectorfield_x, self.vectorfield_y
        
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
            A_x_up = self.advectiveUpwindOperator_x
            A_x_down = self.advectiveDownwindOperator_x
            A_y_up = self.advectiveUpwindOperator_y
            A_y_down = self.advectiveDownwindOperator_y
            
            # The elementwise product of A*u, to use in np.where. 
            # Here A is just the advection constants, in VF, it would be vectorfield_x with np.multiply
            au_x = self.advectionConstants[0]*self.u_old
            au_y = self.advectionConstants[1]*self.u_old
            
            LHS_1_adv = np.matmul(np.where(au_x>=0, au_x, 0), A_x_up)
            LHS_2_adv = np.matmul(np.where(au_x<0, au_x, 0), A_x_down)
            RHS_1_adv = np.matmul(A_y_up, np.where(au_y>=0, au_y, 0))
            RHS_2_adv = np.matmul(A_y_down, np.where(au_y<0, au_y, 0))
            
            self.u_new -= self.dt * (LHS_1_adv + LHS_2_adv + RHS_1_adv + RHS_2_adv)
        
        if VFAdvection:
            A_x_up = self.advectiveUpwindOperator_x
            A_x_down = self.advectiveDownwindOperator_x
            A_y_up = self.advectiveUpwindOperator_y
            A_y_down = self.advectiveDownwindOperator_y
            
            # The order of the vectorfields here is INTENTIONALLY weird to permit the function setVectorField to work intuitively along correct axes: numpy axis bs. 
            # Direction should be verified, but the plt.quiver (VF plot) looks fine.
            au_x = np.multiply(-self.vectorfield_x, self.u_old)
            au_y = np.multiply(self.vectorfield_y, self.u_old)
            
            LHS_1_adv = np.matmul(np.where(au_x>=0, au_x, 0), A_x_up)
            LHS_2_adv = np.matmul(np.where(au_x<0, au_x, 0), A_x_down)
            RHS_1_adv = np.matmul(A_y_up, np.where(au_y>=0, au_y, 0))
            RHS_2_adv = np.matmul(A_y_down, np.where(au_y<0, au_y, 0))
            
            self.u_new -= self.dt * (LHS_1_adv + LHS_2_adv + RHS_1_adv + RHS_2_adv)
            
        #Absorbing boundaries:
        self.overflow_top += np.sum(self.u_new[-1, :])
        self.overflow_bottom += np.sum(self.u_new[0, :])
        
        #Remove value at the overflow boundary
        # self.u_new[0, :] = 0
        # self.u_new[-1, :] = 0
        
        self.u_old = self.u_new
        
    def getMatrix(self):
        return self.u_old * self.x_stepsize * self.y_stepsize
    
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
        return np.sum(self.u_old) * self.x_stepsize * self.y_stepsize
    
    def getOverflowBottom(self):
        return self.overflow_bottom * self.x_stepsize * self.y_stepsize
    
    def getOverflowRatio(self):
        '''Ratio between bottom overflow and total overflow'''
        try:
            return self.overflow_bottom / (self.overflow_bottom+self.overflow_top) * self.x_stepsize * self.y_stepsize
        except:
            return None
        
    def getOverflowTop(self):
        return self.overflow_top * self.x_stepsize * self.y_stepsize
    
    def getOverflow(self):
        return (self.overflow_bottom + self.overflow_top) * self.x_stepsize * self.y_stepsize
        
    def ic(self, type, v):
        if type=='gauss':
            A = v
            x0 = (-25)
            y0 = (44.5)
            sigma_x = 1
            sigma_y = 1

            for i in self.x_idxs:
                for j in self.y_idxs:
                    x,y = self.itc(j, i)
                    value = A * math.exp(-((x - x0)**2) / (2 * sigma_x**2) - ((y - y0)**2) / (2 * sigma_y**2))
                    self.addValue(self.cti(*self.itc(j, i)), value)

            
        if type=='delta':
            self.addValue(self.cti(-25, 44.5), v)
            