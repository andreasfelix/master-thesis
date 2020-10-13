import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

import apace as ap
import apace.plot as aplot


def make_mba(
    n_bends,
    angle=np.pi / 8,
    drift_length=4.0,
    bend_length=3.0,
    quad_length=1.0,
    k1=1.0,
):
    d1 = ap.Drift("d1", drift_length / (8 + 2 * (n_bends - 2)))
    q1 = ap.Quadrupole("q1", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    q2 = ap.Quadrupole("q2", length=quad_length / 2 / 2, k1=-k1)
    q3 = ap.Quadrupole("q3", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    b1 = ap.Dipole("b1", bend_length / n_bends, angle=angle, e1=angle / 2, e2=angle / 2)
    left = [d1, q1, d1, q2, d1]
    right = reversed(left)
    sequence = [*left, b1, *([d1, q3, d1, b1] * (n_bends - 1)), *right]
    return ap.Lattice(f"{n_bends}ba-cell", sequence)


def achromatic_condition(mba, quad_names=["q1", "q2", "q3"]):
    def func(values, quads):
        for value, magnet in zip(values, quads):
            magnet.k1 = value
        try:
            return 50 * np.abs(twiss.eta_x[0]) + np.mean(twiss.beta_x + twiss.beta_y)
        except ap.UnstableLatticeError:
            return np.inf

    quads = [mba[name] for name in quad_names]
    twiss = ap.Twiss(mba, steps_per_element=1)
    results = optimize.minimize(
        func,
        np.array([x.k1 for x in quads]),
        args=quads,
        method="Nelder-Mead",
        bounds=((-4, 4) for _ in quads),
    )
    print(f"{mba.name} with cell length {mba.length}m:")
    print("".join(f"{x.name}: {x.k1}\n" for x in quads))


from pathlib import Path
from subprocess import check_output

base_path = Path(
    (check_output(["git", "rev-parse", "--show-toplevel"])).decode().strip()
)
figure_path = base_path / "figures"

