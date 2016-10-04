
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
