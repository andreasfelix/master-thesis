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


## LatticeJSON: An Attempt towards a Universal Lattice File Format

The definition of the magnetic lattice is stored in a so called lattice file. At the moment there are several of these data formats and all can only be processed by the corresponding simulation software. This variety of different lattice file format is an ongoing issue of accelerator physics and has even its on dedicated wikipedia section [@lattice-file-issues]. There exist several converters between these files, which are able to do the heavy lifiting, but often still require manual adjustments made by a human. But even if the lattice file is availiabe in all common formats, there is still no straightfoward way to load the data into the programming language of your choice. As the most mature accelerator simulations codes come bundled with several optimization routines and a scripting language, this was a smaller problem in the past. But in the last several years, there was an uprise of powerful scripting languages and modern optimization libraries. To leverage these tools it would be is necessary to have convenient access to the lattice data.

As at HZB and for this thesis Python was used, one solution would be to write a robust parser for an existing lattice file format. Candidates would be the MADX[@madx] or elegant[@elegant] lattice file format, which are very similar but not compatible. Both file formats have the problem that syntax is ambiguous: Without further context the parser cannot infer the type of an attribute. For example in

```txt
TWISS, FILE=optics;
```

`optics` is a string and not a variable name. In another case

```txt
RFC: RFCAVITY, HARMON = num;
```

`num` refers to a variable and not a string. In these cases the parser has to know the type of `FILE` and `HARMON` to parse the file correctly. This makes the implementation of a parser non-trivial and ties the file format specific the simulation software. Both lattice file formats also support variables and arithmetic expressions. MADX even supports more advanced constructs like loops, macros and if-else statements. This makes the implementation of such a parser even more difficult and error-prone. If the goal is to be 100% compatible one would have to reimplement a whole programming language, just to load the lattice data. A more feasible solution would be to define a restricted subset of the MADX input file, which would contain only data and no logic. Grammar files which allow to load basic elegant and a subset of MADX lattice files into Python are given in the appendix @sec:elegant-grammar and @sec:madx-grammar, respectively. These work for simple cases but fail for more advanced lattice files, because of the above mentioned reasons.

A better solution for plain lattice data format would be to define a schema for an existing data format, which already has parsers for the the most popular programming languages. One attempt of such an universal lattice file format was the Accelerator Markup language (AML)[@aml] and the Universal Accelerator Parser (UAP)[@uap]. The AML is based on the eXtensible Markup Language (XML), which is syntactically similar to HTML, the standard markup language for web documents. AML's goal was to support the evaluation of arithmetic expressions and two different representations of the magnetic lattice: A "unevaluated" representation with contains nested beamlines as well as variables and a "flat" representaiton, where the sub-lattices are expanded into a flattend array of lattice elements. Furthermore it aimed to support information beyond the lattice description, like control system configurations, magnet history or other documentary data. This way AML could be used as an all-in-one solution for an accelerator facilities's database. As of March 2020, AML and the UAP are no longer maintained.

The AML had high ambitions, which made it difficult to implement. The large amount of feature, like variables and a complex representation of the magnetic lattice, made it, even though it is based on XML, necessary to implement a custom parser for every programming langugage.

This thesis takes a simpler approach: Variables or other dependency relations should not be implemented by the lattice file. This functionality is already availabe in programming languages, and should not be reimplemented in the lattice file. The definition of lattice file should not rely on different representations of the magnetic lattice. The lattice file should be easy to load and should not require an additional parser. The main purpose of this lattice file should be simulation code and the implementation should not be complicated by making it suitable for control system usage.

Further requirements are: The lattice file format should be independent of the simulation tool and programming language. The file format should be commonly used, so there is no need to implemented it for different  programming languages.
It should be easy to generate elegant and MAD-X files from this intermediate format.
It should be taken into account, that the magnetic lattice has a tree-like structure (see @#fig:lattice-tree): The magnetic lattice consist of different elements, like drifts, magnets or cavities, as well as of sub-lattices, which by itself are made of other elements. A universal lattice file format should somehow take this structure into account.

Storing the description of the magnetic lattice raises effectivly two questions (@fig:lattice-representation):

1. How to store the lattice file persistently on disk?
2. How to represent the lattice file within a programming language?

As data structures and object types a specifically tied to a programming language it is not possible to choose arbitary data types. But practically every programming language supports primitives like *strings*, *numbers*, *bools*, *null* and some type of containers structures like *arrays* and *key-value stores*. The goal should be to provide a consistent way to represent the information stored in the lattice files using these generic data types. This representation should not try to invent the next scripting language, but it should be a pure data format. This way the lattice data can be used by any programming language.

![The lattice file has to be stored on disk. Therefore the representation of the lattice file within the programming language has to be serialize into a format that can be stored permanently. Conversely, this persistent data format has to be deserialize into a data structure when the lattice is loaded into a program.](figures/lattice-representation.svg){#fig:lattice-representation}

Fortunately this issues is already solved by JSON [@json], which is an acronym for JavaScript Object Notation. Even though it has its origins in JavaScript, it is a language-independent and open data file format. It is able to describe complex data and is the de-facto standard for exchanging data between web applications. There already exist an huge amount of tools for validating and working with JSON.

JSON effectlify answers both questions as the is a 1:1 correspondence between JSON data types and the generic data types available in almost all programming languages. Once parsed, the lattice description is represented by the same abstraction of data types as when the lattice information was stored on disk. One problem of AML was, that the parsed lattice data, returned by the UAP, had a different structure than the stored XML file. So there were effectively two different representations of the same information.

JSON provides a convenient way to serialize and deserialize generic data types. To make use of JSON, the description of the magnetic lattice has still to defined in terms of these generic data types. Such a definition can be done with a so called JSON schema [@json-schema]. A first definition of such a JSON based lattice file format was done and called LatticeJSON. The LatticeJSON schema file as well as more information on LatticeJSON is available at [@lattice-json].

For example, the definition of a FODO lattice as LatticeJSON file is given by:

```json
{
  "version": "2.0",
  "title": "FODO Lattice",
  "info": "This is the simplest possible strong focusing lattice.",
  "root": "RING",
  "elements": {
    "D1": ["Drift", {"length": 0.55}],
    "Q1": ["Quadrupole", {"length": 0.2, "k1": 1.2}],
    "Q2": ["Quadrupole", {"length": 0.4, "k1": -1.2}],
    "B1": ["Dipole", {"length": 1.5, "angle": 0.392701, "e1": 0.1963505, "e2": 0.1963505}]
  },
  "lattices": {
    "CELL": ["Q1", "D1", "B1", "D1", "Q2", "D1", "B1", "D1", "Q1"],
    "RING": ["CELL", "CELL", "CELL", "CELL", "CELL", "CELL", "CELL", "CELL"]
  }
}
```

To read the quadrupole strength of the Q1 quadrupole in Python one could use:

```python
import json

with open("/path/to/lattice.json") as file:
    lattice = json.load(file)

type_, attributes = lattice["elements"]["Q1"]
print("Quadrupole strength", attributes["k1"])
```

Or, one can use the latticejson library, which validates the lattice file and can load lattices files from URLs.

```python
import latticejson
lattice = lattice.load("https://lattice-database.io/bessy2?mode=stduser")
```

The URL *lattice-database.io* is chosen as an illustrative filler in this example. But it should be a goal to establish a central database of magnetic lattice files, where the operation mode or file format can be passed as a URL parameter. This would give physisicts access to a large number of lattice files, without the overhead maintaining an own set of lattices. As it is straightforward to automatically generate different versions of a JSON file, LatticeJSON could simplify the implementation of such a database significantly.
