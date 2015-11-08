from pytest_bdd.types import WHEN, THEN

import sys
# NOTE: This is awful, but needed because pytest_bdd's __init__ masks
# access to the actual pytest_bdd.scenario module
import pytest_bdd
pytest_bdd_scenario = sys.modules['pytest_bdd.scenario']

def defers_when_steps(step_func):
    '''Decorator to mark a step as deferring when steps'''
    step_func._defers_when_steps = True
    return step_func

def step_needs_when_steps_deferred(step_instance, request, scenario):
    step_func = pytest_bdd_scenario._find_step_function(
            request, step_instance, scenario, encoding='utf-8')
    return step_func_needs_when_steps_deferred(step_func)

def step_func_needs_when_steps_deferred(step_func):
    if hasattr(step_func, '_defers_when_steps'):
        return step_func._defers_when_steps
    else:
        return False

def has_steps_which_need_deferral(scenario, request):
    for step in scenario.steps:
        if step_needs_when_steps_deferred(step, request, scenario):
            if step.type == THEN:
                return True
            else:
                raise Exception(
                        'Only "Then" steps can request "When" step deferral')
    else:
        return False

def defer_when_steps_if_needed(scenario, request):
    if has_steps_which_need_deferral(scenario, request):
        when_steps = [
                step for step in scenario.steps
                if step.type == WHEN]
        scenario._deferred_steps = when_steps
        for when_step in when_steps:
            if when_step not in scenario.steps:
                raise Exception(
                        'Couldn\'t find "When" step {!r} on scenario {!r}. '
                        'This may mean the step was defined in the feature '
                        '"Background".'.format(
                            when_step, scenario))
            scenario._steps.remove(when_step)


def get_deferred_when_steps_callable(scenario, request):

    def run_when_steps():
        for when_step in scenario._deferred_steps:
            step_func = pytest_bdd_scenario._find_step_function(
                    request, when_step, scenario, encoding='utf-8')
            pytest_bdd_scenario._execute_step_function(
                    request, scenario, when_step, step_func)

    return run_when_steps

def add_deferred_when_steps_to_args_if_needed(
        scenario, step_instance, step_func, step_func_args, request):
    # Only add args if step_func is a "Then" step and was decorated
    # by defers_when_steps()
    if (
            step_instance.type == THEN and
            step_needs_when_steps_deferred(step_instance, request, scenario)
    ):
        step_func_args['deferred_when_steps'] = (
            get_deferred_when_steps_callable(scenario, request))
