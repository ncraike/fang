from utils import (
        defer_when_steps_if_needed,
        add_deferred_when_steps_to_args_if_needed)

import pytest

def pytest_bdd_before_scenario(request, feature, scenario):
    """Called before scenario is executed."""
    defer_when_steps_if_needed(scenario, request)

def pytest_bdd_before_step_call(
        request, feature, scenario, step, step_func, step_func_args):
    """Called before step function is executed."""
    add_deferred_when_steps_to_args_if_needed(
            scenario, step, step_func, step_func_args, request)

@pytest.fixture
def deferred_when_steps():
    '''This exists to stop pytest searching for a "deferred_when_steps"
    funcarg.'''
    return "THIS SHOULD HAVE BEEN A CALLABLE OF WHEN STEPS"

# This registers some py.test fixtures
from common.fixtures.dependents import (
        fake_dependent,
        fake_dependent_which_is_a_class)

# This registers several "argument" aliases in the BDD language
import common.bdd.arguments
