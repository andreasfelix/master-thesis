# Implementation

This chapter covers the challenges and consideration made of the implementation of the developed optics code. For a 

## Overview of Used Technology

## Improving the Performance of the Twiss Calculation

- rewrite time critical part in c
- instead of matrix multiplication use ausmulitplizierten term

A relativey simple but effective optimization is

$$ \mathbf{B}(s_1) = \mathbf{R}(s_0,s_1) \cdot \mathbf{B}(s_0) \cdot \mathbf{R}^T(s_0,s_1)
$$

$$
\begin{pmatrix}
    \beta_x & -\alpha_x & 0 & 0 \\
    -\alpha_x & \gamma_x & 0 & 0 \\
    0 & 0 & \beta_x & -\alpha_x \\
    0 & 0 & -\alpha_x & \gamma_x
\end{pmatrix} =
\begin{pmatrix}
    R_{11} & R_{12} & 0 & 0 \\
    R_{21} & R_{22} & 0 & 0 \\
    0 & 0 & R_{33} & R_{34} \\
    0 & 0 & R_{43} & R_{44}
\end{pmatrix}
\begin{pmatrix}
    \beta_x & -\alpha_x & 0 & 0 \\
    -\alpha_x & \gamma_x & 0 & 0 \\
    0 & 0 & \beta_x & -\alpha_x \\
    0 & 0 & -\alpha_x & \gamma_x
\end{pmatrix}
\begin{pmatrix}
    R_{11} & R_{12} & 0 & 0 \\
    R_{21} & R_{22} & 0 & 0 \\
    0 & 0 & R_{33} & R_{34} \\
    0 & 0 & R_{43} & R_{44}
\end{pmatrix}^\mathrm{T}
$$

$$
\begin{aligned}
    \beta(s)  & \quad= & R_{11}^2 \:\beta(s) \quad        & - & 2 R_{11} R_{12} \:\alpha(s)\quad            & + & R_{12}^2 \:\gamma(s)     \\
    \alpha(s) & \quad= & - R_{11} R_{12} \:\beta(s) \quad & + & (R_{11}R_{22} + R_{12}^2)\: \alpha(s) \quad & + & R_{12}R_{22} \:\gamma(s) \\
    \gamma(s) & \quad= & R_{12}^2 \:\beta (s) \quad       & - & 2 R_{12} R_{22} \:\alpha(s) \quad           & + & R_{22}^2 \:\gamma(s) ,
\end{aligned}
$$ {#eq:betatron-function-transformation}

Twiss product is a R^n -> R^m ...:
write twiss multiplication in index notation (similar to einsum) 

TODO: add pythran and numba

![Performance comparison of different twiss calulation implementations.](figures/benchmark-twiss-calculation.svg){#fig:benchmark-twiss-calculation}



## An Object-Orient Representation of the Magnetic Lattice

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


## LatticeJSON: A Universal Lattice File Format
