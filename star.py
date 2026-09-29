from ursina import *


class Star(Entity):

    def __init__(self, position, size=0.03):

        super().__init__(
            model='sphere',
            color=color.white,
            scale=size,
            position=position
        )

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

        # Create star object and add it to the list
        star = Star(
            position=(x, y, z)
        )

        stars.append(star)

    return stars