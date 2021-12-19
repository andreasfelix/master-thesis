from pathlib import Path

import apace as ap
import apace.plot as aplot
import numpy as np
import matplotlib.pyplot as plt

from master_thesis import figure_path


lattice_dir = Path(__file__).parent

fodo = ap.Lattice.from_file(lattice_dir / "lattices/fodo.json")

twiss = ap.Twiss(fodo)

emittance_x = 1e-9
delta = 0.0001
x_beta = np.sqrt(emittance_x * twiss.beta_x) * np.cos(twiss.psi_x)
x_delta = delta * twiss.eta_x
x_delta_2 = 0.5 * delta * twiss.eta_x
x_tot = x_beta + x_delta

fig, ax = plt.subplots()
ax.plot(twiss.s, x_tot, label="x_tot")
ax.plot(twiss.s, x_beta, label="x_beta")
ax.plot(twiss.s, x_delta, label="x_delta")
ax.plot(twiss.s, x_delta_2, label="x_delta_2")
aplot.draw_elements(ax, fodo)

ax.hlines(0, 0, fodo.length, color="black")
ax.set(xlim=(0, fodo.length))

fig.legend()
fig.savefig(figure_path / "transverse-offset.svg")
