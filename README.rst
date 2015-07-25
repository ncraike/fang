Fang: Dependency injection for Python
=====================================

Fang is a dependency injection library for Python.

Dependency injection (DI) is uncommon in Python. It's usually written off as a tool for other languages – languages with static typing, strict interfaces, etc – which is unneeded in Python.

But, dependency injection can actually give plenty of benefits even for Python programs. Among them:

 - much easier unit testing, without complex "mocking out" of names and modules.
 - more maintainable code from deliberate isolation of functions and modules.
 - clearer code with explicit declaration of dependencies.

Why isn't dependency injection used in Python?

Well, dependency injection in other languages is usually quite complex. DI frameworks often use their own configuration language (often written in XML), mandate strict interfaces, use factory classes, and so on. There are a lot of pieces, and few of them fit into Python's existing ecosystem and programming style.

Fang aims to change that. Fang adds dependency injection, but in a Pythonic way, while still maintaining the benefits. Particularly, in Fang:

 - dependencies are specified just by identifier strings, not with interface classes.
 - the constructs which meet dependencies (resource providers) are *just functions*, not factory classes.
 - the dependencies which a piece of code needs and the dependencies it can provide are both declared concisely with decorators.
 - the linking of dependents and resource providers is done at run-time *in Python*, not with a custom-built configuration language.

The pieces used are small and easy to understand: the total library is less than 300 lines. But it's clear and simple enough to serve as a foundation for other features (eg dependency graphs, interface verification), which can be enabled or added on a per-project basis.


Examples
--------
Here's a simple (if contrived) example of a short program which multiplies two numbers. One of the numbers is given as a parameter to a function call. The other number is configured via dependency injection:

.. code-block:: python

    import fang

    di = fang.Di(namespace='.com.example.myproject')

    @di.dependsOn('multiplier')
    def multiply(n):
        '''Multiply the given number n by some configured multiplier.'''
        multiplier = di.resolver.unpack(multiply)
        return multiplier * n

    providers = fang.ResourceProviderRegister(namespace='.com.example.myproject')

    @providers.register('multiplier')
    def give_multiplier():
        '''Give a multiplier of 2.'''
        return 2

    def main():
        # Here at our program entry-point, we configure what set of providers
        # will be used to meet our dependencies
        di.providers.load(providers)
        # Prints 10
        print(multiply(5))

    if __name__ == '__main__':
        main()
