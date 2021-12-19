# Implementation

This chapter covers the challenges and considerations made in implementing the developed optics code *apace*. The first section presents a brief overview of the used technologies. @sec:improving-performance presents the optimizations made to improve the performance of the computation of the Twiss parameters. While a high-level overview of the functionality of the accelerator model is given in @sec:accelerator-model, @sec:implementation-usage goes into more detail on a usage example. Finally, @sec:latticejson introduces the new JSON-based lattice file format *LatticeJSON*.

The complete documentation of the developed code is provided by @sec:appendix-documentation or at:

> [https://apace.readthedocs.io](https://apace.readthedocs.io)

The source code is available at: 

> [https://github.com/andreasfelix/apace](https://github.com/andreasfelix/apace)

## Overview of Used Technology

The new lattice development tool is implemented in the Python language. While Python's large ecosystem of scientific libraries and high-level syntax, sometimes almost similar to plain English, are major benefits, its dynamic nature makes it necessary to make considerations concerning the performance. For example, in Python, even numbers are rich objects at runtime, and integers can hold values of arbitrary size. In addition, collection types like lists only hold references to objects, leading to non-contiguous chunks of data and, therefore, to less efficient memory layouts. Python's dynamic type system offers much flexibility but provides fewer guarantees, leading to many lookups, inefficient loops, and generally involves more steps for any operation than in a statically typed language. Furthermore, the most widely used Python implementation CPython @cpython does not compile to native machine code but instead translates Python files to an intermediate format called bytecode and then executes it on a virtual machine, leading to a performance penalty.

There are various ongoing efforts to improve the performance of CPython [@faster-cpython;@mypyc;@cinder] or to create an alternative faster implementation of the Python language [@pypy;@nuitka]. Nevertheless, even with these optimizations, pure Python cannot compete with low-level languages in numerical performance, making it not well suited to implement a computational-heavy library.

One popular solution to this performance problem is the NumPy package @numpy, which is so widely used that it can be almost considered part of Python when it comes to scientific computing. NumPy provides a highly efficient multidimensional array type, which is, contrary to Python's built-in list, fixed in size, a contiguous chunk of memory, and restricts all elements to be the same type with a fixed bit length. In addition, NumPy comes with a collection of mathematical routines implemented in lower-level languages like C or Fortran. These routines, like matrix multiplication or element-wise operations, are not run by Python's bytecode interpreter but separated from the language runtime at native speed. Thus, using the NumPy package, scientists get the best of both worlds: Python's flexibility and short development times and the performance of natively compiled libraries when working with numerical data. 

All data represented by arrays like the beta or dispersion functions utilize NumPy's array type in the developed code. A limiting factor is when an operation is not expressible by a single NumPy function but has to be composed out of many function calls. Crossing the boundaries between NumPy and Python worlds imposes a performance cost. This performance penalty is minimized the more time is spent within a NumPy routine. For the computation of the Twiss product or the one-turn-matrix of the storage ring, which includes many consecutive multiplications of small 6x6-matrices, the cost of crossing the boundaries, therefore, becomes a limiting factor. For algorithms requiring much indexing, using a Numpy array can even be slower than pure Python code.

Solutions to improve the performance of algorithms in combination with NumPy arrays are the Numba @numba or Pythran @pythran compilers, which can translate a subset of the Python language and some NumPy operations to native machine code. However, to achieve maximum performance, it was decided to implement the time-critical parts of the developed code in C. Therefore, the CFFI package @cffi was used to call the C functions from Python. Furthermore, to fully utilize the hardware, some of the C routines were written with multithreading using the OpenMP API @openmp.

With a share of about 95 percent, most of the code is still implemented in Python. All of this should be invisible to a user of the developed library.

Another popular Python package is the matplotlib library @matplotlib, which provides a framework to create scientific plots. It is very common when plotting the Twiss parameters to visualize the magnetic lattice or annotate the different accelerator sections. Therefore, the developed code provides some functions for this purpose utilizing the matplotlib framework. Furthermore, a function to draw a floorplan for a given magnetic lattice is included.

## Improving the Performance of the Twiss Calculation {#sec:improving-performance}

This section discusses some optimizations to improve the performance of the computation of the one-turn-matrix and the Twiss parameters. The steps for calculating the Twiss parameters can be summarized:

1. Choose an arbitrary point on the orbit as an initial position for the periodicity condition
1. Create an array of $N$ elements starting from the initial point
    $$[\mathrm{A}, \mathrm{B}, \mathrm{C}, \mathrm{D}, ...]$$
1. Map the array of elements to an array of transfer matrices (transfer matrices for individual elements)
    $$[\mathbf{R}_\mathrm{A}, \mathbf{R}_\mathrm{B}, \mathbf{R}_\mathrm{C}, \mathbf{R}_\mathrm{D}, ...]$$
1. Accumulate the transfer matrices to the different orbit positions (transfer matrics from starting point to orbit position of given element). The last matrix of this array $\mathbf{R}_N$ corresponds to the one-turn-matrix.
    $$
    [\mathbf{R}_1, \mathbf{R}_2, \mathbf{R}_3, ..., \mathbf{R}_N] \; \textrm{with} \;
    \mathbf{R}_1 = \mathbf{R}_\mathrm{A}, \;
    \mathbf{R}_2 = \mathbf{R}_\mathrm{B} \mathbf{R}_1, \;
    \mathbf{R}_3 = \mathbf{R}_\mathrm{C}  \mathbf{R}_2 , ...
    $$
1. Calculate initial Twiss parameters from one-turn-matrix $\mathbf{R}_N$ using (periodic solution)
1. Calculate the Twiss product of the initial Twiss matrix with the accumulated transfer matrix at every orbit position

    $$
    \mathbf{B}_n = \mathbf{R}_n \cdot \mathbf{B}_0 \cdot \mathbf{R}_n^\mathrm{T},
    $$

    where $\mathbf{B}_0$ corresponds to the Twiss parameters at the initial position.

During a scan or optimization, the Twiss parameters are calculated multiple times in a row, which allows for a relatively simple but effective optimization in step 3: Supposing not every magnet of the lattice changes during each iteration. Then, if the code keeps track of the changed elements, only the transfer matrices for changed elements must be recomputed. The transfer matrices of the remaining elements can be cached.

![The calculation of the accumulated transfer matrices has to be serial (top). Alternatively the one-turn-matrix $\mathbf{R}_N$ can be calculated in parallel.](figures/matrix-multiplication.svg){#fig:matrix-multiplication}

The calculation of the Twiss parameters is inherently a not fully parallelizable problem because either step 4 or step 6 have to be computed sequentially, leading to two options:

In the first case, calculating the accumulated transfer matrices $\mathbf{R}_n$ for every orbit position makes step 6 parallelizable. However, as each accumulated transfer matrix $\mathbf{R}_n$ depends on the previous transfer matrix $\mathbf{R}_{n-1}$, step 4 must be sequential, shown in the upper part of @fig:matrix-multiplication.

Alternatively, the calculation of the accumulated transfer matrices could be skipped, and the one-turn-matrix $\mathbf{R}_N$ could be computed in parallel as shown in the bottom part of @fig:matrix-multiplication. But, this would make it necessary to calculate the Twiss product using the individual transfer matrices, for example

$$
\mathbf{B}_\mathrm{3} = \mathbf{R}_\mathrm{C} \cdot \mathbf{B}_2 \cdot \mathbf{R}_\mathrm{C}^\mathrm{T},
$$

which would require step 6 to be sequential.

There are two reasons to choose the first option over the second: First, the Twiss product contains two matrix multiplications, while the accumulation of the transfer matrix contains only one. Consequently, the first option performs more work in parallel. Secondly, in option 1, the Twiss product is fully parallelizable with a step complexity of 1 and limited only by the number of threads. On the other hand, the calculation of the one-turn-matrix using parallel reduction has a step complexity of $\log_2(N)$.

![Performance comparison of different implemenations of the Twiss product](figures/benchmark-twiss-calculation.svg){#fig:benchmark-twiss-calculation}

As most of the time is spent in steps 4 and 6, it is critical to make them as fast as possible. @fig:benchmark-twiss-calculation shows a benchmark of different implementations of the Twiss product (step 6). `numpy_dot` corresponds to the naive NumPy implementation where the Twiss product is calculated using `numpy.dot`, leading to $2 N$ function calls. The `numpy.einsum` or `opt_einsum` functions allow calculating any arbitrary operation expressible in index notation within a single function call. For the Twiss product

$$
\mathbf{B}_{nij} = \sum_{kl} \mathbf{R}_{nik} \mathbf{B}_{0kl} \mathbf{R}_{njl}
$$

this corresponds to:


```Python
numpy.einsum("nik,kl,njl->nij", matrices, b0, matrices)
```

The Twiss product was also implemented in C. Once as the full matrix product corresponding to @eq:transformation-beta-matrix and once as a reduced version corresponding to @eq:betatron-function-transformation, which takes advantage of the symmetry of the transfer matrices. Furthermore, the C versions were implemented as sequential and parallel versions, taking advantage of all CPU cores. Finally, the C code was called once using the ctypes package, included in the standard library, and once with the aforementioned CFFI package.

The implementations vastly vary in execution speed. The `numpy.einsum` version is below $N=2000$ significantly faster than the naive NumPy implementation `numpy_dot`. This can probably be attributed to the much fewer function calls. Surprisingly, there is a large performing decrease at about $N \approx 2000$, making the `numpy.einsum` as about as fast as the `numpy_dot` version.

The custom C versions are significantly faster. One reason for that is that the C compiler knows the size of the matrix array is $(N, 6, 6)$ and can therefore produce optimized code for this operation. Furthermore, modern C compilers can automatically take advantage of the *Single Instruction, Multiple Data* (SIMD) instructions shipped with modern CPUs. SIMD instructions allow performing vectorized operations on up to 512 bits at once. By looking at the generated code, it was verified that these SIMD instructions were present in the resulting binary.

Two of the parallel C versions are below $N \approx 1500$ slower than their sequential counterpart. There is some cost in setting up the different threads. If the time spent within the thread is too short, this initial cost limits the executions speed, explaining why the sequential versions are faster for a lower number of matrices $N$. Looking at the graphs of the parallel version, one can see multiple spikes. This is because the slowest core limits the total runtime of a parallel operation. If the CPU is fully utilized, the operating system might briefly stop one core to schedule a background process, leading one thread to be significantly slower than the others.

Finally, the CFFI package has a lower overhead in calling a C function than the ctypes packages. The difference of this overhead is significant up to $N \approx 5000$. For this reason and because CFFI is compatible with more Python implementations, it was decided to use the CFFI package instead of the built-in ctypes package.

## Representation of the Magnetic Lattice {#sec:accelerator-model}

Besides implementing the physical simulation methods, a major difficulty is the representation of the particle accelerator within the simulation software. The goal is to facilitate the usage of existing optimization and learning algorithms. A good conceptual approach is to model the programming interface after the real machine, in a sense, by creating a digital representation of the accelerator. Different simulation methods like tracking or Twiss calculation implementations are built on top of this digital representation.

Together with a simulation method, the interaction of digital representation of the accelerator and the optimizer can be considered an *environment-agent* relationship, visualized in @fig:workflow-optimizer. In that sense, the optimizer is an *agent* changing configuration of the *environment*, the digital representation of the accelerator, and observes the new state corresponding to the result of the simulation method. An event system powers the underlying implementation. Supposing the optimizer changes the strength of a quadrupole. Then, the digital representation of the accelerator informs the simulation method that it must recompute a new state. Next, the optimizer accesses the updated state and accordingly takes another action on the environment. These steps repeat until they reach a satisfactory condition.

![Relationship between the lattice file, the digital representation of the accelerator, the simulation methods, and the optimizer.](figures/workflow-optimizer.svg){#fig:workflow-optimizer}

The description of the accelerator is stored in a so-called lattices file. This file has to be parsed by the simulation software. The different constituents of the accelerator have to be represented by data types available in the given programming language. To provide a convenient interface, this was done in an object-oriented way, primarily using two base classes:

1. `Element` class
2. `Lattice` class

An instance of the `Element` class is a fundamental building block of the particle accelerator. This could be, for example, a `Drift` space, a `Dipole` magnet, or a `Cavity` object. On the other hand, an instance of the `Lattice` class is a sequence of `Element` objects or even other (sub-)`Lattice` objects.

Each element type is a subclass of the `Element` class, which provides common attributes like a `length` or a `name` that uniquely identifies the element. Furthermore, each subclass implements additional attributes to describe the given element type.

![A representation of the BESSY II storage ring design lattice. At the top tree is the  *BESSY II* lattice, which consists out of the *Doublet* and *Triplet* sub-lattices. The *Doublet* and *Triplet* again consist out of two *Achromat* sub-lattices, one *Straight* sub-lattice and two dipole elements.](figures/lattice-tree.svg){#fig:lattice-tree}

The representation of the particle accelerator can be thought of as a tree-like structure, as shown in @fig:lattice-tree, where the `Element` objects are the leaves, the `Lattice` objects are the nodes, and the main `Lattice` object is the root of the tree.

As this object-orient way comes at a price, the simulation methods should use more primitive data structures like arrays. Only the interface to the digital representation of the accelerator should use these higher-level data structures. Moreover, the simulation methods should be implemented as fast as possible.

## Usage {#sec:implementation-usage}

This section gives a small overview of the usage of the developed code. The reader is encouraged to start an interactive Python shell or IPython shell, which has multiline support, and follow along by copying the following code snippets.

The only requirements are Python 3.6 or higher and a C compiler. Then, the most recent version of the developed code, which is 0.1.0 at the moment, can be installed with:

```sh
pip install -U apace
```

The first step is to import the library:


```Python
import apace as ap
```

Next, we will build a FODO-ring consisting out of 8 FODO cells. Therefore we create a drift, a bending magnet, one horizontal and one vertical focusing quadrupole.

```python
d1 = ap.Drift("d1", length=0.55)
b1 = ap.Dipole("b1", length=1.5, angle=0.392699, e1=0.1963505, e2=0.1963505)
q1 = ap.Quadrupole("q1", length=0.2, k1=1.2)
q2 = ap.Quadrupole("q2", length=0.4, k1=-1.2)
```
The first argument corresponds to the name of the element, while the other parameters are self-explaining. By arranging the just created elements, we can build a FODO cell. Copying this cell eight times, we end up with a ring with 8-fold symmetry.

```python
fodo = ap.Lattice("FODO", [q1, d1, b1, d1, q2, d1, b1, d1, q1])
ring = ap.Lattice("RING", 8 * [fodo])
```

To get more information on a specific element, we can use the `print` function to output a table of attributes:

```sh
>>> print(b1)

type            : Dipole
angle           : 0.392701
e1              : 0.1963505
e2              : 0.1963505
k0              : 0.2618006666666667
length          : 1.5
name            : b1
parent_lattices : {FODO}
radius          : 3.8196999752992733
```

These attributes can be accessed using Python's usual `.`-operator.


```python
>>> d1.length
0.55
>>> fodo.length
6.0
```

What is notable is that attributes like the length of a lattice, which depends on its elements' lengths, are automatically updated when one of its elements changes its length.


```python
>>> d1.length = 0.6
>>> fodo.length
6.2
```

Next, our goal is to plot the Twiss parameters of the FODO ring. Therefore, we create an instance of the `Twiss` class, which takes a `Lattice` object as its argument.

```python
twiss = ap.Twiss(ring)
```
We can use matplotlib to plot the beta and dispersion functions:

```Python
import apace.plot as aplot
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(twiss.s, twiss.beta_x, label=r"$\beta_\mathrm{x}$ / m")
ax.plot(twiss.s, twiss.beta_y, label=r"$\beta_\mathrm{x}$ / m")
ax.plot(twiss.s, twiss.eta_x, label=r"$\eta_\mathrm{x}$ / m")
ax.set(xlabel="orbit position $s$ / m")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.1), ncol=3, frameon=False)
fig.show()
```

The developed code comes with a set of convenience functions, which allows us to draw the magnetic lattice and annotate the locations of the individual FODO cells.


```python
aplot.draw_elements(ax, ring, location="bottom")
aplot.draw_sub_lattices(ax, ring, location="bottom")
```

After calling these functions, we end up with the plot shown in @fig:fodo-twiss-apace.

![Twiss parameters for a FODO ring with 8-fold symmetry](figures/fodo-twiss-apace.svg){#fig:fodo-twiss-apace}

In the following example, we will create the famous necktie plot, which marks the regions of quadrupole configurations leading to a stable lattice. We will use an interval $0 < k < 2$ with a sample size of 100. The results will be stored in a 2-dimensional NumPy array.

```Python
import numpy as np

samples = 100
start, end = 0, 2
results = np.empty((samples, samples))
interval = np.linspace(start, end, samples)
```
Next, we loop over the quadrupole strength of the horizontal focusing Q1 and vertical focusing Q2 quadrupoles. In the body of the loop we, store the average beta function if a stable solution exists. Otherwise, we store the *not a number* (nan) value.

```python
for i, q1.k1 in enumerate(interval):
    for j, q2.k1 in enumerate(-interval):
        try:
            results[i, j] = np.mean([twiss.beta_x, twiss.beta_y])
        except ap.UnstableLatticeError:
            results[i, j] = np.nan
```
Again, we can use matplotlib to visualize the results.

```Python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
extent = start, end, start, -end
image = ax.imshow(results.T, extent=extent, origin="lower", vmin=0, vmax=30)
ax.set(xlabel=r"$k_\mathrm{q1}$ / m$^{-2}$", ylabel=r"$k_\mathrm{q2}$ / m$^{-2}$")
fig.colorbar(image, ax=ax).ax.set_title(r"$\beta_\mathrm{mean}$")
fig.show()
```

Executing this code gives the plot in @fig:necktie-plot-apace.

![Necktie plot - The region of quadrupole configurations leading to a stable lattice has the shape of a necktie](figures/necktie-plot-apace.svg){#fig:necktie-plot-apace}


In the last example, we will use a more complex lattice. Lattices can not only be constructed manually as shown above but also loaded from a lattice file. The developed code can load lattice files in the LatticeJSON format, discussed in more detail in the next section, and all formats where converters to the LatticeJSON format exist. At the time of this thesis, these are the elegant and MAD-X lattice file formats.

The `ap.Lattice.from_file` method can be used to create a `Lattice` object from a file. The argument can be a local path or the URL to the lattice file. In our case, we use this function to load the BESSY II standard user lattice from a URL.

```python
url = "https://raw.githubusercontent.com/andreasfelix/master-thesis/main/code/demo/accelerator-model/bessy2_stduser.json"
bessy2 = ap.Lattice.from_file(url)
twiss = ap.Twiss(bessy2)
```

We obtain a reference to an individual element by passing its name to the BESSY II `Lattice` object. In this case, we want a reference to the Q5 quadrupole in the T2 section.

```python
q5t2 = bessy2["Q5T2"]
```

Besides the beta and dispersion functions, the `Twiss` has attributes for the tunes, alpha and gamma functions, emittance, natural chromaticity, and synchrotron radiation integrals. For example, the horizontal and vertical tunes of the BESSY II standard user lattices are given:

```Python
>>> twiss.tune_x, twiss.tune_y
(17.830955250872567, 6.725123956032014)
```

Also, attributes like the tunes, which depend on the strength of the quadrupoles, are automatically updated when a magnet is changed. For example, reducing the strength of the Q5T2 quadrupole leads to a slightly lower horizontal but slightly larger vertical tune:

```Python
>>> q5t2.k1 -= 0.1
>>> twiss.tune_x, twiss.tune_y
(17.80617444219928, 6.745445862447529)
```

Finally, the `stable` attribute indicates if a lattice fulfills the stability condition, defined by @eq:stability-condition.

```python
>>> twiss.stable
True
```

Turning off the Q5T2 quadrupole leads to an unstable lattice.

```python
>>> q5t2.k1 = 0
>>> twiss.stable
False
```

How to achieve a working machine with the Q5T2 quadrupoles turned off is discussed in @sec:q5t2off-bessy-vsr-optics.

## LatticeJSON: An Attempt towards a Universal Lattice File Format {#sec:latticejson}

The definition of the magnetic lattice is stored in a so-called lattice file. There are several of these data formats, and often only their corresponding simulation software can process them. The variety of lattice file formats is such a big issue of the accelerator physics community that it even has its dedicated Wikipedia section [@lattice-file-issues]. Several converters between these files can do the heavy lifting but often still require manual adjustments made by a human. Nevertheless, even if the lattice file is available in all common formats, there is still no straightforward way to load the data into an arbitrary programming language. As the most mature accelerator simulation codes come bundled with a scripting language and optimization routines, this was a lesser problem in the past. However, there has been an uprise of powerful scripting languages and modern optimization libraries in the last several years. To leverage these tools, it would be is necessary to have convenient access to the lattice data.

One solution would be to write a robust parser for an existing lattice file format. Candidates would be the MAD-X @madx or elegant @elegant lattice file formats, which are very similar but not compatible. Both file formats have the problem that their syntax is ambiguous. Without further context, the parser cannot infer an attribute type. For example in

```txt
TWISS, FILE=optics;
```

`optics` is a string and not a variable name. In another case

```txt
RFC: RFCAVITY, HARMON=num;
```

`num` refers to a variable and not a string. In these cases, the parser has to know the type of `FILE` and `HARMON` to parse the file correctly, making implementing a parser non-trivial. Both lattice file formats also support variables and arithmetic expressions. MAD-X even supports more advanced constructs like loops, macros, and if-else statements, making implementing such a parser even more complex and error-prone. If the goal is to be 100% compatible, one would have to reimplement a whole programming language to load the lattice data. A more feasible solution would be to define a restricted subset of the MAD-X input file, which would contain only data and no logic. @sec:elegant-grammar and  @sec:madx-grammar contain grammar files allowing to load simple elegant and a subset of MAD-X lattice files into Python. They work for simple cases but fail for more advanced lattice files because of the reasons mentioned above.

A better solution for a plain lattice data format would be to define a schema for an existing data format, which already has parsers implemented for the most popular programming languages. One attempt of such a universal lattice file format was the Accelerator Markup language (AML) @aml and the Universal Accelerator Parser (UAP) @uap. The AML is based on the eXtensible Markup Language (XML), which is syntactically similar to HTML, the standard markup language for web documents. AML's goal was to support the evaluation of arithmetic expressions and two different representations of the magnetic lattice: An *unevaluated representation* containing nested sub-lattices and variables and a *flat representation*, where the sub-lattices are expanded into a flattened array of elements. Furthermore, it aimed to support information beyond the lattice description, like control system configurations, magnet history, or other documentary data. This way, AML could be used as an all-in-one solution for an accelerator facility database. Unfortunately, as of March 2020, AML and the UAP are no longer maintained.

The AML had high ambitions, which made it challenging to implement: The number of features, like variables and a complex representation of the magnetic lattice, made it, even though it is based on XML, necessary to implement a custom parser for every programming language.

This thesis takes a simpler approach: The lattice file should not implement variables or other dependency relations. This functionality is already available in programming languages and should not be reimplemented in the lattice file. The definition of a lattice file should not rely on different representations of the magnetic lattice. The lattice file should be easy to load and should not require an additional parser. The primary target of this lattice file should be simulation codes, and the implementation should not be made more complicated by making it suitable for control system usage.

Further requirements are: The lattice file format should be independent of the simulation tool and programming language. The underlying file format should be commonly used, so there is no need to implement it for different programming languages. Furthermore, it should be easy to generate elegant and MAD-X files from this intermediate format. Finally, shown in @fig:lattice-tree, the magnetic lattice has a tree-like structure: It consists of different elements, like drifts, magnets, cavities, and sub-lattices, which in turn consist of other elements. A universal lattice file format should take this structure into account.

Storing the description of the magnetic lattice raises effectively two questions (@fig:lattice-representation):

1. How to store the lattice file persistently on disk?
2. How to represent the lattice file within a programming language?

As data structures and object types vary between programming languages, it is impossible to choose arbitrary data types. However, practically every programming language supports primitives like *strings*, *numbers*, *bools*, *null*, and some containers structures like *arrays* and *key-value stores*. So the goal should be to provide a consistent way to represent the information stored in the lattice files using these generic data types. This representation should not try to invent the next scripting language, but it should be a pure data format. That way, the lattice data can be used by any programming language.

![The lattice file has to be stored on disk. Therefore the representation of the lattice file within the programming language has to be serialized into a format that can be stored permanently. Conversely, this persistent data format has to be deserialized into a data structure when the lattice is loaded into a program.](figures/lattice-representation.svg){#fig:lattice-representation}

Fortunately, these issues are already solved by JSON [@json], which is an acronym for JavaScript Object Notation. Even though it has its origins in JavaScript, it is a language-independent and open data file format. It can describe complex data and is the de-facto standard for exchanging data between web applications. There already exist a huge amount of tools for validating and working with JSON.

JSON answers both questions as the is a 1:1 correspondence between JSON data types and the generic data types available in almost all programming languages. Once parsed, the lattice description is represented by the same abstraction of data types as when the lattice information was stored on disk. One problem of AML was, that the parsed lattice data, returned by the UAP, had a different structure than the stored XML file. So there were effectively two different representations of the same information.

JSON provides a convenient way to serialize and deserialize generic data types. To make use of JSON, the description of the magnetic lattice has still to be defined in terms of these generic data types. Such a definition can be achieved with a so-called JSON schema [@json-schema]. A first definition of such a JSON-based lattice file format was done and called LatticeJSON. The LatticeJSON schema file and more information on LatticeJSON are available at [@lattice-json].

For example, the definition of a FODO lattice as LatticeJSON file is given by:

```json
{
  "version": "2.2",
  "title": "FODO Lattice",
  "info": "This is the simplest possible strong focusing lattice.",
  "root": "ring",
  "elements": {
    "d1": ["Drift", {"length": 0.55}],
    "q1": ["Quadrupole", {"length": 0.2, "k1": 1.2}],
    "q2": ["Quadrupole", {"length": 0.4, "k1": -1.2}],
    "b1": ["Dipole", {"length": 1.5, "angle": 0.392701, "e1": 0.1963505, "e2": 0.1963505}]
  },
  "lattices": {
    "cell": ["q1", "d1", "b1", "d1", "q2", "d1", "b1", "d1", "q1"],
    "ring": ["cell", "cell", "cell", "cell", "cell", "cell", "cell", "cell"]
  }
}
```

To read the quadrupole strength of the Q1 quadrupole in Python, one can use:

```Python
import json

with open("/path/to/lattice.json") as file:
    lattice = json.load(file)

type_, attributes = lattice["elements"]["Q1"]
print("Quadrupole strength", attributes["k1"])
```

Alternatively, one can use the LatticeJSON library, which validates the lattice file and can load lattices files from URLs.

```python
import latticejson
lattice = latticejson.load("https://lattice-database.org/bessy2?mode=stduser")
```

The URL *lattice-database.io* is chosen as an illustrative filler in this example. However, it should be a goal to establish a central database of magnetic lattice files, where the operation mode or file format can be passed as a URL parameter. This would give physicists access to a large number of lattice files without the overhead of maintaining their own set of lattices. Furthermore, as it is straightforward to generate different versions of a JSON file automatically, LatticeJSON could simplify the implementation of such a database significantly.
