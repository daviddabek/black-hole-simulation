# Stage 6
# Accretion Disk 

"An accretion disk is a rotating structure of gas, plasma, dust, or stellar debris that spirals inward toward a massive central astronomical object, such as a star, a white dwarf, a neutron star, or a black hole"

The AccretionDisk class implements this. It works to create a flat ring of ~1000 small glowing particles orbiting the black hole. Following real physics, particles closer to the black hole orbit faster than particles further away. This can be explained with Keplerian orbital mechanics combined with extreme gravitational pull from the black hole.

## Physics

For a circular orbit, gravity provides exactly the centripetal force needed:
 
$$
\frac{GMm}{r^2} = \frac{mv^2}{r}
\quad\Rightarrow\quad
v = \sqrt{\frac{GM}{r}}
$$
 
Angular velocity is speed divided by radius:
 
$$
\omega = \frac{v}{r} = \sqrt{\frac{GM}{r^3}}
\quad\Rightarrow\quad
\omega \propto r^{-3/2}
$$
 
That last proportionality is the key result used in the code. It is closely related to **Kepler's third law** (orbital period squared is proportional to radius cubed).

### Where does the inner edge come from?
 
Close to a black hole, circular orbits stop being stable. In general relativity the innermost stable one for a non-spinning black hole is at:
 
$$
r_{ISCO} = 6\,\frac{GM}{c^2} = 3\,R_s
$$


## Simplifications and limitations
 
- Orbits are perfect circles. Real gas gradually spirals inward (this is what "accretion" means).
- The disk is perfectly flat and has no thickness.
- The overall rotation speed is scaled for visuals.
- Newtonian orbital speed is used. Near a black hole, general relativity changes the speeds and orbit shapes.
- No gas physics: no pressure, friction, magnetic fields, turbulence or heating.
- Particles do not interact with each other.
- The tilt is a fixed visual choice.

## Disk thickness (Stage 6A)

Each particle has a fixed vertical offset from the disk's middle plane, drawn from a Gaussian distribution whose spread is proportional to the particle's orbital radius. This produces a flared disk: thin near the black hole, thicker further out.

Topic: Gaussian (normal) distribution
Topic: Scale height / flared accretion disk

## Density variation (Stage 6B)

Particle radii are chosen by raising a uniform random number to a power (`t = u ** 2`), which biases particles towards the inner edge. Real disks have higher surface density closer to the black hole.

Topic: Surface density of an accretion disk
Topic: Non-uniform random sampling

### Added limitations
- The thickness is a visual choice, not derived from gas pressure or temperature.
- The density profile is a visual choice, not a physical model.
- Heights are fixed per particle; there is no vertical motion.

## Brightness and colour (Stage 6C)

Gas closer to the black hole is hotter. In a simple thin-disk model,
temperature falls with radius as T ~ r^(-3/4). Particle brightness follows
this profile, and the colour shifts from near-white yellow at the inner edge
to vivid red-orange at the outer edge.

Brightness actually scales as T^4 (Stefan-Boltzmann law), which would be far
too extreme to display, so only the temperature profile is used.

Topic: Black-body radiation
Topic: Stefan-Boltzmann law
Topic: Shakura-Sunyaev disk temperature profile
Topic: HSV colour model

## Turbulence (Stage 6D)

Each particle bobs up and down with a random speed and starting phase,
which makes the disk look like churning gas rather than rigid rings.

Topic: Turbulence in accretion disks
Topic: Magnetorotational instability
Topic: Perlin noise

### Added limitations
- Colours are stylised, not true black-body colours.
- Brightness uses T, not T^4.
- Bobbing particles are not real turbulence; there is no interaction
  between particles.
- Doppler beaming (the approaching side looking brighter) is not modelled.