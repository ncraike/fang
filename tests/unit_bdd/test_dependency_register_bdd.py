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

@pytest.fixture()
def code_under_test():
    return {
            'to_call': None,
            'args': [],
            'kwargs': {},
            }

@pytest.fixture()
def mock_DependencyRegister_instance():
    mock_DependencyRegister_instance = unittest.mock.NonCallableMock(
            spec=DependencyRegister())
    mock_DependencyRegister_instance.dependents = {}
    mock_DependencyRegister_instance.resources = {}
    return mock_DependencyRegister_instance

@pytest.fixture()
def fake_resource_name():
    return 'fake resource name'

@pytest.fixture()
def fake_dependent():
    return 'fake dependent'

@given(parsers.parse("I am testing the {method_name} method of DependencyRegister"))
def given_the_method_under_test(
        method_name, code_under_test, mock_DependencyRegister_instance):

    code_under_test['to_call'] = getattr(DependencyRegister, method_name)
    code_under_test['args'].append(mock_DependencyRegister_instance)

@given('I have a fake dependent')
def given_a_fake_dependent(code_under_test, fake_dependent):
    code_under_test['args'].append(fake_dependent)

@given('I have a fake resource name')
def given_a_fake_resource_name(code_under_test, fake_resource_name):
    code_under_test['args'].append(fake_resource_name)

@when('I call the method')
def call_the_method(code_under_test):
    to_call, args, kwargs = (
            code_under_test['to_call'],
            code_under_test['args'],
            code_under_test['kwargs'])

    to_call(*args, **kwargs)

@then('the method call should succeed')
@then('it should succeed')
def should_succeed():
    pass
