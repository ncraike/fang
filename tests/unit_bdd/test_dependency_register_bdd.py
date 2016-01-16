
import unittest.mock
import functools
from types import ModuleType

import pytest
from pytest_bdd import scenario, scenarios, given, when, then, parsers

from common.bdd.argument_system import argument_line

#
# Module under test:
#
from fang.dependency_register import DependencyRegister

#
# Load our test scenarios
#
scenarios('features/dependency_register/')

@pytest.fixture
def mock_DependencyRegister_instance():
    mock_DependencyRegister_instance = unittest.mock.NonCallableMock(
            spec=DependencyRegister())
    mock_DependencyRegister_instance.dependents = {}
    mock_DependencyRegister_instance.resources = {}
    return mock_DependencyRegister_instance

@pytest.fixture
def mock_DependencyRegister_class():
    return unittest.mock.Mock(
            spec=DependencyRegister)

@argument_line('a dependent not in dependents')
@pytest.fixture
def fake_dependent_not_in_dependents(pytest_request, **kwargs):
    fake_dependent, mock_DependencyRegister_instance = (
        pytest_request.getfuncargvalue('fake_dependent'),
        pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_dependent is not in instance.dependents
    mock_DependencyRegister_instance.dependents.pop(fake_dependent, None)
    return fake_dependent

@argument_line('a dependent in dependents')
@pytest.fixture
def fake_dependent_in_dependents(pytest_request, **kwargs):
    fake_dependent, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('fake_dependent'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_dependent is in instance.dependents
    mock_DependencyRegister_instance.dependents[fake_dependent] = []
    return fake_dependent

@argument_line('a resource name not in resources')
def fake_resource_name_not_in_resources(pytest_request, **kwargs):
    call_under_test, fake_resource_name, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('call_under_test'),
            pytest_request.getfuncargvalue('fake_resource_name'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_resource_name is not in instance.resources
    mock_DependencyRegister_instance.resources.pop(fake_resource_name, None)
    return fake_resource_name

@argument_line('a resource name in resources')
def fake_resource_name_in_resources(pytest_request, **kwargs):
    call_under_test, fake_resource_name, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('call_under_test'),
            pytest_request.getfuncargvalue('fake_resource_name'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_resource_name is in instance.resources
    mock_DependencyRegister_instance.resources[fake_resource_name] = set()
    return fake_resource_name

@pytest.fixture
@argument_line('a None value')
def a_None_value(**kwargs):
    return None

def _undecorated_function(*args, **kwargs):
    return ('undecorated_function() return value', args, kwargs)

@argument_line('an undecorated function')
@argument_line('the undecorated function')
@pytest.fixture
def an_undecorated_function(pytest_request=None):
    return _undecorated_function

def decorator(f):
    @functools.wraps(f)
    def decorator_wrapper(*args, **kwargs):
        return (
                'decorator_wrapper() added this',
                f(*args, **kwargs))

    return decorator_wrapper

@argument_line('a decorated function')
@argument_line('the decorated function')
@pytest.fixture
def a_decorated_function(pytest_request=None):
    an_undecorated_function = pytest_request.getfuncargvalue(
            'an_undecorated_function')
    return decorator(an_undecorated_function)

@given("I have the click module imported")
def with_click_module_imported(request, fake_click_module):
    patcher = unittest.mock.patch(
            'fang.dependency_register.click', fake_click_module)
    patcher.start()
    request.addfinalizer(patcher.stop)

@then('it should succeed')
def should_succeed():
    pass

@then('the dependent should be in dependents')
def fake_dependent_should_be_in_dependents(
        fake_dependent, mock_DependencyRegister_instance):
    assert fake_dependent in mock_DependencyRegister_instance.dependents

@then('the resource name should be registered for the dependent')
def fake_resource_name_should_be_registered_for_dependent(
        fake_resource_name, fake_dependent, mock_DependencyRegister_instance):
    assert (fake_resource_name in
            mock_DependencyRegister_instance.dependents[fake_dependent])

@argument_line('a resource name in dependents')
def fake_resource_name_in_dependents(pytest_request, **kwargs):
    fake_dependent, fake_resource_name, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('fake_dependent'),
            pytest_request.getfuncargvalue('fake_resource_name'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_dependent is in instance.dependents
    mock_DependencyRegister_instance.dependents[fake_dependent] = [fake_resource_name]
    return fake_dependent

@then('the resource name should be in resources')
def fake_resource_name_should_be_in_resources(
        fake_resource_name, mock_DependencyRegister_instance):
    assert fake_resource_name in mock_DependencyRegister_instance.resources

@then('the dependent should be registered as needing the resource')
def fake_dependent_should_be_registered_as_needing_the_fake_resource(
        fake_resource_name, fake_dependent, mock_DependencyRegister_instance):
    assert (fake_dependent in
            mock_DependencyRegister_instance.resources[fake_resource_name])

