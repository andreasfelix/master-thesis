import math
import pickle

import numpy as np

import apace as ap


def make_dba(three_famlies):
    n_cells = 10  # TODO: does this change the plot?
    angle = math.pi / n_cells
    angle_2 = 0.5 * angle

    d1 = ap.Drift("d1", 0.625)
    b1 = ap.Dipole("b1", 1.5, angle=angle, e1=angle_2, e2=angle_2)
    q1 = ap.Quadrupole("q1", length=0.25, k1=2.7)
    q2 = ap.Quadrupole("q2", length=0.5, k1=-2.0)
    if three_famlies:
        q3 = ap.Quadrupole("q3", length=0.25, k1=2.47)
    else:
        q3 = q1
    cell = ap.Lattice(
        "cell", [d1, q1, d1, q2, d1, b1, d1, q3, q3, d1, b1, d1, q2, d1, q1, d1],
    )
    return ap.Lattice("dba", n_cells * [cell])


def twiss_scan(twiss, quad_1, quad_2, steps=100, max_value=3):
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
result = twiss_scan(twiss, dba["q1"], dba["q2"])

with open("quad_scan_2_families.pickle", "wb") as file:
    pickle.dump(result, file)


# scan: 3 families
dba = make_dba(three_famlies=True)
twiss = ap.Twiss(dba, steps_per_element=2)
q1, q2, q3 = (dba[name] for name in ("q1", "q2", "q3"))
results = [(q3.k1, twiss_scan(twiss, q1, q2)) for q3.k1 in np.linspace(0, 3, 6)]

with open("quad_scan_3_families.pickle", "wb") as file:
    pickle.dump(results, file)
