
class FangError(Exception): pass

class DependentNotFoundError(FangError):

    def __init__(self, dependent=None):
        self.dependent = dependent
        if dependent:
            message = (
                    u"Couldn't find dependencies registered for {!r}"
                    u"".format(dependent))
        else:
            message = (
                    u"Couldn't find dependencies registered for the given "
                    u"dependent")
        super(DependentNotFoundError, self).__init__(message)

class ProviderAlreadyRegisteredError(FangError):

    def __init__(self, resource_name=None, existing_provider=None):
        self.resource_name = resource_name
        self.existing_provider = existing_provider
        if resource_name and existing_provider:
            message = (
                    u'A provider ({provider!r}) has already been '
                    u'registered for resource {resource_name!r}'.format(
                        provider=existing_provider,
                        resource_name=resource_name))
        else:
            message = (
                    u'A provider has already been registered for the '
                    u'resource')
        super(ProviderAlreadyRegisteredError, self).__init__(message)

class ProviderNotFoundError(FangError):

    def __init__(self, resource_name=None):
        self.resource_name = resource_name
        if resource_name:
            message = (
                    u"A provider could not be found for resource {!r}"
                    u"".format(resource_name))
        else:
            message = (
                    u"A provider could not be found for the requested "
                    u"resource")
        super(ProviderNotFoundError, self).__init__(message)

