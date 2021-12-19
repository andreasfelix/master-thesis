import apace as ap
import matplotlib.pyplot as plt
import numpy as np
from fodo import make_fodo

from master_thesis import figure_path

angles = [0, np.pi / 8, np.pi / 4]
fodo = make_fodo(angle=angles[1])
d1, b1, q1, q2 = (fodo[name] for name in ("d1", "b1", "q1", "q2"))
twiss = ap.Twiss(fodo)

steps = 1000
lengths = [0.5, 1.0, 1.5]
n_rows, n_cols = len(lengths) + 1, len(angles)
fig, axs = plt.subplots(
    nrows=n_rows,
    ncols=n_cols,
    figsize=(4 * n_cols, 2.5 * n_rows),
    gridspec_kw={"height_ratios": [0.01, 1, 1, 1]},
)

for ax, angle in zip(axs[0], angles):
    ax.axis("off")
    ax.set_title(
        f"Dipole angle ({np.degrees(angle)}° per cell)", fontweight="bold", pad=0
    )

for column, angle in zip(axs[1:].T, angles):
    b1.angle = angle
    b1.e1 = b1.e2 = 0.5 * angle

    for ax, length in zip(column, lengths):
        d1.length = length
        # breakpoint()
        extent = 0, 2, 0, -2
        results = np.empty((steps, steps))
        for i, q1.k1 in enumerate(np.linspace(*extent[:2], steps)):
            for j, q2.k1 in enumerate(np.linspace(*extent[2:], steps)):
                try:
                    results[i, j] = np.mean(twiss.beta_x) + np.mean(twiss.beta_y)
                except ap.UnstableLatticeError:
                    results[i, j] = np.nan
        image = ax.imshow(
            results.T, extent=extent, origin="lower", vmin=0, vmax=30, cmap="cool"
        )
        ax.set_xlabel(f"$k_\\mathrm{{{q1.name}}}$ / m$^{{-2}}$")
        ax.set_ylabel(f"$k_\\mathrm{{{q2.name}}}$ / m$^{{-2}}$")
        ax.set_title(f"cell length: {fodo.length} m")
        colorbar = fig.colorbar(image, ax=ax)
        colorbar.ax.set_title(r"$\beta_\mathrm{mean}$", fontsize=12, pad=10)

plt.tight_layout()
plt.savefig(figure_path / "necktie-plot.svg")
