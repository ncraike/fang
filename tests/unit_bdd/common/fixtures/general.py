import pytest

import functools

@pytest.fixture
def a_none_value(**kwargs):
    return None

def _undecorated_function(*args, **kwargs):
    return ('undecorated_function() return value', args, kwargs)

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

@pytest.fixture
def a_decorated_function(pytest_request=None):
    an_undecorated_function = pytest_request.getfuncargvalue(
            'an_undecorated_function')
    return decorator(an_undecorated_function)
