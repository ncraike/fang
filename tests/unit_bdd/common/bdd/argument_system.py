import functools

from pytest_bdd import parsers

arguments = []

def give_argument_value_from_parsing_line(
        argument_line, parser, get_argument_value_func,
        **kwargs_for_arg_factories):
    '''
    This asks the given function for the argument value based on the
    argument line.

    The function is given the dictionary of matches from the
    parser, which it may use to create the argument value.
    '''
    matches = parser.parse_arguments(argument_line)
    kwargs_for_arg_factories.update(matches)
    return get_argument_value_func(**kwargs_for_arg_factories)

def register_argument(pattern_or_parser, get_argument_value_func):
    parser = parsers.get_parser(pattern_or_parser)
    give_argument_value = functools.partial(
            give_argument_value_from_parsing_line,
            parser=parser,
            get_argument_value_func=get_argument_value_func)

    argument_entry = (parser.is_matching, give_argument_value)
    arguments.append(argument_entry)

# For use as decorator
def argument_line(pattern_or_parser):
    def decorator(decorated_func):
        register_argument(pattern_or_parser, decorated_func)
        return decorated_func
    return decorator

def get_argument_from_registered(argument_line, **kwargs_for_arg_factories):
    for (is_matching, give_argument_value) in arguments:
        if is_matching(argument_line):
            return give_argument_value(
                    argument_line, **kwargs_for_arg_factories)
    else:
        raise Exception(
                "Couldn't find a match for argument line: {!r}".format(
                    argument_line))

def parse_argument_lines(lines, **kwargs_for_arg_factories):
    return [
            get_argument_from_registered(line, **kwargs_for_arg_factories)
            for line in lines]

def resolve_arg_lines(lines, request):
    return [get_argument_from_registered(line, pytest_request=request)
            for line in lines.splitlines()]

