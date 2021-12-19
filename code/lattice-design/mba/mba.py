import apace as ap
import numpy as np
from scipy import optimize


def make_mba(
    n_bends,
    angle=np.pi / 8,
    drift_length=4.0,
    bend_length=3.0,
    quad_length=1.0,
    k1=1.0,
):
    d1 = ap.Drift("d1", drift_length / (14 + 2 * (n_bends - 2)))
    q1 = ap.Quadrupole("q1", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    q2 = ap.Quadrupole("q2", length=quad_length / 2 / 2, k1=-k1)
    q3 = ap.Quadrupole("q3", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    b1 = ap.Dipole("b1", bend_length / n_bends, angle=angle, e1=angle / 2, e2=angle / 2)
    left = [d1, d1, d1, d1, q1, d1, q2, d1]
    right = reversed(left)
    sequence = [*left, b1, *([d1, q3, d1, b1] * (n_bends - 1)), *right]
    return ap.Lattice(f"{n_bends}ba-cell", sequence)


def make_mba2(
    n_bends,
    angle=np.pi / 8,
    drift_length=4.0,
    bend_length=3.0,
    quad_length=1.0,
    k1=1.0,
):
    d1 = ap.Drift("d1", drift_length / (14 + 4 * (n_bends - 2)))
    q1 = ap.Quadrupole("q1", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    q2 = ap.Quadrupole("q2", length=quad_length / 2 / 2, k1=-k1)
    q3 = ap.Quadrupole("q3", length=quad_length / 2 / (2 + n_bends - 1), k1=k1)
    q4 = ap.Quadrupole("q4", length=quad_length / 2 / (2 + n_bends - 1), k1=-k1)
    b1 = ap.Dipole("b1", bend_length / n_bends, angle=angle, e1=angle / 2, e2=angle / 2)
    left = [d1, d1, d1, d1, q1, d1, q2, d1]
    right = reversed(left)
    sequence = [*left, b1, *([d1, q4, d1, q3, d1, q4, d1, b1] * (n_bends - 1)), *right]
    return ap.Lattice(f"{n_bends}ba-cell", sequence)


def achromatic_condition(mba, quads, energy):
    def func(values, quads):
        for value, magnet in zip(values, quads):
            magnet.k1 = value
        try:
            center = len(twiss.eta_x) // 2
            # return (
            #     np.abs(twiss.eta_x[0])
            #     - 10 * np.sign(twiss.eta_x[center])
            #     + 2 ** (np.max([twiss.beta_x, twiss.beta_y]) / 1000)
            # )
            return (
                np.abs(twiss.eta_x[0])
                + twiss.emittance_x * 1e7
                + 2 ** (np.max([twiss.beta_x, twiss.beta_y]) / 1000)
            )
        except ap.UnstableLatticeError:
            return np.inf

    twiss = ap.Twiss(mba, steps_per_meter=5, energy=energy)
    result = optimize.basinhopping(
        func,
        np.array([x.k1 for x in quads]),
        minimizer_kwargs=dict(method="Nelder-Mead", args=quads),
        seed=0,
        niter=500,
    )
    for quad, k1 in zip(quads, result["lowest_optimization_result"]["x"]):
        quad.k1 = k1

    print(f"{mba.name} with cell length {mba.length}m:")
    print("".join(f"{x.name}: {x.k1}\n" for x in quads))


from pathlib import Path
from subprocess import check_output

base_path = Path(check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
figure_path = base_path / "figures"
