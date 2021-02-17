#%%
import apace as ap
import apace.plot as aplot
import numpy as np
import matplotlib.pyplot as plt

#%%
stduser = ap.Lattice.from_file("b2_stduser_2019_05_07.json")
design = ap.Lattice.from_file("b2_design_lattice_1996.json")

# %%
# change q5t2 -> show how beta_x max changes
# change length bend -> see how length design lattice changes
# change element see how -> twiss.class needs update