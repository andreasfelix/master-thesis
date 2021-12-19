# Developed Code {#sec:appendix-code}

**apace** is yet **a**nother **p**article **a**ccelerator **c**od**e** designed for the optimization of beam optics. It is available as Python package and aims to provide a convenient and straightforward API to make use of Python's numerous scientific libraries.

The source code is available at: 

> [https://github.com/andreasfelix/apace](https://github.com/andreasfelix/apace)

## Installation

Install and update using pip:

```sh
pip install -U apace
```

## Requirements

- Python 3.6 or higher (CPython or PyPy)
- CFFI 1.0.0 or higher
- NumPy/SciPy
- Matplotlib
- C Compiler

## Links

- Documentation: [https://apace.readthedocs.io](https://apace.readthedocs.io)
- API Reference: [https://apace.readthedocs.io/en/stable/reference/apace/index.html](https://apace.readthedocs.io/en/stable/reference/apace/index.html)
- Examples: [https://apace.readthedocs.io/en/stable/examples/index.html](https://apace.readthedocs.io/en/stable/examples/index.html)
- Releases: [https://pypi.org/project/apace/](https://pypi.org/project/apace/)
- Code: [https://github.com/andreasfelix/apace](https://github.com/andreasfelix/apace)
- Issue tracker: [https://github.com/andreasfelix/apace/issues](https://github.com/andreasfelix/apace/issues)

## License

[GNU General Public License v3.0](https://github.com/andreasfelix/apace/blob/main/LICENSE)

# Code to Reproduce the Q5T2off Optics {#sec:code-to-reproduce-q5t2off-optics}

The following code snippets reproduce the Q5T2off optics presented in @sec:optimizing-the-q5t2off-optics. 

```python
import apace as ap
import numpy as np
from scipy import optimize

bessy2 = ap.Lattice.from_file("bessy2_stduser_2019_05_07.json")
twiss = ap.Twiss(bessy2, steps_per_meter=4)
t2_center = np.searchsorted(twiss.s, 45)
beta_ref_x = twiss.beta_x.copy()
beta_ref_y = twiss.beta_y.copy()
```
First, the `apace`, `numpy` and, `scipy.optimize` libraries are imported. Then, a new `Lattice` and `Twiss` object for the current BESSY II standard user optics is created. The `np.searchsorted` is used to obtain the index of the center of the T2 section, located at 45 meters. Finally, the current horizontal and vertical beta functions are copied to be later used as reference values:


```python
t1 = ["Q3P1T1", "Q3P2T1", "Q4P1T1", "Q4P2T1", "Q5P1T1", "Q5P2T1"]
d2 = ["Q3D2", "Q4D2"]
t2 = ["Q3T2", "Q4T2"]
d3 = ["Q3D3", "Q4D3"]
t3 = ["Q3T3", "Q4T3", "Q5T3"]
q5t2 = bessy2["Q5T2"]
quads_turnoff = [bessy2[name] for name in t2]
quads_optimize = [bessy2[name] for name in t1 + d2 + t2 + d3 + t3]
```

The optimization procedure consists of two parts, which use two different sets of quadrupoles defined in this snippet. The first part uses the `quads_turnoff` quadrupoles, corresponding to the quadrupoles in the T2 section. Here, each iteration lowers the value of the Q5T2 quadrupole step by step, while the optimizer tries to compensate the turn-off using the `quads_turnoff` quadrupoles. Then, in the next step, the optimizer tries to optimize the Twiss parameter for similarity with the reference optics. It uses the `quad_optimize` quadrupoles, corresponding to all quadrupoles from the T1 section to the T3 section.


```python
def objective_function(values, quads):
    for quad, value in zip(quads, values):
        quad.k1 = value

    if not twiss.stable:
        return np.inf

    beta_beat_x = np.maximum(1, twiss.beta_x / beta_ref_x) ** 2
    beta_beat_y = np.maximum(1, twiss.beta_y / beta_ref_y) ** 2
    beat_mean = np.trapz(beta_beat_x + beta_beat_y, x=twiss.s) / bessy2.length
    return beat_mean + max(twiss.beta_y[t2_center], 1.6)
```

The snippet above corresponds to the objective function defined in @eq:objectiv-function. The values of `twiss.beta_x` are not equidistant but depend on how long a given element is and how often it is sliced. Integrating the beta beat using the trapezoidal rule `np.trapz` takes the correct weighting factor into account. The `max(twiss.beta_y[t2_center], 1.6)` is used to incentivize a small vertical beta function in the center of the T2 section $\beta_\mathrm{y}(s_\mathrm{T2})$, but it is capped at 1.6 m as these should be enough to fulfill the requirements stated in @sec:q5t2off-constraints.

```python
def run(quads):
    result = optimize.minimize(
        objective_function,
        np.array([x.k1 for x in quads]),
        args=quads,
        method="Nelder-Mead",
    )
    print(f"k1: {q5t2.k1:+.3f}, objective: {result.fun:+.3f}")
    if not twiss.stable:
        raise Exception("Result must be stable!")
```

This snippet defines a run function, which takes one parameter, `quads`. That is the list of quadrupoles used for the optimization. If the Twiss parameters are not stable, the program stops with an error message.


```python
for q5t2.k1 in np.linspace(q5t2.k1, 0, 10):
    run(quads_turnoff)

for _ in range(5):
    run(quads_optimize)

bessy2.as_file("bessy2_q5t2off.json")
```

In the last snippet, the optimization is executed. First, optimization is run using the quadrupoles `quads_turnoff`. For each iteration, the `k1` value of `q5t2` quadrupole is lowered until it reaches zero. In the second loop, the obtained optics is optimized using all quadrupoles. Finally, the optimized Q5T2off optics is saved to disk.

# GUI to Calculate and Set new Power Supply Values {#sec:gui-power-supply-values}

![Screenshot of a simple application to calculate and set new power supply values](figures/gui-power-supply-values.png){#fig:gui-power-supply-values}

Transfering a new quadrupole setting to the machine by manually entering individual power supply values into the control system can be cumbersome and error-prone. Therefore, a simple application with a graphic user interface (GUI) was developed to automate this process. It is written in Python and uses the EPICS interface to interact with the machine. @fig:gui-power-supply-values shows a screenshot of the application. The application is visually split into three parts:

The first two buttons in the upper part load the quadrupole values of the *new lattice* and *reference lattice*. The files must be in the LatticeJSON format. The third button loads the power supply values of the *reference lattice*.

Below, a table shows the reference, current and, new power supply values. The new power supply values

$$ I_\mathrm{new} = \frac{k_\mathrm{new}}{k_\mathrm{old}} I_\mathrm{old} $$

are calculated by the ratio of the new and old quadruple strength times the old power supply values.

The bottom frame contains multiple buttons: The first button stores all quadrupoles' current power supply values to a JSON file. During the LOCO measurement, that should be done to make sure the quadrupole values correspond to the power supply value. The second button computes the new power supply values. The multi-knob-toggle in the middle allows interpolating between two lattices. The user can choose a second lattice file and use a slider to interpolate between the quadrupole values of these two lattices. Finally, the three buttons in the right corner can set the new power supply values or set and restore the current quadrupole setting.

# Transfer Matrices {#sec:appendix-transfer-matrices}

Solving @eq:eom-linearized yields the matrix entries for the transversal offset $u(s)$ and slope $u'(s)$.

Two effects influence the longitudinal offset $l(s)$: First, the path length within an element can vary from the path length of the ideal orbit. Following from @eq:path-length-difference, in linear approximation the total path length within an element of the length $L$ is given by:

$$ Z = \int_{0}^{L} (1 + \kappa_\mathrm{x0}(s) x)\mathrm{d} s
$$ {#eq:total-path-length}

Secondly, the time scales linearly with the relative velocity error $\frac{\Delta v}{v_0}$. Using an approximation from relativistic kinematics 

$$
\frac{\mathrm{d} p}{\mathrm{d} v} = m_0 \gamma + m_0 \frac{v^2}{c^2} \gamma^3 = m_0 \gamma^3 (\frac{1}{\gamma^2} + \frac{v^2}{c^2}) \approx m_0 \gamma^3 = \frac{p}{v} \gamma^2,
$${#eq:relativistic-kinematic-seq}

we can combine both effects and obtain an expression for the longitudinal offset

$$
\begin{aligned}
l(s + L) & = l(s) -(Z-L) + L\frac{\Delta v}{v_0} \\
& \approx l(s) - \int_{s}^{s + L} \kappa_\mathrm{x0}(s') x \mathrm{d} s' + \frac{L}{\gamma^2} \delta_0 .
\end{aligned}
$$ {#eq:logitudinal-offset}

Assuming no radiation, the relative momentum deviation

$$
\begin{aligned}
\delta(s)  = \delta(0) = \delta_0
\end{aligned}
$$ {#eq:momentum-change}

stays constant, resulting in only one nonzero entry in the bottom row of the transfer matrices.

## Drift Space

In a drift space of the length $L$, where $\kappa_\mathrm{x0} = k = 0$, @eq:eom-linearized simplifies to:

$$
\begin{aligned}
x'' &= 0 \\
y'' &= 0
\end{aligned}
$$ {#eq:eom-linearized-drift}

The longitudinal offset $l(s)$ simplifies to:

$$ l(s + L) = l(s) + \frac{L}{\gamma^2} \delta_0
$$ {#eq:logitudinal-offset-drift}

Thus, the transfer matrix of a drift space is:

$$
\textbf{R}_\mathrm{drift} =
\begin{pmatrix}
1 & L & 0 & 0 & 0 & 0          \\
0 & 1 & 0 & 0 & 0 & 0          \\
0 & 0 & 1 & L & 0 & 0          \\
0 & 0 & 0 & 1 & 0 & 0          \\
0 & 0 & 0 & 0 & 1 & L/\gamma^2 \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix}
$$ {#eq:transfer-matrix-drift}

## Dipole Magnet

In a dipole magnet of the length $L$, where $\kappa_\mathrm{x0} \neq 0$ and $k = 0$, @eq:eom-linearized simplifies to

$$
\begin{aligned}
x'' + \kappa_\mathrm{x0}^2 x &= \kappa_\mathrm{x0} \delta \\
y'' &= 0 ,
\end{aligned}
$$ {#eq:eom-linearized-dipole}

which is an inhomogeneous second-order differential equation. The transfer matrix for a bending magnet, solving @eq:eom-linearized-dipole, is

$$
\textbf{R}_\mathrm{b} =
\begin{pmatrix}
c & \frac{s}{\kappa_\mathrm{x0}} & 0 & 0 & 0 & \frac{1-c}{\kappa_\mathrm{x0}} \\
- \kappa_\mathrm{x0} s & c & 0 & 0 & 0 & s \\
0 & 0 & 1 & L & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 \\
-s & \frac{c - 1}{\kappa_\mathrm{x0}} & 0 & 0 & 1 & \frac{L}{\gamma^2} - \frac{\varphi_0 - s}{\kappa_\mathrm{x0}} \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix} ,
$$ {#eq:transfer-matrix-dipole}

where $\varphi_0 = L \kappa_\mathrm{x0}$, $s = \sin{\varphi_0}$, and $c = \cos{\varphi_0}$. The expression above corresponds to a sector magnet, where the entrance and exit angles are zero. The entrance and exit angles $\alpha$, introduced by a rectangular dipole magnet, lead to an effect known as *edge focusing* and can be described by the matrix

$$
\textbf{R}_\mathrm{e} =
\begin{pmatrix}
1 & 0 & 0 & 0 & 0 & 0 \\
\kappa_\mathrm{x0} \tan{\alpha} & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 & 0 & 0 \\
0 & 0 & -\kappa_\mathrm{x0} \tan{\alpha} & 1 & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix} .
$$ {#eq:transfer-matrix-edge}

Consequently, the transfer matrix for a rectangular dipole magnet is

$$ \textbf{R}_\mathrm{b,r} = \textbf{R}_\mathrm{e} \textbf{R}_\mathrm{b} \textbf{R}_\mathrm{e} .
$$ {#eq:transfer-matrix-dipole-rectangular}


## Quadrupole Magnet

In a quadrupole magnet of the length $L$, where $\kappa_\mathrm{x0} = 0$ and $k \neq 0$, @eq:eom-linearized simplifies to:

$$
\begin{aligned}
x'' + k x &= 0\\
y'' - k y &= 0
\end{aligned}
$$ {#eq:eom-linearized-quadrupole}

The longitudinal offset $l(s)$ changes identical as in the drift space, leading to the transfer matrices for a horizontal focusing quadrupole

$$
\textbf{R}_{\textup{q,h}} =
\begin{pmatrix}
c & s/\sqrt{k} & 0 & 0 & 0 & 0 \\
-s\sqrt{k} & c & 0 & 0 & 0 & 0 \\
0 & 0 & ch & sh/\sqrt{k} & 0 & 0 \\
0 & 0 & sh\sqrt{k} & ch & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & L/\gamma^2 \\
0 & 0 & 0 & 0 & 0 & 1 \\
\end{pmatrix}
$${#eq:transfer-matrix-quadrupole-horizontal}

and for the vertical focusing quadrupole

$$
\textbf{R}_{\textup{q,v}} =
\begin{pmatrix}
ch & sh/\sqrt{k} & 0 & 0 & 0 & 0 \\
sh\sqrt{k} & ch & 0 & 0 & 0 & 0 \\
0 & 0 & c & s/\sqrt{k} & 0 & 0 \\
0 & 0 & -s\sqrt{k} & c & 0 & 0 \\
0 & 0 & 0 & 0 & 1 & L/\gamma^2 \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix} ,
$$ {#eq:transfer-matrix-quadrupole-vertical}

where $s = \sin{\sqrt{k}L}$, $c = \cos{\sqrt{k}L}$, $sh = \sinh{\sqrt{k}L}$, and $ch = \cosh{\sqrt{k}L}$.

# Grammar Files of Common Lattice File Formats

The grammar files are given in the Lark grammar language, which is based on the Extended Backus–Naur Form.

## Elegant Grammar File {#sec:elegant-grammar}

This grammar is not 100% consistent with elegants parser:

* Elegant's parser allows tokens to be split by the line continuation character "&". For example, it parses ANGLE=0.123&\n456 without an error. However, this is non-trivial to express with grammar rules and is therefore omitted.
* Elegant's parser allows a trailing " in attribute definitions. This means L=1.23" is parsed without an error. It seems like a bug and is left out.
* Elegant's parser allows unlimited trailing ",", which also seems like a bug.

```txt
%ignore /!.*/            // ignore comments
%ignore /[ \t\f]/+       // ignore whitespace
%ignore /&[ \t\f]*\r?\n/ // line continuation
%import common (SIGNED_INT, SIGNED_FLOAT, SIGNED_NUMBER, ESCAPED_STRING, CNAME)

int         : SIGNED_INT
float       : SIGNED_FLOAT
string      : ESCAPED_STRING
word        : /\w+/
name        : /\w+/ | "\"" /[\w:]+/ "\""
start        : _NEWLINE* (statement _NEWLINE+)*
_NEWLINE    : /[ \t\f]*\r?\n[ \t\f]*/
?statement  : element | lattice | command | "%" assignment
element     : name ":" [name] ("," attribute)* ","?
attribute   : word "=" (int | float | string | word)
lattice     : name ":" "LINE"i "=" arrangement
arrangement : [int "*"] [/-/] "(" object (","+ object)* ")"
?object     : ref_name | arrangement
ref_name    : [int "*"] [/-/] ["\""] /[\w:]+/ ["\""]
command     : name ["," word]
```

Elegant used the so called reverse polish notation (RPN) for its arithmetic expressions. As there is no syntactic distinction between an escaped string and a variable, it is possible that a collision can happen. In this case a variable is wrongly identified as string.

```txt
assignment  : expr "sto" CNAME
?expr       : SIGNED_NUMBER -> number
            | CNAME         -> variable
            | function
            | binary
!function   : expr ("exp" | "sin" | "cos" | "tan" | "asin" | "acos" | "atan")
?binary     : expr expr "+" -> add
            | expr expr "-" -> sub
            | expr expr "*" -> mul
            | expr expr "/" -> div
?start_rpn  : assignment | expr // used to tested the rpn parser
```

## MAD-X Grammar File {#sec:madx-grammar}

The following grammar is only a subset of MAD-X grammar, but it is sufficient to parse basic MAD-X lattice files.

```txt
%ignore /\s+/  // whitespace
%ignore "&" // backwards compatiable line continuation
%ignore /(!|\/\/).*/  // single line comments
%ignore /\/\*(\*(?!\/)|[^*])*\*\//  // multiline comment
%import common (SIGNED_INT, NUMBER, ESCAPED_STRING)

int         : SIGNED_INT
string      : ESCAPED_STRING
word        : /[\w\.]+/
start       : (_statement ";")*
_statement  : element | lattice | command | assignment
element     : word ":" [word] ("," attribute)* ","?
attribute   : word ("=" | ":=") (expr | string)
lattice     : word ":" "LINE"i "=" arrangement
arrangement : [int "*"] [/-/] "(" object ("," object)* ")"
?object     : ref_name | arrangement
ref_name    : [int "*"] [/-/] word
command     : word ("," (word | string | attribute))*
```

As there is no syntactic distinction between a non-escaped word and a variable, we must parse words as variables and test afterward if it is a variable or not.

```txt
assignment  : word ("=" | ":=") expr        -> assignment
?expr       : item
            | "{" expr ("," expr)* ","? "}" -> array
?item       : term
            | expr "+" term                 -> add
            | expr "-" term                 -> sub
?term       : factor
            | term "*" factor               -> mul
            | term "/" factor               -> div
?factor     : power
            | "+" factor                    -> identity
            | "-" factor                    -> neg
?power      : atom
            | power ("^" | "**") power      -> pow
?atom       : NUMBER                        -> number
            | word                          -> variable // see 1.
            | word "(" expr ")"             -> function
            | "(" expr ")"
?start_artih : assignment | expr  // used to tested the arithmetic parser
```

# Documentation {#sec:appendix-documentation}

The documentation is available as a Web version

> [https://apace.readthedocs.io](https://apace.readthedocs.io/) 

or as PDF

> [https://apace.readthedocs.io/_/downloads/en/latest/pdf/](https://apace.readthedocs.io/_/downloads/en/latest/pdf/).

# Bibliography {.unnumbered}
