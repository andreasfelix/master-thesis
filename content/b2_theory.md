# Beam Dynamics in Electron Storage Rings

This chapter introduces the basics of electron beam dynamics in ciruclar accelerators. The books of H. Wiedemann [@wiedemann], A. Wolski [@wolski2018introduction], K. Wille [@wille] and F. Hinterberger [@hinterberger] were the key sources of the following sections.

@sec:linear-beam-dynamics covers the linear optics. In @sec:chromaticity the effect of energy derivations of the particle beam on the betatron tune is discussed. Sectionq

All covered concepts are implemented in the developed beam optics code.

## Linear Beam Dynamics {#sec:linear-beam-dynamics}

As the linear order of beam optics was thourghly described in my Bachelor's Thesis [@andreas_ba], this section skips all derivations and provides only a summary of the most important results.

### The Co-moving coordinate system

To describe the motion of a particle within an accelerator it is common to choose the co-moving Frenet-Serret coordinates, whose origin follows the trajectory of the reference particle.

![Co-moving Frenet-Serret coordinate system](figures/frenet-serret-coordinates.svg){#fig:frenet-serret-coordinates}

The three basis vectors

$$ \begin{aligned}
\mathbf{\hat{e}}_s(s) &= \frac{d \mathbf{r}_0(s)}{d s} & \text{tangent basis vector} \\
\mathbf{\hat{e}}_x(s) && \text{horizontal basis vector} \\
\mathbf{\hat{e}}_y(s) &= \mathbf{\hat{e}}_s(s) \times\mathbf{\hat{e}}_x(s) & \text{vertical basis vector}
\end{aligned}
$$ {#eq:basis-vectors}

span the coordinate system. While the $\mathbf{\hat{e}}_s(s)$ vector moves tangential to the orbit, the horizontal $\mathbf{\hat{e}}_x(s)$ and vertical $\mathbf{\hat{e}}_y(s)$ vectors are perpendicular to it. The distance covered on the ideal orbit is defined as the $s$ coordinate. The $z$ coordinate corresponds to the path length of the individual particle trajectory. The horizontal and vertical coordinates are labeled with $x$ and $y$. For statements which are valid for both transversal planes we will use the general variable $u$.

The position of the individual particle in the laboratory frame is given as the sum of the orbit position $\mathbf{r}_0(s)$ and its $x$ and $y$ coordinates in the Frenet-Serret system:

$$
\mathbf{r}(x,y,s) =  \mathbf{r}_0(s) + x(s) \mathbf{\hat{e}}_x(s) + y(s) \mathbf{\hat{e}}_y(s)
$$ {#eq:position-vector}


The curvature of the particle trajectory $\kappa_x = \frac{1}{\rho_x}$ can be expressed in terms of the individual multipole strengths:
$$
\kappa_x(x,p)
= k_0(p) + k_1(p) x + \frac{1}{2} k_2(p) x^2 + \frac{1}{6} k_3(p) x^3 + ...
$$



### Equations of motion


$$
h = 1 + \kappa_\mathrm{x0} x + \kappa_\mathrm{y0} y
$$

$$
\frac{d^2 \mathbf{r}}{d z^2} = \frac{ec}{\beta E} \left( \frac{d \mathbf{r}}{d z} \times \mathbf{B} \right)
$$ {#eq:lorentz-force}

$$
\mathbf{r}'' - \frac{1}{2z'^2}\frac{d \mathbf{r}}{d s}\frac{d z'^2}{d s} = \frac{ec}{\beta E} z'\left( \mathbf{r}' \times \mathbf{B} \right)
$$ {#eq:eom-1}

$$
\begin{aligned}
x'' = \frac{e c}{\beta E} z' (y'B_{\mathrm{z}} - h B_\mathrm{y}) + \kappa_\mathrm{x0}h + \frac{x'}{2 z'^2}\frac{d z'^2}{d s} \\
y'' = \frac{e c}{\beta E} z' (h B_\mathrm{x} - x'B_{\mathrm{z}}) + \kappa_\mathrm{y0}h + \frac{y'}{2 z'^2}\frac{d z'^2}{d s}
\end{aligned}
$$ {#eq:eom-2}

Exakte Bewegungsgleichung mit $ E \beta = p c$
$$
\begin{aligned}
x'' = \frac{c}{p} z' (y'B_{\mathrm{z}} - h B_\mathrm{y}) + \kappa_\mathrm{x0}h + \frac{x'}{2 z'^2}\frac{d z'^2}{d s} \\
y'' = \frac{c}{p} z' (h B_\mathrm{x} - x'B_{\mathrm{z}}) + \kappa_\mathrm{y0}h + \frac{y'}{2 z'^2}\frac{d z'^2}{d s}
\end{aligned}
$$ {#eq:eom-3}

Approximation 1: $B_\mathrm{z} \approx 0$

$$
\begin{aligned}
x'' = - \frac{e}{p} z' h B_\mathrm{y} + \kappa_\mathrm{x0}h + \frac{x'}{2 z'^2}\frac{d z'^2}{d s} \\
y'' = \frac{e}{p} z' h B_\mathrm{x} + \kappa_\mathrm{y0}h + \frac{y'}{2 z'^2}\frac{d z'^2}{d s}
\end{aligned}
$$ {#eq:eom-4}

Approximation 2: $z' \approx h + \frac{1}{2}(x'^2 + y'^2)(1 - \kappa_x x - \kappa_y y) + ...$ nur ersten Term mitnehmen $z' \approx h$
$$
\begin{aligned}
x'' = - \frac{e}{p} h^2 B_\mathrm{y} + \kappa_\mathrm{x0}h + \frac{x'}{2 z'^2}\frac{d z'^2}{d s} \\
y'' = \frac{e}{p} h^2 B_\mathrm{x} + \kappa_\mathrm{y0}h + \frac{y'}{2 z'^2}\frac{d z'^2}{d s}
\end{aligned}
$$ {#eq:eom-5}

Approximation 3: dritten Term vernachlässigen
$$ \begin{aligned}
x'' = - \frac{e}{p} h^2 B_\mathrm{y} + \kappa_\mathrm{x0}h \\
y'' = \frac{e}{p} h^2 B_\mathrm{x} + \kappa_\mathrm{y0}h
\end{aligned}
$$ {#eq:eom-6}

Umschreiben $p = \frac{p}{p_0} \cdot p_0 = (1 + \delta) p_0$ und $\frac{e}{p_0}B_\mathrm{y} = \kappa_x$ und $\frac{e}{p_0}B_\mathrm{x} = \kappa_y$

$$ \begin{aligned}
x'' = -  \frac{h^2}{(1 + \delta)}  \kappa_\mathrm{x} + \kappa_\mathrm{x0}h \\
y'' =  \frac{ h^2}{(1 + \delta)} \kappa_\mathrm{y} + \kappa_\mathrm{y0}h
\end{aligned}
$$ {#eq:eom-7}

mit

$$ \begin{aligned}
\kappa_\mathrm{x} =  \kappa_\mathrm{x0} + k x + m(x^2-y^2) + ... \\
\kappa_\mathrm{y} =  \kappa_\mathrm{y0} + k y + mxy + ...
\end{aligned}
$$ {#eq:eom-8}


The particle trajectory within non linear elements can be obtained by integrating @eq:eom-7 numerically. This method was for example used to created the plots in @sec:chromaticity.

### Betatron oscillation

![The envelope of a particle beam at the example of a FODO cell. The betatron oscillation for 33 electrons with an emittance of 5 nm rad is shown in the right graphic.](figures/betatron-oscillation.svg){#fig:betatron-oscillation}

By neglecting the off-momentum terms and substituting $K_x(s) = k_0^2(s) + k_1(s)$ for the horizontal and $K_y(s) = - k_1(s)$ for the vertical plane, the linear equations of motion

$$
u''(s) + K_u(s) u(s) = 0
$$ {#eq:hill-equation}

The offset in linear order is given by @eq:betatron-oscillation

$$ u(s) = \sqrt{\epsilon_u \beta_u (s)} \cos(\psi_u(s) + \psi_{u0})
$$ {#eq:betatron-oscillation}

$$ \psi_u(s) = \int_0^s \frac{d \bar{s}}{\beta_u(\bar{s})}.
$$ {#eq:betatron-phase}

$$ Q_u = \frac{1}{2 \pi}\int_s^{s+C} \frac{d \bar{s}}{\beta_u (\bar{s})}
$$ {#eq:tune}

$$ \alpha(s) := \frac{-\beta'(s)}{2}
$$

$$ \gamma(s) := \frac{1 + \alpha^2(s)}{\beta(s)}
$$

the ellipse equation:

$$ \gamma(s) u^2(s) + 2 \alpha(s) u(s)u'(s) + \beta(s) u'^2(s) = \epsilon .
$$ {#eq:phase-space-ellipse}

### Transformation of the Twiss parameter

$$ \mathbf{B}(s) =
    \begin{pmatrix}
        \beta(s) & -\alpha(s) \\
        -\alpha(s) & \gamma(s)
    \end{pmatrix}
$$ {#eq:beta-matrix}

$$ \mathbf{B}(s+L) = \mathbf{R}(s,L) \cdot  \mathbf{B}(s) \cdot  \mathbf{R}^T(s,L)
$$ {#eq:transformation-beta-matrix}

### Dispersion

### Momentum Compaction

## Chromaticity {#sec:chromaticity}

### Natural Chromaticity in a Storage Ring

### Chromaticity Correction

## Synchrotron Radiation
The previous sections discussed the particle motion while neglecting any emission of synchrotron radition. However the random emission of photons has an influence on the amplitude of the betatron and synchrotron oscillations, which changes the beam emittance. At first this might seem like a violation of the Liouville's theorem [reference to previous section]: It states that the phase space distribution of non-interacting particles in conservatives systems is constant along any path. Consequently the occupied volume in phase space must be conserved. The emittance corresponds to the occupied phase space volume of the electron beam. But as soon as an electron emits a photon, the beam emittance only occupies a sub-volume of the total electron-photon phase space, which is spaned by the coordinates of the electron and photon. Thus due to the synchrotron radiation and consistent with the Liouville's theorem the beam emittance can change. The Liouville's theorem still holds true for the entire electron-photon system.

To describe the effects of synchrotron radiation on the beam properties it useful to define the five so-called synchrtoron radiation integrals:

$$ I_1 = \int_0^{C_0} \frac{\eta_x}{\rho} \mathrm{d}s
$$ {#eq:i1}

$$ I_2 = \int_0^{C_0} \frac{1}{\rho^2} \mathrm{d}s
$$ {#eq:i2}

$$ I_3 = \int_0^{C_0} \frac{1}{|\rho|^3} \mathrm{d}s
$$ {#eq:i3}

TODO: include poleface effect (see MAD-X source code or SLAC-Pub-1193)
$$ I_4 = \int_0^{C_0} \frac{\eta_x}{\rho}\left(\frac{1}{\rho^2} + 2k_1\right)\mathrm{d}s
$$ {#eq:i4}

$$ I_5 = \int_0^{C_0} \frac{H_x}{rho^3} \mathrm{d}s
$$ {#eq:i5}

### Radiation damping

![Radiation damping of the betatron oscillation. When a photon is emitted within a magnet in the direction of the particle movement, it reduces the transversal and longitudinal component of the electron's momentum. As the cavity only refills the longitudinal component, the transversal components decreases over time.](figures/betatron-oscillation-damping.svg){#fig:betatron-oscillation-damping}


### Quantum Excitation

But the betatron oscillation amplitude does not damp to zero. The damping is counteracted by the quantum excitation. Due to the quantum nature of the photons, the radiation is not continuous, but happens in discrete chunks of energy.

The five synchrotron radiation integrals give an overview of the radiation properties of a given lattice:


![Quantum excitation of the betatron oscillation. When an electron with the reference momentum $p = p_0$ emits a photon within a bending magnet, it loses energy and will no longer be on the closed orbit. It will now perform betatron oscillations around a dispersive closed orbit $p < p_0$. (based on @wolski2018introduction)](figures/betatron-oscillation-excitation.svg){#fig:betatron-oscillation-excitation}




$$ \mathcal{H}_x = \gamma_x \eta_x^2 + 2 \alpha_x \eta_x \eta_x' + \beta_x \eta_x'^2
$$ {#eq:curly-h}

$$ j_x = 1 - \frac{I_4}{I_2}
$$ {#eq:horizontal-damping-partition-number}

### Natural Emittance {#sec:emittance}

$$ \epsilon_x = C_q \gamma^2 \frac{I_5}{j_x I_2}
$$ {#eq:emittance}

## Lattice Design {#sec:lattice-design}

This sections discusses the concepts introduced using the example of a FODO, a DBA and a TBA lattice.

### The FODO Lattice

### The DBA Lattice

Compare wiedemann 241 vs wolski 3-21

### The TBA Lattice

Compare wiedemann 244
