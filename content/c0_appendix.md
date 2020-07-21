# Appendix

## Developed Code {#sec:appendix-code}

The source code is available at: [https://github.com/andreasfelix/apace]([https://github.com/andreasfelix/apace])

**apace** is yet **a**nother **p**article **a**ccelerator **c**od**e** designed for the optimization of beam optics. It is available as Python package and aims to provide a convenient and straightforward API to make use of Python's numerous scientific libraries.

### Installing

Install and update using pip:

```sh
pip install -U apace
```

### Requirements

- Python 3.6 or higher (CPython or PyPy)
- CFFI 1.0.0 or higher
- NumPy/SciPy
- Matplotlib

### Quick Start

Write some `code` within normal `Text`.

```python
def foo(lala):
    x = 10
    y = x ** 2
    return y
```

Import apace:

```python
import apace as ap
```

Create a ring consisting out of 8 FODO cells:

```python
d1 = ap.Drift('D1', length=0.55)
b1 = ap.Dipole('B1', length=1.5, angle=0.392701, e1=0.1963505, e2=0.1963505)
q1 = ap.Quadrupole('Q1', length=0.2, k1=1.2)
q2 = ap.Quadrupole('Q2', length=0.4, k1=-1.2)
fodo_cell = ap.Lattice('FODO', [q1, d1, b1, d1, q2, d1, b1, d1, q1])
fodo_ring = ap.Lattice('RING', [fodo_cell] * 8)
```

Calculate the Twiss parameters:

```python
twiss = ap.Twiss(fodo_ring)
```

Plot horizontal and vertical beta functions using matplotlib:

```python
import matplotlib.pyplot as plt
plt.plot(twiss.s, twiss.beta_x, twiss.s, twiss.beta_y)
```

### Links

- Documentation: https://apace.readthedocs.io
- API Reference: https://apace.readthedocs.io/en/stable/reference/apace/index.html
- Examples: https://apace.readthedocs.io/en/docs/examples/index.html
- Releases: https://pypi.org/project/apace/
- Code: https://github.com/andreasfelix/apace
- Issue tracker: https://github.com/andreasfelix/apace/issues

### License

[GNU General Public License v3.0](https://github.com/andreasfelix/apace/blob/master/LICENSE)

## Grammar Files of Common Lattice File Formats

The grammar files are given in the Lark grammar language, which is based on the Extended Backus–Naur Form.

### Elegant Grammar File {#sec:elegant-grammar}

This grammer is not 100% consistent with elegants parser:

* Elegants parser allows tokens to be split by the line continuation character "&". For example, it parses ANGLE=0.123&\n456 without an error. This is non-trivial to express with grammar rules and is therefore omitted.
* Elegants parser allows a trailing " in attribute definitions. This means L=1.23" is parsed without an error. Seems like a bug and is left out.
* Elegants parser allows unlimited trailing ",", which also seems like a bug.

```txt
%ignore /!.*/            // ingore comments
%ignore /[ \t\f]/+       // ingore whitespace
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

#### RPN Expression

Elegant used the so called reverse polish notation (RPN) for its arithmetic expressions. As there is no syntactic distinction between an escaped string and a variable, it is possible that a collison can happen. In this case a variable is wrongly identified as string.

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

### MADX Grammar File {#sec:madx-grammar}

This is an restricted subset of MADX which should be sufficient to parse basic lattice files.

```txt
%ignore /\s+/  // whitespace
%ignore "&" // backwards compatiable line continuation
%ignore /(!|\/\/).*/  // single line comments
%ignore /\/\*(\*(?!\/)|[^*])*\*\//  // multiline commetn
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

### Arithmeitc Expressions

As there is no syntactic distinction between a non-escaped word and a variable, we must parse words as variables and test afterwards if it is a variable or not.

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
