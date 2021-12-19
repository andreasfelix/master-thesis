from pathlib import Path
from functools import partialmethod

import matplotlib as mpl

# make creation of svg reproducible
mpl.rcParams["svg.hashsalt"] = "physics"
mpl.figure.Figure.savefig = partialmethod(
    mpl.figure.Figure.savefig, metadata={"Date": None}
)

figure_path = Path(__file__).parent.parent.parent / "figures"
lattices_path = Path(__file__).parent.parent / "lattices"
