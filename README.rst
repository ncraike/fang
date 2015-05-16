Fang: Dependency injection for Python
=====================================

Fang is a dependency injection library for Python.

Dependency injection (DI) is uncommon in Python. It's usually written off as a tool for other languages - languages with static typing, strict interfaces, etc - which is unneeded in Python.

But, dependency injection can actually give plenty of benefits even for Python programs. Among them:

 - much easier unit testing, without complex "mocking out" of names and modules.
 - more maintainable code from deliberate isolation of functions and modules.
 - clearer code with explicit declaration of dependencies.

Why isn't dependency injection used in Python? Well, dependency injection systems in other languages are usually quite complex, often using their own configuration language (often written in XML), strict interfaces, factory classes, etc. There are a lot of pieces, and few of them fit into Python's existing ecosystem and programming style.

Fang aims to change that. Fang adds dependency injection, but in a Pythonic way, while still maintaining the benefits. Particularly, in Fang:

 - dependencies are specified just by identifier strings, not with explicit interface definitions.
 - the constructs which meet dependencies (resource providers) are *just functions*, not factory classes.
 - the dependencies a piece of code needs and the dependencies it can provide are each declared concisely with decorators.
 - the linking of dependents and resource providers is done at run-time *in Python*, not with a custom-build configuration language.
 - the pieces are small and easy to understand, but more features (graphing dependencies, verifying interfaces) can be added on a per project basis.
