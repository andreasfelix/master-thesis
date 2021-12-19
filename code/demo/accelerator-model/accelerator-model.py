#%%
import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt
import numpy as np

#%%
design = ap.Lattice.from_file("b2_design_1996.json")
stduser = ap.Lattice.from_file("b2_stduser.json")

# %%
# 1.
# stduser longer than design
# show D1.length vs D6.length
# change length bend -> see how length design lattice changes

# 2.
# change q5t2 -> show how beta_x_max/tune_x changes
# plt.plot(twiss.s, twiss.beta_x)
# plt.xlim(0, 30)
# draw_elements(plt.gca(), design)
