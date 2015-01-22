
class FangError(Exception): pass

class DependentNotFoundError(FangError):

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

class ProviderAlreadyRegisteredError(FangError):

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

class ProviderNotFoundError(FangError):

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

