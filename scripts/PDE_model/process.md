What's that, a new process file?!?

I thought itd be clearer to separate PDE from discrete for these. So here we are.

# 07-05
FOR VIKTORIA: Started implementing a PDE solver. 

Today I started making a PDE solver. I am trying around stuff with how to go from the finite volume approach to a working computer simulation. I have settled on a graph model, where the nodes are the volumes, and the edges are the boundaries. I first approached this from an edge-first simulation, but am now going to do the following:
for each node, make it clear what its neighbours are: ordered [lrud]. When simulation comes, only affect self in the simulation to avoid double flow. This will slow down sim, but I don't see a better way to do it yet. It should be parallelizable, so that's neat.

# 08-05

Today I want to solve some issues with the PDE solver. Firstly, the advective term appears to be admitting negative values to the solution. This is probably because the flux is not preserved. I will figure out why this is the case.

Has the flux issue been solved? Maybe. I have implemented a system to make the density u be nonnegative, by enforcing mass preservation. But its stability heavily depends on the time scale, and I am worried about how to reconcile time scale with spatial scale. I am also worried about the unit of the time scale. Some of my values so far have been in /day, which means 1 time would correspond to 1 day. At these resolutions, I can't seem to find a balance between performance and stability. Maybe I need to increase the order of my scheme to do this, but that would cost a lot of work.

Before I worry about all that, I am going to include the vector field into the calculation, so that I can see some actual flow behaviour occurring. 

# 10 May

Today I am going to rewrite the PDE model into matrix form. More of a 'write' instead of 'rewrite', as I am going to start from scratch. Today (saturday) I want to implement the 'basic' logic elements (so constant A and D), tomorrow I want to implement the non-constant vector field. Monday is for finishing up shit left to do. First I will get the diffusion working, then the advection. This is to verify the basic results using a pure diffusion equation first, which is simpler to check. Here goes then ._.
