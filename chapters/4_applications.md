# Applications

This chapter covers the applications of the developed optics simulation program. The first section comprises the development and optimization of the Q5T2-off optics of the BESSY II storage ring, which enlargens the available installation length of the cavity module of the BESSY-VSR project. The second section shows how the beta functions within a straight section of the BESSY II storage ring were adjusted for an emittance exchange experiment. Finally, the third section presents the development of a framework to automatically generate summaries for a given set of lattice files.

## Modifying the BESSY II Optics for the VSR project {#sec:q5t2off-bessy-vsr-optics}

The motivation of enlarging the installation length for the cavity module was already set out in @sec:introduction-q5t2off-bessy-vsr-optics. One solution is to turn off the Q5 quadrupoles in the T2 section of the storage ring to gain about 0.7 meters of installation length. The first steps towards such a Q5T2off-optics are described in my bachelor's thesis [@andreas_ba]. With the best solution found, it was possible to achieve a working machine with reasonable injection efficiency and lifetime. The goal should be to improve upon this solution.

The following three subsections provide a summarization of my bachelor's thesis. The first subsection gives an overview of the lattice development of the BESSY II storage ring. The second subsection discusses the constraints for the development of an optics with a turned-off Q5T2 magnet. In @sec:turning-off-the-q5t2-quadrupoles, the results of the bachelor's thesis are presented. The fourth subsection shows how the Q5T2off-optics was further optimized using the developed code of this thesis. The last subsection summarizes the results of a user operation acceptance test of the improved Q5T2off-optics.

### Lattice Design of the BESSY Storage Ring

![The design lattice of the BESSY II storage ring 1996. Full lattice (top), unit cell (bottom) - (extracted from @andreas_ba)](figures/design-lattice.svg){#fig:bessy2-design-lattice}

| Magnet | Quadrupole strength $k$ / m² |
|--------|:--------:|
| Q1     | +2.45190 |
| Q2     | -1.89757 |
| Q3D    | -2.02025 |
| Q4D    | +1.40816 |
| Q3T    | -2.46319 |
| Q4T    | +2.62081 |
| Q5T    | -2.60000 |

: The quadrupole strength of the BESSY II design lattice {#tbl:quadrupole-strengths-design}

The BESSY II storage ring has a double bend achromat lattice with 16 straight sections. The injection requires high horizontal beta functions. At the same time, the superconducting wavelength shifter needs a small horizontal beta function. That led to the decision to develop a lattice with alternating high and low horizontal beta straights @latticedesignbessy2. As a result, the 240 m storage ring has an 8-fold symmetry with the unit cell shown in @fig:bessy2-design-lattice. The seven quadrupole families of the design-lattice are listed in @tbl:quadrupole-strengths-design.

The two horizontal focusing Q1 quadrupoles in the center of the DBA reverse the gradient of the dispersion function as discussed in @sec:the-dba-lattice. The two vertical focusing Q2 quadrupoles are necessary to limit the vertical beam size. The high beta straights have the quadrupole doublet Q3D and Q4D, which are vertical and horizontal focusing, respectively. The low beta straights have the vertical focusing Q3T, horizontal focusing Q4T, and vertical focusing Q5T quadrupole families, which form a triplet. In order to achieve the low horizontal beta function, the Q4T quadrupoles must be significantly stronger than the Q4D quadrupoles. The additional Q5T quadruples are needed to compensate for the stronger vertical defocusing introduced by the Q4T quadrupoles.

![The Twiss parameters in D6 (Emil) and T6 (femto slicing) straights (extracted from @andreas_ba)](figures/bessy-emil-femto-slicing.svg){#fig:bessy-emil-femto-slicing}

Turning off the Q5T2 quadrupoles means turning the T2 triplet section into another doublet section. As the BESSY II storage ring has undergone several modifications since the design lattices from 1996, there are additional constraints that have to be taken into account:

Since 2005, a femto-slicing facility, producing ultra-short x-ray pulses, is commissioned in the D6 section of the BESSY II storage ring [@femto1;@femto2]. A femtosecond laser pulse modulates the electron energy in a wiggler called the modulator. The off-momentum electrons are extracted by the transverse displacement of a bending magnet, and the synchrotron radiation is emitted in the following undulator called the radiator. This femto-slicing experiment required the installation of three additional bending magnets, which together form a dipole chicane, the wiggler U139, and the undulator UE56. Another significant alteration of the BESSY II storage ring was carried out as part of the EMIL project @emil1, which is dedicated to researching materials for renewable energy. It provides multiple beamlines with simultaneous access to soft and hard x-rays. These are provided by the two UE-48 and CPMU-17 undulators, which are canted to separate the generated beam cones. In order to support this setup of the two canted undulators, the vertical focusing quadrupole QIT6 was installed in the center of the T6 straight, which shifts the vertical beam waist to the center of the CPMU-17 device. The Twiss parameters in D6 (Emil) and T6 (femto-slicing) straights are shown in @fig:bessy-emil-femto-slicing.

Another modification of the BESSY II storage ring was the introduction of the so-called injection optics @kuskeli: The horizontal beta function $\beta_x$ was increased in the injection-straight D1 and decreased in all other doublet straights to improve the injection efficiency.

### Constraints for the Development of the Q5T2off-optics {#sec:q5t2off-constraints}

The Twiss parameters of the BESSY II storage ring were carefully tuned to support the mentioned changes. New modifications should not conflict with the lattice development of the last several years. Therefore, when turning off the Q5T2 quadrupoles, it should be made sure that the changes are as local as possible with respect to the T2 section, and perturbations of the Twiss parameters outside of the T2 should be as small as possible.

![The horizontal and vertical beta functions $\beta_{x,y}$ of the current standard user lattice. The value of has to be kept below 4 m to avoid coupled bunch instabilities (based on @ruprecht-phd and extracted from @andreas_ba)](figures/beta-function-in-t2.svg){#fig:beta-function-in-t2}

The VSR cavities set another requirement for the Q5T2off-optics. As addressed by @ruprecht-phd beam-cavity interactions can cause coupled bunch instabilities, which spoil the beam quality. For a fixed threshold transverse cavity impedance

$$
Z_\mathrm{th}^{\perp}(\tau_{\mathrm{d}}^{-1}) = \frac{\tau_\mathrm{d}^{-1}}{\beta} \frac{4 \pi E / e}{\omega_\mathrm{rev} I_\mathrm{DC}}
$$

 the average beam current $I_{\mathrm{DC}}$ is determined by the energy $E$, the damping rate $\tau_{\mathrm{d}}^{-1}$, the angular beam revolution frequency $\omega_\mathrm{rev}$ and the value of the beta function $\beta$ within the cavity. As the requirements of the users of the synchrotron radiation restrain the energy $E$, the circumference of the ring defines the angular beam revolution frequency $\omega_\mathrm{rev}$ and increasing the damping rate $\tau_{\mathrm{d}}^{-1}$ might conflict with aspects of the machine operation, the value of the beta function within the cavity module effectively limits the average beam current $I_{\mathrm{DC}}$. By the estimations of [@ruprecht-phd, p.83], a beta function of below 4 m within the cavity module would be sufficient to store the required current.

![Maxium and average beta functions $\beta_{x,y}$ at the 1.50 GHz and 1.75 GHz cavites as a function of the minimum beta function $\beta_{min}$ (based on [M. Ries, priv. comm., 2017] and extracted from @andreas_ba)](figures/beta-t2-max-average.svg){#fig:beta-t2-max-average}

Assuming a symmetry point, the beta function $\beta(s)$ at the distance from the center of T2 is fully defined by the minimum beta function $\beta_{min}$ at symmetry point:

$$ \beta(s) = \beta_{\mathrm{min}} + \frac{s^2}{\beta_{\mathrm{min}}}
$$ {#eq:beta-function-at-symmetry}

Therefore it is possible to calculate the required minimum beta function $\beta_{min}$ to keep the beta function belows 4 m within the cavity moduel. @fig:beta-t2-max-average shows the maximum and average beta function at the 1.50 GHz and 1.75 GHz cavities as a function of the minimum beta function $\beta_{\mathrm{min}}$. A minimum beta function $\beta_{\mathrm{min}}$ between 0.6 m and 3.4 m is sufficient to keep the average beta below 4 m. A minimum beta function $\beta_{\mathrm{min}}$ between 1 m and 2 m would be optimal to keep the average beta function within the cavity module as small as possible.

### Turning off the Q5T2 Quadrupoles {#sec:turning-off-the-q5t2-quadrupoles}

As stated above, the goal is to minimize the beta functions' perturbation compared to the current standard user optics and keep the changes as local as possible. This can be accomplished by an optimizer that minimizes a fitness function chosen to satisfy the stated objective. However, the fact that not all quadruple settings result in a stable lattice poses a unique challenge: As an unstable quadrupole setting has no solution, all of them are equally bad. Therefore, choosing an objective function that provides a practical value to the optimizer in such a case is not easy. It seems reasonable to return a high constant or infinity. However, this leads to a problem when starting an optimizer in a region of unstable quadrupole settings. Usually, all other quadrupole settings in configuration space in the direct vicinity of an unstable lattice configuration are unstable as well. Therefore, the objective function always returns the same value regardless of which direction the optimizer chooses in the configuration space. Thus, the optimizer is practically left in the dark, and the possibility to converge is left to chance.

Just switching off the Q5T2 quadrupoles in the current standard user optics leads to an unstable lattice. That means that a quadrupole setting with only the Q5T2 quadrupoles turned off cannot be used as a starting configuration for optimization. So first, a stable lattice configuration has to be found, which can then be further improved by an optimizer.

A reasonable approach seems to start by only using quadrupoles in the T2 section to find a stable quadrupole setting. This was directly tested at the machine and also afterward checked by doing a quadrupole scan in simulations. The stability condition of the Twiss parameters

$$ 2 - R_{11}^2 - 2 R_{12} R_{21} - R_{22}^2 > 0
$$ {#eq:stabilty-requirement}

was derived in @sec:transformation-twiss-parameter. The quadrupole scan in @fig:stability-q3-q4 shows the stable regions for different settings of the Q3T2, Q4T2, and Q5T2 magnets.

![The stability of the BESSY II storage ring lattices for different configurations of the quadrupoles in the T2 section. Areas where no stable solution of the Twiss parameters exists, are shaded with diagonal lines. The left plot shows the different quadrupole configurations of the Q5T2 and the Q3T2 quadrupoles. The right plot shows the different quadrupole configurations of the Q5T2 and the Q4T2 quadrupoles. The current standard user optics is marked in red. The blue cross marks the attempt to compensate the turn-off solely with the Q3T2 quadrupoles, which eventually led to an unstable lattice. A stable solution, compensated by the decrease of the Q4T2s quadrupole strength, is shown in green. (extracted from @andreas_ba)](figures/stability-q3-q4.svg){#fig:stability-q3-q4}

At the machine, the first idea was to use the other vertical focusing Q3T2 quadrupoles to compensate for the turn-off of the Q5T2 quadrupoles. Increasing the Q3T2 quadrupoles made it possible to slightly more decrease the Q5T2 quadrupoles. However, at about 94 % of the initial strength of the Q5T2 quadrupoles, the beam was lost. That seems to be consistent with the results of the quadrupole scan. The blue cross in @fig:stability-q3-q4 marks this unstable quadrupole setting.

The next idea was to compensate for the turn-off of the Q5T2 quadrupoles by reducing the strength of the vertical defocusing Q4T2 quadrupoles. That led to a working machine but resulted in a very low injection efficiency. @fig:q5t2off-v1 shows the Twiss parameters where only the Q3T2 and Q4T2 quadrupoles were changed to compensate for the turn-off of the Q5T2 magnets. Compared to the standard user optics, the perturbation of the beta functions is significant all around the ring, which probably led to the low injection efficiency. In particular, the vertical beta function increases substantially in the T1, T3, and T6 sections.

![Beta functions with turned off Q5T2 quadrupoles compensated with the Q3T and Q4T quadrupoles of the T2 section (highlighted in blue). The Twiss parameters of the current standard user are shown in comparison with a dashed line.](figures/twiss_ba_q5t2off_v1_sim_vs_std_cropped.svg){#fig:q5t2off-v1}

The first and most local solution provides a starting point to improve the optics further using an optimizer. The average relative change of the beta function

$$ F(\beta) = \frac{1}{L} \int_0^L \frac{\beta(s)}{\beta_{\mathrm{ref}}(s)}\mathrm{d}s
$$ {#eq:objectiv-function-bachelor}

was chosen as the objective function. Different combinations of quadrupoles were used to compensate for the turn-off of the Q5T2 quadrupoles. Motivation for selecting the different quadrupole sets and a detailed overview of the solutions can be found in my bachelor thesis @andreas_ba. @fig:q5t2off-v4 shows the best solution obtained within the scope of the bachelor thesis. The optics was tested at the storage ring, and a high current with reasonable lifetime and injection efficiency was stored.

![Twiss parameters of the best solution of my bachelor's thesis (solid) in comparison to the standard user optics (dashed).](figures/twiss_ba_q5t2off_sim_vs_std.svg){#fig:q5t2off-v4}

### Optimizing the Q5T2off-optics in Simulations {#sec:optimizing-the-q5t2off-optics}

As stated in the conclusion of my bachelor's thesis, further improvements to the optics are necessary: First, the presented solution has a non-negligible $\beta$-beat outside of the T2 section. The standard user optics is fine-tuned in the injection straight, EMIL and, femto-slicing sections. Therefore, changes introduced by the Q5T2off optics should be as local as possible to avoid conflicting with previously made considerations. The goal is to limit the $\beta$-beat to the T2 and its adjacent neighboring sections. Another issue is that the vertical beta function in the center of the T2 section is with 3.6 m still too high. As stated before, the minimum beta function must be a least 3.4 m and would optimally be between one and two meters. Furthermore, the optics have to be further optimized regarding the non-linear dynamics. Different sextupole settings can be used to optimize the momentum acceptance.

Adjusting the objective function can reduce the $\beta$-beat. My bachelor's thesis used the mean relative residual of the beta function. That meant that a change from 4 m to 2 m corresponding to -50 % had the same weight as a change from 20 m to 30 m (+50 %). Therefore, this incentivized the optimizer to reduce the beta function below the value of the standard user optics at certain positions, resulting in a larger $\beta$-beat. This can be solved by composing the relative change of the beta function $\frac{\beta(s)}{\beta_\mathrm{ref}(s)}$ with a rectified linear unit (ReLU) function $R(x) = \mathrm{max}(1,x)$, which maps every value below one to one. This has the effect of a lower threshold, which disincentivizes to lower the beta function below the reference value at the expense of making it larger somewhere else. Larger changes can be more disincentivized by squaring the relative change. To ensure the vertical beta function $\beta_\mathrm{y}$ is small enough at the center of the T2 section $s_\mathrm{T2}$, it can be included in the objective function.

Taking the mentioned considerations into account, leads to the new objective function:

$$ F(\beta) = \frac{1}{L} \int_0^L R\left(\frac{\beta(s)}{\beta_\mathrm{ref}(s)}\right)^2 \mathrm{d}s + \beta_\mathrm{y}(s_\mathrm{T2}) \:\: \textrm{with } R(x) = \begin{cases} 1, &\textrm{for } x < 1\\ x, &\textrm{else} \end{cases}
$$ {#eq:objectiv-function}

With the developed code, this roughly translates to:

```python
def objective_function(values, quads):
    for quad, value in zip(quads, values):
        quad.k1 = value

    if not twiss.stable:
        return np.inf

    beta_beat_x = np.maximum(1, twiss.beta_x / twiss_ref.beta_x) ** 2
    beta_beat_y = np.maximum(1, twiss.beta_y / twiss_ref.beta_y) ** 2
    return np.mean([beta_beat_x, beta_beat_y]) + twiss.beta_y[t2_center]
```
The optimization procedure was run for different combinations of quadrupoles. Due to the improvements made to the Twiss calculation code, it was now possible to do much more iterations in a much shorter time. Furthermore, it was possible to run the optimization procedure multiple times in a row, using the last optimization result as a starting point for the next. @fig:twiss_q5t2off_sim_vs_std shows the Twiss parameters of the best obtained Q5T2off optics compared to the current standard user optics. A complete code snippet that reproduces the Q5T2off optics and explanation is included in the @sec:code-to-reproduce-q5t2off-optics.

![Twiss parameters of the best Q5T2off optics (solid) in comparison to the current standard user optics (dashed)](figures/twiss_q5t2off_sim_vs_std.svg){#fig:twiss_q5t2off_sim_vs_std}

@fig:q5t2off_ba_vs_ma.svg shows the $\beta$-beat of the new Q5T2off optics compared to the old Q5T2off optics. The old Q5T2off optics has a high horizontal $\beta_\mathrm{x}$-beat in the injection straight and a high vertical $\beta_\mathrm{y}$-beat all around the ring, including the femto-slicing section D6 and EMIL section T6. With the improvements to the Q5T2off optics, the $\beta$-beat outside of T2 and its adjacent sections is effectively negligible. For the horizontal plane, the changes within the T2 and its adjacent sections are primarily negative. For the vertical plane, there are two peaks at the beginning of the adjacent DBA. Furthermore, the vertical beta function at the center of the T2 section was reduced from 3.6 m to 1.8 m.

![Beta beat of the Q5T2off optics with the standard user optics (blue) compared to the beta beat of the best solution of the bachelors thesis (orange)](figures/q5t2off_ba_vs_ma.svg){#fig:q5t2off_ba_vs_ma.svg}


### User Operation Acceptance Test of the Q5T2 Optics {#sec:user-acceptance-test}

With improvements made to the Q5T2off optics, the following steps are to transfer the optics to the machine and test if it is ready for standard user operation. According to @hinterberger, the quadrupole strength is proportional to the current $I$

$$ k \approx 2 \frac{\mu_0 n I}{a^2} \frac{q}{p} \propto I,
$$ {#eq:k-prop-to-I}

where $\mu_0$ is the vacuum permeability, $a$ is the aperture radius and $n$ corresponds to the winding number. Therefore, the new power supply values can be calculated by the ratio of the new and old quadrupole strength times the old power supply value:

$$ I_\mathrm{new} = \frac{k_\mathrm{new}}{k_\mathrm{old}} I_\mathrm{old}
$$ {#eq:new-ps-values}

To make sure that the optics is transferred correctly to the machine, a precise measurement of the current quadrupole strengths $k_\mathrm{old}$ is necessary. Therefore, the Linear Optics From Closed Orbits (LOCO) method [@locosafranek;@mmlbasedloco] from the MatLab Middle Layer [@mmlpaper] can be used to determine the linear optics. The LOCO method first measures the orbit response matrix and the dispersion function. Afterward, the data is fitted to a lattice model to calculate the individual quadrupole strengths.

LOCO-measuring the current standard user optics started of the machine commissioning. Then a new Q5T2off optics was fitted based on the just LOCO-measured standard user optics. Next, the new power supply values were transferred to the machine using a program developed for this purpose, shown in @sec:gui-power-supply-values. After the machine was set to the new Q5T2off optics, another LOCO measurement was carried out to ensure the optics was transferred to the machine correctly. @fig:twiss_q5t2off_loco_vs_q5t2off_sim shows the Twiss parameters of the LOCO measured Q5T2off optics compared to the Twiss parameters of the Q5T2off optics obtained from the optimization. There seem to be some deviations in the horizontal beta function. Especially within some of the doublet sections, the beta function is slightly asymmetric to the center. However, the vertical beta function matches very closely with the one from the simulation. Overall, it can be said that the optics was transferred correctly. Finally, the quadrupole setting of the Q5T2off optics was saved in the control software to make it available for future machine commissions. @fig:twiss_q5t2off_loco_vs_std shows the LOCO-measured Q5T2off optics compared to the current standard user optics.

![Twiss parameters of loco measured Q5T2off optics (solid) in comparison to the Q5T2off optics obtained from the optimization (dashed)](figures/twiss_q5t2off_loco_vs_q5t2off_sim.svg){#fig:twiss_q5t2off_loco_vs_q5t2off_sim}

![Twiss parameters of loco measured Q5T2off optics (solid) in comparison to the current standard user optics (dashed)](figures/twiss_q5t2off_loco_vs_std.svg){#fig:twiss_q5t2off_loco_vs_std}

In another machine commissioning session, the Q5T2off optics was audited for standard user operation. During this user acceptance test, several smaller checks were performed. First, a small injection with low current was done to verify that the optics was correctly restored from the control software. Then, the quadrupoles were cycled to eliminate possible hysteresis effects. The orbit correction was used to improve the orbit. Next, a high current test was carried out. The current was injected up to 250 mA with injection efficiencies between 90% to 95%.

![Lifetime as a function of the vertical noise $V_\mathrm{N}$](figures/lifetime-measurement.png){#fig:lifetime-measurement}

@fig:lifetime-measurement shows the lifetime measurement. A vertical noise is used to inflate the vertical beam size, which reduces the probability of electron collisions within a bunch and therefore increases the lifetime. Touschek lifetime $\tau_\mathrm{T}$ and gas lifetime $\tau_\mathrm{G}$ are 8.5 and 21.4 hours, respectively. All in all, the measured lifetimes are close to the lifetimes of standard user optics.

Up next was the measurement of the kicker lifetimes. Here the kicker magnets of the orbit bump are fired rapidly without actually injecting a beam. If the lifetime is decreased during this process, electrons are lost at the septum, which would limit the possible injection efficiency. However, no effect on lifetime could be detected, which indicates an infinite kicker lifetime.

@tbl:chromaticity-measurement list the results of the chromaticity measurement, containing the values of the tune, first and second-order chromaticity for the Q5T2off optics compared to the standard user optics. The horizontal, vertical, and longitudinal tunes are unchanged. However, the vertical and longitudinal chromaticities of the Q5T2off optics are slightly smaller than in the standard user optics. Also, the 2ⁿᵈ order chromaticities are slightly smaller in the horizontal and vertical plane.

|     |  Tune  | Chroma | Chroma 2ⁿᵈ  |  Tune  | Chroma | Chroma 2ⁿᵈ |
| --- | ------ | ------ | ---------- | ------ | ------ | -------- |
| $x$ | 0.8485 | 1.9245 | -43.2045   | 0.8427 | 2.0929 | -47.2121 |
| $y$ | 0.7259 | 3.1846 | -63.0949   | 0.7264 | 3.1098 | -67.7113 |
| $z$ | 0.0061 | 0.0034 | 0.2384     | 0.0061 | 0.0058 | -0.7480  |
: Tune, first and second order chromaticity of the Q5T2off optics (left) and the standard user optics (right) {#tbl:chromaticity-measurement}

The streak camera was used to measure the length of the different bunches of the BESSY II fill pattern. Single bunch, PPRE bunch, slicing bunch, and multi-bunches had the same length as in the standard user optics. That was expected as the Q5T2off optics did not change the momentum compaction factor $\alpha_\mathrm{c}$.

![Phase acceptance scan off the Q5T2off optics compared to the standard user optics.](figures/phase_acceptance_q5t2off.svg){#fig:phase_acceptance_q5t2off}

As demonstrated in @kuskeli, improving the phase acceptance can increase the momentum acceptance, injection efficiency, and Touschek lifetime. At BESSY II, the longitudinal phase between the booster synchrotron and the storage ring can be varied. This allows measuring the injection efficiency as a function of the phase offset, also called a phase acceptance scan. The resulting curve's full width at half maximum (FWHM) can then define the phase acceptance. @fig:phase_acceptance_q5t2off shows the phase acceptance of Q5T2off optics compared to the standard user optics. Surprisingly, even with non-optimized sextuples, the phase acceptance seems wider but slightly lower than in the standard user optics. The FWHM of the curves are 1.2 ns and 0.9 ns, respectively. The fact that the phase acceptance of the standard optics was so small leaves the suspicion that the sextupole setting was not fully optimized during machine commissioning. Also demonstrated in @kuskeli, a phase acceptance of 1.5 ns FWHM for standard user optics is possible with an optimized sextupole setting.

The optics was run overnight as a long-term test. One thing that remains is to optimize the harmonic sextupole setting. However, all in all, the user acceptance test can be considered a success. Important beam parameters like lifetime, injection efficiency, phase acceptance, chromaticity, and kicker lifetime are as good as in the standard user optics.

## Emittance Exchange Experiment {#sec:emittance-exchange-experiment}

Besides optimizing the Q5T2-off optics, the developed code was also used to modify the BESSY II storage ring optics for an emittance exchange experiment. The experiment required a high horizontal beta function of 15 m at the center of the T2 straight while keeping the perturbation of the beta function small around the rest of the storage ring. The goal was to study if raising the beta function at the position of a skew quadrupole, set up by four striplines, would increase its resonant excitation. In theory, the higher amplitude due to the higher beta function should lead to a stronger skew quadrupole kick, increasing the transverse emittance exchange.

The standard user optics was modified using the objective function

$$ F(\beta) = \frac{1}{L} \int_0^L R\left(\frac{\beta(s)}{\beta_\mathrm{ref}(s)}\right)^2 \mathrm{d}s + (15 \mathrm{m} - \beta_\mathrm{x}(s_\mathrm{T2})) ^ 2  + \lvert\frac{\mathrm{d \beta_\mathrm{x}}}{\mathrm{d} s}(s_\mathrm{T2})\rvert ,
$$ {#eq:objectiv-function-emittance-exchange}

where $R(x) = \mathrm{max}(1,x)$ is the ReLU function thresholding at one. Similar to optimizing the Q5T2off optics, the first term is used to reduce the $\beta_\mathrm{x}$-beat around the rest of the ring. Moreover, the region between 40 m and 50 m is excluded from the integral as this would be in conflict with the second term. The ReLU function R(x) is composed with the relative residual of the beta function $\frac{\beta(s)}{\beta_\mathrm{ref}(s)}$ to disincentivize lowering the beta function below the reference value at the expense of making it larger somewhere else. The second term is used to raise the beta function to 15 m. The first derivative of the beta function $\frac{\mathrm{d \beta_\mathrm{x}}}{\mathrm{d} s}(s_\mathrm{T2})$ ensures the resulting optics is symmetrical at the center of T2 section.

![Optics 1 - High horizontal and low vertical beta and function in the T2 straight.](figures/twiss_t2_high_beta_x.svg){#fig:emittance-exchange-optics-1}

@fig:emittance-exchange-optics-1 shows an optics where all quadrupoles from the D2 to the D3 section were used for the optimization. Already described in @sec:user-acceptance-test, the optics was transferred to the machine by calculating the new power supply values from the old and new quadrupole strength ratio, using the tool shown in @sec:gui-power-supply-values. Afterward, the optics was LOCO-measured to ensure it was transferred correctly.

| Optics  | Skew Excitation | $\sigma_\mathrm{x}$ / μm | $\sigma_\mathrm{x} / \sigma_\mathrm{x,off}$ | $\sigma_\mathrm{y}$ / μm | $\sigma_\mathrm{y} / \sigma_\mathrm{y,off}$ |
|:--:|:--:|:--:|:--:|:--:|:--:|
| Standard User | off | 62.4 |      | 37.0  |      |
| Standard User | on  | 57.0 | 0.91 | 169.0 | 4.57 |
| ⎯ | ⎯ | ⎯ | ⎯ | ⎯ | ⎯ |
| Optics 1      | off | 58.0 |      | 41.3  |      |
| Optics 1      | on  | 52.8 | 0.91 | 227.0 | 5.54 |
| ⎯ | ⎯ | ⎯ | ⎯ | ⎯ | ⎯ |
| Optics 2      | off | 58.8 |      | 44.3  |      |
| Optics 2      | on  | 54.2 | 0.92 | 267.0 | 6.03 |
: Beam size depending on resonant skew excitations for the different optics {#tbl:beam-size-emittance-exchange}

The stripline in the center of the T2 section was set up as a skew quadrupole to excite the beam resonantly. A pinhole at the dipole at the end of the D5 section was used to measure the beam size. @tbl:beam-size-emittance-exchange list the beam sizes for the standard user optics and the optics with the high horizontal beta function with the skew excitation turned on and off. Without any excitation, the standard user optics' horizontal and vertical beam sizes at the pinhole are 62.4 μm and 37.0 μm, respectively. Despite the small coupling of below 2%, the vertical beam size is $\sigma_\mathrm{y}$ comparable to the horizontal beam size $\sigma_\mathrm{x}$, since the vertical beta function $\beta_\mathrm{y}$ is many times larger than the horizontal beta function $\beta_\mathrm{x}$ at the pinhole position. With the resonant skew excitation turned on, the horizontal beam size decreases to 57.0 μm while the vertical beam size increases to 169.0 μm. As the beam size is defined by $\sigma_\mathrm{u} = \sqrt{\epsilon_\mathrm{u} \beta_\mathrm{u}}$, this change corresponds to a decrease of the horizontal emittance to $0.91^2 = 0.83$.

Without the excitation, the optics with the high horizontal beta function has a slightly smaller horizontal beam size $\sigma_\mathrm{x}$ of 58.0 μm and a slightly larger vertical beam size $\sigma_\mathrm{y}$ of 41.3 μm. While the Twiss parameters seem to have been unaffected in the D5 section in simulation, this change can probably still be attributed to a change of the beta functions when the optics was transfered to the machine. Surprisingly, with the skew excitation turned on, the horizontal emittance only decreased to 52.8 μm, corresponding to 91 %, which is the same value as in the standard user optics. Thus, in contradiction to the expected results, the additional horizontal amplitude at the skew quadrupole did not seem influence the emittance exchange.

![Optics 2 - High horizontal and high vertical function in the T2 straight.](figures/twiss_t2_high_beta_x_y.svg){#fig:emittance-exchange-optics-2}

Therefore, during the same machine commissioning session, it was decided to fit a second optics where also the vertical beta function is raised to 15 m. For this, the objective function was extended by the vertical analog of the second and third terms of @eq:objectiv-function-emittance-exchange. @fig:emittance-exchange-optics-2 shows the Twiss parameters of the optics with both beta functions raised to 15 m in the center of the T2 section. The optics was again LOCO-measured to ensure it was transferred to the machine correctly. Again, the horizontal and vertical beam sizes were measured with the skew excitation on and off. Also, this time, the horizontal beam size was decreased to 0.92 of its size without excitation.

While it requires more investigation in simulations as well as in experiments why the larger amplitude at the skew quadrupole did not increase the emittance exchange, the experiment showed that the developed code is flexible enough to support various lattice development tasks.

## Automated Lattice Summaries  {#sec:lattice-summaries}

@sec:automated-lattice-summaries outlined the need for a shared database of lattice files and automatically generated summaries: Physicists often repeat the cumbersome work of manually translating between different lattice file formats. In addition, simulations results are often difficult to reproduce or transfer to similar lattice development tasks. Finally, a standardized visualization of the simulation results would make lattices easier to compare.

An infrastructure that makes not only the lattices files sharable but also the simulation routines and visualization of the results could solve these problems. Ideally, a user only has to add a lattices file to the database. Then, a set of routines leveraging different simulation codes would be run locally or in the cloud. Finally, the simulation results would be summarized by a standardized lattice report. Due to the lattice summarizes being contentwise and visually consistent, the user could conveniently compare different lattices.

Such a framework could be valuable in different scenarios: It could facilitate collaborative lattice development within a facility. For example, in the case of HZB, it could be used to benchmark BESSY III lattice candidates. Furthermore, it could also facilitate the exchange of lattice files between different facilities. One tangible idea would be to create an updated version of the Synchrotron Light Source Data Book [@murphy_1996]. That could be realized by a website where every facility could contribute to. Even in cases of smaller lattice development tasks, which do not involve several people, a standardized interface to set up routines and organize lattice files is still beneficial. Using the same framework for local lattice development incentives collaboration as no extra work is required to share custom simulation routines. Reproducing the simulation result and plots of a colleague would then come down to running one command with the name of the routine and lattice file as arguments:

```sh
lattice-summaries <name-of-routine> <name-of-lattice>
```

This section presents the prove-of-concept framework *lattice-summaries*, developed based on the lattice file format LatticeJSON. Currently, it provides routines to calculate the Twiss parameters using elegant @elegant, MAD-X @madx, or the simulation code developed for this thesis. @sec:lattice-summaries-architecture outlines the architecture of the *lattice-summaries* framework. The following subsections provide a more detailed overview of the different components of the framework.

### Architecture {#sec:lattice-summaries-architecture}

The source code of the *lattice-summaries* framework can be found on GitHub under the *nobeam* organization ([https://github.com/nobeam](https://github.com/nobeam)).

The framework is split up into three different repositories:

1. [lattice-summaries-data](https://github.com/nobeam/lattice-summaries-data): A database of lattices files and optional run parameters
2. [lattice-summaries](https://github.com/nobeam/lattice-summaries): A set of routines leveraging different simulation codes
3. [lattice-summaries-website](https://github.com/nobeam/lattice-summaries-website): A website to inspect the simulation results

![Schematic overview of the lattice summaries architecture](figures/lattice-summaries-how-it-works.svg){#fig:lattice-summaries-how-it-works}

@fig:lattice-summaries-how-it-works gives a schematic overview of the lattice summaries architecture. A user uploads a new lattice file and optional run files to the *lattice-summaries-data* repository, which functions as the database. Then routines defined in the *lattice-summaries* repository are run for all selected lattices. Next, the simulation results are uploaded and served by a static web server. Now the simulation results can be viewed through a website, which dynamically creates the summary views for the given simulation data. The *lattice-summaries-website* repository contains the source code of the website.

The presented architecture was chosen to offer maximum flexibility: Keeping the data repository and repository containing the simulation routines separate makes it possible to support multiple instances. This way, the data repository can be switched out so that different facilities can create their own instances for private lattice development. A public instance, for example, could be used to create an updated version of the Synchrotron Light Source Data Book. Furthermore, this allows the framework to be used for local lattice development, as a local instance of the data repository can be used.

The repository containing the website and the simulations results are also kept separate. That has the advantage that the website does not have to be updated when new simulation results are computed. That is convenient in the case of local lattice development, where the simulation results change frequently.

### Database of Lattice Files {#sec:database-of-lattice-files}

As most lattice file formats are plain text files, using Git seemed reasonable to build the database. The alternative would have been to use some NoSQL database and built a small API on top of it so that people could contribute and review new lattices. However, this seemed like unnecessary work as most of the functionality is already provided by the Git ecosystem. For example, hosting systems for Git repositories like GitHub or GitLab already provide the functionality to contribute, review contributions and run custom code in the event of a new contribution. Furthermore, Git has the advantage that it is ubiquitous, and many physicists are already familiar with how to use it.

The lattices are split into different namespaces so that multiple physicists can work on similar lattices without creating a name collision. In general, the lattice files follow the naming schema:

```sh
<namespace> / <machine>_<familiy>_v_<version>
```

An exemplary folder structure of a lattice database looks like:


```sh
database
├── namespace-1
│  ├── bessy2_design-1996_v_1.json
│  ├── bessy2_stduser-2019-05-07-v_1.json
│  └── info.toml
├── namespace-2
│  ├── bessy3_5ba-20p_v_long-bend-tgrb.lte
│  ├── bessy3_5ba-20p_v_reference.lte
│  └── info.toml
...
```

Every namespace contains an `info.toml` file, which contains additional metadata. That includes the human-readable title, an optional description, a list of authors, a list of labels, and a list of simulation routines that should be run for the given lattice.
The list of simulation routines is necessary because a lattice file might contain special elements unique to a given simulation, not available for the other simulation routines. Possible labels, for example, could be if the lattice contains anti-bends, combined functions magnets, or longitudinal gradient bends. A detailed explanation of adding a lattice to the database can be found in the `README.md` file of the [lattice-summaries-data](https://github.com/nobeam/lattice-summaries-data) repository.

### Set of Routines

The set of routines are responsible for generating the simulation results. This is arguably the most complex part. These routines can be dependent on each other. For example, to run the routine that plots the Twiss parameters, a routine that calculates them must be run first. If the lattice is not available in the necessary format, another routine has to be run before translating the lattice file to the needed format.

The goal is that different simulation codes can power these routines, with more routines being added over time. Currently, the *lattice-summaries* framework provides the following routines: One routine that translates lattice files between the LatticeJSON format and the lattice file formats used by elegant and MAD-X. One routine extracts general information about the lattice, such as the circumference, energy, number of sections, section length, or bends per section. Three routines that compute the Twiss parameters using either elegant, MAD-X, or the developed code for this thesis. Furthermore, three routines that plot the Twiss parameters, a floor plan, or the higher-order chromaticity.

For local lattice development, the users change a config file to use their private version of the lattice database if they need a lattice not available in the shared database. Another convenience feature is that the dependency relation between the routines is lazy evaluated, which means that simulation is not rerun if a user only adjusts code, which is part of a visualization routine. Detailed instructions on the setup and usage are provided in `README.md` file of the [lattice-summaries](https://github.com/nobeam/lattice-summaries) repository.


### Lattice Summaries Website

This website provides a frontend to view the simulation results. The website is developed as a Single Page Application (SPA) using the JavaScript Framework [Vue.js 3](https://vuejs.org/) @vuejs and the build tool [Vite](https://vitejs.dev/) @vitejs. A SPA is a website that, on user interaction, dynamically rewrites the current web page instead of fetching a pre-rendered page from a server. The advantage is that the website does not have to be updated if new simulation results are uploaded. Instead, new pages are created dynamically in the frontend. Furthermore, it makes it possible to use the website for local development. By changing the `DATA_URL` environment variable, the user can display local simulation results.

Currently, the website consists out of three views:

1. A landing page that lists all lattices
2. A lattice view, which lists an overview of the available summaries for that lattice
3. Different types of summary views depending on the simulation routine

![Screenshot of the landing page of the lattice summaries website](figures/lattice-summaries-landing-page.png){#fig:lattice-summaries-landing-page}

@fig:lattice-summaries-landing-page shows a screenshot of the landing page. It provides a search bar where lattices can be filtered by name. Furthermore, lattices can be filtered by *Namespace*, *Machine*, and *Author*. The search results are displayed as cards. These cards provide a short description, links to the corresponding lattice file in different formats, and links to the different types of summaries available for the given lattice.

![Screenshot of an examplary lattice summary of the BESSY II design lattice](figures/lattice-summaries-design-lattice.png){#fig:lattice-summaries-design-lattice}

@fig:lattice-summaries-design-lattice shows an exemplary lattice summary of the BESSY II design lattice generated by the apace simulation code. The lattice summary consists out of different cards which provide different information. Independent of the type of summary, the first card is an info-card identical to the card shown in the search results. All other cards are specific to the type of summary. For example, in the case of the Twiss summary generated by the apace code, the second card provides some general information on the lattice. That includes energy, circumference, number of bends, number of sections or, section length. The third card provides a plot with the beta function and horizontal dispersion function for the unit cell. Other lattice parameters like the momentum compaction factor, emittance, or the synchrotron radiation integrals are listed in a table on the fourth card. The last card shows a floor plan of the unit cells.
