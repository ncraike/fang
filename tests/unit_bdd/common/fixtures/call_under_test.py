import pytest

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
