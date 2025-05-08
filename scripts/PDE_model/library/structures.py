import numpy as np
from scipy.special import kn #Modified bessel function of order n


class Node:
    def __init__(self, x_idx, y_idx, x_centre, y_centre, x_stepsize, y_stepsize, value=0.0):
        self.u_old = value
        self.u_new = 0.0
        
        self.x_centre = x_centre
        self.y_centre = y_centre
        self.position = np.array([self.x_centre, self.y_centre])
        
        self.x_idx = x_idx
        self.y_idx = y_idx
        self.dx = x_stepsize
        self.dy = y_stepsize
        
        self.neighbours = [None, None, None, None]  # Order: [l, r, u, d]
        self.diagonalNeighbours = [None, None, None, None]  # Order: [NE, NW, SE, SW]
        self.flux_sum = 0.0
        
        self.volume = x_stepsize * y_stepsize
        
        #Parameters for the tutel sim :D
        self.swimtimePerDay = 2
        self.swimspeed_s = 0.72*self.swimtimePerDay #km/day
        self.kappa = 0.874
        self.swimdirection_V = np.array([0.307, -0.952])
        self.turningrate_mu = 50 #per day
        
        #Steps to construct D:
        D_leftside = 0.5*(1-kn(2, self.kappa)/kn(0, self.kappa))*np.array([[1, 0], [0, 1]])
        D_rightside = (kn(2, self.kappa)/kn(0, self.kappa)-(kn(1, self.kappa)/kn(0, self.kappa))**2)*np.array([[self.swimdirection_V[0]**2, self.swimdirection_V[0]*self.swimdirection_V[1]], [self.swimdirection_V[0]*self.swimdirection_V[1], self.swimdirection_V[1]**2]])
        
        #self.D = (self.swimspeed_s**2/self.turningrate_mu)*(D_leftside+D_rightside)
        self.D = 0.001 * np.eye(2)
    
    def addValue(self, value):
        '''For initial conditions or flux flow-in.'''
        self.u_old += value
        
    def compute_advective_flux(self, edges):
        for neighbour in self.neighbours:
            if neighbour is None: continue #Logic here for handling edge?
            
            edge = Edge(self, neighbour)
            
            # Comput effective advection velocity through the face
            face_velocity = self.swimspeed_s * (kn(1, self.kappa)/kn(0, self.kappa)) * self.swimdirection_V + edge.vectorFieldDirection
            
            normal_velocity = np.dot(edge.normal, face_velocity)
            
            if normal_velocity >= 0:
                upwind_value = self.u_old
            else:
                upwind_value = neighbour.u_old
            
            flux_advection = normal_velocity * upwind_value
            
            #subtract the flux leaving this node.
            self.flux_sum -= flux_advection
            
    def compute_diffusive_flux(self):
        '''Computes the diffusion flux for the node, based on the surrounding neighbours'''
        # Order of neighbours: lrud
        # Compute the gradient of u between this node and its neighbour
        grad_u_x = (self.neighbours[0].u_old - 2*self.u_old + self.neighbours[1].u_old) / (self.dx**2)
        grad_u_y = (self.neighbours[2].u_old - 2*self.u_old + self.neighbours[3].u_old) / (self.dy**2)
        
        d11 = self.D[0, 0]
        d12 = self.D[0, 1]
        d22 = self.D[1, 1]

        #Second-order differences for Laplacian terms
        d2u_dx2 = grad_u_x / (self.dx**2)
        d2u_dy2 = grad_u_y / (self.dy**2)
        
        NE = self.diagonalNeighbours[0]
        NW = self.diagonalNeighbours[1]
        SE = self.diagonalNeighbours[2]
        SW = self.diagonalNeighbours[3]

        if None not in [NE, NW, SE, SW]:
            d2u_dxdy = (NE.u_old - NW.u_old - SE.u_old + SW.u_old) / (4 * self.dx*self.dy)
        else:
            print("This happened!")
            d2u_dxdy = 0.0  # Fallback if any diagonals are missing
        
        
        # Full anisotropic diffusion operator
        flux_diffusion = 2 * d12 * d2u_dxdy + d11 * d2u_dx2 + d22 * d2u_dy2
        self.flux_sum += flux_diffusion

        
            
class Edge:
    '''An edge connects two nodes. It models the boundary BETWEEN these nodes. So the graphical representation will be CONFUSING! The graph edge would be drawn perpendicularly to the volume edge.'''
    def __init__(self, node1: Node, node2: Node, boundary_type=None):
        self.node1 = node1
        self.node2 = node2
        
        self.normal = self.calculateNormal() #The normal points along the graph edge!
        self.length = self.calculateLength()
        self.position = self.calculatePosition()
        
        self.boundary_type = boundary_type 
        self.vectorFieldDirection = np.array([0, 0]) #The local direction of the ocean stream flow field
        
    def calculateNormal(self):
        '''The normal, oriented from node1 to node2'''
        direction = self.node2.position-self.node1.position
        normal = direction / np.linalg.norm(direction)
        return normal
    
    def calculateLength(self):
        return np.linalg.norm(self.node2.position-self.node1.position)
    
    def calculatePosition(self):
        return 0.5*(self.node1.position+self.node2.position)
    
    def getVectorFieldDirection(self, vectorField):
        '''TODO: implement this'''
        
class Grid:
    def __init__(self, x_carthesian_range, y_carthesian_range):
        '''
        xy_carthesian_range are the range of coordinates. 
        The Grid class works with indices internally, but the user interface is with coordinates.
        '''
        
        self.nodes = []
        self.x_num = 0
        self.y_num = 0
        self.edges = []
        
        self.x_range_max = max(x_carthesian_range)
        self.x_range_min = min(x_carthesian_range)
        self.y_range_max = max(y_carthesian_range)
        self.y_range_min = min(y_carthesian_range)
        
        
        self.all_nodes = []  # Includes ghost nodes
        self.nodes = []      # Simulated (interior) nodes
        self.node_grid = {}

    def compute_fluxes(self, diffusive=True, advective=True):
        for node in self.nodes:
            if advective:
                node.compute_advective_flux(self.edges)
            if diffusive:
                node.compute_diffusive_flux()

    def update_nodes(self, dt):
        for node in self.nodes:
            node.u_new = node.u_old + dt * (node.flux_sum / node.volume)
            node.flux_sum = 0.0

    def swap_fields(self):
        for node in self.nodes:
            node.u_old = node.u_new
            
    def add_value(self, i, j, value):
        self.node_grid[(i, j)].addValue(value)
        
    def cti(self, x, y):
        '''carthesian to index'''
        dx = (self.x_range_max - self.x_range_min) / self.x_num
        dy = (self.y_range_max - self.y_range_min) / self.y_num
        
        i = int((x - self.x_range_min - dx / 2) / dx)
        j = int((y - self.y_range_min - dy / 2) / dy)

        return (i, j)

    
    def itc(self, i, j):
        '''index to carthesian'''
        dx = (self.x_range_max - self.x_range_min) / self.x_num
        dy = (self.y_range_max - self.y_range_min) / self.y_num
        
        x = self.x_range_min + i * dx + dx / 2
        y = self.y_range_min + j * dy + dy / 2
        
        return (x, y)

    
    def make_grid(self, dx, dy):
        nx = int((self.x_range_max - self.x_range_min) / dx)
        ny = int((self.y_range_max - self.y_range_min) / dy)
        
        self.x_num = nx
        self.y_num = ny

        # Expand bounds to include ghost nodes
        for i in range(-1, nx + 1):
            for j in range(-1, ny + 1):
                x = i * dx + dx / 2
                y = j * dy + dy / 2
                node = Node(i, j, x, y, dx, dy)
                self.all_nodes.append(node)
                self.node_grid[(i, j)] = node

                # Add only interior nodes to simulation
                if 0 <= i < nx and 0 <= j < ny:
                    self.nodes.append(node)


        # Now connect neighbors
        for i in range(-1, nx + 1):
            for j in range(-1, ny + 1):
                node = self.node_grid[(i, j)]

                # Initialize neighbor lists
                node.neighbours = [None, None, None, None]
                node.diagonalNeighbours = [None, None, None, None]

                # Direct neighbors [l, r, u, d]
                if (i - 1, j) in self.node_grid:
                    neighbor = self.node_grid[(i - 1, j)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.neighbours[0] = neighbor
                    neighbor.neighbours[1] = node
                    
                if (i + 1, j) in self.node_grid:
                    neighbor = self.node_grid[(i + 1, j)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.neighbours[1] = neighbor
                    neighbor.neighbours[0] = node

                if (i, j + 1) in self.node_grid:
                    neighbor = self.node_grid[(i, j + 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.neighbours[2] = neighbor
                    neighbor.neighbours[3] = node

                if (i, j - 1) in self.node_grid:
                    neighbor = self.node_grid[(i, j - 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.neighbours[3] = neighbor
                    neighbor.neighbours[2] = node

                
                if (i + 1, j - 1) in self.node_grid:
                    neighbor = self.node_grid[(i + 1, j - 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.diagonalNeighbours[2] = neighbor  # SE

                if (i - 1, j - 1) in self.node_grid:
                    neighbor = self.node_grid[(i - 1, j - 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.diagonalNeighbours[3] = neighbor  # SW

                if (i + 1, j + 1) in self.node_grid:
                    neighbor = self.node_grid[(i + 1, j + 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.diagonalNeighbours[0] = neighbor  # NE

                if (i - 1, j + 1) in self.node_grid:
                    neighbor = self.node_grid[(i - 1, j + 1)]
                    self.add_bidirectional_edge(node, neighbor)
                    node.diagonalNeighbours[1] = neighbor  # NW
                    

    def add_bidirectional_edge(self, node_a, node_b):
        edge_ab = Edge(node_a, node_b)
        edge_ba = Edge(node_b, node_a)
        self.edges.append(edge_ab)
        self.edges.append(edge_ba)
        
    def make_plottable(self):
        array = np.zeros([self.x_num, self.y_num])
        for i in range(self.x_num):
            for j in range(self.y_num):
                array[i,j] = self.node_grid[(i, j)].u_old
        
        return array
        
    