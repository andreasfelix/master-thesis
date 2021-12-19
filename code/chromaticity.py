import apace as ap
import numpy as np


def matrix_vs_integration(lattice):
    ## matrix tracking
    track = ap.TrackingMatrix(lattice, dist)
    s_t, x_t = track.s, track.x

    ## tracking by integration
    from apace.tracking_integration import Tracking

    track = Tracking(lattice)
    s, trajectory = track.track(dist)
    x, delta = trajectory[:, 0], trajectory[:, 5]

    import apace.plot as aplot
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 5))
    cmap = plt.get_cmap("rainbow_r")
    delta_min = min(delta[0])
    delta_max = max(delta[0])
    delta_range = delta_max - delta_min

    plt.axhline(0, color="black", linestyle="--", linewidth=1)
    for i in range(x.shape[1]):
        plt.plot(s, x[:, i], color=cmap(0.5 + delta[0, i] / delta_range))

    for i in range(x.shape[1]):
        plt.plot(
            s_t, x_t[:, i], "--", alpha=0.3, color=cmap(0.5 + delta[0, i] / delta_range)
        )

    ax.set(
        xlabel="orbit position $s$ / m",
        ylabel="$x$ / m",
        xlim=(0, lattice.length),
        ylim=(-0.003, 0.003),
    )
    mappable = plt.cm.ScalarMappable(
        norm=plt.Normalize(vmin=delta_min, vmax=delta_max), cmap=cmap
    )
    fig.colorbar(mappable, ax=ax).ax.set_title(r"$\delta$")
    aplot.draw_elements(ax, lattice, labels=True, location="bottom")
    fig.tight_layout()
    return fig


from master_thesis import figure_path

d1 = ap.Drift("d1", length=1)
d2 = ap.Drift("d2", length=0.5)
q1 = ap.Quadrupole("Quadrupole", length=0.5, k1=2)
lattice = ap.Lattice("line", [d1, q1, d1, d2])


dist = np.zeros((6, 6))
d = 0.3
dist[0] = np.array([0.002, 0.0015, 0.001, -0.001, -0.0015, -0.002])
dist[5] = np.array([d, d, 0, 0, -d, -d])

fig = matrix_vs_integration(lattice)
fig.savefig(figure_path / "chromaticity-quadrupole.svg")

d3 = ap.Drift("d3", length=0.125)
s1 = ap.Sextupole("Sextupole", length=0.25, k2=530)
lattice = ap.Lattice("line", [d2, d3, s1, d3, q1, d1, d2])

dist = np.zeros((6, 6))
d = 0.3
dist[0] = np.linspace(0.002, -0.002, 6)
dist[5] = np.linspace(d, -d, 6)

fig = matrix_vs_integration(lattice)
fig.savefig(figure_path / "chromaticity-sextupole.svg")
