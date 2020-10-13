import math
import pickle

import numpy as np

import apace as ap

from dba import make_dba


def quad_scan(twiss, quad_1, quad_2, steps=100, max_value=3):
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
result = quad_scan(twiss, dba["q1"], dba["q2"])

with open("quad_scan_2_families.pickle", "wb") as file:
    pickle.dump(result, file)


# scan: 3 families
dba = make_dba(three_famlies=True)
twiss = ap.Twiss(dba, steps_per_element=2)
q1, q2, q3 = (dba[name] for name in ("q1", "q2", "q3"))
results = [(q3.k1, quad_scan(twiss, q1, q2)) for q3.k1 in np.linspace(2, 3, 6)]

with open("quad_scan_3_families.pickle", "wb") as file:
    pickle.dump(results, file)
