import apace as ap
import matplotlib.pyplot as plt
import numpy as np

from fodo import make_fodo
from master_thesis import figure_path

# wille fodo ring
# fodo = make_fodo(angle=np.pi / 8, drift_length=2.2, bend_length=3, quad_length=0.8)
fodo = make_fodo(angle=np.pi / 8, drift_length=4, bend_length=3, quad_length=1, k1=0.8)
q1, q2 = (fodo[name] for name in ("q1", "q2"))

k1s = np.linspace(0.01, 1.0, 100)
chromaticity_x = np.empty(k1s.shape)
chromaticity_y = np.empty(k1s.shape)
emittance_x = np.empty(k1s.shape)
twiss = ap.Twiss(ap.Lattice("ring", 8 * [fodo]), energy=1000, steps_per_meter=20)

for i, (q1.k1, q2.k1) in enumerate(zip(k1s, -k1s)):
    chromaticity_x[i] = twiss.chromaticity_x
    chromaticity_y[i] = twiss.chromaticity_y
    emittance_x[i] = twiss.emittance_x

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5))

ax1.semilogy(k1s, emittance_x)
ax1.set(xlabel="$k$ / m$^{-2}$", ylabel=r"$\epsilon_\mathrm{x}$ / m rad")
ax1.grid()

ax2.plot(k1s, 8 * chromaticity_x, label=r"$\xi_\mathrm{x}$")
ax2.plot(k1s, chromaticity_y, label=r"$\xi_\mathrm{y}$")
ax2.invert_yaxis()
ax2.set(xlabel="$k$ / m$^{-2}$")
ax2.legend()
ax2.grid()

fig.tight_layout()
fig.savefig(figure_path / "fodo-chromaticity-emittance.svg")
