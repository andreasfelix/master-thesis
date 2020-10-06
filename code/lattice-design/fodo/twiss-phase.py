from math import pi

import apace as ap
import numpy as np
from apace.plot import draw_lattice, plot_twiss, plt

from fodo import create_fodo, figure_path

fodo = create_fodo(pi / 8)
fodo = ap.Lattice("ring", 4 * [fodo])
twiss = ap.Twiss(fodo, energy=1000)
amplitude = 0.001
beta_0 = twiss.beta_x[0]
particles = np.array([[amplitude], [0], [0], [0], [0], [0]])
tracking = ap.TrackingMatrix(fodo, particles)

fig, (ax0, ax1, ax2) = plt.subplots(3, figsize=(6.4, 6.4))

plt.sca(ax0)
envelope = amplitude * np.sqrt(twiss.beta_x / twiss.beta_x[0])
ax0.plot(twiss.s, envelope, "k--")
ax0.plot(twiss.s, -envelope, "k--")
ax0.plot(twiss.s, tracking.x)
draw_lattice(fodo)
ax0.set_xlabel("Orbit position $s$ / m")
ax0.set_ylabel("$x(s)$ / m")

plt.sca(ax1)
envelope = tracking.x[0] / np.sqrt(twiss.beta_x[0])
ax1.axhline(envelope, color="black", linestyle="--")
ax1.axhline(-envelope, color="black", linestyle="--")
ax1.plot(twiss.s, tracking.x.squeeze() / np.sqrt(twiss.beta_x))
ax1.set_ylim(-4e-4, 4e-4)
draw_lattice(fodo, location="bottom")
ax1.set_xlabel("Orbit position $s$ / m")
ax1.set_ylabel(r"$x(s) / \sqrt{\beta(s)}$")

ax2.plot(twiss.psi_x, tracking.x.squeeze() / np.sqrt(twiss.beta_x))
ax2.set_xlabel(r"Betatron phase $\psi_x(s)$")
ax2.set_ylabel(r"$x(s) / \sqrt{\beta(s)}$")
plt.sca(ax2)
plt.xticks(
    [0, pi / 2, pi, 3 * pi / 2, 2 * pi],
    ["$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"],
)

plt.tight_layout()
plt.savefig(figure_path / "fodo-twiss-floquet.svg")
