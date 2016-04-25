

# Class under test:
from fang.resource_provider_register import ResourceProviderRegister

class Test_ResourceProviderRegister__construction:

    def test__after_creation__namespace_should_default_to_None(self):
        instance = ResourceProviderRegister()
        assert instance.namespace is None
    
    def test__after_creation_with_namespace__namespace_should_be_as_given(self):
        instance = ResourceProviderRegister('mynamespace')
        assert instance.namespace == 'mynamespace'
        
    def test__after_creation__resource_providers_should_be_empty(self):
        instance = ResourceProviderRegister()
        assert len(instance.resource_providers) == 0

    def test__after_creation_with_namespace__resource_providers_should_be_empty(self):
        instance = ResourceProviderRegister('mynamespace')
        assert len(instance.resource_providers) == 0

class Test_ResourceProviderRegister_clear:

    def test__with_empty_resource_providers__should_be_empty_after(self):
        instance = ResourceProviderRegister()
        instance.resource_providers = {}

        instance.clear()
        assert len(instance.resource_providers) == 0

    def test__with_resources_in_resource_providers__should_be_empty_after(self):
        instance = ResourceProviderRegister()
        instance.resource_providers = {
            'myresource': 'my value',
            'mycallable': lambda x: x,
        }

        instance.clear()
        assert len(instance.resource_providers) == 0
