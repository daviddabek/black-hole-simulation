# Event Horizon

The event horizon is the boundary surrounding a black hole beyond which nothing can escape to a distant observer, including light. It is not a physical surface. In this simulation, the event horizon is represented visually as a black spherical boundary. This is a simplified visualization rather than a physically complete representation of a black hole.

# The Schwarzschild Radius

The black hole will be non-rotating to make it easier to implement. For a non-rotating black hole, the radius of the event horizon can be calculated using the Schwarzschild Radius. 

Formula: R_s = 2GM/c^2
G - Gravitational Constant, M - Mass, c - Speed of light

## Simulation Scale

The Schwarzschild radius is calculated using real physical constants, but the 3D environment does not use metres as its coordinate system. Using real distances directly would make the scene impractical to visualize. Instead, the physical Schwarzschild radius is calculated first and then represented using a convenient simulation scale. This means the visualization demonstrates the physical relationships without claiming that one 3D unit represents one metre.

## Singularity

The centre of the black hole is described by classical general relativity as containing a singularity, where the theory predicts extreme curvature. This simulation does not attempt to model the singularity because doing so would require physics beyond the simplified model used here. The simulation instead focuses on the event horizon and the observable effects surrounding the black hole.

