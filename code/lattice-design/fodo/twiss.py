import math
import apace as ap
from apace.plot import draw_lattice, plot_twiss, plt
from fodo import create_fodo, figure_path

config = dict(drift_length=4, bend_length=3, quad_length=1, k1=0.8)
fig, axs = plt.subplots(2)

for angle, ax in zip((0, math.pi / 32), axs):
    fodo = create_fodo(angle=angle, **config)
    plt.sca(ax)
    plot_twiss(twiss := ap.Twiss(fodo))
    plt.xlim(0, fodo.length)
    plt.ylim(-1, 25)
    draw_lattice(fodo)
    plt.xticks(rotation=45)

fig.legend(*axs[0].get_legend_handles_labels(), "upper left", ncol=10, frameon=False)
plt.tight_layout(rect=(0, 0, 1, 0.95))
plt.savefig(figure_path / "fodo-twiss.svg")
