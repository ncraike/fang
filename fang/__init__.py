'''
'''

import inspect

try:
    import click
except ImportError:
    click = None

class DIError(Exception): pass

class DependencyRegister:
    def __init__(self):
        # Maps dependents to names of resources they require
        self.dependents = {}
        # Maps names of resources to their dependents
        self.resources = {}

    @classmethod
    def _unwrap_func(cls, decorated_func):
        '''
        This unwraps a decorated func, returning the inner wrapped func.

        This may become unnecessary with Python 3.4's inspect.unwrap().
        '''
        if click is not None:
            # Workaround for click.command() decorator not setting
            # __wrapped__
            if isinstance(decorated_func, click.Command):
                return cls._unwrap_func(decorated_func.callback)

        elif hasattr(decorated_func, '__wrapped__'):
            # Recursion: unwrap more if needed
            return self._unwrap_func(decorated_func.__wrapped__)
        else:
            # decorated_func isn't actually decorated, no more
            # unwrapping to do
            return decorated_func

    @classmethod
    def _unwrap_dependent(cls, dependent):
        # Dependent is effectively a class. Classes are registered as is.
        if inspect.isclass(dependent):
            return dependent
        # dependent is some other kind of callable, eg a function
        else:
            return cls._unwrap_func(dependent)

    def _register_dependent(self, dependent, resource_name):
        if dependent not in self.dependents:
            self.dependents[dependent] = []
        self.dependents[dependent].insert(0, resource_name)

    def _register_resource_dependency(self, resource_name, dependent):
        if resource_name not in self.resources:
            self.resources[resource_name] = set()
        self.resources[resource_name].add(dependent)
        
    def register(self, dependent, resource_name):
        dependent = self._unwrap_dependent(dependent)
        self._register_dependent(dependent, resource_name)
        self._register_resource_dependency(resource_name, dependent)

    def register_by_decorator(self, resource_name):
        def decorator(dependent):
            self.register(dependent, resource_name)
            return dependent
        return decorator

    def query_resources(self, dependent):
        dependent = self._unwrap_dependent(dependent)

        if dependent not in self.dependents:
            raise DependentNotFoundError(dependent=dependent)

        return self.dependents[dependent]

class DependentNotFoundError(DIError):

    def __init__(self, dependent=None):
        self.dependent = dependent
        if dependent:
            message = (
                    "Couldn't find dependencies registered for {!r}"
                    "".format(dependent))
        else:
            message = (
                    "Couldn't find dependencies registered for the given "
                    "dependent")
        super().__init__(message)

class ResourceProviderRegister:
    def __init__(self):
        # Maps resource names to a provider
        self.resource_providers = {}

    def register_callable(self, provider, resource_name):
        if resource_name in self.resource_providers:
            raise ProviderAlreadyRegisteredError(
                    resource_name=resource_name,
                    existing_provider=self.resource_providers[resource_name])

        self.resource_providers[resource_name] = provider

    # For registering providers which always return the same instance
    def register_instance(self, provider, resource_name):
        self.register_callable(lambda : provider, resource_name)

    def resolve(self, resource_name):
        if resource_name not in self.resource_providers:
            raise ProviderNotFoundError(resource_name=resource_name)

        return self.resource_providers[resource_name]()

class ProviderAlreadyRegisteredError(DIError):

    def __init__(self, resource_name=None, existing_provider=None):
        self.resource_name = resource_name
        self.existing_provider = existing_provider
        if resource_name and existing_provider:
            message = (
                    'A provider ({provider!r}) has already been '
                    'registered for resource {resource_name!r}'.format(
                        provider=existing_provider,
                        resource_name=resource_name))
        else:
            message = (
                    'A provider has already been registered for the '
                    'resource')
        super().__init__(message)

class ProviderNotFoundError(DIError):

    def __init__(self, resource_name=None):
        self.resource_name = resource_name
        if resource_name:
            message = (
                    "A provider could not be found for resource {!r}"
                    "".format(resource_name))
        else:
            message = (
                    "A provider could not be found for the requested "
                    "resource")
        super().__init__(message)


# This is effectively what is sometimes termed a "dependency injection
# container".
class DependencyResolver:

    def __init__(
            self,
            dependency_register=None,
            resource_provider_register=None):
        self.dependency_register = dependency_register
        self.resource_provider_register = resource_provider_register

        # Methods delegated to other objects
        self.query_dependents_resources = \
                self.dependency_register.query_resources
        self.resolve = self.resource_provider_register.resolve

    def resolve_all_dependencies(self, dependent):
        return [
                self.resolve(resource_name)
                for resource_name in
                self.query_dependents_resources(dependent)]

    def unpack(self, dependent):
        resources = self.resolve_all_dependencies(dependent)

        # Never return a length-1 list/tuple, to allow easier unpacking
        # eg, avoid need for comma in:
        #   my_one_dep, = my_resolver.unpack_dependencies(my_func)
        if len(resources) == 1:
            return resources[0]
        else:
            return resources

class Di:
    
    def __init__(self, namespace=None):
        self.namespace = namespace
        self.dependencies = DependencyRegister()
        self.providers = ResourceProviderRegister()
        self.resolver = DependencyResolver(
                dependency_register=dependencies,
                resource_provider_register=providers)

        # For use as a decorator
        self.dependsOn = dependencies.register_by_decorator
