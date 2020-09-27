import numpy as np

import apace as ap
import apace.plot as aplot


def update_twiss_plot():
    for ax in fig.axes:
        for line, data in zip(ax.lines, (twiss.beta_x, twiss.beta_y, twiss.eta_x * 10)):
            line.set_data(twiss.s, data)
    fig.canvas.draw_idle()


def sliders(pairs, fig=None):
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button

    if fig is None:
        fig, axs = plt.subplots(nrows=len(pairs) + 1)
    else:
        axs = [
            plt.axes([0.2 + 0.2 * i, 0.05, 0.1, 0.075]) for i in range(len(pairs) + 1)
        ]

    global sliders
    sliders = []
    for ax, (element, attribute) in zip(axs, pairs):
        initial_value = getattr(element, attribute)
        slider = Slider(ax, f"{element.name} {attribute}", -5, 5, initial_value)
        slider.on_changed(
            lambda value, element=element, attribute=attribute: (
                setattr(element, attribute, value),
                update_twiss_plot(),
            )
        )
        sliders.append(slider)  # prevent garbage collection
    Button(axs[-1], "Update").on_clicked(update_twiss_plot)


n_cells = 4
angle = np.pi / n_cells

d1 = ap.Drift("d1", 1.3)
d2 = ap.Drift("d2", 0.275)
d3 = ap.Drift("d3", 0.657)
b1 = ap.Dipole("b1", 1, angle=angle, e1=angle / 2, e2=angle / 2)
q1 = ap.Quadrupole("q1", length=0.2, k1=4.42)
q2 = ap.Quadrupole("q2", length=0.2, k1=-3.14)
q3 = ap.Quadrupole("q3", length=0.2, k1=4.35)
left = [d1, q1, d2, q2, d2, b1, d3, q3]
right = left[::-1]
cell = ap.Lattice("cell", left + right)
lattice = ap.Lattice("max-i", n_cells * [cell])
twiss = ap.Twiss(lattice, energy=550)

# modify max-i
elements = [d1, d2, d3]
values_final = [1.0, 0.5, 0.5]
values_initial = [element.length for element in elements]

n_iterations = 3
for i in range(1, n_iterations + 1):
    factor = i / n_iterations
    for ele, vi, vf in zip(elements, values_initial, values_final):
        ele.length = vi * (1 - factor) + vf * factor
        twiss_plot = aplot.TwissPlot(
            twiss,
            sections=(0, cell.length),
            y_min=-5,
            pairs=[(q1, "k1"), (q2, "k1"), (q3, "k1"),],
        )
        aplot.plt.show()
        lattice.as_file("max-i-modified.json")
