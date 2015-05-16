#!/bin/python

import fang

di = fang.Di(namespace='.com.example.myproject')

@di.dependsOn('multiplier')
def give_result(n):
    '''Multiply the given n by some configured multiplier.'''
    multiplier = di.resolver.unpack(give_result)
    return multiplier * n

providers = fang.ResourceProviderRegister(namespace='.com.example.myproject')

@providers.register('multiplier')
def give_multiplier():
    '''Give a multiplier of 2.'''
    return 2

def main():
    # Here at our program entry-point, we confgure what set of providers
    # will be used to meet our dependencies
    di.providers.load(providers)
    # Prints 10
    print(give_result(5))

if __name__ == '__main__':
    main()
