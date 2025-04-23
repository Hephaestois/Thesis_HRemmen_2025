Hello Viktoria! :)

# This file is meant as a log!
To be specific, this file is meant to serve the purpose of me not forgetting what steps I took to arrive at the model I want, so that later I can write about it in chronological-ish order. At least, in an order that preserves the initial streams of thinking I 'used' to achieve my results.

I will therefor add dates as 'waypoints', and also to give a clear separation of time. This will not be readable like a book, I will have to re-format this later into the actual overleaf text. 

# 23-04
In the meeting today, we discussed which direction to take the project: I have suggested continuing the turtles-thing from Painter, Hillen. Topgether we arrived to 1. a more overseeable scope and 2. a semi-detailed timeline. To reiterate, the timeline is going to be roughly: 
- implement FAAD
- implement the RW with non-constant a and D
- implement the RW in a vector field (with ocean data?)
- implement FAAD in a vector field
- find some analytical solutions to FAAD (and maybe some non'trivial' ones)
- implement RW in a time-dependent vector field
- implement 

The first dataset I want to get, I try to get from: 
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_85cb_974f_1f6c.html
With range: 2018-01-01 -- 2018-01-04,
Lat-Lon: 42-47 N, 331-349 E (as in KJP) (or -29 to -11 E)

This failed. Trying the next link:
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_a2d2_f95d_0258.html
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_a2d2_f95d_0258.htmlTable?water_u[(2020-01-01):1:(2020-01-03)][(0.0):1:(130)][(42):1:(47)][(331):1:(349)],water_v[(2020-01-01):1:(2020-01-03)][(0.0):1:(130)][(42):1:(47)][(331):1:(349)]


Also failed. Trying
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_7e38_7a7b_afe2.html
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_7e38_7a7b_afe2.htmlTable?water_u[(2014-01-01):1:(2014-01-04)][(0.0):1:(130)][(42):1:(47)][(-29):1:(-11)],water_v[(2014-01-01):1:(2014-01-04)][(0.0):1:(130)][(42):1:(47)][(-29):1:(-11)]
The last one seems to have worked!!

I have opted to download as CVS. The specified 42 to 47, -29 to -11, with 'degree stepsize' 0.0523, 0.080 consists of 45MB data per day (with just one measurement per day!!). Therefor, I am going to fetch a new dataset, consisting of just one day, but with degree-multiples of 5 (so delta=0.26) for the latitude, and multiples of 6 for the longitude (so delta=0.48). This difference in delta is due to the length of the interval. I am going to interpolate linearly later anyway, so so long as the 'resolution' of the vector field is reasonable, going more precise shouldn't change a lot.

New dataset (clicking starts a download, 69kb):
http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_7e38_7a7b_afe2.csv?water_u[(2014-01-01):1:(2014-01-01)][(0.0):1:(0)][(42):5:(47)][(-29):6:(-11)],water_v[(2014-01-01):1:(2014-01-01)][(0.0):1:(0)][(42):5:(47)][(-29):6:(-11)]
This is one day of time, with two depth-scales (0 and 2 meter, my bad). 
