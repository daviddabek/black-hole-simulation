from ursina import *
import random
import math

from Star import Star
from BlackHole import BlackHole
from AccretionDisk import AccretionDisk

# Constant for the mass of the sun in kilograms
SOLAR_MASS = 1.989e30

app = Ursina()

# Set up the window properties
window.title = 'Black Hole Simulation'
window.borderless = False
window.fullscreen = False
window.color = color.black

# Custom camera controller for movement in 3D space.
class SpaceCamera(Entity):

    def __init__(self, **kwargs):

        super().__init__()

        self.position = (0, 0, -15)
        self.rotation = (0, 0, 0)
        self.speed = 3

        for key, value in kwargs.items():
            setattr(self, key, value)

    # Uses held_keys to move the camera.
    # time.dt makes movement not be affected by frame rate.
    def update(self):

        if held_keys['w']:
            self.position += self.forward * time.dt * self.speed

        if held_keys['s']:
            self.position -= self.forward * time.dt * self.speed

        if held_keys['a']:
            self.position -= self.right * time.dt * self.speed

        if held_keys['d']:
            self.position += self.right * time.dt * self.speed

camera_controller = SpaceCamera()
camera.parent = camera_controller
camera.position = (0, 0, 0)
player = EditorCamera()

# Creates many Star objects and places them randomly within a spherical region.
def create_star_field(num_stars, radius):

    stars = []

    for _ in range(num_stars):

        # Random distance from the origin
        r = random.uniform(radius * 0.5, radius)

        # Random spherical coordinates
        theta = random.uniform(0, 2 * math.pi) # Azimuthal angle (angle around the sphere). 2pi because 360 degrees = 2pi radians.
        phi = random.uniform(0, math.pi) # Polar angle (simple implementation for now, can be improved for uniform distribution)

        # Convert spherical coordinates to Cartesian coordinates
        x = r * math.sin(phi) * math.cos(theta) # Azimuthal angle (angle around the sphere). 2pi because 360 degrees = 2pi radians.
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)

        # Create a Star object
        Star(
            position=(x, y, z)
        )

        stars.append(Star)

    return stars


# Create the star field
stars = create_star_field(700, 50)


# Black Hole implementation
BlackHole = BlackHole(
    mass=10 * SOLAR_MASS,
    simulation_radius=2
)

disk = AccretionDisk(BlackHole, num_particles=1000)
disk.rotation_x = 20

app.run()