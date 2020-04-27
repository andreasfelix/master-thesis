# Transversal beam dynamics in circular accelerators

This chapter introduces the important methods and physics of transverse motion
of particles in circular accelerators. This thesis only considers the linear
order of beam optics, which are called so in analogy to geometrical light
optics. Its physical concepts were developed by Courant and Snyder [4]. The
following introduction to linear beam optics forms the basis of my python tool.

The books from Klaus Wille [5], Frank Hinterberger [6] and Helmut Wiedemann [7]
are the key sources for this chapter. However the notation and conventions will
slightly differ to match the Elegant [8] style, which I used as main reference
for my simulations.

## Equation of motion of charged particles in magnetic fields

In this section the equations of motion for linear beam optics are derived. The
fundamental force on a particle with the charge q and velocity v is called the
Lorentz force:

$$
\textbf{F}_\mathrm{L} = \textbf{F}_\mathrm{E} + \textbf{F}_\mathrm{B}
                      = q \: \textbf{E} + q \: \textbf{v} \times \textbf{B}
$$ {#eq:lorentz-force}

As an electron in a modern synchrotron radiation source is moving almost with
the speed of light $c_0$ only the magnetic part $F_B$ is of particular interest
in the following. Electric fields with an effect of the same magnitude are
technically not feasible.

The first subsection introduces the standard coordinate system of accelerator
physics, which minimizes the mathematical efforts and which is especially
helpful for the multipole expansion of the magnetic field in the second
subsection. The linear approximation of the equations of motion in the third
subsection is the essential foundation for the transfer matrix method in the
next section.

Test reference for Lorentz force [@eq:lorentz-force]

### The co-moving coordinate system

