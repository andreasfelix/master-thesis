import matplotlib.pyplot as plt
import numpy as np

steps = 50
fodo_length = np.empty(50)
beta_mean = np.empty(50)
beta_min = np.empty(50)
beta_max = np.empty(50)
tune = np.empty(50)
curly_h = np.empty(50)
emittance = np.empty(50)
for i, d1.length in enumerate(np.linspace(0, 5, 50)):
    fodo_length[i] = cell.length
    beta_mean[i] = np.mean(twiss.beta_x)
    beta_min[i] = np.min(twiss.beta_x)
    beta_max[i] = np.max(twiss.beta_x)
    tune[i] = twiss.tune_x
    curly_h[i] = twiss.curly_h
    emittance[i] = twiss.emittance_x


plt.figure()
plt.plot(fodo_length, beta_mean, label="$\\beta_{mean}$")
plt.plot(fodo_length, beta_min, label="$\\beta_{min}$")
plt.plot(fodo_length, beta_max, label="$\\beta_{max}$")
plt.plot(fodo_length, tune, label="$Q_\mathrm{x}$")
plt.legend()
plt.xlabel("Length of FODO cell")
plt.tight_layout()
plt.savefig("scaling-beta.pdf")
