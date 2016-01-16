from .argument_system import argument_line

from ..fixtures.general import (
        a_none_value,
        an_undecorated_function,
        a_decorated_function)
from ..fixtures.click import (
        fake_click_module,
        a_click_Command,
        click_Commands_callback)
from ..fixtures.dependents import (
        fake_dependent,
        fake_dependent_which_is_a_class)
from ..fixtures.resources import (
        fake_resource_name)

argument_line('a dependent')(
        fake_dependent)

argument_line('a dependent which is a class')(
        fake_dependent_which_is_a_class)

argument_line('a resource name')(
        fake_resource_name)
argument_line('the resource name')(
        fake_resource_name)

argument_line('a None value')(
        a_none_value)

argument_line('a click Command')(
        a_click_Command)

argument_line("the click Command's callback")(
        click_Commands_callback)

argument_line('an undecorated function')(
    an_undecorated_function)
argument_line('the undecorated function')(
    an_undecorated_function)

argument_line('a decorated function')(
        a_decorated_function)
argument_line('the decorated function')(
        a_decorated_function)
