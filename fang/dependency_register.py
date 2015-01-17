
from functools import partial
import inspect

from .errors import DependentNotFoundError

try:
    import click
except ImportError:
    click = None


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

        if hasattr(decorated_func, '__wrapped__'):
            # Recursion: unwrap more if needed
            return cls._unwrap_func(decorated_func.__wrapped__)
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
        
    def register(self, resource_name, dependent=None):
        if dependent is None:
            # Give a partial usable as a decorator
            return partial(self.register, resource_name)

        dependent = self._unwrap_dependent(dependent)
        self._register_dependent(dependent, resource_name)
        self._register_resource_dependency(resource_name, dependent)

        # Return dependent to ease use as decorator
        return dependent

    def query_resources(self, dependent):
        dependent = self._unwrap_dependent(dependent)

        if dependent not in self.dependents:
            raise DependentNotFoundError(dependent=dependent)

        return self.dependents[dependent]


