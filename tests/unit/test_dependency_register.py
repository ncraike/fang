
import functools
import unittest.mock

import pytest

from fang.errors import DependentNotFoundError

# Class under test:
from fang.dependency_register import DependencyRegister


# This should be in some kind of testing utils module
def give_unexpected_calls(method_calls, expected_methods_names):
    return [call for call in method_calls
            if call[0] not in expected_methods_names]

class Test_DependencyRegister__construction:

    def test__after_creation__dependents_should_be_empty(self, DependencyRegister_instance):
        assert len(DependencyRegister_instance.dependents) == 0

    def test__after_creation__resources_should_be_empty(self, DependencyRegister_instance):
        assert len(DependencyRegister_instance.resources) == 0

class Test_DependencyRegister__register_dependent:

    def test__giving_dependent_and_resource_name__should_succeed(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_dependent(
                mock_DependencyRegister_instance, fake_dependent, fake_resource_name)

    def test__giving_dependent_not_in_dependents__should_add_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in instance.dependents
        mock_DependencyRegister_instance.dependents.pop(fake_dependent, None)

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_dependent(
                mock_DependencyRegister_instance, fake_dependent, fake_resource_name)

        assert fake_dependent in mock_DependencyRegister_instance.dependents

    def test__giving_dependent_not_in_dependents__should_add_resource_name(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in instance.dependents
        mock_DependencyRegister_instance.dependents.pop(fake_dependent, None)

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_dependent(
                mock_DependencyRegister_instance, fake_dependent, fake_resource_name)

        assert fake_resource_name in mock_DependencyRegister_instance.dependents[fake_dependent]

    def test__giving_dependent_in_dependents__should_add_resource_name(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is in mock_DependencyRegister_instance.dependents
        mock_DependencyRegister_instance.dependents[fake_dependent] = []

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_dependent(
                mock_DependencyRegister_instance, fake_dependent, fake_resource_name)

        assert fake_resource_name in mock_DependencyRegister_instance.dependents[fake_dependent]

class Test_DependencyRegister__register_resource_dependency:

    def test__giving_resource_name_and_dependent__should_succeed(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_resource_dependency(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

    def test__giving_resource_name_not_in_resources__should_add_resource_name(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in mock_DependencyRegister_instance.resources
        mock_DependencyRegister_instance.resources.pop(fake_resource_name, None)

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_resource_dependency(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        assert fake_resource_name in mock_DependencyRegister_instance.resources

    def test__giving_resource_name_not_in_resources__should_add_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in mock_DependencyRegister_instance.resources
        mock_DependencyRegister_instance.resources.pop(fake_resource_name, None)

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_resource_dependency(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        assert fake_dependent in mock_DependencyRegister_instance.resources[fake_resource_name]

    def test__giving_resource_name_in_resources__should_add_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in mock_DependencyRegister_instance.resources
        mock_DependencyRegister_instance.resources[fake_resource_name] = set()

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister._register_resource_dependency(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        assert fake_dependent in mock_DependencyRegister_instance.resources[fake_resource_name]

class Test_DependencyRegister_register:

    def test__giving_None_for_dependent__should_return_partial_of_register(
            self, mock_DependencyRegister_instance, fake_resource_name):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, None)

        # register() should give a partial of self.register with one arg fixed
        assert isinstance(result, functools.partial)
        assert result.func == mock_DependencyRegister_instance.register
        assert result.args == (fake_resource_name,)

    def test__giving_None_for_dependent__should_not_call_any_methods(
            self, mock_DependencyRegister_instance, fake_resource_name):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, None)

        expected_methods_names = {}

        unexpected_calls = give_unexpected_calls(
                mock_DependencyRegister_instance.method_calls, expected_methods_names)

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'Expected method names: {!r}'.format(
                unexpected_calls,
                mock_DependencyRegister_instance.method_calls,
                expected_methods_names))

    def test__giving_resource_name_and_dependent__should_call_self__unwrap_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        # Assert self._unwrap_dependent() called as we expect
        mock_DependencyRegister_instance._unwrap_dependent.assert_called_with(fake_dependent)

    def test__giving_resource_name_and_dependent__should_return_unwrapped_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        # Assert return value was whatever self._unwrap_dependent returned
        assert result == mock_DependencyRegister_instance._unwrap_dependent.return_value

    def test__giving_resource_name_and_dependent__should_call_self__register_dependent(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        unwrapped_dependent = mock_DependencyRegister_instance._unwrap_dependent.return_value

        # Assert self._register_dependent() called as we expect
        mock_DependencyRegister_instance._register_dependent.assert_called_with(
                unwrapped_dependent, fake_resource_name)

    def test__giving_resource_name_and_dependent__should_call_self__register_resource_dependency(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        unwrapped_dependent = mock_DependencyRegister_instance._unwrap_dependent.return_value

        # Assert self._register_resource_dependency() called as we expect
        mock_DependencyRegister_instance._register_resource_dependency.assert_called_with(
                fake_resource_name, unwrapped_dependent)

    def test__giving_resource_name_and_dependent__should_only_call_expected_methods(
            self, mock_DependencyRegister_instance, fake_resource_name, fake_dependent):
        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_DependencyRegister_instance, fake_resource_name, fake_dependent)

        expected_methods_names = {
                '_unwrap_dependent',
                '_register_dependent',
                '_register_resource_dependency'}

        unexpected_calls = give_unexpected_calls(
                mock_DependencyRegister_instance.method_calls, expected_methods_names)

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'Expected method names: {!r}'.format(
                unexpected_calls,
                mock_DependencyRegister_instance.method_calls,
                expected_methods_names))

class Test_DependencyRegister_query_resources:

    def test__giving_dependent__should_call_self__unwrap_dependent(
            self, mock_DependencyRegister_instance, fake_dependent):
        try:
            result = DependencyRegister.query_resources(
                    mock_DependencyRegister_instance, fake_dependent)
        except:
            pass

        # Assert self._unwrap_dependent() called as we expect
        mock_DependencyRegister_instance._unwrap_dependent.assert_called_with(fake_dependent)

    def test__giving_dependent_not_in_self_dependents__should_raise_DependentNotFoundError(
            self, mock_DependencyRegister_instance, fake_dependent):

        # Method under test
        with pytest.raises(DependentNotFoundError):
            result = DependencyRegister.query_resources(
                    mock_DependencyRegister_instance, fake_dependent)

    def test__giving_dependent_in_self_dependents__should_return_resources(
            self, mock_DependencyRegister_instance, fake_dependent, fake_resource_name):

        mock_DependencyRegister_instance._unwrap_dependent.return_value = 'unwrapped dependent'
        mock_DependencyRegister_instance.dependents['unwrapped dependent'] = [fake_resource_name]

        # Method under test
        result = DependencyRegister.query_resources(
                mock_DependencyRegister_instance, fake_dependent)
        assert result == [fake_resource_name]

class Test_DependencyRegister__unwrap_dependent:

    def test__giving_class_dependent__should_return_dependent_as_is(
            self, mock_DependencyRegister_class, fake_dependent_which_is_a_class):

        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_dependent = DependencyRegister._unwrap_dependent.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_dependent(
                mock_DependencyRegister_class, fake_dependent_which_is_a_class)

        assert result == fake_dependent_which_is_a_class

    def test__giving_non_class_dependent__should_call__unwrap_func_with_dependent(
            self, mock_DependencyRegister_class, fake_dependent):
        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_dependent = DependencyRegister._unwrap_dependent.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_dependent(mock_DependencyRegister_class, fake_dependent)

        mock_DependencyRegister_class._unwrap_func.assert_called_with(fake_dependent)

    def test__giving_non_class_dependent__should_return_result_of__unwrap_func(
            self, mock_DependencyRegister_class, fake_dependent):
        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_dependent = DependencyRegister._unwrap_dependent.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_dependent(mock_DependencyRegister_class, fake_dependent)

        assert result == mock_DependencyRegister_class._unwrap_func.return_value

class Test_DependencyRegister__unwrap_func:
    '''
    Test DependencyRegister._unwrap_func().
    '''

    def test__giving_undecorated_function__should_return_function(
            self, mock_DependencyRegister_class, undecorated_function):
        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_func = DependencyRegister._unwrap_func.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_func(mock_DependencyRegister_class, undecorated_function)

        assert result == undecorated_function

    def test__giving_decorated_function__should_make_recursive_call_with_undecorated_function(
            self, mock_DependencyRegister_class, undecorated_function, decorator):

        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_func = DependencyRegister._unwrap_func.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_func(
                mock_DependencyRegister_class, decorator(undecorated_function))

        # Assert recursive call was made as expected
        mock_DependencyRegister_class._unwrap_func.assert_called_with(undecorated_function)

    def test__giving_decorated_function__should_return_result_of_recursive_call(
            self, mock_DependencyRegister_class, undecorated_function, decorator):

        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_func = DependencyRegister._unwrap_func.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_func(
                mock_DependencyRegister_class, decorator(undecorated_function))

        assert result == mock_DependencyRegister_class._unwrap_func.return_value

@pytest.fixture(scope='function')
def with_click_imported(request, fake_click_module):
    '''
    Patch fake.dependency_register.click with a fake version of the
    click module, but just for the length of the test.

    We use pytest "fixture finalization" to cleanup the patching when
    the test is done.
    '''
    patcher = unittest.mock.patch(
            'fang.dependency_register.click', fake_click_module)
    patcher.start()
    request.addfinalizer(patcher.stop)

@pytest.mark.usefixtures('with_click_imported')
class Test_DependencyRegister__unwrap_func__with_click_imported(
        Test_DependencyRegister__unwrap_func):
    '''
    Test DependencyRegister._unwrap_func(), but this time with
    the "click" module (well, a fake version of it) imported.

    We do this to test fang's workaround for the click.command()
    decorator not setting __wrapped__.

    This is done as a sub-class of the previous class, so that in
    addition to testing the click.Command workaround, we also test that
    importing click hasn't broken the other behaviours we just tested
    for.

    This is a bit hacky (I'm not wild about sub-classes in tests), but
    it's the best I can come up with using unittest.mock and pytest.
    '''

    def test__giving_click_command__should_make_recursive_call_with_command_callback(
            self, mock_DependencyRegister_class, fake_click_module,
            fake_click_Command_class):

        click_command = fake_click_Command_class('click.Command callback')

        # This unwraps the @classmethod decoration to reach the original
        # function, so we can specify 'cls' as a mock of the
        # DependencyRegister class.
        _unwrap_func = DependencyRegister._unwrap_func.__func__

        # Class method under test (tested as the undecorated function)
        result = _unwrap_func(
                mock_DependencyRegister_class, click_command)

        mock_DependencyRegister_class._unwrap_func.assert_called_with(
                click_command.callback)
