# FOR VIKTORIA:
This file is the text and presentation notes for the midterm presentation. Feel free to go about here, we'll discuss the final presentation later.



# General structure
Introduction: 
What is the problem? 'How do the turtles find their way home?'. Video of vector field in the background. Introduce the _scope_ of the simulation: You find yourself in this vectorfield. How the hell will you remain in the stream???

Formal introduction:
You can derivate from a position-jump the advection-diffusion equation. Therefor, in simulation, they should yield the same results, right?
Also mention what I mean by advection and diffusion. 'Directed and random movement'?

PDE model:
What is the FAAD model? How do its modelling iterations look like?

Position Jump model:
What is a position jump process? How do the model iterations look? And how is it implemented?

Do the models agree?
Yes! And why! Show the pitfalls and the victories!

# Visual imagery and video-ery

- Finding Nemo turtles? Maybe?
- The waves of the ocean vector field
- Image of North Atlantic Gyre
- Video of pure advection (-diffusion)


# Worked text

## Introduction
Have you ever wondered how turtles find their way around? I mean, the ocean is pretty big, and it's not like Turtles can navigate home, they carry theirs on their backs.
Okay, let's take a more concrete look... this is the North Atlantic Gyre: a pretty big stream circulating between Europe, Africa and the Americas. My presentation for you today
will be about a specific region of the Gyre, located off the coast of Iberia. If we drop an innocent turtle into the waters right here... how could we ever predict what's going to happen to the turtle? And can we do so in a time-efficient manner?? And most importantly of all... with climate change disrupting natural system globally, what traversing the seas become more complicated for the turtles?

## Formal introduction
Let's talk about today's content: I'm going to talk to you about two models to simulate this behaviour inside of an ocean. One model, which I am going to refer to as a Random Walk, or a position jump process takes individual turtles, and determines in which direction they are most likely to move. The other, which I will refer to as the PDE model, starts with densities and determines how these are going to move around, with the influences from a turtle and a vector field. 

Why these two models specifically? Well, people in the past, and I in my paper, have shown that the PDE model is a consequence of the Random Walk model. Specifically when you take some limits of step-size parameters. Today we will not discuss this, and assume the statement to be true: there exists a similarity between the models! I want to take the time today to then explain how each of these models can describe something as complex as ocean flows, and why these models can capture more complex behaviour than you might think at first glance.

## PDE Model
The position jump theory definiely is simpler than that of the PDE model. However, as the PDE model is in many ways simpler than the position jump model, we start here. The PDE model is based on the idea that we can discretize our space, and for each small area, determine the flow between them. Aha! The finite volume method! To move forward in time, we have just used Forward Euler, and that has been fine enough for stability and performance. As the PDE model is in many ways simpler than the position jump model, this is our point of departure.

When we analyse the model we are simulating, we can make out a few terms, namely the advective or directed part, and the diffusive or undirected part. This advection, we can split again into a constant advection, and one due to a vector field. This constant advection is a turtles behaviour, and the vectorfield are the ocean streams! It is fair to ask how the turtles know where they are going. One published paper has shown this knowlege to be caused by turtles 'sensing' regional magnetic fields, and knowing in which direction to swim as a result of that. 

In every simulation, I am going to put a red dot [image] here, to indicate the location where we drop the turtles into the ocean. This rate of introduction is done with 5 turtles per day in each simulation. Also a useful detail to mention: I will simulate the turtles for exactly 100 days, starting at the first of January 2016. Then every time a new day breaks, I will 
If we just let a few turtles loose in a simulated ocean, we get the following:
[video]
In this, the turtles swim roughly 2km/day due to their swimming behaviour, which is spread out due to them not having a GPS. So, when time passes, they move away from their starting position. 
Of course, the ocean makes a large difference in this! So... lets do a different simulation: the turtles aren't doing anything anymore, and we are just looking at ocean currents:
[video]
Allright... Now let's combine these factors!
[video]
And there we have it. This is the first important result: we can see how the advective behaviour of the turtles skews the density towards the bottom, and thus more turtles remain in the Gyre because of their own doing.


## Position Jump model
We move on to a position jump model, where an agent makes discrete steps based on a set of probabilities. So an agent can be described by a set of probabilties left, right, up and down, and the question then is: how could we describe each probability? 
Well, as we just saw, there is a diffusive component, and two advective components. Just the constant terms look like this [video] For comparison, just the effect of the vector field looks like [video]. 





## PDE model



Have you ever wondered how turtles know how to find their way home? 


