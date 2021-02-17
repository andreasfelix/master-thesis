import numpy as np
from tqdm import tqdm

# 1. Create a template run file & template lattice file
lattice_file = """
d1: drif, l=0.55
q1: kquad, l=0.2, k1={q1_k1}
q2: kquad, l=0.4, k1={q2_k1}
b1: csbend, l=1.5, angle=0.392701, e1=0.1963505, e2=0.1963505
cell: line=(q1, d1, b1, d1, q2, d1, b1, d1, q1)
ring: line=(cell, cell, cell, cell, cell, cell, cell, cell)
""".format

# Define parameters for necktie plot
samples = 30
extent = 0, 2
interval = np.linspace(*extent, samples)
results = np.empty((samples, samples))

for i, q1_k1 in enumerate(tqdm(interval)):
    for j, q2_k1 in enumerate(-interval):

        # 2. Manipulate template by inserting input parameters
        with open("lattice.lte", "w") as file:
            file.write(lattice_file(q1_k1=q1_k1, q2_k1=q2_k1))

        # 3. Run simulation
        import subprocess

        subprocess.run(["elegant", "twiss.ele"], stdout=subprocess.DEVNULL)

        # 4. Load back the output files into
        from eleganttools import SDDS

        data = SDDS("twiss.twi").as_dict()
        results[i, j] = (data["betaxAve"] + data["betayAve"]) / 2

# 5. Post-process the results
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
heatmap = ax.imshow(
    results, extent=[*extent, *extent], origin="lower", vmin=0, vmax=30, cmap="cool"
)
ax.set_xlabel("q1$_{{k1}}$ / m$^2$")
ax.set_ylabel("q2$_{{k1}}$ / m$^2$")
ax.set_title("necktie plot")
colorbar = fig.colorbar(heatmap, ax=ax)
colorbar.ax.set_title("$\\beta_{\\mathrm{mean}}$", fontsize=12, pad=10)
fig.tight_layout()
fig.savefig("necktie-plot-elegant.svg")
