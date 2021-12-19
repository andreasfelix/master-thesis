from functools import partial

import apace as ap
import apace.plot as aplot

from master_thesis import figure_path, lattices_path

files = map(
    lattices_path.joinpath,
    [
        "bessy2_stduser_2019_05_07.json",
        "bessy2_q5t2off_v3betaymin_2019_05_07_sim.json",
        "bessy2_q5t2off_v3betaymin_2019_05_07_loco.json",
        "bessy2_stduser_2017_03_28.json",
        "bessy2_q5t2off_v4_2017_03_28.json",
        "bessy2_q5t2off_v1_2017_03_28.json",
        "bessy2_t2_high_x.json",
        "bessy2_t2_high_x_y.json",
    ],
)
lattices = map(ap.Lattice.from_file, files)
(
    twiss_std,
    twiss_sim,
    twiss_loco,
    twiss_ba_std,
    twiss_ba_sim,
    twiss_ba_sim_v1,
    twiss_t2_high_beta_x,
    twiss_t2_high_beta_x_y,
) = map(partial(ap.Twiss, energy=1700, steps_per_meter=100), lattices)

# print("std", twiss_std.emittance_x)
# print("high x", twiss_t2_high_beta_x.emittance_x)
# print("high x y", twiss_t2_high_beta_x_y.emittance_x)
# exit(0)

for name, title, twiss, twiss_ref in [
    [
        "twiss_q5t2off_sim_vs_std",
        "Q5T2off SIM vs Standard User",
        twiss_sim,
        twiss_std,
    ],
    [
        "twiss_q5t2off_loco_vs_std",
        "Q5T2off LOCO vs Standard User",
        twiss_loco,
        twiss_std,
    ],
    [
        "twiss_q5t2off_loco_vs_q5t2off_sim",
        "Q5T2off LOCO vs SIM",
        twiss_loco,
        twiss_sim,
    ],
    [
        "twiss_ba_q5t2off_sim_vs_std",
        "Q5T2off SIM vs Standard User (Bachelor's thesis)",
        twiss_ba_sim,
        twiss_ba_std,
    ],
    [
        "twiss_ba_q5t2off_v1_sim_vs_std",
        "Q5T2off V1 SIM vs Standard User (Bachelor's thesis)",
        twiss_ba_sim_v1,
        twiss_ba_std,
    ],
    [
        "twiss_t2_high_beta_x",
        "High horizontal beta in T2",
        twiss_t2_high_beta_x,
        twiss_std,
    ],
    [
        "twiss_t2_high_beta_x_y",
        "High horizontal and high vertical beta in T2",
        twiss_t2_high_beta_x_y,
        twiss_std,
    ],
]:
    fig = aplot.TwissPlot(
        twiss,
        twiss_ref=twiss_ref,
        sections=[(30, 60)],
        title=title,
    ).fig
    fig.set_size_inches(10, 6.5)
    # hide last tick to right, so it does not overlap
    last_tick = fig.axes[0].xaxis.get_majorticklabels()[-1]
    last_tick.set_visible(False)
    fig.tight_layout()
    fig.savefig(figure_path / f"{name}.svg", metadata={"Date": None})
