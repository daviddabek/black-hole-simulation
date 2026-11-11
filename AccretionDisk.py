import math
import random

from ursina import *


class DiskParticle(Entity):
    """
    One small blob of gas in the accretion disk.

    Each particle moves on a circular orbit. Its position is described by
    three numbers:
        orbital_radius  : distance from the black hole (fixed)
        angle           : how far round the circle it currently is (changes)
        vertical_offset : height above/below the disk's middle plane (fixed)
    """

    def __init__(self, parent, orbital_radius, angle, angular_velocity,
                 particle_color, vertical_offset=0, size=0.08):

        super().__init__(
            parent=parent,
            model='sphere',
            color=particle_color,
            scale=size
        )

        self.orbital_radius = orbital_radius
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.vertical_offset = vertical_offset

        # Place the particle at its starting position.
        self.move(0)

    def move(self, dt):
        """Advance the particle along its circular orbit by dt seconds."""

        self.angle += self.angular_velocity * dt

        # Polar -> Cartesian, in the disk's flat (x, z) plane.
        self.x = self.orbital_radius * math.cos(self.angle)
        self.z = self.orbital_radius * math.sin(self.angle)
        self.y = self.vertical_offset


class AccretionDisk(Entity):
    """
    A flat ring of particles orbiting a black hole.

    Simplifications (see docs/05_accretion_disk.md):
    - Orbits are perfect circles; particles never fall inward.
    - The disk is perfectly flat.
    - Orbital speeds follow Kepler's law (omega ~ r^-1.5), but the overall
      speed is scaled for looks, not in real physical units.
    """

    def __init__(self, black_hole, num_particles=1000,
                 inner_factor=3, outer_factor=7,
                 base_angular_velocity=1.5,
                 thickness_ratio=0.03, density_exponent=2):

        super().__init__(position=black_hole.position)

        horizon_radius = black_hole.simulation_radius

        self.inner_radius = inner_factor * horizon_radius
        self.outer_radius = outer_factor * horizon_radius

        self.base_angular_velocity = base_angular_velocity

        # Disk shape settings (used by create_particle).
        self.thickness_ratio = thickness_ratio
        self.density_exponent = density_exponent

        self.particles = []

        for _ in range(num_particles):
            self.particles.append(self.create_particle())

    def angular_velocity_at(self, radius):
        """
        Kepler's law: omega is proportional to r^(-3/2).

        We scale it so a particle at the inner edge has
        base_angular_velocity.
        """
        ratio = self.inner_radius / radius
        return self.base_angular_velocity * ratio ** 1.5

    def create_particle(self):
        """Create one particle at a random position in the disk."""

        # 0 = inner edge, 1 = outer edge. Raising a random number to a
        # power above 1 pushes values towards 0, so the inner disk is denser.
        t = random.random() ** self.density_exponent

        radius = self.inner_radius + t * (self.outer_radius - self.inner_radius)
        angle = random.uniform(0, 2 * math.pi)

        omega = self.angular_velocity_at(radius)

        # Thicker further out: spread is proportional to radius.
        spread = self.thickness_ratio * radius
        vertical_offset = random.gauss(0, spread)

        # Hue: yellow near the black hole, shifting to red at the outside.
        hue = 50 - 40 * t
        particle_color = color.hsv(hue, 0.85, 1)

        return DiskParticle(
            parent=self,
            orbital_radius=radius,
            angle=angle,
            angular_velocity=omega,
            particle_color=particle_color,
            vertical_offset=vertical_offset
        )

    def update(self):
        # Ursina calls this every frame.

        for particle in self.particles:
            particle.move(time.dt)