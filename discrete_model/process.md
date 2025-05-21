(Opening brackets so that I can use smileys without them being marked invalid: ((((((()


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
 
Options to approach in work right now:
- Document developing the model
- Implement time-dependence
- Do hand-derivation for specific model
- Multithread my process 

# April 25-04 
FOR VIKTORIA: Found a better data source, managed to access it, and made some plots to show it seems correct.

I found a better place to get my data from. 
(Specific website): https://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3.html
(General collection of data): https://tds.hycom.org/thredds/catalog.html

To get the data for the entire year 2015, I am using the following:
https://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_56.3?lat[2050:1:2175],lon[1885:1:2111],time[1452:4:4388],water_u[1452:4:4388][0:1:0][2050:1:2175][1885:1:2111],water_v[1452:4:4388][0:1:0][2050:1:2175][1885:1:2111]
I should note! The time misses a few moments. because it is sampled on 3-hour intervals, this means that specifying 8x3 hour jumps sometimes results in 27-hour days. To omit this issue, I have specified 4x3 hour jumps in the time, so that I can sample, for each moment of 24 hours, the most recent datapoint in the past 24 hours. This is generally going to be unique, and as these are ocean streams, I find that good enough.

The format of the data calls for some functions to preprocess it. I think I will write these today. I wanted to adapt the vectorfield to not be a dataframe anyway, so that I have the option to vectorize some operations. I also think I want to preprocess the possible distances between points. This is to say, for determining which vector to take influence from, I am currently just using a distance calculation based on euclidian distance, for the location of the swimmer to every single datapoint. This was due to format restrictions, and being lazy. The format of the new data would hopefully allow for a more efficient approach, where I slice the dataset based on the location of the swimmen, turning an O(n^2) into a O(n log n) operation with a little luck

My download of the data from the above mentioned source has finished. I intend first to get the data into python (the extension is .dods... what does this mean? How do I use it?), then to make the PLT quiver of one day, and then to make a PLT animation (gif) of each successive day. To get a feel for how the vector field changes, and to see if the stream is comparable to the one in KJP for +100 days, +200 days, +300 days.

The data I acquired is the ocean stream data, dates 01-01-2015 - 01-01-2016, 42-47N (0.04), -29--11E (0.08), in 12 hour intervals. The total data volume appears to be about 160MB. To read this data, I am installing pydap (as per google search).
Time to make a new python file, plotVF.

To access the data, I am using netCDF4. Using pydap (my first attempt) had an issue where it would just change the link. So now netCDF4 is the solution. I am a little affraid of data traffic speed, but I suppose I'll find out.

The data has been accessed. I have created a beautiful video ocean_currents_animation.mp4. It shows the ocean currents starting from 01-01-2014 for 60*3 hours, for a total of 7.5 days. I have also created an image of the vectorfield comparable to KJP, at 01-01-2014+200 days, which is at time-index 146 or time value 127536 (hours from 01-01-2001). These look comparable, so I am going forward with the trust that my method of acquiring a vector field is at least somewhat correct. 

## Making the random walk in a vector field (that is NOT time constant)

FOR VIKTORIA: I have implemented the time-dependent RW.

The dataset I acquired starts on 01-Jul-2014, which has time value 127092. To make a random walk in a non-constant vector field, I need to start at this time, and then increment by 24 hours when the conditions to do this are met. Because I am doing a Position jump-process, I should probably not increase the time-step every simulation-step. I will include a variable to account for this, probably dependent on the turtles step size. For now, I will just let this variable default to one. 

Another issue is that not every datapoint in the dataset is accounted for. They didn't do NaN, meaning that the 'timeline' is not pretty. That is to say, importing all the time values in the dataset results, not all intervals between datapoints are 3 hours! This is a problem, as I want to do a simulation step every 24, and thus can not just count 8 indices.
To alleviate this issue, I am going to count the hours since start (with integer 24-amounts). Then, if it turns out that this multiple of 24 is not in the dataset, I will use the most recent 3-hour multiple that _is_ in the dataset. Doing this, I still have control over the 'flow' of time in my simulation. I hope that the effect of 3 hours is not too severe (allthough maybe the tide makes it so that I should just use the previous days' stream), but it is worth it to investigate the effect of a different choice for this. Damn incomplete datasets!

Because I foresee that downloading data is a significant bottleneck in my project, I am goign to also approach simulating the turtles differently. Previously, there used to be one turtle that would do a walk in a constant vector field. This was fine, because there was no functional difference between having one turtle do 600 walks, or 600 turtles doing one walk. Now, however, if I have one turtle doing 600 walks, I need to cycle through the time range 600 times, whereas if 600 turtles do one walk step by step, I need only cycle through the range 1 time. So this 'reversed' approach is how I will implement the new functions, handling a time-non-constant field.

## May 2nd

Today I want to implement the 'feature' in Painter where the turtles travel 2km per day. This might be a bit of a doozy because of how coordinates work. This is because at 0*North (the equator), the horizontal displacement is further apart than the vertical displacement.
I am going to make a copy of RWinVF, named RWinVF2km. Here, the turtles make steps (influence from both swimming and stream) until they move 2km.

Status update: I just woke from my programmer trance. I see data registers in my cpu itself. 
Anyway, I have implemented a number of features:
    - the probability of moving in a direction now depends on the intensity of the flow of the vector field (so no more weights for the tutels)
    - I have added some 'advanced' tools to make videos, so now the RWinVF2km, which is the new iteration of RWinVF, can make very nice figures
    - I created a progress bar (I was going insane over printing indices), and gave it a time elapsed and time left thing
    - I tried to get the dataset offline for faster runtime (I think it is mostly time limited rn), but failed
    - I made it so that turtles are released 'dayly' as in Painter
    - I made it so that turtles take steps 5 steps every day. I want to extend this to be 'steps until 2km' as in Painter, but this would mean converting angles lon,lat to distances, which is nontrivial.
    - I have tried to optimize the working of some functions. Some stuff is VERY slow right now, and I have some hitches as to why, but some solutions would take a long time to fix. Maybe even longer than it would yield in time I can spend thinking about other stuff. 

## May 4th

FOR VIKTORIA: Mostly refactored code, cleaned up old garbage and made sure stuff works as intended and is scientific accordance. Fixed a huge error regarding probability in the code.


Ereyesterday I implemented a few features that have to do with plotting, and thing I broke something at the end. So my plots had me believe, anyway (What I saw what the turtles all using the same probability and sampling points in the vector field to decide what to do). Today, after correcting a missing absolute value sign, I ran the thing again to check for anomalies, and it seems to have been fixed.

To be certain everything I do is according to the paper by Painter and Hillen, I would like to spend this evening just verifying and documenting a lot of stuff in my program. Every function should get a '''docstring''', and hopefully I can iron out some of the magic trick that currently 'litter' through my stuff. I would also like to sort the file tree structure a little bit, as it is getting too wild.

Because the model is currently quite advanced, I can 'make out' the similarities with Painter and Hillen, but I can not reproduce their findings yet. In part because I do not know where they bounded their simulation area, but also because I think my influence between flow stength and turtle authority is not 'calibrated' correctly. Allthough my turtles currently do not have a directional statistic, including this would make their behaviour more conflicting with Painter and Hillen. This is of course not an issue, but I am trying to figure out why I am _not_ getting their results. When I think adding the directionality will improve the result, I will add the directional statistics.
Continuing on this, I have figured out the mistake! And it was pretty big and very explicable! I wrongly implemented some math for the probabilities, and as such they did not always add to one, usually to less than one. Some instances going as low as 0.5. Because of how I implemented the probability, so that the last cumulative probability always happens if no other happens, this means the last (lrud - Down) was happening an unreasonable amount of the time. With this kink ironed out, I immediately see the claim of Painter to be way more believable, namely that not every single turtle makes it :sad:

I just found out the boundaries Painter used for their continuous model. For the horizontal boundaries, they used absorbing BC, and for the vertical ones no flow BC. Horiz.:42.5-46.5N, Vert.: 28-12W
cont model: 28/12 vertical are no flow

I have the hitch that the traversal functions are doing precisely the same thing, so I think I might combine them. (The time-dep doesn't actually take a time dep VF, it gets a snapshot which is calculated in main, one file above it.) The only difference is the getRWBiasIn[Cont]VF. These have by now been combined, so that every VF-dependent thing uses traverseVF. Very modern 

To add to the mystery, the weight factor for the VF influence is doing weird stuff. I think it is making the strongest direction always be chosen, making the RW into a sort of manhattan distance process. It yields very funky results. See videos 'factor=n'

Currently, when taking the VF to be quite rough, a VERY clear influence of the gridding can be seen (see factor=1 and factor=10). To solve this, tomorrow I will do linear VF interpolation.

## May 5th

FOR VIKTORIA: Compare the two video files factor=10[_fine]. This should give you an idea of the problem I am trying to fix today.

Yesterday I fixed a big error in how probabilities were handled. Phew. Today I want to fix a detail in which the vector field is handled. For performance purposes, I have allowed the vector field to be sampled at a lower density. Currently this is set at 8x (so that there is just 1 used per 64 available). As a result, the model displays a sort of 'gridding' in the simulation. This is due to the high factor (the influence along the axes scale fastest for the dominant direction- so a 45* flow at high factors might as well be orthogonal) in combination with this low resolution (In a finer grid, if every vector were only its strongest component, this result would be smaller. Because of each vector encompassing approx. a 8*0.05 degree side square area (approx 1600km²) they get caught in the dominant flow direction of this stream).
To adress this issue, I will have to figure out what this factor should be. A linear interpolation should also help make this issue less apparent, as the flow a turtle then more precisely depends on its location. First, I am running the factor=10 example once more, but this time with the VF grid twice as fine. In doing this, I hope to see the gridding I discussed disappear.



First thing today, I have added a function lonlat_to_meter, which I intend to use to limit the swim length of a turtle to a certain amount. Upon doing some analysis, I find the min stepsize is 76.6km/deg, maximum is 82.1km/deg. To accomodate for realistic swimming behaviour, I want the turtles to walk 2km/day. This is then achieved, at a stepsize of 0.005 deg in each direction, by making 5 steps. (Approx. math, 2/(80*0.005)). This means that in the minimum, the turtle 'underperforms' by swimming 1915m, and overperforms by swimming 2.053m. Close enough for my purposes.

## May 8th

I have been working on the PDE model. I want to continue on the discrete model a little, too, as this one is still not finished. I currently need to dial in the influence of the vector field, and also make the turtles have an orientation. To achieve this, I want to re-weight the Von Mises distribution to LRUD, so that their expectation (and maybe variance?) add up to the same direction, and 1.

I have decided to determine the individual walkers' probability of movement by taking an integral of the Von Mises distribution with parameters specified by Painter. This means that the probability of the agent moving in any direction should correspond in weight to the probability of the Von Mises going in a certain direction.
This added term seems to increase the tutels awareness of direction, and also corrects the model's tendency for all of them to head upwards. Now I 'just' need to calibrate the flow strength and movement strenght so that the results in Painter are reproduced.

I also want to make the vectorfield linearly interpolated

## May 21st

It has been a while since I've worked on the discrete process. I am glad I have reopened it, though!

Yesterday Viktoria and I have discussed about a problem that has been on my mind regarding the position-jump process: how do I make it so that an agent swims 2km per day, if it is in a vectorfield which influences its movement without costing the turtle energy?

This problem has been on my mind a lot, because ignoring this issue makes the system variant under galilean transformation. I know that these models can be used to describe brownian motion, and therefor my model should be physical, which requires invariance under galilean tranformations. See Einsteins theory of relativity for more information on this topic :)

Solving this problem is very hard when looked at face-value, but when I had my realisation, it wasn't so bad! If the influence a walker has on its own movement is p, and the influence the flowfield has is f, then the probability of movement is (p+f)/(P+F) in each direction. So the walkers own contribution has become p/(P+F), so if it originally had swam 1km, now it has swam only 1/(P+F) to go the same distance. So let the turtle do more steps until SUM 1/(P+F) = 1, and suddenly it all works! what a wonderful world.

Implementing this wasn't so hard, just give every turtle a counter and when its probability exceeds 1, stop its simulation until the next VF is added. Now turtles in a field go fast, and turtles not in a field go slow!

Now I will move on to making a script, figures and images for my presentation tomorrow.

