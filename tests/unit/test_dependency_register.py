
import pytest

# Module under test:
from fang.dependency_register import DependencyRegister

import functools


@pytest.fixture(scope='function')
def dep_reg():
    return DependencyRegister()

class Test_DependencyRegister__construction:

    def test__new_dep_reg_can_be_created(self, dep_reg):
        pass

    def test__on_new_dep_reg__dependents_should_be_empty(self, dep_reg):
        assert len(dep_reg.dependents) == 0

    def test__on_new_dep_reg__resources_should_be_empty(self, dep_reg):
        assert len(dep_reg.resources) == 0

class Test_DependencyRegister_register:

    def test__can_call_with_just_resource_name(self, dep_reg):
        dep_reg.register('fake resource name')

    def test__calling_with_just_resource_name_should_give_partial(
            self, dep_reg):

        result = dep_reg.register('fake resource name')

        # register() should give a partial of itself with one arg fixed
        assert isinstance(result, functools.partial)
        assert result.func == dep_reg.register
        assert result.args == ('fake resource name',)

    def test__can_call_with_resource_name_and_dependent(self, dep_reg):
        dep_reg.register('fake resource name', 'fake dependent')

    def test__calling_with_dependent_should_return_dependent(self, dep_reg):
        result = dep_reg.register('fake resource name', 'fake dependent')
        assert result == 'fake dependent'
