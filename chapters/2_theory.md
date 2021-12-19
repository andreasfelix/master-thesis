# Beam Dynamics in Electron Storage Rings

This chapter covers all concepts of electron beam dynamics in circular accelerators needed for implementing the developed beam optics code *apace*. The books of H. Wiedemann [@wiedemann], A. Wolski [@wolski], K. Wille [@wille] and, F. Hinterberger [@hinterberger] are the main sources of this chapter.

Electrons in a storage ring oscillate around a curved ideal path. Transforming this ideal orbit away using a different coordinate system than Cartesian coordinates will facilitate our work in the following sections. Therefore, the first section introduces the co-moving Frenet-Serret coordinate system. Next, @sec:equations-of-motion derives the equations of motions in this new coordinate system. Linearizing these equations of motion allows for an analytical description of the particle beam, presented in  @sec:linear-beam-dynamics. The following @sec:chromaticity addresses the effects of energy deviations of the particle beam on the betatron tune and ways to limit these chromatic errors. @sec:synchrotron-radiation provides a brief overview of the effects of synchrotron radiation on the beam properties. Finally, the last section discusses the concepts introduced at the example of different periodic lattices.

## The Co-moving Coordinate System {#sec:frenet-serret-coordinates}

To describe the motion of a particle in circular accelerators, one usually chooses the co-moving *Frenet-Serret coordinates*, whose origin follows the trajectory of the reference particle.

![Co-moving Frenet-Serret coordinate system](figures/frenet-serret-coordinates.svg){#fig:frenet-serret-coordinates}

The three basis vectors

$$
\begin{aligned}
\mathbf{\hat{e}}_\mathrm{s}(s) &= \frac{\mathrm{d} \mathbf{r}_0(s)}{\mathrm{d}  s} & \text{tangent basis vector} \\
\mathbf{\hat{e}}_\mathrm{x}(s) && \text{horizontal basis vector} \\
\mathbf{\hat{e}}_\mathrm{y}(s) &= \mathbf{\hat{e}}_\mathrm{s}(s) \times\mathbf{\hat{e}}_\mathrm{x}(s) & \text{vertical basis vector}
\end{aligned}
$$ {#eq:basis-vectors}

span the Frenet-Serret coordinate system. While the $\mathbf{\hat{e}}_\mathrm{s}(s)$ vector moves tangential to the orbit, the horizontal $\mathbf{\hat{e}}_\mathrm{x}(s)$ and vertical $\mathbf{\hat{e}}_\mathrm{y}(s)$ vectors are perpendicular to it. The $s$ coordinate describes the distance covered on the ideal orbit. The $z$ coordinate defines the path length of the individual particle trajectory. The horizontal and vertical coordinates correspond to $x$ and $y$, respectively. For statements that are valid for both transversal planes, we will use the general variable $u$.

In the Frenet-Serret system, the sum of the coordinate system’s origin $\mathbf{r}_0(s)$, the horizontal displacement $x(s) \mathbf{\hat{e}}_\mathrm{x}(s)$, and the vertical displacement $y(s) \mathbf{\hat{e}}_\mathrm{y}(s)$ from the nominal orbit corresponds to the position vector of the individual particle:

$$
\mathbf{r}(x,y,s) = \mathbf{r}_0(s) + x(s) \mathbf{\hat{e}}_\mathrm{x}(s) + y(s) \mathbf{\hat{e}}_\mathrm{y}(s)
$$ {#eq:frenet-serret-position}

In the following, we use a dot to denote a derivative with respect to time $t$ and a prime mark to denote a derivative with respect to the orbit position $s$. Then the velocity and acceleration in the Frenet-Serret system are

$$
\dot{\textbf{r}}(x,y,s) = \dot{s} x' \mathbf{\hat{e}}_\mathrm{x}(s) + \dot{s} y' \mathbf{\hat{e}}_\mathrm{y}(s) + \dot{s} h \mathbf{\hat{e}}_\mathrm{s}(s)
$$ {#eq:frenet-serret-velocity}

and

$$ \begin{aligned}
\ddot{\textbf{r}}(x,y,s)
&= \left(x''\dot{s}^2 + x' \ddot{s} - h \kappa_\mathrm{x0} \dot{s}^2 \right) \mathbf{\hat{e}}_\mathrm{x}(s) \\
&+ \left(y'' \dot{s}^2 + y' \ddot{s} - h \kappa_\mathrm{y0} \dot{s}^2\right) \mathbf{\hat{e}}_\mathrm{y}(s) \\
&+ \left(2 \kappa_\mathrm{x0} x'\dot{s}^2+ 2 \kappa_\mathrm{y0} y'\dot{s}^2+h \ddot{s}\right) \mathbf{\hat{e}}_\mathrm{s}(s) .
\end{aligned}
$$ {#eq:frenet-serret-acceleration}

Here we introduced

$$
h = 1 + \kappa_\mathrm{x0} x + \kappa_\mathrm{y0} y ,
$$ {#eq:needsaname}

where $\kappa_\mathrm{x0}$ and $\kappa_\mathrm{y0}$ correspond to the horizontal and vertical curvature of the ideal orbit, respectively.

## Equations of Motion {#sec:equations-of-motion}

A particle with the charge $q$ and the mass $m$ moving through a structure of magnets experiences the magnetic part of the Lorentz force, which defines its equations of motion

$$
\ddot{\mathbf{r}} = \frac{q}{m} (\dot{\mathbf{r}} \times \mathbf{B}) ,
$$ {#eq:lorentz-force}

where $\mathbf{B}$ is the magnetic field vector. Assuming a vanishing longitudinal component of the magnetic field $B_\mathrm{z} \approx 0$, we obtain the equations of motion in the Frenet-Serret coordinates by substituting @eq:frenet-serret-velocity and @eq:frenet-serret-acceleration into @eq:lorentz-force:

$$ \begin{aligned}
x'' \dot{s}^2 + x' \ddot{s} - \dot{s}^2 \kappa_\mathrm{x0} h &= -\frac{q}{m} B_\mathrm{y}  h \dot{s}\\
y'' \dot{s}^2 + y' \ddot{s} - \dot{s}^2 \kappa_\mathrm{y0} h &= \frac{q}{m} B_\mathrm{x}  h \dot{s}
\end{aligned}
$$ {#eq:eom-1}

The second time derivate of the orbit position $\ddot{s}$ changes when a particle travels with an offset through a bending magnet or when it moves with an angle divergence to the orbit. However, as the transversal velocities of a relativistic particle beam are small compared to the longitudinal components, the first time derivate of the orbit position $\dot{s}$ changes slowly. Therefore we can approximate

$$
\ddot{s} \approx 0,
$$ {#eq:zero-ddot-s}

simplifying the equations of motion

$$ \begin{aligned}
x'' &= -\frac{q h}{m \dot{s}} B_\textup{y} + \kappa_\textup{x0} h \\
y'' &= \frac{q h}{m \dot{s}} B_\textup{x} + \kappa_\textup{y0} h .
\end{aligned}
$$ {#eq:eom-2}

When a magnetic field deflects a charged particle, the Lorentz force takes the place of the centripetal force

$$ \begin{aligned}
\mathbf{F}_\mathrm{centripetal} &= \mathbf{F}_\mathrm{Lorentz} \\
- m v^2 \boldsymbol{\kappa} &= q (\dot{\mathbf{r}} \times \mathbf{B}) .
\end{aligned}
$$ {#eq:lorentz-force-centripetal}

Here, the horizontal $\kappa_\mathrm{x}$ and vertical $\kappa_\mathrm{y}$ curvatures are defined as the curvatures experienced by an on-momentum particle due to the magnet lattice:

$$
\begin{aligned}
\kappa_\mathrm{x} (x,y,s) = \frac{1}{\rho_\mathrm{x} (x,y,s)} &= \frac{q}{p_0} B_\mathrm{y}(x,y,s) \\
\kappa_\mathrm{y} (x,y,s) = \frac{1}{\rho_\mathrm{y} (x,y,s)} &=-\frac{q}{p_0} B_\mathrm{x}(x,y,s)
\end{aligned}
$$ {#eq:curvature-lorentz}

![Path length difference between the orbit and an individual particle trajectory](figures/path-length-difference.svg){#fig:path-length-difference}

Applying the linear approximation of the relationship between the path length of the orbit and the path length of an individual particle trajectory

$$ \mathrm{d}z = (1 + \kappa_\mathrm{x0} x + \kappa_\mathrm{y0} y) \mathrm{d}s + \mathcal{O}(2),
$$ {#eq:path-length-difference}

shown in @fig:path-length-difference, yields the momentum as an expression of the time derivative of the orbit position $\dot{s}$:

$$ p = m v \approx (1 + \kappa_\mathrm{x0} x + \kappa_\mathrm{y0} y) \dot{s} = m h \dot{s}
$$ {#eq:momentum-orbit-position}

We define the relative momentum deviation

$$ \delta = \frac{\Delta p}{p_0}
$$ {#eq:relative-momentum-deviation}

as the ratio of the momentum deviation $\Delta p$ and the momentum of the ideal particle $p_0$. Then we can express a particle's momentum

$$
p = p_0 + \Delta p = p_0 (1 + \delta)
$$ {#eq:momentum-as-relative-momentum}

in terms of its momentum deviation $\delta$ and the ideal momentum $p_0$.

Subsituting @eq:curvature-lorentz, @eq:momentum-orbit-position, and @eq:momentum-as-relative-momentum into @eq:eom-2, we obtain a second-order differential equation for the equations of motion

$$
\begin{aligned}
x'' &= - \frac{h^2}{(1 + \delta)} \kappa_\mathrm{x} + h \kappa_\mathrm{x0} \\
y'' &=  \frac{h^2}{(1 + \delta)} \kappa_\mathrm{y} + h \kappa_\mathrm{y0},
\end{aligned}
$$ {#eq:eom-integratable}

completely defined by the geometric multipole strengths of the magnetic lattice of the accelerator

$$
\begin{aligned}
\kappa_\mathrm{x}(x,y,s) &= \kappa_\mathrm{x0}(s) + k(s) x + m(s) (x^2 - y^2) + ... \\
\kappa_\mathrm{y}(x,y,s) &= \kappa_\mathrm{y0}(s) + k(s) y + m(s) x y + ... \; .
\end{aligned}
$$ {#eq:expansion-of-curvature}

Integrating @eq:eom-integratable yields the individual particle trajectories and can be used to track particles through non-linear elements. An experimental implementation of this method is included in the developed code, but it is not as performant as other tracking methods of more mature codes. Nevertheless, it was, for example, used to create the plots in @sec:chromaticity.

## Linear Beam Dynamics {#sec:linear-beam-dynamics}

@eq:eom-integratable does not allow for analytical investigations. Courant and Synder @courantsnyder developed a formalism that allows describing the particle beam using analytic quantities by linearizing the equations of motion. My bachelor's thesis @andreas_ba thoroughly discussed the theory of linear beam dynamics. Therefore this section skips most of the derivations and only provides a summary of the most important results.

### Linearized Equations of Motion

To linearize @eq:eom-integratable, we expand the expression

$$
\frac{1}{1 + \delta} =  1 - \delta + \mathcal{O}(2)
$$ {#eq:taylor-momentum}

in $\delta$, leading to:

$$
\begin{aligned}
x'' &= - (1 - \delta)(1 + \kappa_\mathrm{x0})^2 (\kappa_\mathrm{x0} + k x) + \kappa_\mathrm{x0} (1 + \kappa_\mathrm{x0} x)\\
y'' &= (1 - \delta)(1 + \kappa_\mathrm{x0})^2 k y
\end{aligned}
$$ {#eq:eom-momentum-approximaton}

Multiplying out the parentheses and only keeping terms linear in $x$, $y$, and $\delta$, we obtain the linearized equations of motion:

$$
\begin{aligned}
x'' + (\kappa_\mathrm{x0}^2 + k) x &= \kappa_\mathrm{x0} \delta \\
y'' - k y &= 0
\end{aligned}
$$ {#eq:eom-linearized}

@eq:eom-linearized is a linear second order differential equation, which can be solved analytically. Therefore, the transformation of the particle trajectory

$$
\begin{aligned}
\textbf{X}(s) =
\begin{pmatrix}
x(s) \\ x'(s) \\ y(s) \\ y'(s) \\ l(s) \\ \delta(s)
\end{pmatrix}
=
\begin{pmatrix}
\textup{horizontal offset} \\ \textup{horizontal slope} \\ \textup{vertical offset}\\ \textup{vertical slope} \\ \textup{longitudinal offset}  \\ \textup{relative momentum deviation}
\end{pmatrix}
\end{aligned}
$$ {#eq:particle-vector}

through beam transport elements can be described as a matrix multiplication

$$ \textbf{X}(s+L) = \textbf{R}(s,s+L) \textbf{X}(s) ,
$$ {#eq:transformation-particle-vector}

where $\mathbf{R}$ is a $6 \times 6$ transfer matrix. The solutions of @eq:eom-linearized for a drift section ($\kappa_\mathrm{x0} = k = 0$), for a dipole magnet ($\kappa_\mathrm{x0} \neq 0, k = 0$), and for a quadrupole ($\kappa_\mathrm{x0} = 0, k \neq 0$) are included in @sec:appendix-transfer-matrices.

### Betatron Oscillation {#sec:betatron-oscillation}

Tracking a particle through the beam transport system by applying the different transfer matrices of beam transport elements yields the individual particle trajectory. However, Courant and Synder @courantsnyder developed a formalism, revealing more insightful analytical properties of the entire particle beam. The *Courant-Snyder functions*, sometimes called *Twiss parameters*, arise from separating the on- and off-momentum motion.

Therefore, we first solve the linearized equations of motion, @eq:eom-linearized, for the *dispersion-free* case, leading us to the most fundamental quantity of the transversal beam motion, the beta function $\beta(s)$. Then, in @sec:dispersion, we introduce the dispersion function $\eta(s)$ to account for the transverse motions caused by momentum deviations.

By neglecting the off-momentum terms and combining the focusing terms into one parameter $K_\mathrm{x}(s) = \kappa_\mathrm{x0}^2(s) + k(s)$ for the horizontal and $K_\mathrm{y}(s) = - k(s)$ for the vertical plane, the linear equations of motion become

$$ u''(s) + K_u(s) u(s) = 0 .
$$ {#eq:hill-equation}

@eq:hill-equation, known as *Hill's equation*, is a second-order linear ordinary differential equation similar to the harmonic oscillator. The difference is that the parameter $K(s) = K(s + C)$ is not constant but is a function periodic with the circumference of the accelerator $C$. The *Floquet's theorem* states that Hill's equation has two linearly independent solutions, given by the product of a complex exponential function and a periodic function @magnus_winkler. The real part of the general solution of Hill's equation is

$$ u(s) = \sqrt{\epsilon_u \beta_u (s)} \cos(\psi_u(s) + \psi_{u0}),
$$ {#eq:betatron-oscillation}

where we identify the integration constants $\epsilon$ and $\psi_0$ with the emittance and the initial betatron phase, respectively. The beta function $\beta_u(s)$ is periodic with the circumference of the accelerator $C$.

![The envelope of a particle beam at the example of a FODO cell. The right plot shows the betatron oscillation for 33 electrons with an emittance of 5 nm rad. (extracted from @andreas_ba)](figures/betatron-oscillation.svg){#fig:betatron-oscillation}

@fig:betatron-oscillation shows the particle trajectories and the beam envelope as defined by @eq:betatron-oscillation. The individual particles oscillate within the envelope

$$ E(s) = \pm \sqrt{\epsilon \beta(s)} .
$$ {#eq:betatron-envelope}

As the beta function $\beta(s)$ determines the shape of this envelope, and therefore the transverse beam size, it is considered one of the most important quantities in circular accelerator physics.

By substituting @eq:betatron-oscillation and its second derivative into @eq:hill-equation, we obtain an expression for the *betatron phase*

$$ \psi_u(s) = \int_0^s \frac{\mathrm{d} s^*}{\beta_u(s^*)} .
$$ {#eq:betatron-phase}

The *tune*

$$ Q_u = \frac{1}{2 \pi}\int_s^{s+C} \frac{d s^*}{\beta_u (s^*)}
$$ {#eq:tune}

describes the number of betatron oscillations per turn.

By rearranging @eq:betatron-oscillation and its first derivative with respect to the orbit position $s$

$$ u'(s) = -\frac{\sqrt{\epsilon}}{\sqrt{\beta_u (s)}}(\alpha_u(s)\cos(\psi_u(s) + \psi_{u0}) + \sin(\psi_u(s) + \psi_{u0})) ,
$$ {#eq:betatron-oscillation-first-derivative}

we obtain an ellipse equation for the Twiss parameters

$$ \epsilon_u = \gamma_u(s) u^2(s) + 2 \alpha_u(s) u(s)u'(s) + \beta_u(s) u'^2(s) ,
$$ {#eq:phase-space-ellipse}

where

$$ \alpha(s) := \frac{-\beta'(s)}{2}
$$

and

$$ \gamma(s) := \frac{1 + \alpha^2(s)}{\beta(s)} .
$$

Following @eq:phase-space-ellipse, the trajectory of betatron oscillation forms an ellipse in the $(u, u')$-phase space. The Twiss parameters $\alpha(s)$, $\beta(s)$, and $\gamma(s)$ determine the shape of this ellipse at the orbit position $s$. The emittance $\epsilon$, which we introduced as an integration constant, describes the occupied phase space volume of the ellipse $A = \pi \epsilon$, according to *Liouville's theorem* a constant of motion @Nolting2018.

Furthermore, supposing the Twiss parameters $\alpha$, $\beta$, and $\gamma$ are know for the positons $s$ and $s + L$. Then, the 2×2-sub-matrices $\mathbf{R}_u^{2\times 2}(s,L)$ of $\mathbf{R}(s, L)$ describing the transformation of a particle from the orbit position $s$ to $s + L$ within horizontal or vertical plane is

$$ \mathbf{R}_u^{2\times 2}(s,L) =
\begin{pmatrix}
\sqrt{\frac{\beta_1}{\beta_0}}(\cos{\psi_1} + \alpha_0 \sin{\psi_1}) & \sqrt{\beta_0\beta_1} \sin{\psi_1} \\
\frac{\alpha_0 - \alpha_1}{\sqrt{\beta_0\beta_1}} \cos{\psi_1} - \frac{1 + \alpha_0\alpha_1 }{\sqrt{\beta_0\beta_1}} \sin{\psi_1}  & \sqrt{\frac{\beta_0}{\beta_1}}(\cos{\psi_1} - \alpha_1 \sin{\psi_1}) ,
\end{pmatrix}
$$ {#eq:transfer-matrix-beta}

where $\beta_0 = \beta_u(s)$, $\beta_1 = \beta_u(s+L)$, $\alpha_0 = \alpha_u(s)$, $\alpha_1 = \alpha_u(s+L)$, and $\psi_1 = \psi_u(s+L)$.


### Transformation of the Twiss parameters {#sec:transformation-twiss-parameter}

@eq:phase-space-ellipse can be written in matrix form:

$$
\epsilon_u =
\begin{pmatrix}
u(s) & u'(s)
\end{pmatrix}
\begin{pmatrix}
\gamma_u(s) & \alpha_u(s) \\
\alpha_u(s) & \beta_u(s)
\end{pmatrix}
\begin{pmatrix}
u(s) \\
u'(s)
\end{pmatrix}
$$ {#eq:phase-space-ellipse-matrix}

We define the *Twiss matrix*

$$ \mathbf{B}_u(s) =
\begin{pmatrix}
\beta_u(s) & -\alpha_u(s) \\
-\alpha_u(s) & \gamma_u(s)
\end{pmatrix} .
$$ {#eq:beta-matrix}

Since the emittance $\epsilon$ is the same at the position $s$ and $s + L$, rearranging @eq:phase-space-ellipse-matrix

$$
\begin{aligned}
\epsilon & = \textbf{X}^\mathrm{T}(s) \textbf{B}^{-1}(s) \textbf{X}(s) \\
& = \textbf{X}^\mathrm{T}(s) \textbf{R}^\mathrm{T} (\textbf{R}^\mathrm{T})^{-1} \textbf{B}^{-1}(s) \textbf{R}^{-1} \textbf{R} \textbf{X}(s) \\
& = (\textbf{R} \textbf{X}(s) )^\mathrm{T} (\textbf{R} \textbf{B}(s) \textbf{R}^\mathrm{T})^{-1} (\textbf{R} \textbf{X}(s)) \\
& = \textbf{X}^\mathrm{T}(s+L) (\textbf{R} \textbf{B}(s) \textbf{R}^\mathrm{T})^{-1} \textbf{X}(s+L) \\
& \overset{!}{=} \textbf{X}^\mathrm{T}(s+L) \textbf{B}^{-1}(s+L) \textbf{X}(s+L),
\end{aligned}
$$ {#eq:transformation-beta-matrix-derivation}

results in an expression for the transformation of the Twiss parameters

$$ \mathbf{B}(s+L) = \mathbf{R}(s,L) \mathbf{B}(s) \mathbf{R}^\mathrm{T}(s,L) .
$$ {#eq:transformation-beta-matrix}

Multiplying the matrices of @eq:transformation-beta-matrix yields a system of linear equations

$$
\begin{aligned}
\beta(s+L) &= R_{11}^2\beta(s)-2R_{11}R_{12}\alpha(s)+R_{12}^2\gamma(s)\\
\alpha(s+L) &= -R_{11}R_{12}\beta(s)+(R_{11}R_{22}+R_{12}^2)\alpha(s)+R_{12}R_{22}\gamma(s)\\
\gamma(s+L) &= R_{12}^2\beta(s)-2R_{12}R_{22}\alpha(s)+R_{22}^2\gamma(s) .
\end{aligned}
$$ {#eq:betatron-function-transformation}

For a stable solution to exist, the Twiss functions must have the same value after one revolution, leading to the periodicity condition for circular accelerators

$$
\begin{aligned}
\beta(s)  &= \beta(s + C_0)  \\
\alpha(s) &= \alpha(s + C_0) \\
\gamma(s) &= \gamma(s + C_0) ,
\end{aligned}
$$ {#eq:beta-perodicity-condition}

where $C_0$ is the length of the ideal orbit. Using this condition we can solve the system of linear equations of @eq:betatron-function-transformation, yielding the Twiss functions as expression of the one-turn-matrix $\mathbf{R}(s, C_0)$:

$$
\begin{aligned}
\beta(s)  &= \frac{2 R_{12}}{\sqrt{2 - R_{11}^2 - 2 R_{12} R_{21} - R_{22}^2}} \\
\alpha(s) &= \frac{R_{11}-R_{22}}{2 R_{12}} \beta(s) \\
\gamma(s) &= \frac{1 + \alpha^2(s)}{\beta(s)}.
\end{aligned}
$$ {#eq:beta-initial-values}

From the expression of the beta function $\beta(s)$ in @eq:beta-initial-values, it follows that a stable solution only exists for

$$ 2 - R_{11}^2 - 2 R_{12} R_{21} - R_{22}^2 > 0 ,
$$ {#eq:stability-condition}

defining a stability criteria.

### Dispersion {#sec:dispersion}

The *dispersion function*

$$ \eta_u(s) = \frac{\mathrm{d} u(s)}{\mathrm{d} \delta}
$$ {#eq:dispersion-function-definition}

describes the change in the transverse offset $u(s)$ with respect to the relative momentum deviation $\delta$. Therefore, the trajectory of an off-momentum particle is given by the sum of the betatron oscillation $u_\beta(s)$ and the dispersive offset $u_\delta = \eta_u(s) \delta$:

$$ u(s) = u_\beta(s) + u_\delta(s) = u_\beta(s) + \eta_u(s) \delta
$$ {#eq:transverse-offset-dispersion}

Supposing the values of the dispersion function $\eta(s)$ and its derivative $\eta'(s)$ are known at the orbit position $s$. Then, the transfer matrix $\mathbf{R}(s, L)$ determines their values at the orbit position $s + L$:

$$
\begin{aligned}
\eta(s + L) &= R_{11} \eta(s) + R_{12} \eta'(s) + R_{16} \\
\eta'(s + L) &= R_{21} \eta(s) + R_{22} \eta'(s) + R_{26}
\end{aligned}
$$ {#eq:dispersion-transformation}

Using the periodicity condition for circular accelerators

$$
\begin{aligned}
\eta(s)  &= \eta(s + C_0)  \\
\eta'(s) &= \eta'(s + C_0)
\end{aligned}
$$ {#eq:dispersion-perodicity-condition}

the dispersion function $\eta(s)$ and its derivative $\eta'(s)$ can be expressed in terms of the one-turn-matrix $\mathbf{R}(s, C_0)$:

$$
\begin{aligned}
\eta(s)  &= \frac{R_{16}(1 - R_{22}) + R_{12}R_{26}}{2 - R_{11} - R_{22}} \\
\eta'(s) &= \frac{R_{16}(1 - R_{11}) + R_{21}R_{16}}{2 - R_{11} - R_{22}}
\end{aligned}
$$ {#eq:dispersion-initial-values}

To calculate the graph of $\eta(s)$ and $\eta'(s)$ along the entire ring, @eq:dispersion-initial-values can be used to calculate the values $\eta_0  = \eta(s_0)$ and $\eta'_0  = \eta'(s_0)$ at an initial orbit position $s_0$. Afterward, @eq:dispersion-transformation yields the values of $\eta(s)$ and $\eta'(s)$ for all other orbit positions $s$.


### Momentum Compaction

The *momentum compaction factor*

$$
\begin{aligned}
\alpha_\mathrm{c} = \frac{1}{C_0}\frac{\mathrm{d} C}{\mathrm{d}\delta} \quad \mathrm{with} \quad C = C_\beta + \Delta C_\delta,
\end{aligned}
$$ {#eq:momentum-compation-factor}

is defined as the ratio between the change in the path length of a dispersive particle for one revolution $C$ with respect to the relative momentum deviation $\delta$ and the path length of the ideal orbit $C_0$. While $C_\beta$ is the path length of an on-momentum particle,

$$
\Delta C_\delta = C - C_\beta = \int_0^{C} \mathrm{d} z - \int_0^{C_\beta} \mathrm{d} z'
$$ {#eq:dispersive-path-length}

corresponds to the path length difference caused by the momentum deviation. Applying the linear approximation of the path length element $\mathrm{d}z \approx (1 + \kappa_\mathrm{x0} x) \mathrm{d}s$, introduced in @eq:path-length-difference, to @eq:dispersive-path-length yields

$$
\begin{aligned}
\Delta C_\delta &= \int_0^{C_0} 1 + \kappa_\mathrm{x0}(s) (u_\beta(s) + u_\delta(s)) \mathrm{d} s - \int_0^{C_0} 1 + \kappa_\mathrm{x0}(s)u_\beta(s) \mathrm{d} s \\
&= \delta \int_0^{C_0} \kappa_\mathrm{x0}(s) \eta(s)  \mathrm{d} s .
\end{aligned}
$$ {#eq:dispersive-path-length-approximation}

Substituting @eq:dispersive-path-length-approximation into @eq:momentum-compation-factor, we obtain an expression for the momentum compaction factor

$$
\begin{aligned}
\alpha_\textup{c} = \frac{1}{C_0} \int_0^{C_0} \kappa_\mathrm{x0}(s) \eta(s)  \mathrm{d} s ,
\end{aligned}
$$ {#eq:momentum-compation-factor-expression}

corresponding to the mean value of the product between the curvature of the ideal orbit $\kappa_\mathrm{x0}(s)$ and the dispersion function $\eta(s)$.


## Chromaticity {#sec:chromaticity}

As discussed in the previous section, many effects of beam dynamics can be explained by the analysis of the linear equations of motion. However, certain phenomena can only be understood considering the higher-order terms.

The first subsection discusses the influence of energy deviations on the betatron tune and why they are harmful to the beam quality. Using elements with non-linear field components can limit these effects, described in the following subsection.

### Natural Chromaticity in a Storage Ring {#sec:natural-chromaticity}

The number of betatron oscillations per turn, defined by the tune, is determined by the position and strength of the quadrupole and bending magnets. However, as the experienced multipole strength of a particle depends on its momentum, off-momentum particles will complete a different number of betatron oscillations per turn. @fig:chromaticity-quadrupole shows the influence of the momentum deviation on the focal length of a quadrupole. Generally, particles with a higher momentum $\delta > 0$ are less deflected by a quadrupole, resulting in fewer betatron oscillations. On the other hand, particles with a negative momentum deviation $\delta < 0$ undergo a larger deflection, leading to a higher tune.

![Impact of the momentum deviation on the focal length of a quadrupole. The trajectories were calculated by integrating @eq:eom-integratable. The dashed lines correspond to the particle trajectories without momentum deviation $\delta = 0$. The stronger deflection for particles with $\delta < 0$ (red) leads to a shorter focal length. Particles with $\delta > 0$ (blue) are less deflected, resulting in a longer focal length. In the case of on-momentum particle $\delta = 0$ (green), the trajectories are identical to the linear case.](figures/chromaticity-quadrupole.svg){#fig:chromaticity-quadrupole}

The *chromaticity*

$$
\xi_\mathrm{u} = \frac{\mathrm{d} Q_\mathrm{u}}{\mathrm{d} \delta}
$$ {#eq:chromaticity-definition}

describes the change in the betatron tune with respect to the relative momentum deviation $\delta$. In linear approximation, the perturbed quadrupole strength caused by the momentum deviation

$$
k_\mathrm{p}(s, p) = \frac{q}{p}\frac{\mathrm{d}B_\mathrm{y}}{\mathrm{d}x} = \frac{q}{p_0(1 + \delta)}\frac{\mathrm{d}B_\mathrm{y}}{\mathrm{d}x} \approx (1 - \delta)\frac{q}{p_0}\frac{\mathrm{d}B_\mathrm{y}}{\mathrm{d}x} = k + \Delta k
$$ {#eq:quadrupole-strength}

has the same effect as a gradient error

$$
\Delta k = -k\delta .
$$ {#eq:quadrupole-error}

Therefore, to derive the effect of this gradient error, we introduce a perturbation in form of a thin quadrupole 

$$ \mathbf{Q}_\mathrm{p} =
\begin{pmatrix}
1 & 0 \\
-\Delta k \mathrm{d}s & 1
\end{pmatrix}
$$ {#eq:quadrupole-pertubation}

with the infinite focal lenth $\frac{1}{\Delta k \mathrm{d}s}$. Here we look at the 2×2-sub matrix, which only transforms the horizontal or vertical componentes of the particle vector $\mathbf{X}$. According to @eq:transfer-matrix-beta the 2×2-one-turn-matrix in the horizontal or vertical plane

$$ \mathbf{R} =
\begin{pmatrix}
\cos{\Psi} + \alpha_0 \sin{\Psi} & \beta_0 \sin{\Psi} \\
-\frac{1 + \alpha_0^2}{\beta_0} \sin{\Psi} & \cos{\Psi} - \alpha_0 \sin{\Psi}
\end{pmatrix}
$$ {#eq:one-turn-beta}

can be written as an expression of the Twiss parameters, where $\Psi = 2 \pi Q$. Hence, we can express the perturbed one-turn-matrix in terms of the unperturbed Twiss parameters:

$$
\begin{aligned}
\mathbf{R}_\mathrm{p} &= \mathbf{R} \mathbf{Q}_\mathrm{p} \\
&=
\begin{pmatrix}
\cos \Psi + \alpha_0 \sin{\Psi} & \beta_0 \sin \Psi \\
- \frac{1}{\beta_0} \sin \Psi & \cos \Psi - \alpha_0 \sin{\Psi}
\end{pmatrix}
\begin{pmatrix}
1 & 0 \\
- \Delta k \mathrm{d}s & 1
\end{pmatrix} \\
&= \begin{pmatrix}
\cos \Psi + \alpha_0 \sin{\Psi}  - \beta_0 \Delta k \mathrm{d}s \sin \Psi & \cdots \\
\cdots & \cos \Psi - \alpha_0 \sin{\Psi} 
\end{pmatrix} \\
\end{aligned}
$$ {#eq:one-turn-pertubation}

By calculating the trace of the perturbed one-turn-matrix

$$
\begin{aligned}
\mathrm{Tr}(\mathbf{R}_\mathrm{p}) &\overset{!}{=} \mathrm{Tr}(\mathbf{R}\mathbf{Q}_\mathrm{p}) \\
2 \cos \Psi_\mathrm{p} &= 2 \cos \Psi - \beta_0 \Delta k \mathrm{d}s \sin \Psi
\end{aligned}
$$ {#eq:trace-one-turn-pertubation}

we obtain

$$
\cos{\Psi} \cos{\mathrm{d}\Delta\Psi} - \sin{\Psi} \sin{\mathrm{d}\Delta\Psi} = \cos \Psi - \frac{1}{2}\beta_0 \Delta k \mathrm{d}s \sin \Psi,
$$ {#eq:trace-one-turn-pertubation-approx}

where $\Psi_\mathrm{p} = \Psi + \mathrm{d}\Delta\Psi$. For small tune pertubations $\Delta Q$, we can use the small-angle approximiation of the trigonometric functions $\cos{\mathrm{d}\Delta\Psi} \approx 1$ and $\sin{\mathrm{d}\Delta\Psi} \approx \mathrm{d}\Delta\Psi$, resulting in an expression for the differential of the tune pertubation 

$$
\begin{aligned}
\mathrm{d} \Delta Q &= \frac{1}{4 \pi} \beta_0 \Delta k \mathrm{d}s \\
&= -\frac{1}{4 \pi} \delta \beta_0 k \mathrm{d}s .
\end{aligned}
$$ {#eq:tune-differential}

By integrating @eq:tune-differential and substituting it into @eq:chromaticity-definition, we obtain an expression for the *natural chromaticities*

$$
\begin{aligned}
\xi_\mathrm{x}^\mathrm{n} &= - \frac{1}{4 \pi} \int_0^C \beta_\mathrm{x}(s) k(s) \mathrm{d} s \\
\xi_\mathrm{y}^\mathrm{n} &= + \frac{1}{4 \pi} \int_0^C \beta_\mathrm{y}(s) k(s) \mathrm{d} s ,
\end{aligned}
$$ {#eq:natural-chromaticities}

which only takes the contribution of the momentum-dependent quadrupole strength into account. Since particles with a positive momentum deviation ($\delta > 0$) experience a weaker focusing, the natural chromaticities $\xi_u^\mathrm{n}$ are always negative.

### Chromaticity Correction

Two effects cause chromaticities to be undesirable in circular accelerators, making it necessary to correct for these chromatic errors. First, resonances between the betatron oscillation and the magnetic fields arising at specific values of the betatron tune can lead to a beam loss. Thus, for high chromaticities, where even particles with small momentum deviations experience a large tune shift, moving particles into resonance becomes more likely. Moreover, particles have vastly different tunes for high chromaticities, corresponding to a tune spread in the tune diagram. Hence, the accelerator has to be operated at a distance to the nearest resonances larger than the tune spread, imposing strict constraints on possible tunes and making it challenging to choose an operational tune.

Secondly, so-called *head-tail instabilities*, a collective effect between the electrons of the head and tail of a bunch, grow proportional with the chromaticity.

![Influence of sextupole placed at a position of non-zero dispersion. Similar to @fig:chromaticity-quadrupole, the trajectories were calculated by integrating @eq:eom-integratable. The dashed lines correspond to the particle trajectories without momentum deviation $\delta = 0$. The non-linearity of the sextupole corrects the chromatic error of the quadrupole, resulting in a focal point of the dispersive particle.](figures/chromaticity-sextupole.svg){#fig:chromaticity-sextupole}

Non-linear elements can compensate for the chromaticities introduced by the momentum-dependent quadrupole strength. The goal is to give particles with a positive momentum deviation $\delta > 0$ an additional kick and counterbalance the stronger kick, which particles with a negative momentum deviation $\delta < 0$ experience. @fig:chromaticity-sextupole shows a sextupole compensating for the chromaticity introduced by a quadrupole. A sextupole magnet behaves in one plane like an amplitude-dependent quadrupole magnet. Therefore, a sextupole has the desired effect at a position of dispersion $\eta \neq 0$, where the particles are sorted by their momentum deviation $\delta$.

Using the additional sextupole kick experienced by a dispersive particle $\Delta k = m \eta \delta$, we can, analog to @sec:natural-chromaticity, derive an expression for the part of the chromaticity introduced by the sextupole magnets

$$
\begin{aligned}
\xi_\mathrm{x}^\mathrm{s} &= + \frac{1}{4 \pi} \int_0^C \beta_\mathrm{x}(s) m(s) \eta_\mathrm{x}(s) \mathrm{d} s \\
\xi_\mathrm{y}^\mathrm{s} &= - \frac{1}{4 \pi} \int_0^C \beta_\mathrm{y}(s) m(s) \eta_\mathrm{x}(s) \mathrm{d} s .
\end{aligned}
$$ {#eq:natural-chromaticities-sextupoles}

We obtain the total chromaticity from the sum of the natural chromaticity $\xi^\mathrm{n}$ and the chromaticity caused by the sextupole magnets $\xi^\mathrm{s}$

$$
\begin{aligned}
\xi_\mathrm{x} &= - \frac{1}{4 \pi} \int_0^C \beta_\mathrm{x}(s) (k(s) - m(s) \eta_\mathrm{x}(s)) \mathrm{d} s \\
\xi_\mathrm{y} &= + \frac{1}{4 \pi} \int_0^C \beta_\mathrm{y}(s) (k(s) - m(s) \eta_\mathrm{x}(s)) \mathrm{d} s .
\end{aligned}
$$ {#eq:natural-chromaticities-total}

## Synchrotron Radiation {#sec:synchrotron-radiation}

A resting electron produces a static electric field but does not emit radiation, which would violate the law of conservation of energy since a stationary electron has no kinetic energy to use. The same must hold for a uniformly moving electron as it is stationary in another inertial frame of reference. However, if a charged particle is accelerated, it produces an electromagnetic wave. According to Maxwell's equations, the change in the electric field results in a magnetic field. In turn, the variations of the magnetic field produce an electric field. These periodical oscillations in the electromagnetic field, which propagate energy at the speed of light $c$, are known as *electromagnetic radiation*.

In the case of a charged particle in a circular accelerator where it is accelerated radially in a bending magnet, undulator, or wiggler at relativistic speed, this radiation is called *synchrotron radiation*. The previous sections discussed the beam dynamics while neglecting the emission of synchrotron radiation. However, the random emission of photons of a radially accelerated electron influences the amplitude of its betatron and synchrotron oscillations, which changes the beam emittance.

At first, this might seem like a violation of Liouville's theorem @Nolting2018: It describes the time evolution of an ensemble of classical systems and states that the phase-space distribution of these systems is constant along any path. However, it is also applicable to a single system of $N$ non-interacting electrons as such a system can be seen equivalent to an ensemble of $N$ systems. Thus, for non-interacting electrons, the emittance, which corresponds to the occupied volume in phase space, must be conserved. However, as soon as an electron emits a photon, the electron beam emittance only occupies a sub-volume of the total electron-photon phase space, spanned by the coordinates of the electron and photon. Thus due to the synchrotron radiation and consistent with Liouville's theorem, the beam emittance can change. Nevertheless, Liouville's theorem still holds for the entire electron-photon system. Therefore, contrary to a proton beam, where the synchrotron radiation is neglectable, the electron beam emittance is not a constant of motion. 

In the following, we will derive the influence of synchrotron radiation on the electron beam emittance, where the report of Sands @sands1970 was the primary source for this section. It is convenient to define the five so-called *synchrotron radiation integrals* @helm1973, to facilitate the mathematical work:

$$ I_1 = \int_0^{C} \kappa_\mathrm{x0}(s)\eta_\mathrm{x}(s) \mathrm{d}s
$$ {#eq:i1}

$$ I_2 = \int_0^{C} \kappa_\mathrm{x0}(s)^2 \mathrm{d}s
$$ {#eq:i2}

$$ I_3 = \int_0^{C} |\kappa_\mathrm{x0}(s)|^3  \mathrm{d}s
$$ {#eq:i3}

$$ I_4 = \int_0^{C} \kappa_\mathrm{x0}(s) \eta_\mathrm{x}(s) \left(\kappa_\mathrm{x0}(s)^2 + 2 k(s) \right)\mathrm{d}s
$$ {#eq:i4}

$$ I_5 = \int_0^{C} |\kappa_\mathrm{x0}(s)|^3 \mathcal{H}_\mathrm{x} (s) \mathrm{d}s
$$ {#eq:i5}

With

$$ \mathcal{H}_\mathrm{x} = \gamma_\mathrm{x} \eta_\mathrm{x}^2 + 2 \alpha_\mathrm{x} \eta_\mathrm{x} \eta_\mathrm{x}' + \beta_\mathrm{x} \eta_\mathrm{x}'^2.
$$ {#eq:curly-h}

we introduced the so-called *curly $\mathcal{H}$ function*, fully defined by the Twiss parameters. Note that for an accurate calculation of the fourth synchrotron radiation integral in @eq:i4 we also have to consider the dipole edge focusing. In the developed code, this was adopted from the MAD-X source @madx.

### Radiation Damping of Betatron Oscillations

![Radiation damping of the betatron oscillation. The emission of a photon changes the transverse and longitudinal components of an electron's momentum. But as the cavity only refills the longitudinal component, the transverse momentum components decrease over time.](figures/betatron-oscillation-damping.svg){#fig:betatron-oscillation-damping}

As shown in @fig:betatron-oscillation-damping, a radially accelerated electron emits synchrotron radiation in its general direction of motion, leading to a decrease of the longitudinal and transversal components of its momentum. However, the electric field of the cavity only restores the electron's longitudinal momentum. Over time, the interplay of both of these effects leads to a damping of the electron's betatron oscillation. While this effect is commonly called the *radiation damping*, the damping of the betatron oscillations occurs in the cavity. The emission of synchrotron radiation does not - apart from slightly changing the focusing strength of the magnets due to the energy loss - directly affect the amplitude of the betatron oscillations. However, the damping is still a second-order effect of the synchrotron radiation, as, without it, the cavity would not restore the longitudinal momentum.

To quantify the influence of the synchrotron radiation on the amplitude of the betatron oscillations, we make some assumptions:

* First, we assume the emission of synchrotron radiation is precisely parallel to the momentum of the electron.
* Second, we assume a continuous emission of synchrotron radiation over a given path length.
* Finally, we assume the acceleration happens continuously along the ring.

Under these assumptions, the betatron oscillations would dampen to zero. However, due to the quantum nature of photons, the emission happens in discrete chunks of energy, making the second assumption not entirely reasonable. The discrete emissions lead to a counteracting excitation which will be considered in @sec:quantum-excitation.

We recall the definition of the emittance

$$ \epsilon_u = \gamma_u u^2 + 2 \alpha_u uu' + \beta_u u'^2 ,
$$ {#eq:phase-space-ellipse-radiation-damping}

from @eq:phase-space-ellipse. Note that the coordinates $u$ and $u'$ correspond to the betatron coordinates, which do not include the offset and slope caused by the momentum dispersion. By using the above definition of the emittance, we obtain an expression for the variation of the emittance with respect to the transverse coordinates $u$ and $u'$

$$ \delta \epsilon_u = (2 \gamma_u u + 2 \alpha_u u') \delta u + (2 \alpha_u u + 2 \beta_u u') \delta u' .
$$ {#eq:variation-emittance}

Neither the emission of a photon nor the acceleration immediately changes the transverse displacement of an electron $u$, leading to $\delta u = 0$. The sum of the synchrotron radiation and the cavity forces results in a variation of transverse momentum

$$\delta\mathbf{p_\perp} = \delta \mathbf{p_\mathrm{ph}} + \delta \mathbf{p_\mathrm{rf}} .
$$ {#eq:resulting-transverse-momentum-change}

Therefore the variation of transverse slope $u'$ is

$$ u' + \delta u' = \frac{p_\perp + \delta p_\perp}{p_\parallel} = u' + \frac{\delta p_\perp}{p_\parallel} .
$$ {#eq:variation-vertical-slope}

Furthermore, we have to take into account the influence of the momentum deviation. Therefore, we will first solve the dispersion-free vertical case $\eta_\mathrm{y} = 0$ and then add an additional term for the horizontal case $\eta_\mathrm{x}, where \neq 0$.

With $\delta p_\perp = -y' \delta p_\mathrm{rf}$ and $p_\parallel \approx p$, we can conclude for the variation of the vertical coordinates

$$ \delta y = 0, \quad \delta y' = -y' \frac{\delta p_\mathrm{rf}}{p} = -y' \frac{\delta E_\mathrm{rf}}{E_0}
$$ {#eq:variation-vertical-coordinates}

and obtain an expression of the variation of the vertical emittance

$$ \delta \epsilon_\mathrm{y} = -(2 \alpha_\mathrm{y} y y' + 2 \beta_\mathrm{y} y'^2) \frac{\delta E_\mathrm{rf}}{E_0},
$$ {#eq:variation-emittance-vertical-1}

where $\delta E_\mathrm{rf}$ corresponds to the energy refilled by the cavity, not the energy decrease due to the damping $\delta E = c \sqrt{p_\parallel^2 + (p_\perp + \delta p_\perp)^2} - c \sqrt{p_\parallel^2 + p_\perp^2} \approx c \frac{p_\perp \delta p_\perp}{p} \approx c y' \delta p_\perp$. Under the assumption of a uniform distribution of betatron phases $\psi$, we must average over @eq:variation-emittance-vertical-1. Therefore we solve the integrals

$$
\begin{aligned}
\langle y y' \rangle &= \frac{1}{2 \pi} \int_0^{2 \pi} y y' \mathrm{d} \psi \\
&= - \frac{1}{2 \pi} \int_0^{2 \pi} \epsilon_\mathrm{y} (\alpha_\mathrm{y} (\cos{\psi})^2 + \sin{\psi} \cos{\psi}) \mathrm{d} \psi \\
&= -\frac{\epsilon_\mathrm{y} \alpha_\mathrm{y}}{2}
\end{aligned}
$$ {#eq:average-y-y-prime}

and

$$
\begin{aligned}
\langle y'^2 \rangle &= \frac{1}{2 \pi} \int_0^{2 \pi} y'^2 \mathrm{d} \psi \\
&= \frac{1}{2 \pi} \int_0^{2 \pi} \frac{\epsilon_\mathrm{y}}{\beta_\mathrm{y}} (\alpha_\mathrm{y}^2 (\cos{\psi})^2 + \alpha_\mathrm{y} \sin{\psi} \cos{\psi} +(\sin{\psi})^2) \mathrm{d} \psi \\
&= \frac{\epsilon_\mathrm{y}}{2 \beta_\mathrm{y}} (\alpha_\mathrm{y}^2 + 1) \\
&= \frac{\epsilon_\mathrm{y} \gamma_\mathrm{y}}{2}
\end{aligned}
$$ {#eq:average-y-prime-squared}

and substitute them into @eq:variation-emittance-vertical-1:

$$ \delta \epsilon_\mathrm{y} = \epsilon_\mathrm{y} (\alpha_\mathrm{y}^2 - \beta_\mathrm{y} \gamma_\mathrm{y}) \frac{\delta E_\mathrm{rf}}{E_0} = - \epsilon_\mathrm{y} \frac{\delta E_\mathrm{rf}}{E_0} 
$$ {#eq:variation-emittance-vertical-2}

Over the time of one revolution $T_0$, the energy chunks $\delta E_\mathrm{rf}$ add up to the total radiation loss $U_0$. Therefore, following our third assumption, we write an expression for the time derivative of the vertical emittance

$$ \frac{\mathrm{d} \epsilon_\mathrm{y}}{\mathrm{d} t} = \frac{\mathrm{d} \delta \epsilon_\mathrm{y}}{\mathrm{d} t} = -\epsilon_\mathrm{y} \frac{1}{E_0} \frac{\mathrm{d} \delta E_\mathrm{rf}}{\mathrm{d} t} = -\epsilon_\mathrm{y} \frac{U_0}{E_0T_0} .
$$ {#eq:emittance-vertical-derivative}

For the variation of the horizontal emittance

$$ \delta \epsilon_\mathrm{x} = - \epsilon_\mathrm{x} \frac{U_0}{E_0 T_0} + \delta \epsilon_\mathrm{x}^{\delta}
$$ {#eq:variation-emittance-horizontal-1}

we have to consider an additional term $\delta \epsilon_\mathrm{x}^{\delta}$ caused by the momentum dispersion. As discussed in @sec:dispersion, the total horizontal displacement $x_\mathrm{tot}$ is sum of betatron displacement $x(s) = \sqrt{\epsilon \beta(s)} \cos(\psi(s) + \psi_0)$ and dispersive displacement $x_\delta(s) = \eta(s) \delta$:

$$ x_\mathrm{tot}(s) = x(s) + \eta(s) \delta \quad \mathrm{and} \quad x'_\mathrm{tot}(s) =  x'(s) + \eta'(s) \delta
$$ {#eq:total-horizontal-offset}

As the energy loss due to the emission of a photon cannot immediately change the total displacement $x_\mathrm{tot}$ or slope $x'_\mathrm{tot}$ of an electron, the betatron coordinates $x$ and $x'$ must compensate the change in the dispersive coordinates $x_\delta$ and $x'_\delta$. Therefore the variation of the betatron coordinates $x$ and $x'$ is

$$ \delta x = -x_\delta(s) =  - \eta_\mathrm{x} \frac{\delta E_\mathrm{ph}}{E_0}, \quad \delta x' = -x'_\delta(s) = -\eta_\mathrm{x}' \frac{\delta E_\mathrm{ph}}{E_0} ,
$$ {#eq:variation-horizontal-coordinates}

where $\delta E_\mathrm{ph}$ is the variation of the electron energy caused by the synchrotron radiation. Substituting @eq:variation-horizontal-coordinates into @eq:variation-emittance yields the additional term of the variation of the horizontal emittance

$$ \delta \epsilon_\mathrm{x}^\delta = -(2 \gamma_\mathrm{x} x + 2 \alpha_\mathrm{x} x') \eta_\mathrm{x} \frac{\delta E_\mathrm{ph}}{E_0} - (2 \alpha_\mathrm{x} x + 2 \beta_\mathrm{x} x') \eta_\mathrm{x}' \frac{\delta E_\mathrm{ph}}{E_0} .
$$ {#eq:variation-emittance-horizontal-2}

From @sands1970, we use the expression for the radiation power

$$ P_\gamma(s) = C_\gamma \frac{e^2 c^3}{2 \pi} E^2 B^2 = C_\gamma \frac{c}{2 \pi} E^4 \kappa(s)^2 ,
$$ {#eq:radiation-power}

where $E$ and $B$ corresponds to the electric and magnetic fields, respectively, and we introduced a constant

$$ C_\gamma = \frac{e^2}{3 \epsilon_0 (m c^2)^4} .
$$ {#eq:constant-radiation-power}

As $P \propto E^2 B^2$, the radiation power is in linear approximation

$$
\begin{aligned}
P &\approx P_0 + \frac{\mathrm{d} P}{\mathrm{d} E} \Bigr|_{\substack{E=E_0}} \Delta E + \frac{\mathrm{d} P}{\mathrm{d} B} \Bigr|_{\substack{B=B_0}} \Delta B \\
&= P_0 (1 + 2 \frac{\Delta E}{E_0} + 2 \frac{\Delta B}{B_0}) .
\end{aligned}
$$ {#eq:linear-approximation-radiation-power-1}

Subsituting $\Delta B \approx \frac{\mathrm{d}B}{\mathrm{d} x} x$, $\frac{\mathrm{d}B}{\mathrm{d} x} = \frac{k}{\kappa_\mathrm{x0}} B$ and $\Delta E = E_0 \delta$ into @eq:linear-approximation-radiation-power-1, yields

$$ P \approx P_0 (1 + 2 \delta + 2 \frac{k}{\kappa_\mathrm{x0}}x) .
$$ {#eq:linear-approximation-radiation-power-2}

With $t = z / c$ and @eq:linear-approximation-radiation-power-2 we can write for the variation of the Energy

$$ \delta E_\mathrm{ph} = - \frac{P}{c} \delta z \approx -\frac{P}{c} (1 + \kappa_\mathrm{x_0} x)\delta s \approx - \frac{1}{c} P_0 (1 + 2 \delta + 2 \frac{k}{\kappa_\mathrm{x0}}x) (1 + \kappa_\mathrm{x_0} x) \delta s .
$$ {#eq:energy-loss-variation}

Using @eq:energy-loss-variation, we can average over all betatron phases $\psi$

$$
\begin{aligned}
\langle \delta \epsilon_\mathrm{x}^\delta \rangle &= - \frac{1}{2 \pi} \int_0^{2 \pi} ((2 \gamma_\mathrm{x} x + 2 \alpha_\mathrm{x} x') \eta_\mathrm{x}  + (2 \alpha_\mathrm{x} x + 2 \beta_\mathrm{x} x') \eta_\mathrm{x}') \frac{\delta E}{E_0} \mathrm{d} \psi \\
&= \frac{P_0 \delta s}{\pi c E_0} \int_0^{2 \pi} ((\gamma_\mathrm{x} x + \alpha_\mathrm{x} x') \eta_\mathrm{x} + (\alpha_\mathrm{x} x + \beta_\mathrm{x} x') \eta_\mathrm{x}') (1 + 2 \delta + 2 \frac{k}{\kappa_\mathrm{x0}}x) (1 + \kappa_\mathrm{x_0} x) \mathrm{d} \psi .
\end{aligned}
$$ {#eq:average-horizontal-emittance-variation}

Only even terms in $x$ and $x'$ will contribute a finite value, while odd terms in $x$ and $x'$ vanish. Analogous to @eq:average-y-y-prime we find that $\langle x x' \rangle = -\frac{\epsilon_\mathrm{x} \alpha_\mathrm{x}}{2}$ and for average of $x^2$ we obtain

$$
\langle x^2 \rangle = \frac{1}{2 \pi} \int_0^{2 \pi} x^2 \mathrm{d} \psi
= \frac{1}{2 \pi} \int_0^{2 \pi} \epsilon_\mathrm{x} \beta_\mathrm{x} (\cos{\psi})^2 \mathrm{d} \psi
= \frac{\epsilon_\mathrm{x} \beta_\mathrm{x}}{2} ,
$$ {#eq:average-x-squared}

which we substitute into @eq:energy-loss-variation:

$$
\begin{aligned}
\langle \delta \epsilon_\mathrm{x}^\delta \rangle 
&= \frac{P_0 \delta s}{\pi c E_0} \int_0^{2 \pi} ((\gamma_\mathrm{x} x^2 + \alpha_\mathrm{x} x x') \eta_\mathrm{x} + (\alpha_\mathrm{x} x^2 + \beta_\mathrm{x} x x') \eta_\mathrm{x}') (\kappa_\mathrm{x0} + 2 \frac{k}{\kappa_\mathrm{x0}}) \mathrm{d} \psi \\
&= \frac{P_0 \delta s}{c E_0} ((\gamma_\mathrm{x} \epsilon_\mathrm{x} \beta_\mathrm{x} - \alpha_\mathrm{x} \epsilon_\mathrm{x} \alpha_\mathrm{x}) \eta_\mathrm{x} + (\alpha_\mathrm{x} \epsilon_\mathrm{x} \beta_\mathrm{x} - \beta_\mathrm{x} \epsilon_\mathrm{x} \alpha_\mathrm{x}) \eta_\mathrm{x}') (\kappa_\mathrm{x0} + 2 \frac{k}{\kappa_\mathrm{x0}}) \\
&= \frac{P_0 \delta s}{c E_0} \epsilon_\mathrm{x} (\gamma_\mathrm{x} \beta_\mathrm{x} - \alpha_\mathrm{x}^2) \eta_\mathrm{x} (\kappa_\mathrm{x0} + 2 \frac{k}{\kappa_\mathrm{x0}})\\
&= \frac{P_0 \delta s}{c E_0} \epsilon_\mathrm{x} \eta_\mathrm{x} (\kappa_\mathrm{x0} + 2 \frac{k}{\kappa_\mathrm{x0}})\\
\end{aligned}
$$ {#eq:average-horizontal-emittance-variation-2}

Using the relationships $\mathrm{d} t = \mathrm{d} z / c$, we define nominal radiation loss per turn

$$ U_0 = \int_0^{T_0} P_0 \mathrm{d} t = \frac{1}{c} \int_0^{C_0} P_0 \mathrm{d} s = \frac{C_\gamma E_0^4}{2 \pi} \int_0^{C_0} \kappa_\mathrm{x0}(s)^2 \mathrm{d} s ,
$$ {#eq:energy-loss-radiation}

where we made use of the fact that for the nominal particle $s = z$. By comparing @eq:radiation-power and @eq:energy-loss-radiation, we obtain an expression for the nominal radiation power

$$ P_0(s) = \mathrm{const} \cdot \kappa_\mathrm{x0}(s)^2 = \frac{U_0 c}{\mathrm{\int_0^C \kappa_\mathrm{x0}(s)^2 \mathrm{d} s}} \kappa_\mathrm{x0}(s)^2
$$ {#eq:nominal-radiation-power}

in terms of the curvature of the ideal orbit $\kappa_\mathrm{x0}$ and the nominal energy loss per turn $U_0$. Substituting @eq:nominal-radiation-power into @eq:average-horizontal-emittance-variation-2 and integrating over one turn yields the  change of the horizontal emittance caused by radiation damping

$$
\begin{aligned}
\frac{\mathrm{d} \epsilon_\mathrm{x}}{\mathrm{d} t} 
&= -\epsilon_\mathrm{x} \frac{U_0}{E_0 T_0} \left(1 - \frac{\int_0^{C} \kappa_\mathrm{x0} \eta_\mathrm{x} \left(\kappa_\mathrm{x0}^2 + 2 k \right)\mathrm{d}s}{\int_0^{C} \kappa_\mathrm{x0}^2 \mathrm{d}s}\right) \\
&= -\epsilon_\mathrm{x} \frac{U_0}{E_0 T_0} \left(1 - \frac{I_4}{I_2}\right) ,
\end{aligned}
$$ {#eq:emittance-horizontal-derivative}

where we inserted the second and fourth synchrotron radiation integrals defined in @eq:i2 and @eq:i4.

### Quantum Excitation {#sec:quantum-excitation}

![Quantum excitation of the betatron oscillation. When an electron with the reference momentum $p = p_0$ emits a photon within a bending magnet, it loses energy and will no longer be on the on-energy closed orbit. It will now perform betatron oscillations around a dispersive closed orbit $p < p_0$. (based on @wolski)](figures/betatron-oscillation-excitation.svg){#fig:betatron-oscillation-excitation}

Until now, we assumed the radiation would be emitted continuously along a given path length parallel to the particle's momentum. If this were the case, then after some time, the betatron amplitude would damp to zero. However, due to the quantum nature of photons, the radiation is not emitted continuously but rather happens in discrete chunks of energy, resulting in an excitation of the emittance called *quantum excitation*. Illustrated in @fig:betatron-oscillation-excitation, the discontinuous
jump in energy caused by the emission of a photon of discrete energy forces the electron on a dispersive orbit $p \neq p_0$. Subsequently, the electron now performs betatron oscillations around the new closed orbit.

Furthermore, the photons are not emitted precisely parallel to the electron's velocity but rather in a cone, resulting in a change in the direction of the momentum. That also excites the betatron oscillation and prevents the emittance from damping to zero, even if the emission of synchrotron radiation would be continuous. However, as the latter effect is much smaller than the former, we will neglect this effect for the following considerations.

For same argument leading to @eq:variation-horizontal-coordinates, the emission of a photon with the discrete energy $\delta E$ leads to a variation of the betatron offset and betatron slope:

$$ \delta x = - \eta_\mathrm{x} \frac{\delta E}{E_0}, \quad \delta x' = -\eta_\mathrm{x}' \frac{\delta E}{E_0}
$$ {#eq:variation-emittance-quantum-excitation-1}

Inserting $\delta x$ and $\delta x'$ into the definition of the phase space ellipse from @eq:phase-space-ellipse-radiation-damping, we obtain an expression for the variation of the emittance caused by the emission of a discrete photon of the energy $\delta E$

$$
\begin{aligned}
\delta \epsilon_\mathrm{x}^\mathrm{q} &= (\gamma_\mathrm{x} \eta_\mathrm{x}^2 + 2 \alpha_\mathrm{x} \eta_\mathrm{x} \eta_\mathrm{x}' + \beta_\mathrm{x} \eta_\mathrm{x}'^2) \left(\frac{\delta E}{E_0}\right)^2 \\
&= \mathcal{H}_\mathrm{x} \left(\frac{\delta E}{E_0}\right)^2 ,
\end{aligned}
$$ {#eq:variation-emittance-excitation}

where we substituted the curly $\mathcal{H}$ function defined in @eq:curly-h. As the photons are emitted randomly with different energies $\delta E$, we have to average @eq:variation-emittance-excitation over the energy distribution of the photons. Therefore, we introduce a new quantity $\dot{n}(\epsilon)$ which denotes number of photons emitted per time unit in the energy interval $[\epsilon, \epsilon + \mathrm{d} \epsilon]$.

According to @sands1970, the squared emitted energy per time unit is 

$$ \dot{N} \langle \epsilon^2 \rangle = \int_0^\infty \epsilon^2 \dot{n}(\epsilon) \mathrm{d} \epsilon = 2 C_\mathrm{q} \gamma^2 \frac{U_0 E_0}{T_0} \frac{|\kappa_\mathrm{x0}|^3}{\langle \kappa_\mathrm{x0}^2 \rangle_s} ,
$$ {#eq:squared-emitted-energy-per-time}

where

$$ C_\mathrm{q} = \frac{55}{32\sqrt{3}} \frac{\hbar}{mc}
$$ {#eq:c-q}

is to the so-called *quantum constant*.

Using @eq:squared-emitted-energy-per-time, we can integrate @eq:variation-emittance-excitation along the length of the ring to obtain an expression for change of the horizontal emittance caused by the quantum excitation

$$
\begin{aligned}
\frac{\mathrm{d} \epsilon_\mathrm{x}^\mathrm{q}}{\mathrm{d} t}
&= \frac{1}{E_0^2} \int_0^C \mathcal{H}_\mathrm{x} \dot{N}\langle (\delta E)^2 \rangle \mathrm{d} s \\
&= \frac{2}{E_0^2} \int_0^C \mathcal{H}_\mathrm{x} C_\mathrm{q} \gamma^2 \frac{U_0 E_0}{T_0} \frac{|\kappa_\mathrm{x0}|^3}{\langle \kappa_\mathrm{x0}^2 \rangle_s} \mathrm{d} s \\
&= 2 C_\mathrm{q} \gamma^2 \frac{U_0}{E_0 T_0} \frac{\int_0^C \mathcal{H}_\mathrm{x} |\kappa_\mathrm{x0}|^3 \mathrm{d} s}{\int_0^C \kappa_\mathrm{x0}^2 \mathrm{d} s} \\
&= 2 C_\mathrm{q} \gamma^2 \frac{U_0}{E_0 T_0} \frac{I_5}{I_2},
\end{aligned}
$$ {#eq:emittance-horizontal-derivative-excitation}

where in the last step, we substituted the second and fifth synchrotron radiation integrals $I_2$ and $I_5$ defined in @eq:i2 and @eq:i5. Note that the change of the emittance is positive, which corresponds to an excitation of the emittance.

### Equilibrium Emittance {#sec:emittance}

As discussed in the last two subsections, two counteracting effects are changing the amplitude of the betatron oscillations. The total time derivative of the emittance corresponds to the sum of both, i.e., @eq:emittance-horizontal-derivative and @eq:emittance-horizontal-derivative-excitation:

$$
\begin{aligned}
\frac{\mathrm{d} \epsilon_\mathrm{x}}{\mathrm{d} t} &= \frac{\mathrm{d} \epsilon_\mathrm{x}^\mathrm{q}}{\mathrm{d} t} + \frac{\mathrm{d} \epsilon_\mathrm{x}^\mathrm{r}}{\mathrm{d} t} \\
&= 2 C_\mathrm{q} \gamma^2 \frac{U_0}{E_0 T_0} \frac{I_5}{I_2} - \epsilon_\mathrm{x} \frac{U_0}{E_0 T_0} \left(1 - \frac{I_4}{I_2}\right) \\
&= \frac{U_0}{E_0 T_0} \left(2 C_\mathrm{q} \gamma^2 \frac{I_5}{I_2} - \epsilon_\mathrm{x} \left(1 - \frac{I_4}{I_2}\right)\right)
\end{aligned}
$$ {#eq:total-time-derivative-emittance}

While the synchrotron damping leads to an exponential decay of the emittance, the quantum excitation is independent of the amplitude causing the emittance to grow constantly. Therefore eventually, both effects become equally strong, leading to a zero time derivative of the emittance

$$
\begin{aligned}
\frac{\mathrm{d} \epsilon_\mathrm{x}}{\mathrm{d} t} \Bigr|_{\substack{\epsilon_\mathrm{x}=\epsilon_\mathrm{x}^\mathrm{eq}}} &= 0 \\
\epsilon_\mathrm{x}^\mathrm{eq} \left(1 - \frac{I_4}{I_2}\right) &= 2 C_\mathrm{q} \gamma^2 \frac{I_5}{I_2}
\end{aligned}
$$ {#eq:total-time-derivative-equilibrium-emittance}

at a value known as *equilibrium emittance*

$$
\epsilon_\mathrm{x}^\mathrm{eq} = 2 C_\mathrm{q} \gamma^2 \frac{I_5}{I_2 - I_4} .
$$ {#eq:equilibrium-emittance}

Note that the magnetic lattice fully defines @eq:equilibrium-emittance. For electron storage rings, this has a very practical consequence: The equilibrium emittance is unrelated and therefore not limited by the emittance of the source. Consequently, any arbitrary injected particle distribution damps to the value of the equilibrium emittance.

In the literature, the expression for the equilibrium emittance often differs by a factor of two from @eq:equilibrium-emittance. The reason is that many books use the root-mean-square of the horizontal betatron displacement

$$ \sigma_{\mathrm{x}\beta}(s) = \langle x_\beta(s)^2 \rangle = \frac{1}{2 \pi} \int_0^{2 \pi} \epsilon_\mathrm{x} \beta_\mathrm{x}(s) \cos(\psi_\mathrm{x}(s) + \psi_\mathrm{x0})^2 = \frac{1}{2} \epsilon_\mathrm{x} \beta_\mathrm{x}(s)
$$ {#eq:rms-horionztal-displacement}

to establish an alternative definition of the emittance

$$ \frac{\sigma_{\mathrm{x}\beta}^\mathrm{eq}(s)}{\beta_\mathrm{x}(s)} = \frac{1}{2} \epsilon_\mathrm{x}^\mathrm{eq} = C_\mathrm{q} \gamma^2 \frac{I_5}{I_2 - I_4} .
$$ {#eq:alternative-equilibrium-emittance}

## Lattice Design {#sec:lattice-design}

As shown in the last section, the choice of magnetic lattice for a circular electron ring defines the magnitude of synchrotron radiation and the equilibrium emittance of the particle beam. The previous sections introduced the most important analytical parameters of electron beam dynamics. In this section, we want to discuss the concepts introduced at the example of different periodic lattices. At first, we will cover the FODO lattice, which is the most simple, strong-focusing lattice. However, it has some disadvantages, making it an unfavorable choice for modern high-energy synchrotron radiation facilities. Therefore, in the following subsection, we move on to the double bend achromat lattice (DBA). Due to its dispersion-free straights, it is a more suitable choice for insertion devices, and it has compared to the FODO lattice a lower equilibrium emittance. All plots are created by the developed code.


### The FODO Lattice

The FODO cell is the simplest possible strong-focusing lattice. It consists out of alternating horizontal and vertical focusing quadrupoles with drift spaces in between, which give the cell its name: A horizontal **F**ocusing quadrupole, a drift space (**0** force), a horizontal **D**efocusing, and a drift space (**0** force). A schematic of the FODO lattice is shown in @fig:fodo-schematic.

![Schematic of a FODO cell](figures/fodo-schematic.svg){#fig:fodo-schematic}

We can use the periodic condition of @sec:transformation-twiss-parameter to calculate the optical functions $\beta(s)$ and $\eta(s)$. The periodic solution of the Twiss parameters $\beta(s)$ and $\eta(s)$ for a FODO lattice without dipoles ($R = 0$) are shown in the upper plot of @fig:fodo-twiss.

![Top: Twiss parameters of the FODO cell without dipoles. Bottom: Twiss parameters of a FODO cell with dipoles (solid) compared to a cell without dipoles (dashed, from top).](figures/fodo-twiss.svg){#fig:fodo-twiss}


While the horizontal beta function $\beta_\mathrm{x}(s)$ reaches its maximum at the center of the horizontal focusing quadrupole *q1*, the vertical beta function $\beta_\mathrm{y}(s)$ has its maximum at the center of the vertical focusing quadrupole *q2*. As the dispersion is introduced by bending magnets, this FODO cell has a vanishing dispersion function $\eta_\mathrm{x}(s)$. A high dispersion function is especially undesirable at the location of insertion devices, which would significantly increase the quantum excitation. A circular accelerator must have bending magnets, as - by definition - it has to close at some point, which makes a non-vanishing dispersion function $\eta_\mathrm{x}(s)$ inevitable. However, as discussed in the following subsection, it is still possible to design a lattice with no dispersion within certain sections of the ring.

The simplest way to create a FODO-based circular accelerator is to place a bending magnet in the center of every drift space. The Twiss parameters $\beta(s)$ and $\eta(s)$ for such a FODO cell with dipoles ($R = \frac{\pi}{8}$) are shown in the lower plot of @fig:fodo-twiss. @tbl:fodo-parameter lists a comparison of the lattice parameters for both FODO cells.

|                                                 |   without dipoles |   with dipoles |
|:------------------------------------------------|------------------:|---------------:|
| Cell length $L$ / m                             |              8.00 |           8.00 |
| Bending angle $\varphi$                         |              0.00 |$\frac{\pi}{8}$ |
| Quadrupole strength $k$ / m$^{-2}$              |              0.80 |           0.80 |
| Horizontal tune $Q_\mathrm{x}$                  |              0.28 |           0.28 |
| Vertical tune $Q_\mathrm{y}$                    |              0.28 |           0.30 |
| Max. horizontal beta $\beta_\mathrm{x,max}$ / m |             14.11 |          14.05 |
| Max. vertical beta $\beta_\mathrm{y,max}$ / m   |             14.11 |          13.82 |
| Max. dispersion $\eta_\mathrm{x,max}$ / m       |              0.00 |           1.85 |

: Lattice parameter of the FODO cell from @fig:fodo-twiss {#tbl:fodo-parameter}

As one can see, the dipoles introduced a non-zero dispersion function $\eta_\mathrm{x}(s)$ with a graph similar to the horizontal beta function: A maximum of 1.8 meters at the center of the horizontal focusing quadrupole *q1* and a minimum of 0.8 meters at the center of the vertical focusing quadrupole *q2*. Due to the horizontal weak-focusing of the dipoles and vertical focusing of the dipole edges, the maxima of the horizontal and vertical beta functions are slightly smaller than in the FODO cell without dipoles. For the same reasons, the vertical tune $Q_\mathrm{y}$ is a bit larger.

![Top: The horizontal and vertical beta functions $\beta(s)$. Middle: The horizontal and vertical alpha functions $\alpha(s)$. Bottom: The betatron phase $\psi(s)$](figures/fodo-twiss-2.svg){#fig:fodo-twiss-2}

Discussed in @sec:betatron-oscillation, the evolution of phase space ellipse of the beam is fully defined by the $\beta_u(s)$, $\alpha_u(s)$ and $\gamma_u(s)$ functions. @fig:fodo-twiss-2 shows the graph of the $\beta_u(s)$ and $\alpha_u(s)$ functions together with betatron phases $\psi_u(s)$.  According to their definition $\alpha_u(s) = -\beta_u'(s) / 2$ , the alpha functions $\alpha_u(s)$ become zero when the beta functions $\beta_u(s)$ are maximum and reach their maximum when the beta functions $\beta_u(s)$ change the most. The horizontal betatron phase $\psi_\mathrm{x}(s)$ changes the most in the vertical focusing quadrupole *q2* and its adjacent drift spaces. In contrast, the changes within the starting and ending *q1* quadrupoles are almost negligible. For the vertical betatron phase $\psi_\mathrm{y}(s)$, it is the other way around. However, due to the edge focusing of the bending magnets, the total vertical phase advance $Q_\mathrm{y}$ is slightly larger than in the horizontal plane.

![Top: exemplary trajectory of a single particle (solid blue) and beam envelope (dashed black). Middle: Normalized particle trajectory along the orbit position (floquet transformation). Bottom: Normalized particle trajectory as a function of the betatron phase.](figures/fodo-twiss-floquet.svg){#fig:fodo-twiss-floquet}

The product of the periodic beam amplitude $\sqrt{\epsilon\beta(s)}$ and the cosine of the betatron phase $\psi_u(s)$ defines the trajectory of a particle in a strictly linear lattice

$$ u(s) = \sqrt{\epsilon\beta_u(s)}\cos{(\psi_u(s) + \psi_0)} ,
$$

as shown at the example of four consecutive FODO cells in the upper part of @fig:fodo-twiss-floquet. The particle performs betatron oscillations according to its betatron phase $\psi_u(s) + \psi_{u,0}$ within the beam envelope $\sqrt{\epsilon\beta(s)}$. The second plot of @fig:fodo-twiss-floquet shows the same trajectory using Floquet's coordinates $u(s) / \sqrt{\beta(s)}$. In these coordinates, the beam envelope $\sqrt{\epsilon\beta(s)}$ becomes a constant and the particle performs oscillations distorted by the betatron phase $\psi_u(s)$. When plotting the particle trajectory against the betatron phase $\psi_u$(s) instead of the orbit position $s$, shown in the third plot of @fig:fodo-twiss-floquet, the oscillation has a perfect sinusoidal shape. Note that in this representation, the elements of magnetic lattice become distorted according to their phase advance $\psi_u(s_1,s_2)$.

![Mean beta function for different configurations of a FODO cell. For the FODO lattice, the space of stable quadrupole configurations has the form of a necktie and is therefore often called Necktie-Plot.](figures/necktie-plot.svg){#fig:necktie-plot}

@fig:necktie-plot shows a scan over possible quadrupole settings for FODO cells with different lengths $L$ and deflection angles, where we used the stability condition from @eq:stability-condition. Not all configurations of quadrupole strengths result in a stable lattice. One condition is that the focal length of a quadrupole must be greater than its distance to the next quadrupole. Assuming the focal length would be smaller, then the transverse displacement $u$ of a particle and its derivative $\frac{du}{ds}$ would have the same sign at the start of the following quadrupole, leading to a negative feedback loop. For each pass-through, the deflection would become stronger and stronger in the next quadrupole, eventually leading to the loss of the particle beam.

The area of stable solutions for a FODO cell without bending magnets is symmetrical to the diagonal. For low quadrupole strengths, both quadrupoles need to have a similar strength to create a stable lattice. With increasing quadrupole strength, a larger deviation of both quadrupole strengths is possible, leading to the stable area's necktie shape. The maximum quadrupole strength is limited by the condition that the focal length of the quadrupoles must be greater than their distance from each other. The smallest average beta function $\beta_\mathrm{mean}$ for a FODO cell with a length of 6 meters without bending magnets is achieved when both quadrupoles are set to about 1.1 m$^{-2}$.

With increasing cell length the area of stable solutions decreases. This is again due to the requirement that the focal length of the quadrupoles must be larger than their distance. This means that moving the quadrupoles closer together allows for greater field strengths.

The second and third row of @fig:necktie-plot shows the stability plots for different FODO cells with dipoles with bending angle per cell of $\pi / 8$ and $\pi / 4$, respectively. The dipoles edges lead to an additional defocusing in the horizontal plane and focusing in the vertical plane. Therefore, the necktie plot is shifted towards smaller values on the axis of the vertical focusing quadrupole *q2* depending on the dipole's deflection angle. Furthermore, dipole edge's vertical focusing widens the space of stable configurations for lower quadrupole strengths, as a stable solution is possible even if the quadrupole *q2* is turned off.

The smallest average beta function $\beta_\mathrm{mean}$ for a FODO cell with a deflection angle of $\pi / 8$ per cell and with a length of 6 meters is achieved when the horizontal focusing quadrupole is set to 0.8 m$^{-2}$ and the vertical focusing quadrupole is set to 1.1 m$^{-2}$. Similar to the FODO cell without dipoles, the area of stable solutions is increases when the cell length decreases.

![Chromaticity and equilibrium emittance of a FODO lattice at 1 GeV.](figures/fodo-chromaticity-emittance.svg){#fig:fodo-chromaticity-emittance}

The left part of @fig:fodo-chromaticity-emittance shows the influence of the quadrupole strength on the equilibrium emittance of a FODO cell, where both the horizontal and vertical focusing quadrupoles have the same strength. As one can see, due to the choice of stronger quadrupole, it is possible to reduce the emittance by multiple orders of magnitude. Unfortunately, as shown in the right part of @fig:fodo-chromaticity-emittance, the chromaticity rises with stronger quadrupole values, limiting the achievable emittance as the compensation of the chromaticities leads to a limitation of the dynamic aperture.

All in all, the FODO lattice is less optimal for modern low-emittance synchrotron light sources. For high-energy colliders, the FODO lattice is useful as it maximizes the ratio of bendings magnets per circumference. However, in a synchrotron facility, one generally wants to maximize the ratio of free straights per circumference to utilize insertion devices. Furthermore, the high dispersion function of the FODO lattice leads to a large equilibrium emittance, which is increased even more due to the additional quantum excitation of insertion devices at the location of high dispersion functions. Therefore, the following section presents a lattice with a smaller equilibrium emittance that is more suitable for insertion devices.

### The DBA Lattice {#sec:the-dba-lattice}

As discussed in @sec:quantum-excitation, quantum excitation increases the emittance of the particle beam, which is a crucial quantity for synchrotron radiation users. The *double bend achromat* (DBA) lattice, also known as *Chasman–Green lattice* [@Chasman1975], is one type of lattice to achieve a lower emittance than with the FODO lattice presented in the last subsection. In addition, the DBA lattice's dispersion-free sections are suitable for placing insertion devices, minimizing their contribution to the quantum excitation.

![Schematic of the DBA. The dispersive particle trajectories are highlighted in red.](figures/dba-schematic.svg){#fig:dba-schematic}

@fig:dba-schematic shows the working principle of a DBA cell: In its simplest form, the DBA consists of two dipoles and one quadrupole. The horizontal focusing quadrupole stands between two bending magnets. The quadruple strength is chosen in such a way that it reverses the gradient of the dispersion function $\eta_\mathrm{x}'(s)$ so that the second bending magnet cancels out the dispersion $\eta_\mathrm{x}(s)$ introduced by the first dipole.

![Three DBA cells with different distances between bending and quadrupole magnet.](figures/dba-distance.svg){#fig:dba-distance}

Not only the quadrupole's strength but also its distance to the surrounding dipoles must be chosen correctly to fulfill the achromatic condition. @fig:dba-distance shows the dispersion function $\eta_\mathrm{x}$, its derivative with respect to the orbit position $\eta_\mathrm{x}'$ and the trajectory of multiple dispersive particles for three different DBA cells, where the quadrupole strengths $k$ are identical, but the distance between bending magnets and quadrupole is different. The color of the particle trajectories indicates if the momentum deviation is positive or negative. In analogy with the rainbow spectrum of visible light, a particle trajectory drawn in color towards purple represents a positive momentum deviation $\delta > 0$. In contrast, a color towards red corresponds to a negative momentum deviation $\delta < 0$.

In the upper plot, the distance between the dipole magnets and the quadrupole is too short. Here, the dispersion function $\eta_\mathrm{x}$ did not have enough space to build up so that the quadrupole could fully reverse the gradient of the dispersion function $\eta_\mathrm{x}'$. Consequently, after the beam exits the cell, there is a non-vanishing dispersion function $\eta_\mathrm{x} > 0$. Alternatively, one could increase the quadrupole strength $k$ to meet the achromatic condition. In the second case, the quadrupole strength $k$ and the distance between the dipole magnets and the quadrupole match perfectly. As a result, the quadrupole exactly reverses the gradient of the dispersion function $\eta_\mathrm{x}'$ so that the dispersion $\eta_\mathrm{x}$ outside the cell vanishes. In the last plot, the distance between the bending magnets and the quadrupole is too large, resulting in a negative dispersion function $\eta_\mathrm{x} < 0$ at the end of the cell. In this case, choosing a lower quadrupole strength $k$ would satisfy the achromatic condition.

![Twiss parameters of the DBA cell.](figures/dba-twiss.svg){#fig:dba-twiss}

Usually, there are additional quadrupoles outside the achromat to form a complete DBA cell. @fig:dba-twiss shows the graphs of the beta functions $\beta_u(s)$, the dispersion functions $\eta_\mathrm{x}(s)$ and $\eta_\mathrm{x}'(s)$ and the betatron phases $\psi_u(s)$ of a DBA cell with two additional quadrupoles *q1* and *q2* outside of the achromat. Additionally, @tbl:dba-parameter lists important lattice parameters of this DBA cell.

|                                                    |   DBA |
|:---------------------------------------------------|------:|
| Cell length $L$ / m                                |  8.00 |
| Bending angle $\varphi$                            |  $\frac{\pi}{16}$ |
| Quadrupole strength $k_\mathrm{Q1}$ / m$^{-2}$     |  4.10 |
| Quadrupole strength $k_\mathrm{Q2}$ / m$^{-2}$     | -6.05 |
| Quadrupole strength $k_\mathrm{Q3}$ / m$^{-2}$     |  7.82 |
| Horizontal tune $Q_\mathrm{x}$                     |  0.75 |
| Vertical tune $Q_\mathrm{y}$                       |  0.57 |
| Maximum horizontal beta $\beta_\mathrm{x,max}$ / m | 27.57 |
| Maximum vertical beta $\beta_\mathrm{y,max}$ / m   | 27.88 |
| Maximum dispersion $\eta_\mathrm{x,max}$ / m       |  0.26 |

:DBA lattice parameters {#tbl:dba-parameter}

Here the quadrupoles *q1* and *q2* provide the horizontal and vertical focusing of the particle beam. As discussed above, the quadrupole *q3* reverses the gradient of the dispersion function $\eta_\mathrm{x}'$. For the second dipole to have precisely the opposite effect on dispersion as the first, the particles must perform exactly half a betatron oscillation from the center of the first dipole to the center of the second dipole. This condition corresponds to a phase advance of $\psi_\mathrm{x}(s_\mathrm{center_1}, s_\mathrm{center_2}) = \pi$, marked in the bottom plot of @fig:dba-twiss.

![Quadrupole scan for a DBA with three quadrupole families. In constrast to the Necktie-plot here, different islands of stable lattice configurations emerge.](figures/dba-quad_scan_3_families.svg){#fig:dba-quad-scan}

Not all quadrupole configurations satisfy the stability condition from @eq:stability-condition, making it significantly more difficult to find the optimal quadrupole setting for a given objective. In the case of the FODO cell, which has only two parameters, it is relatively straightforward as it is possible to scan over all possible quadrupole settings, as shown in @fig:necktie-plot. Furthermore, even though unstable lattice configurations exist, there is only one contiguous area of stable configurations. However, as shown in @fig:dba-quad-scan, even for the simple DBA lattice of @fig:dba-twiss, which only has three different quadrupole families, there emerge multiple areas where a stable solution exists. While it is for three quadrupole families still possible to scan over all possible values, this becomes unfeasible for six or more magnets @andreas_ba. These discontinuities, leading to the islands of stable lattice configurations, make optimizers only useable within a given island and therefore pose one of the most challenging tasks in lattice development. @sec:turning-off-the-q5t2-quadrupoles discusses how some of these problems have been dealt with for the Q5T2off lattice of the BESSY II storage ring.

Overall, the DBA lattice is suitable for a low emittance synchrotron light source and therefore was a very common choice among many third-generation light sources, including BESSY II. However, the multi-bend achromat (MBA) lattice allows for even smaller emittances, making it a popular choice for fourth-generation light sources. The additional quadrupoles placed between the bending magnets keep the dispersion function further down, resulting in a smaller emittance.

Note that the achromatic condition does not necessarily lead to the smallest equilibrium emittance, as defined in @eq:equilibrium-emittance. As demonstrated in @farvacque, another trend is to break the achromatic condition and leak a finite value of the dispersion function $\eta_\mathrm{x}$ into the straight sections. That effectively distributes the dispersion function $\eta_\mathrm{x}$ along the ring and reduces it within the dipole magnets. As long as the dispersion function $\eta_\mathrm{x}$ does not become too large within the insertion devices, distributing the dispersion function over the entire ring can reduce the equilibrium emittance. 
