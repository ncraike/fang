#!/bin/python
'''
This example is used in README.rst as the first introduction to Fang.
'''

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
