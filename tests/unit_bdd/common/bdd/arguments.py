from .argument_system import argument_line

from ..fixtures.dependents import (
        fake_dependent,
        fake_dependent_which_is_a_class)

argument_line('a dependent')(
        fake_dependent)

argument_line('a dependent which is a class')(
        fake_dependent_which_is_a_class)
