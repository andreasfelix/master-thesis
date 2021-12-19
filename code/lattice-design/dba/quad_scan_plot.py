import pickle

import matplotlib.pyplot as plt
import numpy as np

from master_thesis import figure_path

#%% plot: scan 2 families

# TODO: draw lattice on top of plot

with open("quad_scan_2_families.pickle", "rb") as file:
    extent, beta_mean, eta_straight = pickle.load(file)

fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
for ax, (title, value) in zip(
    axs, (("$\\beta_{avg}$", beta_mean), ("$\\eta_{x,straight}$", eta_straight))
):
    image = ax.imshow(
        value.T,
        cmap="rainbow",
        extent=extent,
        origin="lower",
        vmin=0,
        vmax=np.nanmedian(value),
    )
    ax.set(xlim=(-8, 8), ylim=(-8, 8))
    ax.set(xlabel="$k_{{q1}}$", ylabel=f"$k_{{q2}}$")
    colorbar = fig.colorbar(image, ax=ax)
    colorbar.ax.set_title(title)


plt.tight_layout()
plt.savefig(figure_path / "dba-quad_scan_2_families.svg")


#%% plot: scan 3 families
with open("quad_scan_3_families.pickle", "rb") as file:
    results = pickle.load(file)

n_rows = 2
n_cols = len(results)
fig, axs = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(3.8 * n_cols, 3 * n_rows))

for i, (q1_k1, (extent, beta_mean, eta_straight)) in enumerate(results):
    for j, (title, value) in enumerate(
        [("$\\beta_{avg}$", beta_mean), ("$\\eta_{x,straight}$", eta_straight)]
    ):
        ax = axs[j, i]
        image = ax.imshow(
            value.T,
            cmap="rainbow",
            extent=extent,
            origin="lower",
            vmin=0,
            vmax=np.nanmedian(value),
        )
        ax.set_title(f"$k_{{q1}}$ = {q1_k1:.2f} m$^{{-2}}$")
        ax.set(xlabel=r"$k_{q2}$ / m$^{-2}$", ylabel=r"$k_{q3}$ / m$^{-2}$")
        colorbar = fig.colorbar(image, ax=ax)
        colorbar.ax.set_title(title)

plt.tight_layout()
plt.savefig(figure_path / "dba-quad_scan_3_families.svg")

# #%% plot 3d
# fig = plt.figure()
# ax = fig.gca(projection="3d")
# title = "$\\beta_{x,avg}$"
# heatmap = ax.plot_surface(
#     *np.meshgrid(values_i, values_j), beta_mean, rstride=8, cstride=8, alpha=0.75
# )
# ax.contourf(
#     *np.meshgrid(values_i, values_j),
#     beta_mean,
#     zdir="z",
#     offset=-100,
#     cmap=cm.coolwarm,
#     vmax=30,
# )
# ax.contourf(
#     *np.meshgrid(values_i, values_j), beta_mean, zdir="x", offset=-4, cmap=cm.coolwarm
# )
# ax.contourf(
#     *np.meshgrid(values_i, values_j), beta_mean, zdir="y", offset=4, cmap=cm.coolwarm,
# )
# ax.set_xlim(-4, 4)
# ax.set_ylim(-4, 4)
# ax.set_zlim(-100, 150)
# ax.set_xlabel(f"Q1$_{{k1}}$")
# ax.set_ylabel(f"Q2$_{{k1}}$")
# ax.set_zlabel(title)
# ax.set_title(title)
# plt.gcf().colorbar(heatmap, ax=ax)

# plt.tight_layout()
# plt.savefig("plots/dba-3d.pdf")

# # %%
