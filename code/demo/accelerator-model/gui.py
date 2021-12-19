from pathlib import Path

import apace as ap
import apace.plot as aplot
import matplotlib.pyplot as plt
import streamlit as st

lattice_files = list(Path().parent.rglob("*.json"))
lattice_file = st.sidebar.selectbox("Lattice File", sorted(lattice_files))
lattice = ap.Lattice.from_file(lattice_file)

energy = st.sidebar.number_input("Energy / MeV", 0, 3000, 1700, 100)
sub_lattice_names = [x.name for x in lattice.sub_lattices]
sections = st.sidebar.multiselect("Sections", sorted(sub_lattice_names))
x = ["beta_x", "beta_y", "eta_x", "eta_x_dds", "psi_x", "psi_y", "alpha_x", "alpha_y"]
twiss_functions = st.sidebar.multiselect("Twiss Functions", x, x[:3])

quads = list(filter(lambda x: isinstance(x, ap.Quadrupole), lattice.elements))
for quad in sorted(quads, key=lambda quad: quad.name):
    quad.k1 = st.sidebar.slider(quad.name, quad.k1 - 0.5, quad.k1 + 0.5, quad.k1)

twiss = ap.Twiss(lattice, energy=energy)
if not twiss.stable:
    st.warning("this configuration is not stable!")
    st.stop()

st.title(f"Twiss Functions")
fig = aplot.TwissPlot(twiss, sections=sections, twiss_functions=twiss_functions).fig
fig.set_size_inches(8, 5)
st.pyplot(fig)

st.title(f"Floor Plan")
fig, ax = plt.subplots()
aplot.floor_plan(ax, lattice.children[1])
ax.axis("off")
st.pyplot(fig)
