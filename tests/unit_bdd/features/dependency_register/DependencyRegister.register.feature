Feature: DependencyRegister.register
    A method to register a dependent depending on a resource

Background:
    Given I am testing the register method of DependencyRegister

Scenario: Calling with dependent as None (should return partial)
    When I call the method with:
        a fake resource name
        a None value
    Then the result should be a partial
    And the resulting partial's function should be the method
    And the resulting partial's arguments should be:
        the fake resource name

Scenario: Calling with dependent as None (should not call any methods)
    When I call the method with:
        a fake resource name
        a None value
    Then no other methods should be called
