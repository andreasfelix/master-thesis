import pickle

import apace as ap
import numpy as np
from dba import make_dba


def quad_scan(twiss, quad_1, quad_2, steps=1000, max_value=8):
    eta_straight = np.empty((steps, steps))
    beta_mean = np.empty((steps, steps))
    extent = 2 * [-max_value, max_value]
    for i, quad_1.k1 in enumerate(np.linspace(*extent[:2], steps)):
        for j, quad_2.k1 in enumerate(np.linspace(*extent[2:], steps)):
            try:
                beta_mean[i, j] = 0.5 * (np.mean(twiss.beta_x) + np.mean(twiss.beta_y))
                eta_straight[i, j] = twiss.eta_x[0]
            except ap.UnstableLatticeError:
                beta_mean[i, j] = np.nan
                eta_straight[i, j] = np.nan
    return extent, beta_mean, eta_straight


# scan: 2 families
dba = make_dba(three_famlies=False)
twiss = ap.Twiss(dba, steps_per_element=2)
results = quad_scan(twiss, dba["q1"], dba["q2"])

with open("quad_scan_2_families.pickle", "wb") as file:
    pickle.dump(results, file)


# scan: 3 families
dba = make_dba(three_famlies=True)
twiss = ap.Twiss(dba, steps_per_element=2)
q1, q2, q3 = (dba[name] for name in ("q1", "q2", "q3"))
results = [(q1.k1, quad_scan(twiss, q2, q3)) for q1.k1 in [3.0, 3.5, 4.0]]

with open("quad_scan_3_families.pickle", "wb") as file:
    pickle.dump(results, file)
