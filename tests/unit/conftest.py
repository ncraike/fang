
import unittest.mock
import functools
from types import ModuleType

import pytest

# Module under test:
from fang.dependency_register import DependencyRegister

@pytest.fixture(scope='function')
def dep_reg():
    return DependencyRegister()

@pytest.fixture(scope='function')
def mock_dep_reg():
    mock_dep_reg = unittest.mock.NonCallableMock(
            spec=DependencyRegister())
    mock_dep_reg.dependents = {}
    mock_dep_reg.resources = {}
    return mock_dep_reg

@pytest.fixture(scope='function')
def mock_dep_reg_class():
    return unittest.mock.Mock(
            spec=DependencyRegister)

@pytest.fixture(scope='function')
def fake_resource_name():
    return 'fake resource name'

@pytest.fixture(scope='function')
def fake_dependent():
    return 'fake dependent'

@pytest.fixture(scope='function')
def undecorated_function():
    def undecorated_function(*args, **kwargs):
        return ('undecorated_function() return value', args, kwargs)

@pytest.fixture(scope='function')
def decorator():
    def decorator(f):
        @functools.wraps(f)
        def decorator_wrapper(*args, **kwargs):
            return (
                    'decorator_wrapper() added this',
                    f(*args, **kwargs))

        return decorator_wrapper

    return decorator

@pytest.fixture(scope='function')
def fake_dependent_which_is_a_class():
    class FakeDependentWhichIsAClass:
        pass
    return FakeDependentWhichIsAClass

@pytest.fixture(scope='function')
def fake_click_Command_class():
    class Command:
        '''A fake click.Command class which just implements behaviour we
        need for tests.'''

        def __init__(self, function_to_wrap):
            self.callback = function_to_wrap

    return Command

@pytest.fixture(scope='function')
def fake_click_module(fake_click_Command_class):
    click = ModuleType('click')
    click.Command = fake_click_Command_class
    return click
