<h1 align="center">A new Python-based Lattice Development Tool and its
Applications at BESSY II</h1>

- **Author:** Felix Andreas
- **Supervisors:** Prof. Dr. Andreas Jankowiak and Dr. Paul Goslawski
- **Institution:** [Department of Physics, Faculty of Mathematics and
Natural Sciences, Humboldt-Universität zu
Berlin](https://www.physik.hu-berlin.de)
- **Date:** December 20, 2021

<div align="center">

| [![Screen](https://api.iconify.design/carbon:screen.svg) Web](https://felix-andreas.github.io/master-thesis/) | [![PDF](https://api.iconify.design/carbon:document-pdf.svg) PDF](https://felix-andreas.github.io/master-thesis/thesis.pdf) |
| - | - |

</div>

## Abstract

Due to the BESSY-VSR upgrade and the design of the next synchrotron
radiation facility BESSY III, there are several lattice development
tasks at the Helmholtz-Zentrum Berlin (HZB). Within the last several
years, there was a significant shift in the physics community from
standalone plotting programs, optimization routines, and numerical
libraries towards the Python programming language, which absorbed these
tools into different packages. At HZB, Python is the predominant
programming language used to set up the execution of simulations and to
post-process their results. The issue with existing and mature particle
accelerator simulation codes is that it is not trivial to integrate them
into a typical Python workflow. Many physicists have written several
wrapper scripts around the existing simulation codes to leverage the
power of Python's rich ecosystem of scientific tools. The issue with
these wrappers is that there are often not reusable because they are
very specific to a particular task and often rely on string manipulation
of the lattice files or run files, which can be very error-prone and is
computationally inefficient. Furthermore, these wrapper scripts only
give access to the simulation results and not to the underlying internal
models of the simulation codes, like the magnetic lattice or information
about individual magnets. Therefore it was decided to develop a new
Python package that generates an accelerator model from a given lattice
file. This model can be queried for information on individual magnets
and on properties of composed structures like the length of a cell. It
is designed in such an extensible way that it can be used as a
foundation for different simulation methods, which can be built on top
of it. Such a method, which is capable of computing the Twiss
parameters, dispersion function, chromaticity, emittance, and
synchrotron radiation integrals, was implemented. This thesis covers how
this new tool was developed and then used to optimize the O5T2off optics
for the BESSY-VSR project, adapt the beta functions of the BESSY II
storage ring for an emittance exchange experiment, and create a
framework of automated lattice summaries, which could be useful for the
development of a future BESSY III lattice. The developed code does not
aim to replace the more mature and full-featured existing particle
accelerator codes. However, it extends the ecosystem of accelerator
tools by enabling fundamental lattice development using the Python
language.

## Build Instructions

1. Start development shell

    ```console
    nix develop
    ```

1. Render web version

    ```console
    make html
    ```

1. Render printable HTML

    ```console
    make print
    ```
1. Serve `dist` folder and save `print.html` from Google Chrome as `dist/thesis.pdf`

    ```console
    live-server dist
    ```

1. Add bookmarks and metadata to PDF

    ```console
    python layout/bookmarks.py
    ```

1. (Optional) Render README.md from template `layout/templates/README.md`

    ```console
    make README.md
    ```

1. Deploy `dist` folder to GitHub Pages

    ```console
    make deploy
    ```
