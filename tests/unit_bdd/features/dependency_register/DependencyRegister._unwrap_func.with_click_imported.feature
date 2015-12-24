Feature: DependencyRegister._unwrap_func
    An internal class method to help unwrap decorators around functions

Background:
    Given I am testing the _unwrap_func class-method of DependencyRegister
    Given I have the click module imported

Scenario: Calling with an undecorated function
    When I call the method with:
        an undecorated function
    Then the result should be the undecorated function

Scenario: Callling with a decorated function (should make recursive call)
    When I call the method with:
        a decorated function
    Then the method _unwrap_func should be called with:
        the undecorated function

Scenario: Callling with a decorated function (should return result of recursive call)
    When I call the method with:
        a decorated function
    Then the result should be the return value of method _unwrap_func

Scenario: Callling with a click Command
    When I call the method with:
        a click Command
    Then the method _unwrap_func should be called with:
        the click Command's callback