What's that, a new process file?!?

I thought itd be clearer to separate PDE from discrete for these. So here we are.

# 07-05
FOR VIKTORIA: Started implementing a PDE solver. 

Today I started making a PDE solver. I am trying around stuff with how to go from the finite volume approach to a working computer simulation. I have settled on a graph model, where the nodes are the volumes, and the edges are the boundaries. I first approached this from an edge-first simulation, but am now going to do the following:
for each node, make it clear what its neighbours are: ordered [lrud]. When simulation comes, only affect self in the simulation to avoid double flow. This will slow down sim, but I don't see a better way to do it yet. It should be parallelizable, so that's neat.

