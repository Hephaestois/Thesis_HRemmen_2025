Hello Viktoria! :)

# This file is meant as a log!
To be specific, this file is meant to serve the purpose of me not forgetting what steps I took to arrive at the model I want, so that later I can write about it in chronological-ish order. At least, in an order that preserves the initial streams of thinking I 'used' to achieve my results.

I will therefor add dates as 'waypoints', and also to give a clear separation of time. This will not be readable like a book, I will have to re-format this later into the actual overleaf text. 

# April 23-04
FOR VIKTORIA: Found sources, started vectorfield implementation.

In the meeting today, we discussed which direction to take the project: I have suggested continuing the turtles-thing from Painter, Hillen. Topgether we arrived to 1. a more overseeable scope and 2. a semi-detailed timeline. To reiterate, the timeline is going to be roughly: 
- implement FAAD
- implement the RW with non-constant a and D
- implement the RW in a vector field (with ocean data?)
- implement FAAD in a vector field
- find some analytical solutions to FAAD (and maybe some non'trivial' ones)
- implement RW in a time-dependent vector field
- implement 

The first dataset I want to get, I want
With range: 2018-01-01 -- 2018-01-04,
Lat(y)-Lon(x): 42-47 N, 331-349 E (as in KJP, approximately) (or -29 to -11 E)

After 3 failed attempts,
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_7e38_7a7b_afe2.html
WORKS!!!! (omg)

I have opted to download as CVS. The specified 42 to 47, -29 to -11, with 'degree stepsize' 0.0523, 0.080 consists of 45MB data per day (with just one measurement per day!!). Therefor, I am going to fetch a new dataset, consisting of just one day, but with degree-multiples of 5 (so delta=0.26) for the latitude, and multiples of 6 for the longitude (so delta=0.48). This difference in delta is due to the length of the interval. I am going to interpolate linearly later anyway, so so long as the 'resolution' of the vector field is reasonable, going more precise shouldn't change a lot.

New dataset (clicking starts a download, 69kb):
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_7e38_7a7b_afe2.csv?water_u[(2014-01-01):1:(2014-01-01)][(0.0):1:(0)][(42):5:(47)][(-29):6:(-11)],water_v[(2014-01-01):1:(2014-01-01)][(0.0):1:(0)][(42):5:(47)][(-29):6:(-11)]
This is one day of time, with two depth-scales (0 and 2 meter, my bad). 

Now I just need to implement an actor in a vector field 1. reacting to the vector field and 2. acting in the vector field.

Started trying to interpolate the vectorfield. I dont know yet how to make this vector into a probability, but I'll have the data to do so ready when I do know how to.

# April 24-04
FOR VIKTORIA: play around with RRWinVF. Don't go too crazy with the N_swims and swim_length, maybe keep their product under 50.000, execution time ~1minute?. (Repeated Random walk in Vector Field)

Today I managed to implement the turtle floating in a vectorfield. I have not used interpolation, but instead just assume the value of the closest gridpoint that has a vector value. For a fine enough grid, this should be doable. It is not possible to precompute these values due to vectorfield being a dataframe, but the speedup probably wouldn't be huge. Performance gains can be had here, though.

The implementation works as follows: Put a turtle in a stream, make sure you DO NOT GET LAT/LON MIXED UP (lon corr. to x, lat to y). Then using numpy find the closest gridpoint to a location. Now assign probabilities to moving lrud so that they sum to one and point in the direction of the vector field.

This is of course not taking into account the swimming behaviour of the turtles. I have considered this to be postponed right now, but it should be not a lot harder than just choosing two weights and modifying their behaviour by those weights. I am now going to turn my attention towards the repeated swim simulation of the turtles, to see a density arise.

I have implemented the repeated 'float', a RW with only vector field influence.
I have now also implemented the repeated 'swim', a RW with influence from the turtles and the field. To combine the influence from the turtles and the field, I have created weights to average the static and dynamic probabilities of movement.

I think I will now (have to) start to approach the PDE based solution. Because I am not looking very forward to doing this (how tf do I incorporate the vector field into FEniCS?!?), I will instead start with expanding the text in the overleaf. Maybe later today I will also try to implement the time-varying vector field, but I don't think its feasible to acquire my data on this wifi network. Or I will do some by-hand math on existence and stuff that into the overleaf. Yay.

I would also like to try to optimize the simulation of the turtles. Currently the program is using just one thread, but it would be ideal if each turtle could be simulated by one thread, to a total of 16 threads on my laptop and home computer tower. Later this could be increased to allow supercomputing??! :D
 


