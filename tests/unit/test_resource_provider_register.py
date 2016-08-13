
import functools
import unittest.mock
import pytest

from fang.errors import ProviderAlreadyRegisteredError

# Class under test:
from fang.resource_provider_register import ResourceProviderRegister

@pytest.fixture()
def mock_instance():
    mock_instance = unittest.mock.NonCallableMock(
            spec=ResourceProviderRegister())
    mock_instance.namespace = None
    mock_instance.resource_providers = {}
    return mock_instance

@pytest.fixture()
def resource_name():
    return 'test.resource'

@pytest.fixture()
def resource():
    def fake_resource(x):
        return x
    return fake_resource

@pytest.fixture()
def resource_provider(resource):
    def fake_resource_provider():
        return resource
    return fake_resource_provider

def give_unexpected_calls(method_calls, expected_methods_names):
    '''

    TODO: Move this to a common test utils module.
    '''
    return [call for call in method_calls
            if call[0] not in expected_methods_names]

class Test_ResourceProviderRegister__construction:

    def test__after_creation__namespace_should_default_to_None(self):
        instance = ResourceProviderRegister()
        assert instance.namespace is None
    
    def test__after_creation_with_namespace__namespace_should_be_as_given(self):
        instance = ResourceProviderRegister('mynamespace')
        assert instance.namespace == 'mynamespace'
        
    def test__after_creation__resource_providers_should_be_empty(self):
        instance = ResourceProviderRegister()
        assert len(instance.resource_providers) == 0

    def test__after_creation_with_namespace__resource_providers_should_be_empty(self):
        instance = ResourceProviderRegister('mynamespace')
        assert len(instance.resource_providers) == 0

class Test_ResourceProviderRegister_clear:

    def test__with_empty_resource_providers__should_be_empty_after(self):
        instance = ResourceProviderRegister()
        instance.resource_providers = {}

        instance.clear()
        assert len(instance.resource_providers) == 0

    def test__with_resources_in_resource_providers__should_be_empty_after(self):
        instance = ResourceProviderRegister()
        instance.resource_providers = {
            'myresource': 'my value',
            'mycallable': lambda x: x,
        }

        instance.clear()
        assert len(instance.resource_providers) == 0

class Test_ResourceProviderRegister_register:
    '''
    Test the instance method ResourceProviderRegister.register().

    NOTE: In these tests we call the method on the class, not the
    instance, so we can give a mock instance in place of self. This
    lets us check if register() calls any other instance methods.
    '''

    def test__giving_no_provider__should_return_partial(
            self, mock_instance, resource_name):
        '''
        If register() is called with resource_name but no provider,
        register() should return a partial of register() with the
        resource_name argument fixed.

        '''
        result = ResourceProviderRegister.register(
                mock_instance, resource_name)

        assert isinstance(result, functools.partial)
        assert result.func == mock_instance.register
        assert result.args == (resource_name,)

    def test__giving_no_provider__should_not_call_any_other_methods(
            self, mock_instance, resource_name):
        '''
        If register() is called with resource_name but no provider,
        no other instance methods should be called.
        '''

        result = ResourceProviderRegister.register(
                mock_instance, resource_name)

        unexpected_calls = give_unexpected_calls(
                mock_instance.method_calls, [])

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'No method calls were expected'.format(
                unexpected_calls,
                mock_DependenyRegister_instance.method_calls))

    def test__giving_provider__should_register_under_name(
            self, mock_instance, resource_name, resource_provider):

        result = ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        assert mock_instance.resource_providers[resource_name] == resource_provider

    def test__giving_provider_already_registered__should_raise(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        with pytest.raises(ProviderAlreadyRegisteredError):
            ResourceProviderRegister.register(
                    mock_instance, resource_name, resource_provider)

    def test__giving_provider_already_registered_and_override_false__should_raise(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        with pytest.raises(ProviderAlreadyRegisteredError):
            ResourceProviderRegister.register(
                    mock_instance, resource_name, resource_provider,
                    allow_override=False)

    def test__giving_provider_already_registered_and_override_true__should_register(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider,
                allow_override=True)

        assert mock_instance.resource_providers[resource_name] == resource_provider
