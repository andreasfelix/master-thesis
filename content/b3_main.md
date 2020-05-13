# Simulation and Measurements

Test references equation of different section. *@eq:betatron-oscilation

## Implementation of the Optics Simulation Program

### Overview of used Technology

### Performance Comparision of different Implementations of Twiss Computations

### An Object-Orient Representation of the Magnetic Lattice

This section gives a short overview of the purpose of the Python library *apace*. A comprehensive documentation can be found at: [https://apace.readthedocs.io](https://apace.readthedocs.io)

A main difficutly besides of the implementation of the physical simulation methods is the representation of the particle accelerator within the simulation software. To leverage the exisiting optimization and learning algorithms it is benefical to have a digital version of the machine.

This digital representation is often called an *environment* which the optimizer or agents can act on. The different tracking or twiss calculation implementations are build on top of this enviroment. If the agent changes the environment, by for example changing the value of a magnet, the enviroment informs the simulation method that it needs to recompute the new state of the particle beam. Once the the new state is computed the optimizer can observe the new state and take a new action on the environment. These steps are repeated until a satisfying state is reached. (See @fig:workflow-optimizer)

![Relationship between the lattice file, the digital representation of the accelerator, the simulation methods and the optimizer.](figures/workflow-optimizer.svg){#fig:workflow-optimizer}


The description of accelerator is stored in a so called lattices file. This file has to be parsed by the simulation software and the different constituents of the accelerator have to be represented by data types which are availalbe in the given programming language.

As Python is predominantly used at HZB and it was chosen to implement the digital representation of the accelerator. To provide a convenient interface this was done by done in a object-oriented way primarliy using two base classes:

1. `Element` class
2. `Lattice` class

An instance of `Element` class is a fundamental building block of the particle accerlator. This could be for example a `Drift` space, a `Dipole` magnet or a `Cavity` object. On the other hand, an instance of the `Lattice` class is a sequence of `Element` objects or even other (sub-)`Lattice` objects.

Each different element type is a subclasss of the `Element` class, which provides common attributes like a `length` or `name`, which uniquely identifies the element. Each subclass implements additional attributes to describe the given element type. This

As this object-orient way comes at a price, the simulation methods itself should use more primitve data structures like arrays. Only the interface to digital version of the particle accelerator should use this higher-level data structures. The simulation methods should be implemented as fast as possible.

The representation of the particle accelerator can be thought of as a tree-like structure, as shown in @fig:lattice-tree, where the `Element` objects are the leafs, the sublattices are the nodes and the main lattices is the root the tree.

![A representation of the BESSY II storage ring design lattice. At the top tree is the  *BESSY II* lattice, which consists out of the the *Doublet* and *Triplet* sub-lattices. The *Doublet* and *Triplet* again consist out of two *Achromat* sub-lattices, one *Straight* sub-lattice and two dipole elements.](figures/lattice-tree.svg){#fig:lattice-tree}

## Adjusting the BESSY II Optics for the VSR project

### Optimizing the Q5T2 optics in simulations

### User Operation Acceptance Test of the Q5T2 Optics

1. Injection Efficiency
2. Kicker Lifetime
3. IDs, bumps
4. High current test
5. General effects on user operations

## High beta function in T2 (Emittance Exchange)

