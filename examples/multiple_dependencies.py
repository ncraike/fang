#!/bin/python
'''
This example is used in README.rst to demonstrate how a function
specifies multiple dependencies.
'''

import fang

di = fang.Di(namespace='.com.example.myproject')

@di.dependsOn('multiplier')
@di.dependsOn('offset')
def multiply_and_add(n):
    '''Multiply the given number n by some configured multiplier, and
    then add a configured offset.'''
    multiplier, offset = di.resolver.unpack(multiply_and_add)
    return (multiplier * n) + offset

providers = fang.ResourceProviderRegister(namespace='.com.example.myproject')

@providers.register('multiplier')
def give_multiplier():
    '''Give a multiplier of 2.'''
    return 2

@providers.register('offset')
def give_offset():
    '''Give an offset value of 3.'''
    return 3

def main():
    # Here at our program entry-point, we configure what set of providers
    # will be used to meet our dependencies
    di.providers.load(providers)
    # Prints 13
    print(multiply_and_add(5))

if __name__ == '__main__':
    main()
