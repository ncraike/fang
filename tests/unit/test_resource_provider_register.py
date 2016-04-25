
import functools
import unittest.mock
import pytest

# Class under test:
from fang.resource_provider_register import ResourceProviderRegister

@pytest.fixture()
def mock_instance():
    mock_instance = unittest.mock.NonCallableMock(
            spec=ResourceProviderRegister())
    mock_instance.dependents = {}
    mock_instance.resources = {}
    return mock_instance

@pytest.fixture()
def resource_name():
    return 'test.resource'

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

    def test__giving_no_provider_arg___should_return_partial(
            self, mock_instance, resource_name):
        '''
        If register() is called with resource_name but no provider,
        register() should return a partial of register() with the
        resource_name argument fixed.

        NOTE: In this test we call the method on the class, not an
        instance, so we can give a mock instance for self.
        '''
        result = ResourceProviderRegister.register(
                mock_instance, resource_name)

        assert isinstance(result, functools.partial)
        assert result.func == mock_instance.register
        assert result.args == (resource_name,)
