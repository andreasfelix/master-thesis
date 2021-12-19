import apace as ap


def make_fodo(angle, drift_length=4.0, bend_length=3.0, quad_length=1.0, k1=0.8):
    q1 = ap.Quadrupole("q1", quad_length / 4, k1)
    q2 = ap.Quadrupole("q2", quad_length / 2, -k1)
    if angle != 0:
        d1 = ap.Drift("d1", drift_length / 4)
        b1 = ap.Dipole("b1", bend_length / 2, angle / 2, e1=angle / 4, e2=angle / 4)
        sequence = [q1, d1, b1, d1, q2, d1, b1, d1, q1]
    else:
        d1 = ap.Drift("d1", (drift_length + bend_length) / 2)
        sequence = [q1, d1, q2, d1, q1]
    return ap.Lattice("fodo-cell", sequence)
