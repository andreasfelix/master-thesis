import apace as ap

d1 = ap.Drift("d1", length=0.55)
b1 = ap.Dipole("b1", length=1.5, angle=0.392701, e1=0.1963505, e2=0.1963505)
q1 = ap.Quadrupole("q1", length=0.2, k1=1.2)
q2 = ap.Quadrupole("q2", length=0.4, k1=-1.2)
fodo = ap.Lattice("FODO", [q1, d1, b1, d1, q2, d1, b1, d1, q1])
ring = ap.Lattice("RING", 8 * [fodo])

twiss = ap.Twiss(ring)

import apace.plot as aplot
import matplotlib.pyplot as plt

from master_thesis import figure_path

fig, ax = plt.subplots()
ax.plot(twiss.s, twiss.beta_x, label=r"$\beta_\mathrm{x}$ / m")
ax.plot(twiss.s, twiss.beta_y, label=r"$\beta_\mathrm{x}$ / m")
ax.plot(twiss.s, twiss.eta_x, label=r"$\eta_\mathrm{x}$ / m")
ax.set(xlabel="orbit position $s$ / m")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)
aplot.draw_elements(ax, ring, location="bottom")
aplot.draw_sub_lattices(ax, ring, location="bottom")
fig.tight_layout()
plt.savefig(figure_path / "fodo-twiss-apace.svg")
