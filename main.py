from ursina import *
import random
import math

app = Ursina()

window.title = 'Black Hole Simulation'
window.borderless = False
window.fullscreen = False
window.color = color.black

# Creating a custom camera controller class to handle movement in 3D space.
class SpaceCamera(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.position = (0, 0, -15)
        self.rotation = (0, 0, 0)
        self.speed = 3

        for key, value in kwargs.items():
            setattr(self, key, value)

# Using the held_keys dictionary to check for key presses and move the camera accordingly
# "time.dt" is used to make the movement frame-rate independent.
    def update(self):
        if held_keys['w']:
            self.position += self.forward * time.dt * self.speed
        if held_keys['s']:
            self.position -= self.forward * time.dt * self.speed
        if held_keys['a']:
            self.position -= self.right * time.dt * self.speed
        if held_keys['d']:
            self.position += self.right * time.dt * self.speed
        if held_keys['space']:
            self.position -= self.up * time.dt * self.speed
        if held_keys['shift']:
            self.position += self.down * time.dt * self.speed

camera_controller = SpaceCamera()
camera.parent = camera_controller

def create_star_field(num_stars, radius):
    stars = []

    for _ in range(num_stars):

        r = random.uniform(radius * 0.5, radius)  # Random distance from the origin

        # Randomly generate spherical coordinates
        theta = random.uniform(0, 2 * math.pi)  # Azimuthal angle (angle around the sphere). 2pi because 360 degrees = 2pi radians.
        phi = random.uniform(0, math.pi)        # Polar angle (simple implementation for now, can be improved for uniform distribution)

        # Convert spherical coordinates to Cartesian coordinates
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)

        # Create a star entity at the calculated position
        star = Entity(
            model='sphere', 
            color=color.white, 
            scale=0.1, 
            position=(x, y, z)
            )
        stars.append(star)
    return stars

star_field = create_star_field(700, 100)
    

player = EditorCamera()

app.run()