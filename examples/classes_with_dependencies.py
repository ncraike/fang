#!/bin/python
'''
This example is used in README.rst to demonstrate how a class
specifies dependencies.

Unlike the other examples, this file is intended to be read as a single
module within a larger (hypothetical) project.
'''

import fang
from myproject import di

providers = fang.ResourceProviderRegister(namespace='.com.example.myproject')

@di.dependsOn('config.region')
@di.dependsOn('auth.credentials')
@di.dependsOn('network.http')
class ApiAccess:

    def __init__(self):
        (self.region,
                self.credentials,
                self.http) = di.resolver.unpack(ApiAccess)

    def connect(self):
        self.connection = self.http.connect(region.url)
        # etc

providers.register('api_access', ApiAccess)
