import apace as ap
import apace.plot as aplot

ref = ap.Twiss(ap.Lattice.from_file("bessy2_stduser_2019_05_07.json"))
twiss = ap.Twiss(ap.Lattice.from_file("bessy2_q5t2off.json"))

fig = aplot.TwissPlot(twiss, twiss_ref=ref, sections=[(30, 60)], title="Q5T2off").fig
fig.set_size_inches(14, 8)
fig.tight_layout()
fig.savefig("q5t2off.svg")
