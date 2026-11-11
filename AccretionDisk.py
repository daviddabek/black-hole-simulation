import math
import random

from ursina import *


class DiskParticle(Entity):
    """
    One small blob of gas in the accretion disk.

    Each particle moves on a circular orbit. Its position is described by:
        orbital_radius  : distance from the black hole (fixed)
        angle           : how far round the circle it currently is (changes)
        vertical_offset : home height above/below the middle plane (fixed)

    It also bobs gently up and down to fake turbulence:
        wobble_size  : how far it bobs (fixed)
        wobble_speed : how fast it bobs (fixed)
        wobble_phase : where it is in its bob cycle (changes)
    """

    def __init__(self, parent, orbital_radius, angle, angular_velocity,
                 particle_color, vertical_offset=0, wobble_size=0,
                 size=0.08):

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

        # Fake turbulence: a random bobbing motion for each particle.
        self.wobble_size = wobble_size
        self.wobble_speed = random.uniform(0.5, 1.5)
        self.wobble_phase = random.uniform(0, 2 * math.pi)

        # Place the particle at its starting position.
        self.move(0)

    def move(self, dt):
        """Advance the particle along its orbit and bobbing cycle by dt seconds."""

        self.angle += self.angular_velocity * dt
        self.wobble_phase += self.wobble_speed * dt

        # Polar -> Cartesian, in the disk's flat (x, z) plane.
        self.x = self.orbital_radius * math.cos(self.angle)
        self.z = self.orbital_radius * math.sin(self.angle)

        # Home height plus a gentle bob.
        self.y = self.vertical_offset + self.wobble_size * math.sin(self.wobble_phase)


class AccretionDisk(Entity):
    """
    A thick ring of particles orbiting a black hole.

    Simplifications (see docs/05_accretion_disk.md):
    - Orbits are perfect circles; particles never fall inward.
    - Orbital speeds follow Kepler's law (omega ~ r^-1.5), but the overall
      speed is scaled for looks, not in real physical units.
    - Thickness, density, colour and turbulence are visual choices,
      loosely inspired by real disks, not physical models.
    """

    def __init__(self, black_hole, num_particles=1000,
                 inner_factor=3, outer_factor=7,
                 base_angular_velocity=1.5,
                 thickness_ratio=0.03, density_exponent=2,
                 turbulence=0.5):

        super().__init__(position=black_hole.position)

        horizon_radius = black_hole.simulation_radius

        self.inner_radius = inner_factor * horizon_radius
        self.outer_radius = outer_factor * horizon_radius

        self.base_angular_velocity = base_angular_velocity

        # Disk shape settings (used by create_particle).
        self.thickness_ratio = thickness_ratio
        self.density_exponent = density_exponent
        self.turbulence = turbulence

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

    def particle_color_at(self, radius, t):
        """
        Hotter gas is brighter and whiter, cooler gas is dimmer and redder.

        radius : the particle's orbital radius
        t      : 0 at the inner edge, 1 at the outer edge
        """

        # Simple disk temperature profile: T ~ r^(-3/4).
        # This is 1 at the inner edge and smaller further out.
        ratio = self.inner_radius / radius
        temperature = ratio ** 0.75

        # Hue: yellow near the black hole, shifting to red at the outside.
        hue = 50 - 40 * t

        # Saturation: nearly white (hot) at the inside, vivid at the outside.
        saturation = 0.25 + 0.65 * t

        # Value (brightness): follows temperature, with a little random
        # variation so neighbouring particles are not identical.
        value = temperature * random.uniform(0.7, 1.0)

        return color.hsv(hue, saturation, value)

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

        # Bobbing is a fraction of the thickness.
        wobble_size = self.turbulence * spread

        particle_color = self.particle_color_at(radius, t)

        return DiskParticle(
            parent=self,
            orbital_radius=radius,
            angle=angle,
            angular_velocity=omega,
            particle_color=particle_color,
            vertical_offset=vertical_offset,
            wobble_size=wobble_size
        )

    def update(self):
        # Ursina calls this every frame.

        for particle in self.particles:
            particle.move(time.dt)