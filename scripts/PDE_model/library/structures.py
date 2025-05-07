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
        
        self.neighbours = []
        self.flux_sum = 0.0
        
        self.volume = x_stepsize * y_stepsize
        
        #Parameters for the tutel sim :D
        self.swimspeed_s = 0.72
        self.kappa = 1
        self.swimdirection_V = np.array([0, -1])
        self.D = 1
        pass
    
    def setValue(self, value):
        '''For initial conditions or flux flow-in.'''
        self.u_old = value
        
    def compute_advective_flux(self, edges):
        for neighbour in self.neighbours:
            edge = Edge(self, neighbour)
            flux_advection = np.dot(edge.normal, self.swimspeed_s * (kn(1, self.kappa)/kn(0, self.kappa)) * self.swimdirection_V + edge.vectorFieldDirection) * (neighbour.u_old - self.u_old)
            #This flux is positive from 1->2. So 1 loses this amount, 2 will gain it when simulation comes.
            self.flux_sum -= flux_advection
            
    def compute_diffusive_flux(self):
        '''Computes the diffusion flux for the node, based on the surrounding neighbours'''
        for neighbour in self.neighbours:
            # Compute the gradient of u between this node and its neighbour
            grad_u = (neighbour.u_old - self.u_old) / np.linalg.norm(neighbour.position - self.position)
            
            # Compute the diffusion flux: F_diff = -D * grad(u)
            flux_diffusion = self.D * grad_u
            
            # Add the diffusion flux contribution to the flux sums
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
    def __init__(self):
        self.nodes = []
        self.x_num = 0
        self.y_num = 0
        self.edges = []
        self.node_grid = {}  # Dictionary to access nodes by (i, j)

    def compute_fluxes(self):
        for node in self.nodes:
            node.compute_advective_flux(self.edges)
            node.compute_diffusive_flux()
            
    def update_nodes(self, dt):
        for node in self.nodes:
            node.u_new=node.u_old + dt * (node.flux_sum / node.volume)
            node.flux_sum = 0.0
    
    def swap_fields(self):
        for node in self.nodes:
            node.u_old = node.u_new
            
    def make_grid(self, x_length, y_length, dx, dy):
        nx = int(x_length / dx)
        ny = int(y_length / dy)
        self.x_num = nx
        self.y_num = ny

        # Create nodes
        for i in range(nx):
            for j in range(ny):
                x = i * dx + dx / 2
                y = j * dy + dy / 2
                node = Node(i, j, x, y, dx, dy)
                self.nodes.append(node)
                self.node_grid[(i, j)] = node

        # Create edges (bidirectional)
        for i in range(nx):
            for j in range(ny):
                node = self.node_grid[(i, j)]

                # Right neighbor
                if i + 1 < nx:
                    neighbor = self.node_grid[(i + 1, j)]
                    self.add_bidirectional_edge(node, neighbor)

                # Top neighbor
                if j + 1 < ny:
                    neighbor = self.node_grid[(i, j + 1)]
                    self.add_bidirectional_edge(node, neighbor)

    def add_bidirectional_edge(self, node_a, node_b):
        edge_ab = Edge(node_a, node_b)
        edge_ba = Edge(node_b, node_a)
        self.edges.append(edge_ab)
        self.edges.append(edge_ba)

        # Optional: add neighbors for node-based flux computations
        node_a.neighbours.append(node_b)
        node_b.neighbours.append(node_a)

    def add_bidirectional_edge(self, node_a, node_b):
        edge_ab = Edge(node_a, node_b)
        edge_ba = Edge(node_b, node_a)
        self.edges.append(edge_ab)
        self.edges.append(edge_ba)

        # Optional: add neighbors for node-based flux computations
        node_a.neighbours.append(node_b)
        node_b.neighbours.append(node_a)
        
    def make_plottable(self):
        print(self.x_num, self.y_num)
        array = np.zeros([self.x_num, self.y_num])
        for i in range(self.x_num):
            for j in range(self.y_num):
                array[i,j] = self.node_grid[(i, j)].u_old
        
        return array
        
    