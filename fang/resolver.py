
from .errors import ProviderNotFoundError

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

    def are_all_dependencies_met_for(self, dependent):
        for resource_name in self.query_dependents_resources(dependent):
            try:
                self.resolve(resource_name)
            except ProviderNotFoundError as e:
                # TODO: Add error logging here
                return False
        else:
            return True
