import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from scipy import optimize

from dba import dba, quads

twiss = ap.Twiss(dba, steps_per_element=2)

#%% fit achromatic condition
max_value = 10
bounds = ((-max_value, max_value) for _ in quads)


def func(values, *quads):
    for value, magnet in zip(values, quads):
        magnet.k1 = np.clip(value, -max_value, max_value)
    try:
        twiss.n_steps // 2
        # return abs(
        #     5 * twiss.eta_x[0] - twiss.eta_x[twiss.n_steps // 2]
        # ) + 0.001 * np.mean(twiss.beta_x + twiss.beta_y)
        return (
            200 * np.abs(twiss.eta_x[0])
            + np.mean(twiss.beta_x + twiss.beta_y)
            + 20 * max(values)
        )
        # return twiss.eta_x[0]
    except ap.UnstableLatticeError:
        return np.inf


results = optimize.minimize(
    func,
    np.array([x.k1 for x in quads]),
    args=quads,
    method="Nelder-Mead",
    bounds=bounds,
)

print(f"{dba.name} with cell length {cell.length}m:")
print("".join(f"{x.name}: {x.k1}\n" for x in quads))

ax = plt.subplot(2, 1, 1)
aplot.plot_twiss(twiss, ax=ax, eta_x_scale=100)
aplot.draw_lattice(dba, x_max=cell.length)
ax.set_xlim(0, cell.length)
ax.legend(
    loc="lower left", bbox_to_anchor=(0.0, 1.05), ncol=10, frameon=False,
)
print(f"eta_x0: {twiss.eta_x[0]}")
