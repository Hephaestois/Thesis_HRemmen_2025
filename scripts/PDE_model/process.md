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

I will start with the np.where thing, as I really appreaciate the way it solves my previous problem of handling my numerical scheme: originally, if the flow direction was negative, I would change the scheme to account for the reversed direction of flow, but now I will just apply both schemes, but only to the parts where the flow is positive resp. negative. 

Hazel from the past future, now the now: The change has been successful. I was hanting a bug at some point which was just me not removing old code, so some simulation part was running twice. That is now fixed, and the changes have been implemented. I think it is possible to add the constant and nonconstant parts together, but I will wait with doing that until I have gotten the nonconstant VF into the simulation. For now, the resolutions seem to scale in a feasible manner: using grid sizes of 0.012 degrees (so 10x higher resolution than the flow data, coming in at 1.2km per stepsize) and dt of 0.01, a period of 14.4 minutes, simulating a full day takes 13 seconds. This means that at this scale, simulating the entire suite will take 3900 seconds or 1 hour and 15 minutes. Reducing the resolution can drastically increase this, but the download time for data is also a factor to consider. 

# 14 May
Today I _wanted_ to work on my overleaf, but the gods have willed an outage to strike, hence I must work on the code I was avoiding to work on. Therefor, I will implement the time-changing vector field today. First I will just get one vectorfield working, as I should be able to compare with another simulation I ran, and then I will get the time-changing in.

# 16 May
Yesterday was a very slow day for myself. I have done some work then, but haven't written it down. It was mostly in the overleaf, but doesn't deserve mention.

Today I have had a realization: Instead of calclulating a function that interpolates a on a grid, and to then sample that on my function u, I can also approach this the other way around. I am okay with a less efficient function here, so I am going to do the following steps:
 - Extract the coordinate of a gridpoint in u
 - Find the index of this coordinate in the dataset
 - Find the value at this index in the dataset
 - Assign it to the coordinate of the gridpoint
 - Rinse and repeat in for loops.
Doing this, I am 'skipping' issues with dimensionality and such: all my values are fetched at once.
I am not anymore interpolating with this, but because my integrating a random VF has shown the method to be quite robust, I am not affraid of instability. I have increased the random field strength to [-25, 25]. This did not cause issues with stability if dt was changed appropriately. Considering the values in the dataset fall roughly within this range, I am satisfied to just go with no interpolation.

I think the vectorfield is working correctly. I want to verify by plotting the VF using plt.quiver. So I am going to do that.
Judging by the PLT quiver, I can now surely say that the VF is working correctly. The changing vectorfield is of course harder to plot, so for that I just use the most recent vector field we encountered.

# 17 may
Did some writing work in Overleaf, code was mostly idle today.

# 18 May
Today I want to fix two issues I know exist. One is the scale-relevance on the density. Changing the space-step (also a problem which I have now fixed) to a larger or smaller step changed the solution more than is justifyable with resolution arguments. Therefor, there must be an influence of space-step on solution which is obviously wrong. I think this happens because I have rescaled the flow field units to meter per day, but I want to try to set this to be x_stepsize degrees / t_stepsize days 

# 19 May

HUGE RESULTS
I have calibrated A, figured out its units are degrees per day, and thus made the daily swim distance to be equal to 2km/day as in Painter and Hillen. Using this I have calibrated the strength of the flow field by converting m/s to degrees per day. I changed my simulation to run on the data from 2016. Now I have gotten very convincing results extremely similar to Painter and Hillen. GREAT SUCCESS!!!

To accomodate for simulating more recent years, I have created 'FVM2016.py' in the directory 'years'. This is because the datasets have different lengths, and the logic of switching between them would be too spaghetti to do in general, so I will do it specifically for each dataset. 

This means that either the plots don't get a vector field overlaid, or plotting is separated but is dependent on the vector fields which would be a lot of work. In any case I will save the datasets, so that plots without a vecctorfield can always be reproduced.

I am currently running a simulation at the 0.04x0.04x0.001 scale. This is quite slow, but most of that time is taken up by datasets being sent around. I should _probably_ look into faster dataset acquisition. Downloading them locally might be the solution after all?

# 20 may

(written on 19 may, for future hazel)
To make the vectorfield-swapping functional, I need to provide the program with the multiple URLs the data is being acquired from, and switch them when 'time runs out'. The time variable still needs to remain within the permissible steps on which the data is defined. This means that I will need a pretty bulky amount of logic, which I mmight wrap in a separate function if it is not too outlandishly complicated.

# 21 may

I have gotten the Discrete model working. Tonight I want to get some tools ready to make figures and such for the presentation I need to hold tomorrow. This means I need to create video plotting programs, preferably for both the PDE and discrete models, but as a start the PDE model should be animated.
To achieve this, first the method of saving data for the PDE model should be adapted: currently only the 'last timestep' is saved. I will not be saving each intermediate, but at least the days would be worthwhile to save. So first: revamp the method of saving.




# List of attendees/invites for the final presentation: (who still need to know a location)

Vader & Moeder
Frey
Sol & Yoshi van der Eng (TBD)
Familie & familie van Frey (TBD who exactly)
Sam Mooney & Anne Mooney (TBD)
Taico Aerts
Uni vrienden & Middelbare school vrienden (TBD who exactly)

Supervisors: Havva & Jeroen

