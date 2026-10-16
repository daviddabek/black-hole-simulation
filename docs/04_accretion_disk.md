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