import numpy as np
import apace as ap


def create_fodo(angle, drift_length=4.0, bend_length=3.0, quad_length=1.0, k1=1.2):
    q1 = ap.Quadrupole("q1", length=quad_length / 4, k1=k1)
    q2 = ap.Quadrupole("q2", length=quad_length / 2, k1=-k1)
    if angle != 0:
        d1 = ap.Drift("d1", drift_length / 4)
        b1 = ap.Dipole("b1", bend_length / 2, angle=angle, e1=angle / 2, e2=angle / 2)
        sequence = [q1, d1, b1, d1, q2, d1, b1, d1, q1]
    else:
        d1 = ap.Drift("d1", (drift_length + bend_length) / 2)
        sequence = [q1, d1, q2, d1, q1]
    return ap.Lattice("fodo-cell", sequence)


from subprocess import check_output
from pathlib import Path

base_path = Path(
    (check_output(["git", "rev-parse", "--show-toplevel"])).decode().strip()
)
figure_path = base_path / "figures"
