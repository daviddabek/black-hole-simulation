from ursina import *

SOLAR_MASS = 1.989e30  # Mass of the Sun in kilograms

class BlackHole(Entity):

    # Constants for gravitational constant and speed of light
    G = 6.67430e-11
    C = 299792458

    def __init__(self, mass, simulation_radius=2):

        self.mass = mass
        self.simulation_radius = simulation_radius # Simulation radius for visualization purposes

        # Calculate the Schwarzschild radius using the formula: R_s = 2GM/c^2
        self.schwarzschild_radius = (
            2 * self.G * self.mass
        ) / (self.C ** 2)

        super().__init__(
            model='sphere',
            color=color.black,
            scale=simulation_radius * 2,
            position=(0, 0, 0)
        )

def create_black_hole(mass, simulation_radius):
    black_hole = BlackHole(mass=mass, simulation_radius=simulation_radius)
    return black_hole