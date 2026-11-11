import math

from ursina import *


SOLAR_MASS = 1.989e30


class BlackHole(Entity):

    G = 6.67430e-11
    C = 299792458

    def __init__(self, mass, simulation_radius=2):

        self.mass = mass
        self.simulation_radius = simulation_radius

        # Calculate the Schwarzschild radius:
        # R_s = 2GM / c^2
        self.schwarzschild_radius = (
            2 * self.G * self.mass
        ) / (self.C ** 2)

        # The visual sphere represents the event horizon, so
        # simulation_radius units = schwarzschild_radius metres.
        self.metres_per_unit = self.schwarzschild_radius / self.simulation_radius

        super().__init__(
            model='sphere',
            color=color.black,
            scale=simulation_radius * 2,
            position=(0, 0, 0)
        )

    def distance_from_centre(self, point):
        """Distance from the black hole's centre to a point, in simulation units."""
        return (point - self.position).length()

    def distance_in_schwarzschild_radii(self, point):
        """Distance from the centre as a multiple of Rs (1 = on the horizon)."""
        return self.distance_from_centre(point) / self.simulation_radius

    def gravitational_acceleration(self, point):
        """
        Newtonian gravity at a point, in m/s^2:  g = GM / r^2

        Only meaningful outside the event horizon. This is an
        approximation; real gravity is stronger close to the black hole.
        """
        r_metres = self.distance_from_centre(point) * self.metres_per_unit
        return self.G * self.mass / r_metres ** 2

    def time_dilation_factor(self, point):
        """
        How fast time runs at a point compared to far away.

        sqrt(1 - Rs / r):  1 = normal speed, 0 = completely frozen.
        Exact for a stationary observer outside a non-spinning black hole.
        """
        r_in_rs = self.distance_in_schwarzschild_radii(point)

        # The formula is not valid at or inside the horizon.
        if r_in_rs <= 1:
            return 0

        return math.sqrt(1 - 1 / r_in_rs)