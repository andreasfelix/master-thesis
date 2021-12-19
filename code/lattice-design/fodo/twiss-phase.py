from math import pi

import apace as ap
import matplotlib.pyplot as plt
import numpy as np
from apace.plot import draw_elements
from fodo import make_fodo

from master_thesis import figure_path

n_cells = 4
cell = make_fodo(pi / 8)
fodo = ap.Lattice(f"{n_cells}-fodo", n_cells * [cell])
twiss = ap.Twiss(fodo, energy=1000)
amplitude = 0.001
beta_0 = twiss.beta_x[0]
particles = np.array([[amplitude], [0], [0], [0], [0], [0]])
tracking = ap.TrackingMatrix(fodo, particles)

fig, (ax0, ax1, ax2) = plt.subplots(3, figsize=(6.4, 6.4))

envelope = amplitude * np.sqrt(twiss.beta_x / twiss.beta_x[0])
ax0.plot(twiss.s, envelope, "k--")
ax0.plot(twiss.s, -envelope, "k--")
ax0.plot(twiss.s, tracking.x)
ax0.set(xlim=(0, fodo.length))
ax0.set(xlabel="Orbit position $s$ / m", ylabel="$x(s)$ / m")
draw_elements(ax0, fodo)

envelope = tracking.x[0] / np.sqrt(twiss.beta_x[0])
ax1.axhline(envelope, color="black", linestyle="--")
ax1.axhline(-envelope, color="black", linestyle="--")
ax1.plot(twiss.s, tracking.x.squeeze() / np.sqrt(twiss.beta_x))
ax1.set(xlim=(0, fodo.length), ylim=(-4e-4, 4e-4))
ax1.set(xlabel="Orbit position $s$ / m", ylabel=r"$x(s) / \sqrt{\beta(s)}$")
draw_elements(ax1, fodo)

# plot phase-displacement
ax2.plot(twiss.psi_x, tracking.x.squeeze() / np.sqrt(twiss.beta_x))
ax2.axhline(envelope, color="black", linestyle="--")
ax2.axhline(-envelope, color="black", linestyle="--")

# change length of elements to length in psi_x
positions = np.add.accumulate([0, *(x.length for x in fodo.sequence)])
psi = np.interp(positions, twiss.s, twiss.psi_x)
lengths_stretched = psi[1:] - psi[:-1]
q1 = ap.Quadrupole("q1", lengths_stretched[0], 0)
d1 = ap.Drift("d1", lengths_stretched[1], 0)
b1 = ap.Dipole("b1", lengths_stretched[2], 0)
d2 = ap.Drift("d2", lengths_stretched[3], 0)
q2 = ap.Quadrupole("q2", lengths_stretched[4], 0)
cell_stretched = ap.Lattice("fodo-stretched", [q1, d1, b1, d2, q2, d2, b1, d1, q1])
fodo_stretched = ap.Lattice(f"{n_cells}-fodo-stretched", n_cells * [cell_stretched])
ax2.set(xlim=(0, twiss.psi_x[-1]), ylim=(-4e-4, 4e-4))
draw_elements(ax2, fodo_stretched)

ax2.set_xlabel(r"Betatron phase $\psi_x(s)$")
ax2.set_ylabel(r"$x(s) / \sqrt{\beta(s)}$")
plt.xticks(
    [0, pi / 2, pi, 3 * pi / 2, 2 * pi],
    ["$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"],
)

plt.tight_layout()
plt.savefig(figure_path / "fodo-twiss-floquet.svg")
