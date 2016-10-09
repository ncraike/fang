
import functools
from unittest.mock import NonCallableMock

import pytest

from fang.dependency_register import DependencyRegister
from fang.resource_provider_register import ResourceProviderRegister

# Class under test:
from fang.resolver import DependencyResolver

@pytest.fixture()
def mock_instance():
    mock_instance = NonCallableMock(spec=DependencyResolver)
    mock_instance.dependency_register = NonCallableMock(
            spec=DependencyRegister())
    mock_instance.resource_provider_register = NonCallableMock(
            spec=ResourceProviderRegister())
    return mock_instance

@pytest.fixture()
def mock_DependencyRegister():
    mock = NonCallableMock(spec=DependencyRegister())
    mock.dependents = {}
    mock.resources = {}
    return mock

@pytest.fixture()
def mock_ResourceProviderRegister():
    mock = NonCallableMock(spec=ResourceProviderRegister())
    mock.namespace = None
    mock.resource_providers = {}
    return mock

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

class Test_DependencyResolver__construction:

    @pytest.mark.xfail(raises=AttributeError)
    def test__after_creation_with_no_args__dependency_register_should_be_None(self):
        '''
        This test fails due to [issue #12]
        (https://github.com/ncraike/fang/issues/12).

        The fix for #12 will likely change behaviour to require args to
        create a DependencyResolver instance, so this whole test will
        become invalid and be removed.

        For now, though, I'm keeping this test and marking it as an
        "expected failure", as a reminder that the bug needs fixing and
        this class has inconsistent, breaking behaviour.
        '''
        instance = DependencyResolver()
        assert instance.dependency_register is None

    def test__after_creation__dependency_register_should_be_init(
            self, mock_DependencyRegister, mock_ResourceProviderRegister):
        instance = DependencyResolver(
                mock_DependencyRegister, mock_ResourceProviderRegister)

        assert instance.dependency_register is mock_DependencyRegister

    def test__after_creation__resource_provider_register_should_be_init(
            self, mock_DependencyRegister, mock_ResourceProviderRegister):
        instance = DependencyResolver(
                mock_DependencyRegister, mock_ResourceProviderRegister)

        assert instance.resource_provider_register is mock_ResourceProviderRegister

    def test__after_creation__query_dependents_resource_should_be_delegated(
            self, mock_DependencyRegister, mock_ResourceProviderRegister):
        instance = DependencyResolver(
                mock_DependencyRegister, mock_ResourceProviderRegister)

        assert instance.query_dependents_resources is mock_DependencyRegister.query_resources

    def test__after_creation__resolve_should_be_delegated(
            self, mock_DependencyRegister, mock_ResourceProviderRegister):
        instance = DependencyResolver(
                mock_DependencyRegister, mock_ResourceProviderRegister)

        assert instance.resolve is mock_ResourceProviderRegister.resolve
