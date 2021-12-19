import apace as ap
import matplotlib.pyplot as plt
import numpy as np
from fodo import make_fodo

from master_thesis import figure_path

fodo = make_fodo(np.pi / 32)
twiss = ap.Twiss(fodo)

steps = 50
fodo_length = np.empty(50)
beta_mean = np.empty(50)
beta_min = np.empty(50)
beta_max = np.empty(50)
tune = np.empty(50)
curly_h = np.empty(50)
emittance = np.empty(50)
drift = fodo["d1"]
q1 = fodo["q1"]
q2 = fodo["q2"]
q1.k1 = q2.k1 = 0.5
b1 = fodo["b1"]
b1.k0 = 0
b1.e1 = 0
b1.e2 = 0
cell = fodo["cell"]
for i, drift.length in enumerate(np.linspace(0.0, 5.0, 50)):
    fodo_length[i] = cell.length
    beta_mean[i] = np.mean(twiss.beta_x) + np.mean(twiss.beta_y)
    beta_min[i] = np.min(twiss.beta_x) + np.min(twiss.beta_y)
    beta_max[i] = np.max(twiss.beta_x) + np.max(twiss.beta_y)
    tune[i] = twiss.tune_x
    # curly_h[i] = np.mean(twiss.curly_h)
    # emittance[i] = twiss.emittance_x

phase = 360 * tune

plt.figure()
plt.plot(phase, beta_mean, label="$\\beta_{mean}$")
plt.plot(phase, beta_min, label="$\\beta_{min}$")
plt.plot(phase, beta_max, label="$\\beta_{max}$")
idx = np.argmin(beta_max)
plt.plot(phase[idx], beta_max[idx], "rx")
# plt.plot(phase, curly_h, label="$\\mathscr{H}_{mean}$")
# plt.plot(phase, emittance, label="$\\epsilon_{x}$")
plt.legend()
plt.xlabel("Phase advance $\\phi$ / °")
plt.tight_layout()
plt.savefig(figure_path / "phase_advance.pdf")
