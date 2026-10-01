import math
import random

from ursina import *


class DiskParticle(Entity):
    """
    One small blob of gas in the accretion disk.

    Each particle moves on a circular orbit. Its position is described by
    two numbers:
        orbital_radius : distance from the black hole (fixed)
        angle          : how far round the circle it currently is (changes)
    """

    def __init__(self, parent, orbital_radius, angle, angular_velocity,
                 particle_color, size=0.08):

        super().__init__(
            parent=parent,
            model='sphere',
            color=particle_color,
            scale=size
        )

        self.orbital_radius = orbital_radius
        self.angle = angle
        self.angular_velocity = angular_velocity

        # Place the particle at its starting position.
        self.move(0)

    def move(self, dt):
        """Advance the particle along its circular orbit by dt seconds."""

        self.angle += self.angular_velocity * dt

        # Polar -> Cartesian, in the disk's flat (x, z) plane.
        self.x = self.orbital_radius * math.cos(self.angle)
        self.z = self.orbital_radius * math.sin(self.angle)
        self.y = 0


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
                 base_angular_velocity=1.5):

        super().__init__(position=black_hole.position)

        # The black hole's radius in simulation units.
        horizon_radius = black_hole.simulation_radius

        # Inner edge = 3 x Schwarzschild radius (the ISCO).
        # Outer edge is a visual choice.
        self.inner_radius = inner_factor * horizon_radius
        self.outer_radius = outer_factor * horizon_radius

        # Angular velocity of a particle at the inner edge (radians/second).
        self.base_angular_velocity = base_angular_velocity

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
        # Create one particle at a random radius and random angle."""

        radius = random.uniform(self.inner_radius, self.outer_radius)
        angle = random.uniform(0, 2 * math.pi)

        omega = self.angular_velocity_at(radius)

        # 0 = at the inner edge, 1 = at the outer edge.
        t = (radius - self.inner_radius) / (self.outer_radius - self.inner_radius)

        # Hue (colour wheel position in degrees): yellow near the
        # black hole, shifting to red at the outside.
        hue = 50 - 40 * t
        particle_color = color.hsv(hue, 0.85, 1)

        return DiskParticle(
            parent=self,
            orbital_radius=radius,
            angle=angle,
            angular_velocity=omega,
            particle_color=particle_color
        )

    def update(self):
        # Ursina calls this every frame.

        for particle in self.particles:
            particle.move(time.dt)