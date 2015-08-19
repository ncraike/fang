

class Test_DependencyRegister__construction:

    def test__on_new_dep_reg__dependents_should_be_empty(self, dep_reg):
        assert len(dep_reg.dependents) == 0

    def test__on_new_dep_reg__resources_should_be_empty(self, dep_reg):
        assert len(dep_reg.resources) == 0
