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

Scenario: Calling with resource name and dependent (should call _unwrap_dependent)
    When I call the method with:
        a fake resource name
        a fake dependent
    Then the method _unwrap_dependent should be called with:
        a fake dependent

Scenario: Calling with resource name and dependent (should return unwrapped dependent)
    When I call the method with:
        a fake resource name
        a fake dependent
    Then the result should be the return value of method _unwrap_dependent

Scenario: Calling with resource name and dependent (should call _register_dependent)
    When I call the method with:
        a fake resource name
        a fake dependent
    Then the method _register_dependent should be called with:
        the return value of method _unwrap_dependent
        a fake resource name

Scenario: Calling with resource name and dependent (should call _register_resource_dependency)
    When I call the method with:
        a fake resource name
        a fake dependent
    Then the method _register_resource_dependency should be called with:
        a fake resource name
        the return value of method _unwrap_dependent
