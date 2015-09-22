
import functools

# Class under test:
from fang.dependency_register import DependencyRegister


# This should be in some kind of testing utils module
def give_unexpected_calls(method_calls, expected_methods_names):
    return [call for call in method_calls
            if call[0] not in expected_methods_names]

class Test_DependencyRegister__construction:

    def test__after_creation__dependents_should_be_empty(self, dep_reg):
        assert len(dep_reg.dependents) == 0

    def test__after_creation__resources_should_be_empty(self, dep_reg):
        assert len(dep_reg.resources) == 0

class Test_DependencyRegister__register_dependent:

    def test__giving_dependent_and_resource_name__should_succeed(
            self, dep_reg, fake_resource_name, fake_dependent):
        dep_reg._register_dependent(fake_dependent, fake_resource_name)

    def test__giving_dependent_not_in_dependents__should_add_dependent(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in dep_reg.dependents
        dep_reg.dependents.pop(fake_dependent, None)

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_dependent in dep_reg.dependents

    def test__giving_dependent_not_in_dependents__should_add_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in dep_reg.dependents
        dep_reg.dependents.pop(fake_dependent, None)

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_resource_name in dep_reg.dependents[fake_dependent]

    def test__giving_dependent_in_dependents__should_add_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is in dep_reg.dependents
        dep_reg.dependents[fake_dependent] = []

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_resource_name in dep_reg.dependents[fake_dependent]

class Test_DependencyRegister__register_resource_dependency:

    def test__giving_resource_name_and_dependent__should_succeed(
            self, dep_reg, fake_resource_name, fake_dependent):
        dep_reg._register_resource_dependency(
                fake_resource_name, fake_dependent)

    def test__giving_resource_name_not_in_resources__should_add_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in dep_reg.resources
        dep_reg.resources.pop(fake_resource_name, None)

        dep_reg._register_resource_dependency(
                fake_resource_name, fake_dependent)

        assert fake_resource_name in dep_reg.resources

    def test__giving_resource_name_not_in_resources__should_add_dependent(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in dep_reg.resources
        dep_reg.resources.pop(fake_resource_name, None)

        dep_reg._register_resource_dependency(
                fake_resource_name, fake_dependent)

        assert fake_dependent in dep_reg.resources[fake_resource_name]

    def test__giving_resource_name_in_resources__should_add_dependent(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_resource_name is not in dep_reg.resources
        dep_reg.resources[fake_resource_name] = set()

        dep_reg._register_resource_dependency(
                fake_resource_name, fake_dependent)

        assert fake_dependent in dep_reg.resources[fake_resource_name]

class Test_DependencyRegister_register:

    def test__giving_None_for_dependent__should_return_partial_of_register(
            self, dep_reg, mock_dep_reg, fake_resource_name):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, None)

        # register() should give a partial of self.register with one arg fixed
        assert isinstance(result, functools.partial)
        assert result.func == mock_dep_reg.register
        assert result.args == (fake_resource_name,)

    def test__giving_resource_name_and_dependent__should_call_self__unwrap_dependent(
            self, dep_reg, mock_dep_reg, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, fake_dependent)

        # Assert self._unwrap_dependent() called as we expect
        mock_dep_reg._unwrap_dependent.assert_called_with(fake_dependent)

    def test__giving_resource_name_and_dependent__should_return_unwrapped_dependent(
            self, dep_reg, mock_dep_reg, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, fake_dependent)

        # Assert return value was whatever self._unwrap_dependent returned
        assert result == mock_dep_reg._unwrap_dependent.return_value

    def test__giving_resource_name_and_dependent__should_call_self__register_dependent(
            self, dep_reg, mock_dep_reg, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, fake_dependent)

        unwrapped_dependent = mock_dep_reg._unwrap_dependent.return_value

        # Assert self._register_dependent() called as we expect
        mock_dep_reg._register_dependent.assert_called_with(
                unwrapped_dependent, fake_resource_name)

    def test__giving_resource_name_and_dependent__should_call_self__register_resource_dependency(
            self, dep_reg, mock_dep_reg, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, fake_dependent)

        unwrapped_dependent = mock_dep_reg._unwrap_dependent.return_value

        # Assert self._register_resource_dependency() called as we expect
        mock_dep_reg._register_resource_dependency.assert_called_with(
                fake_resource_name, unwrapped_dependent)

    def test__giving_resource_name_and_dependent__should_only_call_expected_methods(
            self, dep_reg, mock_dep_reg, fake_resource_name, fake_dependent):

        # Method under test
        #
        # We call the method on the class, not an instance, so we can
        # give a mock instance as 'self'
        result = DependencyRegister.register(
                mock_dep_reg, fake_resource_name, fake_dependent)

        expected_methods_names = {
                '_unwrap_dependent',
                '_register_dependent',
                '_register_resource_dependency'}

        unexpected_calls = give_unexpected_calls(
                mock_dep_reg.method_calls, expected_methods_names)

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'Expected method names: {!r}'.format(
                unexpected_calls,
                mock_dep_reg.method_calls,
                expected_methods_names))
