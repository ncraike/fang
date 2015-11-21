Feature: DependencyRegister._unwrap_func
    An internal class method to help unwrap decorators around functions

Background:
    Given I am testing the _unwrap_func class-method of DependencyRegister

Scenario: Calling with an undecorated function
    When I call the method with:
        an undecorated function
    Then the result should be the undecorated function
