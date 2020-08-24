# Introduction

The first section of this chapter comprises a brief overview of the current status of the third generation light source BESSY II. The second section 

## old stuff

- Simulation tool to optimize the BESSY II optics with regard to the VSR Optics was developed in the Bachelors thesis. This tool was improved significantly and was used to further optimize the best solution of the BA. This tool can also be used for other LatticeDesign related tasks:

- Beam Physics of lightsource lattices (auch MBA): Comparing the most important lattices & parameters (emittance, Einheitszelle Twiss(betax/y, dispx)) of a few exemplary lattices
- The goal is to use this tool to develop a lattice of the BESSY II successor in the phd

- The goal of this thesis was to further enhance this tool. Discuss its capabitlites at the example of canonical lattices FODO, DBA, TBA. Its application for real world use cases is descirbed in  ...


## Current Status of BESSY II

- Viel los in der Welt: MBA lattices worldwide as updates for lowest emittance, but no timing: https://www.maxiv.lu.se/science/accelerator-physics/current-projects/timing-modes-for-the-max-iv-storage-rings/


- Complex filling pattern and low alpha -> VSR and using TRIBs to separate bunches
- vsr module benotiegt mehr platz. BA hat eine loesung fuer gefunden. diese optics muss wieter verbessert werden.


- Q5t2 und andre lattice modifications brauchen ein optimierungs program fuer twiss. warum eine neue software geschrieben wude anstatt exisiterende zu nutzen is in motivations erklaert.
- ein Python API/Wrapper fuer die complexen C programme elegant und MADX zu schreiben, scheint schwieriger zu sein, als ein simpleren optics optimierer in python von scrztch zu schreiben. fuer lattice design erstmal nur twiss, tune, emittance synch integrals wichtig.

## Motivation: The need of a Python interface for particle accelerator simulations

Fuer die optimierung von BESSY II lattice und fuer die entwicklung von BESSY3 lattice wird ein lattice development tool gebraucht! Da alle Python nutzen, waere es wuenschenswert, wenn diese ein native Python anbindung hat!

MAD-X [@madx] and elegant [@elegant] are the most mature and commonly used accelerator physics simulation codes. Both programs a driven by an input file - often called runfile. This file defines various simulation parameters, but can also be used to define an optimization procedure. After the execution the results are stored in an output file. Over the years there emerged various toolkits and programs to inspect, post-process and plot these results. Sometimes, for complex runs more flexibiltiy is needed, which is the reason Python is commonly used for post-processing and analysis of the simulation data.

Python has a rich ecosystem of numerical libaries and optimization tools, which is growing day by day. It has become the go-to language for scientific computing and machine learning. A typical workflow of using MAD-X or elegant with Python would be (see @fig:workflow-analysis-python):

1. Create a run file
2. Run the simulation as defined by the runfile
3. Store the results as file.
4. Load the simulation results into Python and post-process the data.
5. Output the post-processed data. (e.g. a plot or a new optics file)

![An examplary workflow for using MAD-X or elegant from Python.](figures/workflow-analysis-python.svg){#fig:workflow-analysis-python}

One issue of this workflow is that not all information contained within the data-structues and models of the simulation software is included in the output files. For example MAD-X and elegant do not include complete model of the accelerator's lattice, but only an arrays of elements for the simulated orbit positions. Another issue is that the execution of MAD-X and elegant can only be driven be their respective run-file. Altough both run-files provide basic features of a programming language, such as variables, loops or if-else statements, their capablitlies are extremely limited in comparison to Python. Therefore it would be desirable to drive the execution of the simulation using Python. Full access to the accelerator model of these simulations softwares would require to implemented a Python interface for MAD-X or elegant. PyMAD [@pymad] was an attempt to create a Python API for MAD-X. As Python is a highly object oriented language an MAD-X is mainly written in C and Fortran, it is not trivial to design an API which fits the different programming paradigms of these languages. The PyMAD project is unmaintained since 2017.

To still leverage the powerful optimizers of the Python ecosystem one common workaroud is to use a template run-file: At the beginning of each iteration Python is used to generate a unique run-file by inserting the values of the optimization parameters into the template lattice-file. Using this new run-file Python then starts the simulation software as sub-process, parses the results, calculates the values of the fitness function and let the optimizer compute the values of the optimization arguments for the next iteration. This is repeated until the terminating condition of the optimizer is met. Afterwards the final results are saved to a file. This workflow is illustrated in @fig:workflow-python-driven

![Driving the execution of MAD-X or elegant using Python. A new run-file is generated for each iteration of the optimization process.](figures/workflow-python-driven.svg){#fig:workflow-python-driven}

has several drawbacks:

* It is computationally very inefficient: The simulation software has to parse the run-file and rebuild the accelerator model for each iteration, because the memory is freed after the program terminates.
* Storing simulation results in a file and loading them into Python for each iteration is another performance issue: Hard disks are many magnitudes slower then computer memory. Even though this could be enhanced by using a RAM disk, serializing and deserializing the simulation results for each iteration is still not optimal.
* Substituting strings in a run-file is very error prone and can lead to hard to find bugs.

For these reasons it would be desirable to have an direct Python API to drive the execution of accelerator simulations. As discussed above, integrating one of the existing simulation codes in Python is a difficult task. It was therefore decicided to develop a new optics code as native Python package. As Python is a dynamically typed language and its major implementation CPython does not convert the source code directly into native machine instruction, ordinary Python programs execute slower than programs written in lower level languages like C or Fortran. To ensure extremly fast calculation of the Twiss parameter, which are necessary because high-dimensional optimization often require millions of iterations, time-critical parts were implemented using the C language.

The code is partially basded on scripts written for the Q5T2-off optics of my Bachelor's thesis. At the time of this theis, the code is capable of calculating most of the linear parameters like the Twiss paramter, the dispersion function, the betatron phase and tune, the momentum compaction factor, the natural chromaticity, emittance and synchrotron radiation integrals. At the moment particle tracking is only implemented by the matrix method. There is an experimental branch which is able to do particle tracking by integrating the equations of motion, but it is not well tested but is still used for some plots in this thesis.

A main feature of the developed code is its accelerator model, which includes an internal dependency graph between the elements of the accelerator: Whenever an element changes on of its attributes it automatically notifies all its dependents. For example if an magnet changes its length it notifies its containing lattice that its length has to be recomputed, which then again notifies then a simulation method, that the linear optics parameter have to be recalculated the next time their accesed. This is not only convenient for the users, because they do not have to keep track complex dependency relations, but also ensures, that only outdated properties are recomputed and no performance is wasted on calculating already known values.

Furthermore this accelerator model provides an extensible foundation for future simulation methods. At HZB there is currently work going on to enable particle tracking using Lie maps [reference tom/jernej], which could be implemented on top of this accelerator model.

An introduction to the physical foundation of the developed code is provided in the next chapter.
