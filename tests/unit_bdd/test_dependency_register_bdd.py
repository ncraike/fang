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

@given(parsers.parse(
    "I am testing the {method_name} method of DependencyRegister"))
def given_the_method_under_test(
        method_name, call_under_test, mock_DependencyRegister_instance):

    call_under_test['callable'] = getattr(DependencyRegister, method_name)
    call_under_test['args'].append(mock_DependencyRegister_instance)

ARG_LINES = {
        'a fake dependent': 'fake_dependent',
        'a fake dependent not in dependents':
            'fake_dependent_not_in_dependents',
        'a fake resource name': 'fake_resource_name',
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

@then('the method call should succeed')
@then('it should succeed')
def should_succeed():
    pass

@then('the fake dependent should be in dependents')
def fake_dependent_should_be_in_dependents(
        fake_dependent, mock_DependencyRegister_instance):
    assert fake_dependent in mock_DependencyRegister_instance.dependents
