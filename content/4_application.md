# Applications

This chapter covers the applications of the developed optics simulation progam at the BESSY II storage ring. The first section comprises the development of the Q5T2-off optics with regard to the VSR project. In the second section the shows how the code was used to adapt the beta functions within a straight for a emittance exchange experiment. Possible future applications are discussed in the third chapter.

## Adjusting the BESSY II Optics for the VSR project

The cavity module needs more space than initially assumed ...

### Optimizing the Q5T2 Optics in Simulations

The first steps towards a Q5T2 optics are described in my bachelor's thesis [@andreas_ba]. With the best solution found it was possible to achieve a working machine with reasonable injection efficency and lifetime. An issue was the relatively high beta beat along the storage ring. As the sextupole settings is carefully finetuned for the current standard user mode and to avoid confilicitng with previous made considerations, the goal should be to reduce the beta beat as much as possible.

Due to the improvements made to the Twiss calculation code, it was now possible to do much more iterations in a much shorter time span: An 

$$
F(\beta) = \frac{1}{L} \int_0^L R\left(\frac{\beta(s)}{\beta_{\mathrm{ref}}(s)}\right)^2 \mathrm{d}s \quad \textrm{with } R(x) = \begin{cases} 1, &\textrm{for } x < 1\\ x, &\textrm{else} \end{cases}
$$ {#eq:objectiv-function}

With the developed code this roughly translates to:

```python
def fitness(params):
    for element, attribute, param in zip(elements, attributes, params):
        setattr(element, attribute, param)

        if not twiss_fit.stable:
            return float("inf")

        beta_x_beat = twiss.beta_x / ref_twiss.beta_x
        beta_y_beat = twiss.beta_y / ref_twiss.beta_y
        beta_x_beat[beta_x_beat < 1] = 1
        beta_y_beat[beta_y_beat < 1] = 1
        beta_x_beat **= 2
        beta_y_beat **= 2
        return np.mean([beta_x_beat, beta_y_beat])

scipy.optimize.minimize(fitness, initial_values)
```

**Ausflug der nichts damit zu tun hat (Exkurs): Splitting the D2/D3 families**

### User Operation Acceptance Test of the Q5T2 Optics

The new obtained opitcs was


multiknob

1. Injection Efficiency
2. Kicker Lifetime
3. IDs, bumps
4. High current test
5. General effects on user operations

<!-- extracted From old abstract

A tool was developed which can change the minimum beta function within the given straight by interpolating between two different optics. The sextupoles were used to optimize the phase acceptance to such an extent that they were better than in the current standard optics. In another session the optics was successful audited for user operation by testing for high current, life time, kicker lifetime, bunch length and chromaticity. -->

## High Beta Functions in T2 (Emittance Exchange)

Besides of the Q5T2-off optics, the developed Twiss optimization code was also used for an emittance exchange experiment. The experiment required a large and constant beta function of 15m along the whole T2 straight while retaining the beta function the same within the rest of the storage ring.

![High horizontal and low vertical beta and function in the T2 straight.](figures/emittance-exchange-optics-1.png){#fig:emittance-exchange-optics-1}

![High horizontal and hight vertical function in the T2 straight.](figures/emittance-exchange-optics-2.png){#fig:emittance-exchange-optics-2}

## Future Applications
