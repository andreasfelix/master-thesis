# Introduction

This thesis presents the development of the new lattice design tool *apace*, the new JSON-based lattice file format *LatticeJSON*, and some of their applications.

This first chapter provides a brief overview of the third-generation light source BESSY II and some of its current lattices design tasks. Then, it discusses the challenges of integrating the existing simulation codes in a modern and high-level programming language like Python, which sets the motivation for the development of a new optics code as part of this thesis.

The second chapter covers the physical concepts of beam dynamics in electron storage rings needed to implement the new lattice design tool.

The third chapter addresses various challenges and considerations made during the implementation. Furthermore, it gives a short overview of the capabilities of the developed Python package.

The fourth chapter presents the applications of the developed optics simulation program for two optics changes at the BESSY II storage ring.

The last chapter concludes the thesis with a summary of the results and gives an outlook into its potential use cases in the future.

The appendix includes the documentation, the API reference, and the source code of the developed Python package.

## BESSY II - A Third Generation Light Source

The third-generation synchrotron light source BESSY II is located in Berlin Adlershof and is operated by the research institute Helmholtz-Zentrum Berlin (HZB) since 1998. Its purpose is to provide extremely brilliant synchrotron light pulses in the range of terahertz radiation to hard X-rays. The storage ring has a circumference of 240 m and is equipped with 50 beamlines. A graphic overview of BESSY II is shown in [@fig:bessy2-floorplan]. In addition, the most important parameters of the storage ring are listed in [@tbl:bessy2-parameters].

![Floor plan of the synchrotron light source BESSY II (extracted from @ruprecht-phd)](figures/bessy2-floorplan.svg){#fig:bessy2-floorplan}

| Parameter                 | Value     |
| ------------------------- | --------- |
| nominal energy            | 1.7 GeV   |
| horizontal emittance      | ≈ 7 nm rad |
| circumference             | 240 m     |
| RF-frequency              | 500 MHz   |
| revolution time           | 800 ns    |
| beam current              | 300 mA    |
| number of cells           | 16        |
| number of bending magnets | 32        |
| bending radius            | 4.354 m   |
| beam-lines                | ≈ 42       |
: Parameters of the BESSY II storage ring {#tbl:bessy2-parameters}

The electrons are emitted by a DC grid cathode and are accelerated up to 90 keV. In the following linear accelerator (LINAC), their energy is increased up to 50 MeV [@linac]. Next, the electrons are transferred to the booster synchrotron, where they are accelerated up to 1.7 GeV and injected into the storage ring cumulatively so that a beam current of 300 mA is maintained (*top-up*). The electrons can be stored for up to 10 hours and emit, depending on the type of deflection (bending magnet, wiggler, or undulator), photon energies from 10 eV up to 15 keV.

At BESSY II, it is possible to operate the machine in two different modes. Most of the time, the storage ring is set to the standard user optics with 15 ps bunch length. During two weeks of the year, the lattice is changed to the low $\alpha$ optics, which provide buckets with 3 ps bunch length [@abobakr2003]. This can be realized by reducing the momentum compaction factor $\alpha_{\mathrm{c}}$ from  $7 \cdot 10^{-4}$ to $4 \cdot 10^{-5}$. The coherent synchrotron radiation instability leads to a limiting bursting threshold current, which scales with ~$\alpha_{\mathrm{c}}$. Therefore the photon flux has to be reduced significantly in comparison to the standard optics. At this time, high flux users cannot run experiments, which is why the low alpha mode can only be provided for short periods.

## Lattice Development at HZB - Examples

This section introduces some of the lattice development tasks at HZB, which have been addressed using the developed code.

### Enlarging the Available Installation Length for the VSR Cryomodule {#sec:introduction-q5t2off-bessy-vsr-optics}

Due to increasing interest in studies that require very short photon pulses, HZB is developing a new operational mode called Variable pulse-length Storage Ring (VSR) [@vsrstudy], which aims to fulfill the requirements of the users who need short 2 ps bunches and of the users relying on the high average beam current, which is mainly stored in the 15 ps long bunches. The idea is to store long and short bunches in one storage ring simultaneously by establishing a beating pattern of higher harmonic cavities providing alternating longitudinal focusing gradients for two different bunch lengths.

![Voltage of the VSR cavities and their sum. The alternating large (blue) and small (red) gradients lead to short and longer bunches, respectively. (based on [@vsrstudy] and [@ruprecht-phd])](figures/vsr-cavity-voltage.svg){#fig:vsr-cavity-voltage}

This will be achieved by the installation of an additional cavity module consisting of two 1.5 GHz and two 1.75 GHz cavities. The superposition of these two new frequencies and the existing 0.5 GHz cavity leads to alternating high (blue) and low gradients (blue) shown in @fig:vsr-cavity-voltage. The long bunches are located at the small voltage gradients, where the voltages of the 1.5 GHz and 1.75 GHz cavities cancel out. The short bunches, with higher current than in the low alpha mode, are produced at the high voltage gradient, where the voltages of the cavities add up.

![The currently available space within the T2 section of the storage ring. Removing the Q5 quadrupoles would lead to about 0.7 m of additional installation lenght for a larger cryomodule. (yellow - Dipole, red - Quadrupole, green - Sextupole)](figures/vsr-installation-length.svg){#fig:vsr-installation-length}

The additional cavity module will be installed in the T2 section of the BESSY II storage ring, shown in @fig:vsr-installation-length. One challenge - addressed by my bachelor's thesis @andreas_ba - is that the module needs more space than initially assumed. One solution is to remove the two Q5T2 quadrupoles to gain about 0.7 meters of installation length. The goal is to switch off the Q5T2 quadrupoles in simulations while maintaining the most important transverse linear parameters as the beta functions, tune, and momentum compaction factor. The best optics presented showed that a turn-off of the Q5T2 quadrupoles in the T2 straight is possible. Furthermore, the optics was tested at the storage ring, where it was possible to store high current with reasonable lifetime and injection efficiency.

As already stated in the conclusion of the bachelor's thesis, the presented optics have to be further optimized regarding different aspects: There is still a non-negligible beta beat outside of the T2 section. The linear optics could be further improved by overcoming some limitations of the code of the bachelor's thesis. Depending on the number of parameters, some optimization runs took several days. Optimizing time-critical parts of the developed code would allow optimizing using a higher number of quadrupole configurations. Also, the capability to mask certain regions, which would not be taking into account by the objective function, or set the beta functions to the desired value in the cavity module could further improve the obtained optics. That would require a significant rewrite of the developed code. Adjusting the objective function of the optimization method, discussed in @sec:q5t2off-bessy-vsr-optics, could improve the linear result. Besides the optimization of the linear beam dynamics, the optics has to be further optimized with regard to the non-linear dynamics. Different sextupole settings can be used to optimize the phase and momentum acceptance.

### Emittance Exchange Experiment

With the uprise of 4ᵗʰ generation light sources, the discussion of round beams becomes more relevant. A round beam is produced when the emittance is the same in both transversal planes. Such an emittance exchange is helpful in two use cases:

First, discussed in @kuskekramer2016, an exchange of the transverse beam emittances can improve the injection efficiency. Since the beam is injected in the horizontal plane and the beam emittance is much larger in the horizontal plane for an electron synchrotron, the horizontal emittance primarily defines the required acceptance for a high injection efficiency. Therefore, reducing the horizontal emittance in the booster synchrotron, shown in @fig:aperture-emittance-requirement, by partially transferring it into the vertical plane can significantly lower the required acceptance of the storage ring and thus increase the injection efficiency.

![Influence of the horizontal emittance of the injected beam on the required aperture for high injection efficiency (based on [@kuskekramer2016])](figures/aperture-emittance-requirement.svg){#fig:aperture-emittance-requirement}

Another reason for an emittance exchange is the generation of round beams in the storage ring. The goal is to match the electron beam phase space with the phase space of the emitted photon beam at the radiation source to optimize the photon beam's brilliance and coherent fraction.

There are different techniques to generate round beams. For example, operating on a coupling resonance or driving a skew excitation resonantly with the beam. One experiment to study the influence of the resonant skew excitation on the emittance exchange depending on the size of the beta function required an optics change in one of the triplet sections of the storage ring. @sec:emittance-exchange-experiment presents how the developed code was used to raise the horizontal beta function from 1.2 m to 15 m at the center of the straight.

### Automated Lattice Summaries {#sec:automated-lattice-summaries}

At HZB, the development of the Conceptual Design Report (CDR) of the BESSY II successor BESSY III has started. Many lattice candidates arise during the development of an entirely new accelerator lattice, which themselves require serval iterations. These numerous versions of lattices are created by different physicists making different considerations and optimizing for different parameters. Due to the variety of accelerator physics codes, the lattice files and simulation results are stored in different formats. Even though many accelerator codes provide the option to export the lattice files to different formats, this often does not work flawlessly and requires editing these files manually afterward. That makes sharing and comparing the different lattices candidates during the design phase very cumbersome and unnecessarily time-consuming. 

The number of different simulation codes and lattice file formats is probably due to the variety of different lattice development tasks. Certain tasks can be very specific to a given facility and require a feature, which may not be implemented in one of the existing codes. Due to some codes not being open-source or since it can be easier to implement a certain feature from scratch than integrating it into one of the existing codes, this probably led to the historical fragmentation of accelerator physics codes and lattice file formats.

On the other hand, the boundary conditions for a new BESSY III lattice are well defined. Therefore, especially for fundamental lattices development, mainly linear beam dynamics, it should be possible to automate the process of sharing lattice files and simulation results.

Ideally, there would be a shared database of lattices. The lattices files would be automatically generated in multiple formats every time a lattice is added to the database. In the same way, a predefined set of simulations would be run. The simulation results could then be summarized in the form of a lattice report, for example, through a web page. Such a framework of automatically generated lattice summaries would also be useful for existing lattices. For example, to benchmark a BESSY III candidate lattice with one of the existing 4ᵗʰ generation light sources or build an updated version of the Synchrotron Light Source Data Book [@murphy_1996].

As a starting point and to facilitate the creation of such a database, it might be helpful to use a slimmed-down version of lattice file formats. Such a restricted version would only contain basic element types such as drifts and multipoles. As these elements are available in all accelerator codes, this would make a one-to-one translation between the lattice file formats possible. Furthermore, with the lattice files available in the different formats, automated routines could be set up for the different simulations codes.

A prove-of-concept framework of automated lattice summaries was developed using the new lattice design tool and JSON-based lattice file format and will be presented in @sec:lattice-summaries.

### Smaller Lattice Development Tasks at the BESSY II Storage Ring

Sometimes there are smaller lattice development tasks, where, for example, a user needs to know the value of the beta function at a specific position in the storage ring. Often this task requires some post-processing, which at HZB is mainly done in Python. Thus, having a native Python interface to the accelerator model and the Twiss parameters would be very beneficial for these tasks.

## Motivation: The Need for a Python Interface to Particle Accelerator Simulations

MAD-X [@madx] and elegant [@elegant] are some of the most mature and commonly used accelerator physics simulation codes, among many others, listed here [@accelerator-physics-codes]. Both programs a driven by an input file - often called run-file. This file defines various simulation parameters but can also be used to define an optimization procedure. After the execution, the results are stored in an output file. Over the years, various toolkits and programs emerged to inspect, post-process, and plot these results. Elegant even comes with its own post-processing toolkit SDDS [@sdds-toolkit]. Sometimes, for complex runs, more flexibility is needed, which is why Python is commonly used for post-processing and analysis of the simulation data.

Python has a rich ecosystem of numerical libraries and optimization tools, which is growing day by day. It has become the go-to language for scientific computing and machine learning. A typical workflow of using MAD-X or elegant with Python would be (see @fig:workflow-analysis-python):

1. Create a run file
2. Run the simulation defined by the run-file
3. Store the results as a file.
4. Load the simulation results into Python and post-process the data.
5. Output the post-processed data. (e.g. a plot or a new optics file)

![An exemplary workflow for using MAD-X or elegant from Python.](figures/workflow-analysis-python.svg){#fig:workflow-analysis-python}

One issue of this workflow is that not all information contained within the data structures and models of the simulation software is included in the output files. For example, MAD-X and elegant do not include a complete model of the accelerator's lattice but only an array of elements for the simulated orbit positions. Another issue is that the execution of MAD-X and elegant can only be driven by their respective run-file. Although both run-files provide basic features of a programming language, such as variables, loops, or if-else statements, their capabilities are extremely limited compared to Python. Therefore it would be desirable to drive the execution of the simulation using Python. Full access to the accelerator model of these simulations software would require implementing a Python interface for MAD-X or elegant. PyMAD [@pymad] is an attempt to create a Python API for MAD-X. As Python is a highly object-oriented language and MAD-X is mainly written in C and Fortran, it is not trivial to design an API that fits the different programming paradigms of these languages. The PyMAD project was unmaintained since 2017 but was recently picked up by the Heidelberg Ion-Beam Therapy Center (HIT) [@cpymad].

![Driving the execution of MAD-X or elegant using Python. A new run-file is generated for each iteration of the optimization process.](figures/workflow-python-driven.svg){#fig:workflow-python-driven}

To still leverage the powerful optimizers of the Python ecosystem, one common workaround is to use a template lattice-file or run-file: At the beginning of each iteration, Python generates a unique input file by inserting the values of the optimization parameters into the template file. Using this new run-file, Python then starts the simulation software as a sub-process, parses the results, calculates the value of the fitness function, and lets the optimizer compute the values of the optimization arguments for the next iteration. This is repeated until the terminating condition of the optimizer is met. Afterward, the final results are saved to a file. This workflow, illustrated in @fig:workflow-python-driven, has several drawbacks:

* No direct access to the accelerator model.
* It is computationally very inefficient: The simulation software has to parse the run-file and rebuild the accelerator model for each iteration because the memory is freed after the program terminates.
* Storing simulation results in a file and loading them into Python for each iteration is another performance issue: Hard disks are many magnitudes slower than computer memory. Even though this could be enhanced by using a RAM disk, serializing and deserializing the simulation results for each iteration are still not optimal.
* Substituting strings in a run-file is very error-prone and can lead to hard-to-find bugs.

For these reasons, it would be desirable to have a direct Python API to drive the execution of accelerator simulations. As discussed above, integrating one of the existing simulation codes in Python is a difficult task. It was therefore decided to develop a new optics code as a native Python package. As Python is a dynamically typed language and its major implementation CPython @cpython does not convert the source code directly into native machine instruction, ordinary Python programs execute slower than programs written in lower-level languages like C or Fortran. To ensure an extremely fast calculation of the Twiss parameters, which is necessary because high-dimensional optimizations often require millions of iterations, time-critical parts were implemented in the C language.

The code is partially based on scripts written for the Q5T2-off optics of my bachelor's thesis. At the time of this thesis, the code is capable of calculating most of the linear parameters like the Twiss parameters, the dispersion function, the betatron phase, the tune, the momentum compaction factor, the natural chromaticity, the emittance, and synchrotron radiation integrals. Particle tracking is implemented by the matrix method. In addition, an experimental branch can do particle tracking by integrating the equations of motion, which is used for some plots in this thesis but not well tested.

A main feature of the developed code is its accelerator model, which includes an internal dependency graph between the accelerator elements: Whenever an element changes one of its attributes, it automatically notifies all its dependents. For example, suppose a magnet changes its length. In that case, it notifies its containing lattice that its length has to be recomputed, which in turn notifies a simulation method that the linear optics parameters have to be recalculated the next time they are accessed. That is convenient for the users because they do not have to keep track of complex dependency relations and ensure that only outdated properties are recomputed. No performance is wasted on calculating already known values.

The next chapter provides an introduction to the physical foundation of the developed code.
