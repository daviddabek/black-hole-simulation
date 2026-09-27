# Objective 1.0
Create a free flying 3D camera to allow the user to move freely through the simulated environment.

# Implementation of movement
"time.dt" is used to make the movement frame-rate independent, without it, the camera would move faster on higher 
frame rates and slower on lower frame rates.

# Creating star field
I will use spherical coordinates to randomly distribute stars in the simulation. 
This will be done instead of just randomising 'x, y and z' because that would create a cube of stars, which 
would not capture the effect of objects naturally extending in all directions from the centre (the black hole).

The initial star field uses a random value for the polar angle using `phi = random.uniform(0, math.pi)`. 
This is simple to implement, but it does not distribute stars perfectly evenly across the sphere because the 
surface area changes between the poles and the equator.
The problem is that equal changes in the angle don't represent equal amounts of space. There is less surface 
area near the top and bottom (the poles) than around the middle (the equator).
A more mathematically accurate distribution can be implemented later using `cos(phi)` to produce a more uniform star field.