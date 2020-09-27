import matplotlib.pyplot as plt
import numpy as np

import apace as ap
import apace.plot as aplot
from quad_scan import make_dba

dba = make_dba(three_famlies=False)
twiss = ap.Twiss(dba, steps_per_element=10)
steps = 50
max_value = 4
quad_1 = dba["q1"]
quad_2 = dba["q2"]

eta_straight = np.empty((steps, steps))
beta_mean = np.empty((steps, steps))
tune_x = np.empty((steps, steps))
tune_y = np.empty((steps, steps))
extent = 2 * [-max_value, max_value]
for i, quad_1.k1 in enumerate(np.linspace(*extent[:2], steps)):
    for j, quad_2.k1 in enumerate(np.linspace(*extent[2:], steps)):
        try:
            beta_mean[i, j] = 0.5 * (np.mean(twiss.beta_x) + np.mean(twiss.beta_y))
            eta_straight[i, j] = twiss.eta_x[0]
            tune_x[i, j] = twiss.tune_x
            tune_y[i, j] = twiss.tune_y
        except ap.UnstableLatticeError:
            beta_mean[i, j] = np.nan
            eta_straight[i, j] = np.nan
            tune_x[i, j] = np.nan
            tune_y[i, j] = np.nan


fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
for ax, (title, value) in zip(
    axs.flatten(),
    (
        ("$\\beta_{x,avg}$", beta_mean),
        ("$\\eta_{x,straight}$", eta_straight),
        ("$Q_{x}$", tune_x),
        ("$Q_{y}$", tune_y),
    ),
):
    heatmap = ax.imshow(
        value,
        cmap="rainbow",
        extent=extent,
        origin="lower",
        vmin=0,
        vmax=np.nanmedian(value),
    )
    ax.set_xlabel(f"Q1$_{{k1}}$")
    ax.set_ylabel(f"Q2$_{{k1}}$")
    ax.set_title(title)
    fig.colorbar(heatmap, ax=ax)


plt.tight_layout()
# plt.show()
plt.savefig("../plots/dba_quad_scan_2_families.pdf")



quad_1.k1 = 2.3
quad_2.k1 = -1.72
aplot.twiss_plot(twiss, sections=(0, dba["cell"].length), eta_x_scale=1000)
plt.savefig("../plots/dba_twiss.pdf")
dba.as_file("dba.json")
