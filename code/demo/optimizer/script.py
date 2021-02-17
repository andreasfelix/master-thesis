import apace as ap
import numpy as np
from scipy import optimize

bessy2 = ap.Lattice.from_file("b2_stduser_2019_05_07.json")
twiss = ap.Twiss(bessy2, steps_per_element=5)
q5t2 = bessy2["Q5T2"]
quads = list(bessy2[name] for name in ["Q3T2", "Q4T2", "Q3D2", "Q4D2", "Q3D3", "Q4D3"])
mask = 40.5, 49.5
steps = 500
linspace = np.linspace(0, bessy2.length, steps)
start, stop = int(mask[0] / bessy2.length * steps), int(mask[1] / bessy2.length * steps)
positions = np.delete(linspace, np.s_[start:stop]).copy()
ref_x = np.interp(positions, twiss.s, twiss.beta_x)
ref_y = np.interp(positions, twiss.s, twiss.beta_y)


def func(values, quads):
    for quad, value in zip(quads, values):
        quad.k1 = value

    if not twiss.stable:
        return np.inf

    beta_x = np.interp(positions, twiss.s, twiss.beta_x)
    beta_y = np.interp(positions, twiss.s, twiss.beta_y)
    beta_x_beat = beta_x / ref_x
    beta_y_beat = beta_y / ref_y
    beta_x_beat[beta_x_beat < 1] = 1
    beta_y_beat[beta_y_beat < 1] = 1
    beta_x_beat **= 2
    beta_y_beat **= 2
    return np.mean([beta_x_beat, beta_y_beat])


for q5t2.k1 in np.linspace(q5t2.k1, 0, 50):
    result = optimize.minimize(
        func,
        np.array([x.k1 for x in quads]),
        args=quads,
        method="Nelder-Mead",
    )
    print(f"k1: {q5t2.k1:+.3f}, objective: {result.fun:+.3f}")

    if not twiss.stable:
        raise Exception("Result is not stable!")

bessy2.as_file("b2_q5t2off.json")
