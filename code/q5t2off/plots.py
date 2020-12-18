from pathlib import Path
import apace as ap

lattices_path = Path(__file__).parent / "lattices"

std = lattices_path / "bessy2_stduser_2019_05_07.json"
sim = lattices_path / "bessy2_q5t2off_v3betaymin_2019_05_07_sim.json"
loco = lattices_path / "bessy2_q5t2off_v3betaymin_2019_05_07_loco.json"

lattice_std = ap.Lattice.from_file(std)
lattice_sim = ap.Lattice.from_file(sim)
lattice_loco = ap.Lattice.from_file(loco)
twiss_std = ap.Twiss(lattice_std, energy=1700)
twiss_sim = ap.Twiss(lattice_sim, energy=1700)
twiss_loco = ap.Twiss(lattice_loco, energy=1700)

import matplotlib.pyplot as plt
import apace.plot as aplot

fig_std_sim, ax_q5t2off_std = plt.subplots()
aplot.plot_twiss(ax_q5t2off_std, twiss_loco)
aplot.plot_twiss(ax_q5t2off_std, twiss_std, line_style="dashed")
aplot.draw_elements(ax_q5t2off_std, lattice_std, labels=False)
fig_std_sim.savefig("twiss_std_vs_q5t2off_loco.svg")

fig_std_sim, ax_sim_loco = plt.subplots()
aplot.plot_twiss(ax_sim_loco, twiss_sim)
aplot.plot_twiss(ax_sim_loco, twiss_loco, line_style="dashed")
aplot.draw_elements(ax_sim_loco, lattice_std, labels=False)
fig_std_sim.savefig("twiss_q5t2off_sim_vs_loco.svg")
