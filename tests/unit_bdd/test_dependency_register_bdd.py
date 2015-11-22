
import unittest.mock
import functools
from types import ModuleType

import pytest
from pytest_bdd import scenario, scenarios, given, when, then, parsers

import fang.errors
from utils import defers_when_steps

#
# Module under test:
#
from fang.dependency_register import DependencyRegister

#
# Load our test scenarios
#
scenarios('features/dependency_register/')

arguments = []

def give_argument_value_from_parsing_line(
        argument_line, parser, get_argument_value_func,
        **kwargs_for_arg_factories):
    '''
    This asks the given function for the argument value based on the
    argument line.

    The function is given the dictionary of matches from the
    parser, which it may use to create the argument value.
    '''
    matches = parser.parse_arguments(argument_line)
    kwargs_for_arg_factories.update(matches)
    return get_argument_value_func(**kwargs_for_arg_factories)

def register_argument(pattern_or_parser, get_argument_value_func):
    parser = parsers.get_parser(pattern_or_parser)
    give_argument_value = functools.partial(
            give_argument_value_from_parsing_line,
            parser=parser,
            get_argument_value_func=get_argument_value_func)

    argument_entry = (parser.is_matching, give_argument_value)
    arguments.append(argument_entry)

# For use as decorator
def argument_line(pattern_or_parser):
    def decorator(decorated_func):
        register_argument(pattern_or_parser, decorated_func)
        return decorated_func
    return decorator

def get_argument_from_registered(argument_line, **kwargs_for_arg_factories):
    for (is_matching, give_argument_value) in arguments:
        if is_matching(argument_line):
            return give_argument_value(
                    argument_line, **kwargs_for_arg_factories)
    else:
        raise Exception(
                "Couldn't find a match for argument line: {!r}".format(
                    argument_line))

def parse_argument_lines(lines, **kwargs_for_arg_factories):
    return [
            get_argument_from_registered(line, **kwargs_for_arg_factories)
            for line in lines]

@pytest.fixture
def world_state():
    return {
            'call_under_test': {
                'callable': None,
                'args': [],
                'kwargs': {},
                'callable_on_instance': None,
                'special_options': {
                    'ignore_exceptions': False,
                },
                'result': 'NO RESULT YET',
                },
            'instance': None,
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
def mock_DependencyRegister_class():
    return unittest.mock.Mock(
            spec=DependencyRegister)

@pytest.fixture
@argument_line('a fake resource name')
@argument_line('the fake resource name')
def fake_resource_name(**kwargs):
    return 'fake resource name'

@pytest.fixture
@argument_line('a fake dependent')
def fake_dependent(**kwargs):
    return 'fake dependent'

@argument_line('a fake dependent not in dependents')
def fake_dependent_not_in_dependents(pytest_request, **kwargs):
    fake_dependent, mock_DependencyRegister_instance = (
        pytest_request.getfuncargvalue('fake_dependent'),
        pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_dependent is not in instance.dependents
    mock_DependencyRegister_instance.dependents.pop(fake_dependent, None)
    return fake_dependent

@argument_line('a fake dependent in dependents')
def fake_dependent_in_dependents(pytest_request, **kwargs):
    fake_dependent, fake_resource_name, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('fake_dependent'),
            pytest_request.getfuncargvalue('fake_resource_name'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_dependent is in instance.dependents
    mock_DependencyRegister_instance.dependents[fake_dependent] = [fake_resource_name]
    return fake_dependent

class FakeDependentWhichIsAClass:
    pass

@argument_line('a fake dependent which is a class')
def fake_dependent_which_is_a_class(pytest_request, **kwargs):
    return FakeDependentWhichIsAClass

@argument_line('a fake resource name not in resources')
def fake_resource_name_not_in_resources(pytest_request, **kwargs):
    call_under_test, fake_resource_name, mock_DependencyRegister_instance = (
            pytest_request.getfuncargvalue('call_under_test'),
            pytest_request.getfuncargvalue('fake_resource_name'),
            pytest_request.getfuncargvalue('mock_DependencyRegister_instance'))
    # Ensure that fake_resource_name is not in instance.resources
    mock_DependencyRegister_instance.resources.pop(fake_resource_name, None)
    return fake_resource_name

@argument_line('a fake resource name in resources')
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

@argument_line(parsers.parse(
    'the return value of method {method_name}'))
def the_return_value_of_mock_method(method_name, pytest_request=None):
    world_state = pytest_request.getfuncargvalue('world_state')
    method = getattr(world_state['instance'], method_name)
    return method.return_value

def _undecorated_function(*args, **kwargs):
    return ('undecorated_function() return value', args, kwargs)

@argument_line(parsers.parse(
    'an undecorated function'))
@argument_line(parsers.parse(
    'the undecorated function'))
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

@argument_line(parsers.parse('a decorated function'))
@argument_line(parsers.parse('the decorated function'))
@pytest.fixture
def a_decorated_function(pytest_request=None):
    an_undecorated_function = pytest_request.getfuncargvalue(
            'an_undecorated_function')
    return decorator(an_undecorated_function)

@given(parsers.parse(
    "I am testing the {method_name} method of DependencyRegister"))
def given_the_method_under_test(
        method_name, call_under_test, world_state, mock_DependencyRegister_instance):

    call_under_test['callable'] = getattr(DependencyRegister, method_name)
    call_under_test['args'].append(mock_DependencyRegister_instance)
    call_under_test['callable_on_instance'] = getattr(
            mock_DependencyRegister_instance, method_name)
    world_state['instance'] = mock_DependencyRegister_instance

@given(parsers.parse(
    "I am testing the {method_name} class-method of DependencyRegister"))
def given_the_class_method_under_test(
        method_name, call_under_test, world_state,
        mock_DependencyRegister_class):

    # This unwraps the @classmethod decoration to reach the original
    # function, so we can specify 'cls' as a mock of the
    # DependencyRegister class.
    unwrapped_class_method = getattr(
            getattr(
                DependencyRegister,
                method_name),
            '__func__')

    call_under_test['callable'] = unwrapped_class_method
    call_under_test['args'].append(mock_DependencyRegister_class)

    call_under_test['callable_on_instance'] = getattr(
            mock_DependencyRegister_class, method_name)
    world_state['instance'] = mock_DependencyRegister_class

def resolve_arg_lines(lines, request):
    return [get_argument_from_registered(line, pytest_request=request)
            for line in lines.splitlines()]

@given('I am ignoring all exceptions during the method call')
def ignoring_exceptions_during_method_call(call_under_test):
    call_under_test['special_options']['ignore_exceptions'] = True

@given(parsers.parse(
    "the method {method_name} will return its one argument unchanged"))
def given_method_will_return_its_one_arg_unchanged(method_name, world_state):
    instance = world_state['instance']
    setattr(instance, method_name, lambda x: x)

@pytest.fixture
def fake_click_Command_class():
    class Command:
        '''A fake click.Command class which just implements behaviour we
        need for tests.'''

        def __init__(self, function_to_wrap):
            self.callback = function_to_wrap

    return Command

@pytest.fixture
def fake_click_module(fake_click_Command_class):
    click = ModuleType('click')
    click.Command = fake_click_Command_class
    return click

@given("I have the click module imported")
def with_click_module_imported(request, fake_click_module):
    patcher = unittest.mock.patch(
            'fang.dependency_register.click', fake_click_module)
    patcher.start()
    request.addfinalizer(patcher.stop)

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

    if call_under_test['special_options']['ignore_exceptions']:
        try:
            result = to_call(*args, **kwargs)
            call_under_test['result'] = result
        except:
            call_under_test['result'] = "EXCEPTION OCCURRED"

    else:
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

def give_unexpected_calls(method_calls, expected_methods_names):
    return [call for call in method_calls
            if call[0] not in expected_methods_names]

@then('no other methods should be called')
def no_methods_should_be_called(world_state):
    return assert_only_expected_methods_called([], world_state)

@then(parsers.parse(
    "only these methods should be called:\n{method_name_lines}"))
def only_these_methods_should_be_called(method_name_lines, world_state):
    return assert_only_expected_methods_called(
            method_name_lines.splitlines(),
            world_state)

def assert_only_expected_methods_called(expected_methods_names, world_state):
    instance = world_state['instance']
    unexpected_calls = give_unexpected_calls(
            instance.method_calls, expected_methods_names)
    assert unexpected_calls == [], (
            'Unexpected methods called: {!r} \n'
            'Called methods: {!r} \n'
            'Expected method names: {!r}'.format(
            unexpected_calls,
            instance.method_calls,
            expected_methods_names))

@then(parsers.parse(
    'the method {method_name} should be called with:\n{arg_lines}'))
def method_should_be_called_with_args(
        method_name, arg_lines, world_state, request):
    expected_method_called = getattr(world_state['instance'], method_name)
    expected_args = resolve_arg_lines(arg_lines, request)

    expected_method_called.assert_called_with(*expected_args)

@then(parsers.parse(
    'the result should be the return value of method {method_name}'))
def result_should_be_return_value_of(method_name, world_state, call_under_test):
    method = getattr(world_state['instance'], method_name)
    assert call_under_test['result'] == method.return_value

@defers_when_steps
@then(parsers.parse(
    'the exception {exception_name} should be raised'))
def exception_should_be_raised(exception_name, deferred_when_steps):
    expected_exception = getattr(fang.errors, exception_name)
    with pytest.raises(expected_exception):
        deferred_when_steps()

@then(parsers.parse(
    'the result should contain:\n{arg_lines}'))
def result_should_contain(arg_lines, call_under_test, request):
    result = call_under_test['result']
    items = resolve_arg_lines(arg_lines, request)
    for item in items:
        assert item in result

@then(parsers.parse(
    'the result should be {one_arg}'))
def result_should_be(one_arg, call_under_test, request):
    result = call_under_test['result']
    expected_result = get_argument_from_registered(
            one_arg,
            pytest_request=request)
    assert result == expected_result
