# Beam Dynamics in Electron Storage Rings

This chapter introduces the basics of electron beam dynamics in ciruclar accelerators. The books of H. Wiedemann [@wiedemann], A. Wolski [@wolski2018introduction], K. Wille [@wille] and F. Hinterberger [@hinterberger] were the key sources of the following sections.

@sec:linear-beam-dynamics covers the linear optics. In @sec:chromaticity the effect of energy derivations of the particle beam on the betatron tune is discussed. Sectionq

All covered concepts are implemented in the developed beam optics code.

## Linear Beam Dynamics {#sec:linear-beam-dynamics}

As the linear order of beam optics was thourghly described in my Bachelor's Thesis [@andreas_ba], this section does not give any derivations and instead provides a summary of the most important results.

### The Co-moving coordinate system

The position of the individual particle in the laboratory frame is given as the sum of its coordinates in the Frenet-Serret system and of the orbit position $\textbf{r}_0(s)$

$$
\mathbf{r}(x,y,s) =  \mathbf{r}_0(s) + x(s) \mathbf{\hat{e}}_x(s) + y(s) \mathbf{\hat{e}}_y(s)
$$ {#eq:position-vector}

![Co-moving Frenet-Serret coordinate system](figures/frenet-serret-coordinates.svg){#fig:frenet-serret-coordinates}

The curvature of the particle trajectory $\kappa_x = \frac{1}{\rho_x}$ can be expressed in terms of the individual multipole strengths:
$$
\kappa_x(x,p)
= k_0(p) + k_1(p) x + \frac{1}{2} k_2(p) x^2 + \frac{1}{6} k_3(p) x^3 + ...
$$

Linearized Equations of Motion:
$$
x''(s) + \left[ k_0^2(s) + k_1(s) \right] x(s) = k_0 \delta
$$
$$
y''(s) - k_1(s) y(s) = 0
$$ {#eq:linearized-eom}

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

$$ \textbf{B}(s) =
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

## Synchrotron Radiation Integrals {#sec:radiation-integrals}

$$ I_5 = \int_0^{C_0} \frac{H_x}{rho^3} \mathrm{d}s
$$ {#eq:i5}

## Natural Emittance {#sec:emittance}

## Lattice Design {#sec:lattice-design}

This sections discusses the concepts introduced using the example of a FODO, a DBA and a TBA lattice.

### The FODO Lattice

### The DBA Lattice

Compare wiedemann 241 vs wolski 3-21

### The TBA Lattice

Compare wiedemann 244
