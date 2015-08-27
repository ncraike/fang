

class Test_DependencyRegister__construction:

    def test__on_new_dep_reg__dependents_should_be_empty(self, dep_reg):
        assert len(dep_reg.dependents) == 0

    def test__on_new_dep_reg__resources_should_be_empty(self, dep_reg):
        assert len(dep_reg.resources) == 0

class Test_DependencyRegister__register_dependent:

    def test__can_call_with_dependent_and_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        dep_reg._register_dependent(fake_dependent, fake_resource_name)

    def test__if_dependent_is_not_in_dependents_calling_adds_it(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in dep_reg.dependents
        dep_reg.dependents.pop(fake_dependent, None)

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_dependent in dep_reg.dependents

    def test__if_dependent_is_not_in_dependents_calling_adds_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is not in dep_reg.dependents
        dep_reg.dependents.pop(fake_dependent, None)

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_resource_name in dep_reg.dependents[fake_dependent]

    def test__if_dependent_is_in_dependents_calling_adds_resource_name(
            self, dep_reg, fake_resource_name, fake_dependent):
        # Ensure that fake_dependent is in dep_reg.dependents
        dep_reg.dependents[fake_dependent] = []

        dep_reg._register_dependent(fake_dependent, fake_resource_name)

        assert fake_resource_name in dep_reg.dependents[fake_dependent]
