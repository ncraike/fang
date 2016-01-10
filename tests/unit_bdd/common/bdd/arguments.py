from .argument_system import argument_line

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

argument_line('a click Command')(
        a_click_Command)

argument_line("the click Command's callback")(
        click_Commands_callback)
