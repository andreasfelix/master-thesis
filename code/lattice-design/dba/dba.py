import apace as ap
import numpy as np
from scipy import optimize


def make_dba(
    angle=np.pi / 8,
    drift_length=4.0,
    bend_length=3.0,
    quad_length=1.0,
    k1=0.8,
    three_famlies=True,
):
    d1 = ap.Drift("d1", drift_length / 8)
    b1 = ap.Dipole("b1", bend_length / 2, angle=angle / 2, e1=angle / 4, e2=angle / 4)
    q1 = ap.Quadrupole("q1", length=quad_length / 5, k1=k1)
    q2 = ap.Quadrupole("q2", length=quad_length / 5, k1=-k1)
    q3 = ap.Quadrupole("q3", length=quad_length / 5, k1=k1) if three_famlies else q1
    return ap.Lattice(
        "dba-cell", [d1, q1, d1, q2, d1, b1, d1, q3, d1, b1, d1, q2, d1, q1, d1]
    )


def achromatic_condition(dba, quad_names=["q1", "q2", "q3"]):
    def func(values, quads):
        for value, magnet in zip(values, quads):
            magnet.k1 = value
        try:
            return 50 * np.abs(twiss.eta_x[0]) + np.max([twiss.beta_x, twiss.beta_y])
        except ap.UnstableLatticeError:
            return np.inf

    quads = [dba[name] for name in quad_names]
    twiss = ap.Twiss(dba, steps_per_element=1)
    optimize.minimize(
        func,
        np.array([x.k1 for x in quads]),
        args=quads,
        method="Nelder-Mead",
        bounds=((-8, 8) for _ in quads),
    )
    print(f"{dba.name} with cell length {dba.length}m:")
    print("".join(f"{x.name}: {x.k1}\n" for x in quads))


from pathlib import Path
from subprocess import check_output

base_path = Path(check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
figure_path = base_path / "figures"
