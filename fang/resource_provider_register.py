
from functools import partial

from .errors import (
        FangError,
        ProviderAlreadyRegisteredError,
        ProviderNotFoundError)

class ResourceProviderRegister:
    def __init__(self, namespace=None):
        self.namespace = namespace
        # Maps resource names to a provider
        self.resource_providers = {}

    def register(self, resource_name, provider=None, allow_override=False):
        if provider is None:
            # Give a partial usable as a decorator
            return partial(
                    self.register,
                    resource_name, allow_override=allow_override)

        if ((not allow_override) and
                resource_name in self.resource_providers):
            raise ProviderAlreadyRegisteredError(
                    resource_name=resource_name,
                    existing_provider=self.resource_providers[resource_name])

        self.resource_providers[resource_name] = provider

        # Return provider to ease use as decorator
        return provider

    register_callable = register

    # For registering providers which always return the same instance
    def register_instance(self, resource_name, instance=None, **kwargs):
        if instance is None:
            # Give a partial usable as a decorator
            return partial(self.register_instance, resource_name, **kwargs)

        self.register(resource_name, provider=(lambda : instance), **kwargs)
        return instance

    def mass_register(self, resource_names_to_providers, **kwargs):
        for resource_name, provider in resource_names_to_providers.items():
            self.register_instance(resource_name, provider, **kwargs)

    def load(self, other_register, allow_overrides=False):
        if not allow_overrides:
            own_keys = self.resource_providers.keys()
            other_keys = other_register.resource_providers.keys()
            common_keys = own_keys & other_keys
            if common_keys:
                # TODO Add new FangError sub-class?
                raise FangError(
                        'This register already has providers for keys: '
                        '{!r}'.format(common_keys))

        self.resource_providers.update(
                other_register.resource_providers)

    def clear(self):
        self.resource_providers.clear()

    def resolve(self, resource_name):
        if resource_name not in self.resource_providers:
            raise ProviderNotFoundError(resource_name=resource_name)

        return self.resource_providers[resource_name]()

