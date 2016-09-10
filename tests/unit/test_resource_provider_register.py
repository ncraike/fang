
import functools
import unittest.mock
import pytest

from fang.errors import FangError, ProviderAlreadyRegisteredError

# Class under test:
from fang.resource_provider_register import ResourceProviderRegister

@pytest.fixture()
def mock_instance():
    mock_instance = unittest.mock.NonCallableMock(
            spec=ResourceProviderRegister())
    mock_instance.namespace = None
    mock_instance.resource_providers = {}
    return mock_instance

other_instance = mock_instance
pytest.fixture(other_instance)

@pytest.fixture()
def resource_name():
    return 'test.resource'

@pytest.fixture()
def resource():
    def fake_resource(x):
        return x
    return fake_resource

@pytest.fixture()
def resource_provider(resource):
    def fake_resource_provider():
        return resource
    return fake_resource_provider

def give_unexpected_calls(method_calls, expected_methods_names):
    '''

    TODO: Move this to a common test utils module.
    '''
    return [call for call in method_calls
            if call[0] not in expected_methods_names]

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

class Test_ResourceProviderRegister_register:
    '''
    Test the instance method ResourceProviderRegister.register().

    NOTE: In these tests we call the method on the class, not the
    instance, so we can give a mock instance in place of self. This
    lets us check if register() calls any other instance methods.
    '''

    def test__giving_no_provider__should_return_partial(
            self, mock_instance, resource_name):
        '''
        If register() is called with resource_name but no provider,
        register() should return a partial of register() with the
        resource_name argument fixed.

        '''
        result = ResourceProviderRegister.register(
                mock_instance, resource_name)

        assert isinstance(result, functools.partial)
        assert result.func == mock_instance.register
        assert result.args == (resource_name,)

    def test__giving_no_provider__should_not_call_any_other_methods(
            self, mock_instance, resource_name):
        '''
        If register() is called with resource_name but no provider,
        no other instance methods should be called.
        '''

        result = ResourceProviderRegister.register(
                mock_instance, resource_name)

        unexpected_calls = give_unexpected_calls(
                mock_instance.method_calls, [])

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'No method calls were expected'.format(
                unexpected_calls,
                mock_DependenyRegister_instance.method_calls))

    def test__giving_provider__should_register_under_name(
            self, mock_instance, resource_name, resource_provider):

        result = ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        assert mock_instance.resource_providers[resource_name] == resource_provider

    def test__giving_provider_already_registered__should_raise(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        with pytest.raises(ProviderAlreadyRegisteredError):
            ResourceProviderRegister.register(
                    mock_instance, resource_name, resource_provider)

    def test__giving_provider_already_registered_and_override_false__should_raise(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        with pytest.raises(ProviderAlreadyRegisteredError):
            ResourceProviderRegister.register(
                    mock_instance, resource_name, resource_provider,
                    allow_override=False)

    def test__giving_provider_already_registered_and_override_true__should_register(
            self, mock_instance, resource_name, resource_provider):

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider)

        ResourceProviderRegister.register(
                mock_instance, resource_name, resource_provider,
                allow_override=True)

        assert mock_instance.resource_providers[resource_name] == resource_provider

class Test_ResourceProviderRegister_register_instance:
    '''
    Test the instance method ResourceProviderRegister.register_instance().

    NOTE: In these tests we call the method on the class, not the
    instance, so we can give a mock instance in place of self. This
    lets us test how register_instance() calls other instance methods.
    '''

    def test__giving_no_instance__should_return_partial(
            self, mock_instance, resource_name):
        '''
        If register_instance() is called with resource_name but no
        instance, register_instance() should return a partial of
        register_instance() with the resource_name argument fixed.

        '''
        result = ResourceProviderRegister.register_instance(
                mock_instance, resource_name)

        assert isinstance(result, functools.partial)
        assert result.func == mock_instance.register_instance
        assert result.args == (resource_name,)

    def test__giving_no_instance_and_extra_kwargs__should_return_partial_with_kwargs(
            self, mock_instance, resource_name):
        '''
        If register_instance() is called with resource_name, no
        instance, and additional keyword arguments, register_instance()
        should return a partial of register_instance() which includes
        those additional keyword arguments.
        '''
        result = ResourceProviderRegister.register_instance(
                mock_instance, resource_name, a='b', c='d')

        assert isinstance(result, functools.partial)
        assert result.keywords['a'] == 'b'
        assert result.keywords['c'] == 'd'

    def test__giving_resource_as_instance__should_return_resource(
            self, mock_instance, resource_name, resource):
        '''
        If register_instance() is called with an instance, that instance
        should be returned from the call.

        This eases uses of register_instance() as a decorator.
        '''
        result = ResourceProviderRegister.register_instance(
                mock_instance, resource_name, resource)
        assert result == resource

    def test__giving_resource_as_instance__should_call_register_with_resource_name_and_callable(
            self, mock_instance, resource_name, resource):
        '''
        If register_instance() is called with an instance,
        register_instance() should call register() with a callable which
        returns that instance. This callable acts as a "resource
        provider" which always provides this instance.
        '''
        result = ResourceProviderRegister.register_instance(
                mock_instance, resource_name, resource)

        method, args, kwargs = mock_instance.method_calls[0]

        assert method == 'register', "resource() should have been called"
        assert args == (resource_name,), (
                "resource() should have been called with the resource name")

        assert 'provider' in kwargs, (
                "register() should have been given a 'provider' keyword "
                "argument")
        given_provider = kwargs['provider']
        assert callable(given_provider), (
                "register()'s 'provider' keyword-argument should be callable")
        assert given_provider() == resource, (
                "register()'s 'provider' keyword-argument should give the "
                "resource when called")

    def test__giving_resource_as_instance_and_extra_kwargs__should_call_register_with_kwargs(
            self, mock_instance, resource_name, resource):
        '''
        If register_instance() is called with an instance and additional
        keyword arguments, register_instance() should include those
        keyword arguments when calling register().
        '''
        result = ResourceProviderRegister.register_instance(
                mock_instance, resource_name, resource, a='b', c='d')
        method, args, kwargs = mock_instance.method_calls[0]

        assert method == 'register', "resource() should have been called"
        assert kwargs['a'] == 'b'
        assert kwargs['c'] == 'd'

class Test_ResourceProviderRegister_mass_register:

    def test__giving_empty_dict__should_not_call_other_methods(
            self, mock_instance):
        '''
        If mass_register() is called with an empty dict, no other
        instance methods should be called.
        '''
        result = ResourceProviderRegister.mass_register(mock_instance, {})

        unexpected_calls = give_unexpected_calls(
                mock_instance.method_calls, [])

        assert not unexpected_calls, (
                'Unexpected methods called: {!r} \n'
                'Called methods: {!r} \n'
                'No method calls were expected'.format(
                unexpected_calls,
                mock_instance.method_calls))

    def test__giving_empty_dict__should_return_None(
            self, mock_instance):
        '''
        If mass_register() is called with an empty dict, it should
        return None.
        '''
        result = ResourceProviderRegister.mass_register(mock_instance, {})
        assert result is None

    def test__giving_name_and_resource__should_call_register_instance(
            self, mock_instance, resource_name, resource):
        result = ResourceProviderRegister.mass_register(
                mock_instance, {resource_name: resource})

        assert len(mock_instance.method_calls) == 1
        assert ('register_instance', (resource_name, resource), {}
                ) in mock_instance.method_calls

    def test__giving_name_and_resource__should_return_None(
            self, mock_instance, resource_name, resource):
        result = ResourceProviderRegister.mass_register(
                mock_instance, {resource_name: resource})
        assert result is None

    def test__giving_n_names_and_resources__should_call_register_instance_n_times(
            self, mock_instance):
        result = ResourceProviderRegister.mass_register(
                mock_instance,
                {
                    'test.resource.name.1': 'resource1',
                    'test.resource.name.2': 'resource2',
                    'test.resource.name.3': 'resource3',
                })

        assert len(mock_instance.method_calls) == 3
        assert ('register_instance', ('test.resource.name.1', 'resource1'), {}
                ) in mock_instance.method_calls
        assert ('register_instance', ('test.resource.name.2', 'resource2'), {}
                ) in mock_instance.method_calls
        assert ('register_instance', ('test.resource.name.3', 'resource3'), {}
                ) in mock_instance.method_calls

    def test__giving_n_names_and_resources__should_return_None(
            self, mock_instance):
        result = ResourceProviderRegister.mass_register(
                mock_instance,
                {
                    'test.resource.name.1': 'resource1',
                    'test.resource.name.2': 'resource2',
                    'test.resource.name.3': 'resource3',
                })
        assert result is None

    def test__giving_kwargs__should_call_register_instance_with_kwargs(
            self, mock_instance):

        given_kwargs = dict(a=1, b=2)

        result = ResourceProviderRegister.mass_register(
                mock_instance,
                {
                    'test.resource.name.1': 'resource1',
                    'test.resource.name.2': 'resource2',
                    'test.resource.name.3': 'resource3',
                },
                **given_kwargs)

        for call in mock_instance.method_calls:
            method, args, kwargs = call
            assert kwargs == given_kwargs, (
                    '{!r} should have had keyword arguments {!r}'.format(
                        call, given_kwargs))

class Test_ResourceProviderRegister_load:

    def test__giving_other_register__should_load_resources(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.3': 'new resource',
        }

        ResourceProviderRegister.load(mock_instance, other_instance)

        assert mock_instance.resource_providers == {
                'test.resource.name.1': 'old resource',
                'test.resource.name.3': 'new resource',
        }

    def test__giving_register_with_common_keys__should_raise(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }

        with pytest.raises(FangError):
            ResourceProviderRegister.load(mock_instance, other_instance)

    def test__giving_register_with_common_keys__should_not_update(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }

        try:
            ResourceProviderRegister.load(
                    mock_instance, other_instance, allow_overrides=False)
        except FangError as e:
            pass

        assert mock_instance.resource_providers == {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }

    def test__giving_register_with_common_keys_allow_overrides_False__should_raise(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }

        with pytest.raises(FangError):
            ResourceProviderRegister.load(
                    mock_instance, other_instance, allow_overrides=False)

    def test__giving_register_with_common_keys_allow_overrides_False__should_not_update(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }

        try:
            ResourceProviderRegister.load(
                    mock_instance, other_instance, allow_overrides=False)
        except FangError as e:
            pass

        assert mock_instance.resource_providers == {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }

    def test__giving_register_with_common_keys_allow_overrides_True__should_override(
            self, mock_instance, other_instance):
        mock_instance.resource_providers = {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'old resource',
        }
        other_instance.resource_providers = {
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }

        ResourceProviderRegister.load(
                mock_instance, other_instance, allow_overrides=True)

        assert mock_instance.resource_providers == {
                'test.resource.name.1': 'old resource',
                'test.resource.name.2': 'new resource',
                'test.resource.name.3': 'new resource',
        }, 'resource_providers should have been overriden with new resources'
