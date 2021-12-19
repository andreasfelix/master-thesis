import matplotlib.pyplot as plt
import numpy as np

from master_thesis import figure_path

sigmas_injected = [5, 2]
sigma_stored = 1
septum_thickness = 10
x_stored = 0
x_septum = septum_thickness + 4 * sigma_stored
lims = 70
n_particle = 4000

fig, axs = plt.subplots(ncols=2, figsize=(8, 4), dpi=300)
for ax, sigma_injected in zip(axs, sigmas_injected):
    x_injected = septum_thickness + 4 * sigma_stored + 4 * sigma_injected
    aperture = 8 * sigma_injected + 4 * sigma_stored + septum_thickness

    # stored beam
    mean = [x_stored, 0]
    cov = [[sigma_stored ** 2, 0], [0, sigma_stored ** 2]]
    positions = np.random.multivariate_normal(mean, cov, n_particle)
    ax.scatter(*positions.T, 0.05, marker=".", color="black", rasterized=True)
    ax.annotate("Stored Beam", (0, 6), ha="center", color="black")

    # injected beam
    mean = [-x_injected, 0]
    cov = [[sigma_injected ** 2, 0], [0, sigma_injected ** 2]]
    positions = np.random.multivariate_normal(mean, cov, n_particle)
    ax.scatter(*positions.T, 0.05, marker=".", rasterized=True)
    ax.annotate("Injected Beam", (-5, 13), ha="center", c="#1f77b4")

    ax.set_aspect("equal")
    ax.spines["left"].set_position(("data", 40))
    ax.spines["left"].zorder = -9
    ax.spines["bottom"].set_position(("data", 0))
    ax.spines["bottom"].zorder = -9
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(40, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

    # septum
    color = "darkorange"
    ax.annotate("Septum", (-7, -9), ha="center", color=color)
    ax.add_patch(plt.Rectangle((-x_septum, -1.5), septum_thickness, 3, color=color))

    # acceptance
    color = "darkred"
    ax.add_patch(
        plt.Circle((0, 0), radius=aperture, color=color, fill=None, linestyle="dashed")
    )
    ax.annotate("Required Acceptance", (0, 34), ha="center", color=color)

    ax.set_xlim(-lims, lims)
    ax.set_ylim(-lims, lims)
    ax.set_xlabel("x", loc="right")
    ax.set_ylabel("x'", loc="top")

fig.tight_layout()
fig.savefig(figure_path / "aperture-emittance-requirement.svg")
