from math import pi

import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt
import numpy as np

bessy2 = ap.Lattice.from_file("lattices/tribs.json")
twiss = ap.Twiss(bessy2, energy=1700)


fig = plt.figure("blabla", (20, 10))

plt.plot(twiss.s, np.sqrt(twiss.emittance_x * twiss.beta_x), "k--")
plt.plot(twiss.s, -np.sqrt(twiss.emittance_x * twiss.beta_x), "k--")
for turn, color in zip(range(3), "rbg"):
    plt.plot(
        twiss.s,
        np.sqrt(twiss.emittance_x * twiss.beta_x)
        * np.cos(twiss.psi_x + turn * 2 * pi * twiss.tune_x),
        color,
        label=f"turn {turn}",
    )
plt.legend()
aplot.draw_lattice(bessy2, annotate_elements=False)

fig.savefig("tribs.pdf")
