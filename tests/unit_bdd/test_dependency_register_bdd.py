from pytest_bdd import scenario, scenarios, given, when, then, parsers

import unittest.mock
import functools
from types import ModuleType

import pytest

#
# Module under test:
#
from fang.dependency_register import DependencyRegister

#
# Load our test scenarios
#
scenarios('features/dependency_register/')

@pytest.fixture
def world_state():
    return {
            'call_under_test': {
                'callable': None,
                'args': [],
                'kwargs': {},
                'callable_on_instance': None,
            },
    }

@pytest.fixture
def call_under_test(world_state):
    return world_state['call_under_test']

@pytest.fixture
def mock_DependencyRegister_instance():
    mock_DependencyRegister_instance = unittest.mock.NonCallableMock(
            spec=DependencyRegister())
    mock_DependencyRegister_instance.dependents = {}
    mock_DependencyRegister_instance.resources = {}
    return mock_DependencyRegister_instance

@pytest.fixture
def fake_resource_name():
    return 'fake resource name'

@pytest.fixture
def fake_dependent():
    return 'fake dependent'

@pytest.fixture
def fake_dependent_not_in_dependents(
        call_under_test, fake_dependent, mock_DependencyRegister_instance):
    # Ensure that fake_dependent is not in instance.dependents
    mock_DependencyRegister_instance.dependents.pop(fake_dependent, None)
    return fake_dependent

@pytest.fixture
def fake_dependent_in_dependents(
        call_under_test, fake_dependent, mock_DependencyRegister_instance):
    # Ensure that fake_dependent is in instance.dependents
    mock_DependencyRegister_instance.dependents[fake_dependent] = []
    return fake_dependent

@pytest.fixture
def fake_resource_name_not_in_resources(
        call_under_test, fake_resource_name, mock_DependencyRegister_instance):
    # Ensure that fake_resource_name is not in instance.resources
    mock_DependencyRegister_instance.resources.pop(fake_resource_name, None)
    return fake_resource_name

@pytest.fixture
def fake_resource_name_in_resources(
        call_under_test, fake_resource_name, mock_DependencyRegister_instance):
    # Ensure that fake_resource_name is in instance.resources
    mock_DependencyRegister_instance.resources[fake_resource_name] = set()
    return fake_resource_name

@pytest.fixture
def a_None_value():
    return None

@given(parsers.parse(
    "I am testing the {method_name} method of DependencyRegister"))
def given_the_method_under_test(
        method_name, call_under_test, mock_DependencyRegister_instance):

    call_under_test['callable'] = getattr(DependencyRegister, method_name)
    call_under_test['args'].append(mock_DependencyRegister_instance)
    call_under_test['callable_on_instance'] = getattr(
            mock_DependencyRegister_instance, method_name)

ARG_LINES = {
    'a fake dependent': 'fake_dependent',
    'a fake dependent not in dependents': 'fake_dependent_not_in_dependents',
    'a fake dependent in dependents': 'fake_dependent_in_dependents',
    'a fake resource name': 'fake_resource_name',
    'the fake resource name': 'fake_resource_name',
    'a fake resource name not in resources': 'fake_resource_name_not_in_resources',
    'a fake resource name in resources': 'fake_resource_name_in_resources',
    'a None value': 'a_None_value',
}

def resolve_arg_lines(lines, request):
    return [
            request.getfuncargvalue(ARG_LINES[line])
            for line in lines.splitlines()]

@when('I call the method')
@when(parsers.parse(
    'I call the method with:\n{arg_lines}'))
def call_the_method(call_under_test, request, arg_lines=''):
    to_call, args, kwargs = (
            call_under_test['callable'],
            call_under_test['args'],
            call_under_test['kwargs'])

    more_args = resolve_arg_lines(arg_lines, request)
    args.extend(more_args)

    result = to_call(*args, **kwargs)
    call_under_test['result'] = result

@then('it should succeed')
def should_succeed():
    pass

@then('the fake dependent should be in dependents')
def fake_dependent_should_be_in_dependents(
        fake_dependent, mock_DependencyRegister_instance):
    assert fake_dependent in mock_DependencyRegister_instance.dependents

@then('the fake resource name should be registered for the dependent')
def fake_resource_name_should_be_registered_for_dependent(
        fake_resource_name, fake_dependent, mock_DependencyRegister_instance):
    assert (fake_resource_name in
            mock_DependencyRegister_instance.dependents[fake_dependent])

@then('the fake resource name should be in resources')
def fake_resource_name_should_be_in_resources(
        fake_resource_name, mock_DependencyRegister_instance):
    assert fake_resource_name in mock_DependencyRegister_instance.resources

@then('the fake dependent should be registered as needing the fake resource')
def fake_dependent_should_be_registered_as_needing_the_fake_resource(
        fake_resource_name, fake_dependent, mock_DependencyRegister_instance):
    assert (fake_dependent in
            mock_DependencyRegister_instance.resources[fake_resource_name])

@then('the result should be a partial')
def result_should_be_a_partial(call_under_test):
    result = call_under_test['result']
    assert isinstance(result, functools.partial)

@then("the resulting partial's function should be the method")
def resulting_partials_func_should_be_a_method(call_under_test):
    result = call_under_test['result']
    # This is kind of weird, because we actually expect the method on
    # the mock instance, even though we called the method on the class
    assert result.func == call_under_test['callable_on_instance']

@then(parsers.parse("the resulting partial's arguments should be:\n{arg_lines}"))
def resulting_partials_func_should_be_a_method(arg_lines, call_under_test, request):
    result = call_under_test['result']
    expected_args = tuple(resolve_arg_lines(arg_lines, request))
    assert result.args == expected_args
