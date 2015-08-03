Fang: Dependency injection for Python
=====================================

Fang is a dependency injection library for Python.

Fang adds dependency injection in Pythonic way, without requiring the elements more usually seen in "big OO" languages. Particularly:

- dependencies are specified by identifier strings, rather than strict interface classes or types.
- the constructs which meet dependencies (resource providers) are *just functions*, not factory classes.
- the dependencies which a piece of code needs and the dependencies it can provide are both declared concisely with decorators.
- the linking of dependents and resource providers is done at run-time *in Python*, not with a custom-built configuration language.

The pieces used are small and easy to understand: the total library is less than 300 lines. But it's clear and simple enough to serve as a foundation for other features (eg dependency graphs, interface verification), which can enabled or added on a per-project basis.
