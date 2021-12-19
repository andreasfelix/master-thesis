import apace as ap
import numpy as np
from scipy import optimize

bessy2 = ap.Lattice.from_file("bessy2_stduser.json")
twiss = ap.Twiss(bessy2, steps_per_meter=4)
t2_center = np.searchsorted(twiss.s, 45)
beta_ref_x = twiss.beta_x.copy()
beta_ref_y = twiss.beta_y.copy()

t1 = ["Q3P1T1", "Q3P2T1", "Q4P1T1", "Q4P2T1", "Q5P1T1", "Q5P2T1"]
d2 = ["Q3D2", "Q4D2"]
t2 = ["Q3T2", "Q4T2"]
d3 = ["Q3D3", "Q4D3"]
t3 = ["Q3T3", "Q4T3", "Q5T3"]
q5t2 = bessy2["Q5T2"]
quads_turnoff = [bessy2[name] for name in t2]
quads_optimize = [bessy2[name] for name in t1 + d2 + t2 + d3 + t3]


def objective_function(values, quads):
    for quad, value in zip(quads, values):
        quad.k1 = value

    if not twiss.stable:
        return np.inf

    beta_beat_x = np.maximum(1, twiss.beta_x / beta_ref_x) ** 2
    beta_beat_y = np.maximum(1, twiss.beta_y / beta_ref_y) ** 2
    beat_mean = np.trapz(beta_beat_x + beta_beat_y, x=twiss.s) / bessy2.length
    return beat_mean + max(twiss.beta_y[t2_center], 1.6)


def run(quads):
    result = optimize.minimize(
        objective_function,
        np.array([x.k1 for x in quads]),
        args=quads,
        method="Nelder-Mead",
    )
    print(f"k1: {q5t2.k1:+.3f}, objective: {result.fun:+.3f}")
    if not twiss.stable:
        raise Exception("Result must be stable!")


for q5t2.k1 in np.linspace(q5t2.k1, 0, 10):
    run(quads_turnoff)

for _ in range(5):
    run(quads_optimize)

bessy2.as_file("bessy2_q5t2off.json")
