import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt

bessy2 = ap.Lattice.from_file("b2_stduser_2019_05_07.json")
ref = ap.Twiss(bessy2)
bessy2 = ap.Lattice.from_file("b2_q5t2off.json")
twiss = ap.Twiss(bessy2)

fig, ax = plt.subplots(figsize=(16, 9))
ax.plot(twiss.s, twiss.beta_x, "r")
ax.plot(twiss.s, twiss.beta_y, "b")
ax.plot(twiss.s, ref.beta_x, "r--")
ax.plot(twiss.s, ref.beta_y, "b--")
aplot.draw_elements(ax, bessy2, labels=False)
fig.tight_layout()
fig.savefig("q5t2off.svg")
