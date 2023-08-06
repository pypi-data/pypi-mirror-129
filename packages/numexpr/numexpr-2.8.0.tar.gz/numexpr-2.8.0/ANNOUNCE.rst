========================
Announcing NumExpr 2.8.0
========================

Hi everyone, 

**Under development.**

Project documentation is available at:

http://numexpr.readthedocs.io/

Changes from 2.7.3 to 2.8.0
---------------------------

* Wheels for Python 3.10 are now provided.
* Support for Python 2.7 and 3.5 has been discontinued. 
* All residual support for Python 2.X syntax has been removed, and therefore 
  the setup build no longer makes calls to the `2to3` script. The `setup.py` 
  has been refactored to be more modern.
* The examples on how to link into Intel VML/MKL/oneAPI now use the dynamic 
  library.

What's Numexpr?
---------------

Numexpr is a fast numerical expression evaluator for NumPy.  With it,
expressions that operate on arrays (like "3*a+4*b") are accelerated
and use less memory than doing the same calculation in Python.

It has multi-threaded capabilities, as well as support for Intel's
MKL (Math Kernel Library), which allows an extremely fast evaluation
of transcendental functions (sin, cos, tan, exp, log...) while
squeezing the last drop of performance out of your multi-core
processors.  Look here for a some benchmarks of numexpr using MKL:

https://github.com/pydata/numexpr/wiki/NumexprMKL

Its only dependency is NumPy (MKL is optional), so it works well as an
easy-to-deploy, easy-to-use, computational engine for projects that
don't want to adopt other solutions requiring more heavy dependencies.

Where I can find Numexpr?
-------------------------

The project is hosted at GitHub in:

https://github.com/pydata/numexpr

You can get the packages from PyPI as well (but not for RC releases):

http://pypi.python.org/pypi/numexpr

Documentation is hosted at:

http://numexpr.readthedocs.io/en/latest/

Share your experience
---------------------

Let us know of any bugs, suggestions, gripes, kudos, etc. you may
have.

Enjoy data!
