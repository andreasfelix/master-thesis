import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt

from master_thesis import figure_path, lattices_path

files = map(
    lattices_path.joinpath,
    [
        "bessy2_stduser_2019_05_07.json",
        "bessy2_q5t2off_v3betaymin_2019_05_07_sim.json",
        "bessy2_stduser_2017_03_28.json",
        "bessy2_q5t2off_v4_2017_03_28.json",
        "bessy2_stduser_2017_08_04.json",
        "bessy2_q5t2off_v4_2017_08_04.json",
    ],
)
lattices = map(ap.Lattice.from_file, files)
(
    twiss_ma_std,
    twiss_ma_sim,
    twiss_ba_std,
    twiss_ba_sim,
    twiss_ba_std2,
    twiss_ba_sim2,
) = map(ap.Twiss, lattices)

lattice_ma_std = twiss_ma_std.lattice

beta_beat_ma_x = twiss_ma_sim.beta_x - twiss_ma_std.beta_x
beta_beat_ma_y = twiss_ma_sim.beta_y - twiss_ma_std.beta_y
beta_beat_ba_x = twiss_ba_sim.beta_x - twiss_ba_std.beta_x
beta_beat_ba_y = twiss_ba_sim.beta_y - twiss_ba_std.beta_y
# beta_beat_ba_x2 = twiss_ba_sim2.beta_x - twiss_ba_std2.beta_x
# beta_beat_ba_y2 = twiss_ba_sim2.beta_y - twiss_ba_std2.beta_y


fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(10, 6.5))

ax1.plot(twiss_ma_std.s, beta_beat_ma_x, label=r"$\beta_\mathrm{x}$-beat (Master)")
ax1.plot(twiss_ma_std.s, beta_beat_ba_x, label=r"$\beta_\mathrm{x}$-beat (Bachelor)")
# ax1.plot(twiss_ma_std.s, beta_beat_ba_x2)

ax2.plot(twiss_ba_std.s, beta_beat_ma_y, label=r"$\beta_\mathrm{y}$-beat (Master)")
ax2.plot(twiss_ba_std.s, beta_beat_ba_y, label=r"$\beta_\mathrm{y}$-beat (Bachelor)")
# ax2.plot(twiss_ba_std.s, beta_beat_ba_y2)

for ax in ax1, ax2:
    ax.set_xlim(0, lattice_ma_std.length)
    ax.set(ylabel=r"$(\beta_u^\mathrm{q5t2off} - \beta_u^\mathrm{stduser})$ / m")
    ax.legend(loc="lower right")
    aplot.draw_sub_lattices(ax, lattice_ma_std)
    aplot.draw_elements(ax, lattice_ma_std, labels=False)
    # hide last tick to right, so it does not overlap
    last_tick = ax.xaxis.get_majorticklabels()[-1]
    last_tick.set_visible(False)

ax2.set(xlabel="orbit position $s$ / m")

fig.tight_layout()
fig.savefig(figure_path / "q5t2off_ba_vs_ma.svg")
