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

End of day: I have implemented the diffusion successfully. I have skipped the diagonal terms for now, but they might go unused anyway, so why bother. The advection seems to work somewhat, but when I turn the arguments negative, I see weird stuff in the wrong direction. This is proabbly some flaw in my logic which I'm going to fix tomorrow / later tonight

# 11 May

Today, its time to get advection working. It (seems to) work, but only when the coefficients in A are positive. When negative, the advection still goes in the positive direction, and starts to checkerboard really hard.

The first fix I want to do, is to make the constant advection working. To do this, I am going to use a first-order upwind scheme.
The advection now seems to work. It still needs to have the boundary conditions added, and I am doubting the way I approach the creation of A itself right now. Especially because I would like my grid to be rectangular, but with square volumes (they are now rectangular to make the grid square). For this change, my matrices need to be NxM, whereas they are all NxN right now. It should luckily not be a too huge change.

TODO For today:
 - Allow a square grid
 - Introduce advective BC's
 - Introduce the dependence on the vectorfield.

So far, I have mostly fought and fought with indices. My carthesian is (lon, lat) or (x, y). But numpy VERY ANNOYINGLY (i am genuinely extremely upset right now) uses [j, i], if i<->x and j<->y. This has caused numerous errors because there is not one central place to handle this discrepancy, so I am in a sort of loop trying to find the bug and fixing it at one place, breaking it at the other. I am so done.

I seem to have gotten the cti and itc stuff sort of working for grids where dx=/=dy, but with a caveat. Sometimes it just spits back an index out of bounds error, but only for specific values. This happens for example for 0.01, but not for 0.1 nor 0.03. So just, wiggle the dx and dy around until it stops complaining?

I am now working on getting the advection working again, because it of course broke in the process.

Advection appears to be working, but the directionality broke (it now just always points down-right, for some reason)

# 12 may

Today I have spent most of my day writing parts of text in the Overleaf. I have also spent part of the morning fixing up my advection code. I have run through the math of forward differences again, as it was a MESS. It is currently 11:24PM and by god will I not sleep before I have advection working in every direction. Currently the advection only works when the scalars are positive, and I know why this is and how to fix. When it becomes negative, I need to compensate for that by changing my differentiation scheme. This is to ensure that I am doing my advection in the direction of the flow. If I don't do this, I do not get a numerically stable scheme.

I did not expect to be done after 9 minutes, but it works now. I suppose I will spend some extra time on boundary conditions now.

# 13 may

Today I should start with boundary conditions, but I want to start with the non constant advection math. This I will do on paper, so just a moment while I do that :D

I have reached a conclusion about how to determine the flux from the field. LUCKILY it is still matrix calculations, just with a flux modification determined by the flow field. Letting a_x and a_y denote the components of the vectorfield so that A(x,t)=(a_x(x,t), a_y(x,t)) then we can rewrite u_t=div(Au) as 
u_t = del_x (a_x * u) + del_y (a_y * u)
Where a_x * u is elementwise multiplication, as a_x acts as scalars for each element of u. Then we apply the del_X and del_y operators in the same way as in the constant vector field.

The hard part then is getting the data into python. For this I want to use the follow 'process' (pipeline?):
- Get data once per simstep (This is not once per timestep, the timestep is smaller than simstep for resolution purposes)
- Use scipy to linearly interpolate this data, so that it is transformed from the gridpoints HYCOM uses to the gridpoints my density function uses.  (Once per simstep)
- Use this data for every timestep in a simstep. 
- Repeat

The first two of these steps will be wrapped in the grid.getVectorField function, which sets scipy linearInterpolate functions mapping (x,y) (or i,j?)->water_u or water_v, respectively. These are then applied inside grid.getVectorField to get two grids self.water_u and self.water_v which are on the exact same grid as self.u_old. 

# Meeting 13-05
After the meeting, I have the following points:
 - 'Ignore' the mass that leaves the area, or at least don't set it to zero. Add the mass which leaves to a counter. 
 - To determine which numerical integration method to use in different places of the matrix: np.where to determine whether to use forward/backward difference. Filter matrix on in this way.
 - Mark parts of the overleaf text for Viktoria to judge.

I will start with the np.where thing, as I really appreaciate the way it solves my previous problem of handling my numerical scheme: originally, if the flow direction was negative, I would change the scheme to account for the reversed direction of flow, but now I will just apply both schemes, but only to the parts where the flow is positive resp. negative. To start the implementation, I want to rewrite the constant advection to not use conditionals: 










