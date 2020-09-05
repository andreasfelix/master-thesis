import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

import math

n_cells = 30
angle = math.pi / n_cells
angle_2 = 0.5 * angle

# DBA
d1 = ap.Drift("d1", 0.75)
q1 = ap.Quadrupole("q1", length=0.125, k1=1.0)
q2 = ap.Quadrupole("q2", length=0.25, k1=-1.0)
b1 = ap.Dipole("b1", 1.5, angle=angle, e1=angle_2, e2=angle_2)
cell = ap.Lattice(
    "cell", [d1, q1, d1, q2, d1, b1, d1, q1, q1, d1, b1, d1, q2, d1, q1, d1],
)
dba = ap.Lattice("dba", n_cells * [cell])
twiss = ap.Twiss(dba, steps_per_element=1)
magnets = q1, q2


# fit achromatic condition
def func(values, *args):
    magnets = args
    for value, magnet in zip(values, magnets):
        magnet.k1 = value

    try:
        return 20000 * twiss.eta_x[0] + np.mean(twiss.beta_x + twiss.beta_y)
    except ap.UnstableLatticeError:
        return np.inf


results = optimize.minimize(
    func, np.array([x.k1 for x in magnets]), magnets, "Nelder-Mead"
)

print(f"{dba.name} with cell length {cell.length}m:")
print("".join(f"{x.name}: {x.k1}\n" for x in magnets))

ax = plt.subplot(2, 1, 1)
aplot.plot_twiss(twiss, ax=ax)
aplot.draw_lattice(dba, x_max=cell.length)
ax.set_xlim(0, cell.length)


# quadrupole scan
steps = 200
eta_straight = np.empty((steps, steps))
beta_mean = np.empty((steps, steps))
extent = [-3, 3, -3, 3]
magnets = q1, q2
for i, magnets[0].k1 in enumerate(np.linspace(*extent[:2], steps)):
    for j, magnets[1].k1 in enumerate(np.linspace(*extent[2:], steps)):
        try:
            beta_mean[i, j] = np.mean(twiss.beta_x) + np.mean(twiss.beta_y)
            eta_straight[i, j] = twiss.eta_x[0]
        except ap.UnstableLatticeError:
            beta_mean[i, j] = np.nan
            eta_straight[i, j] = np.nan

for i, (title, value) in enumerate(
    (("$\\beta_{x,avg}$", beta_mean), ("$\\eta_{x,straight}$", eta_straight)), 3
):
    ax = plt.subplot(2, 2, i)
    heatmap = ax.imshow(
        value, extent=extent, cmap="RdBu", origin="lower", vmax=np.nanmedian(value),
    )
    ax.set_xlabel(f"{magnets[0].name}$_{{k1}}$")
    ax.set_ylabel(f"{magnets[1].name}$_{{k1}}$")
    ax.set_title(title)
    plt.plot(results.x[0], results.x[1], "x")
    plt.gcf().colorbar(heatmap, ax=ax)


plt.tight_layout()
plt.savefig("plots/dba.pdf")
