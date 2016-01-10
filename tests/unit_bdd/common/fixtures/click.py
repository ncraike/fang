
from types import ModuleType

import pytest

# fake click.Command
class Command:
    '''A fake click.Command class which just implements behaviour we
    need for tests.'''

    def __init__(self, function_to_wrap):
        self.callback = function_to_wrap

def Command_callback():
    return 'This is the callback for a fake click.Command instance'

@pytest.fixture
def fake_click_module():
    click = ModuleType('click')
    click.Command = Command
    return click

@pytest.fixture
def a_click_Command(pytest_request=None):
    return Command(Command_callback)

@pytest.fixture
def click_Commands_callback(pytest_request):
    return Command_callback
