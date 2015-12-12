Feature: DependencyRegister.query_resources
    A method to query the resources needed by a dependent

Background:
    Given I am testing the query_resources method of DependencyRegister

Scenario: Calling with dependent (should call _unwrap_dependent)
    Given I am ignoring all exceptions during the method call
    When I call the method with:
        a dependent
    Then the method _unwrap_dependent should be called with:
        a dependent

Scenario: Calling with a dependent not in dependents
    Given the method _unwrap_dependent will return its one argument unchanged
    When I call the method with:
        a dependent not in dependents
    Then the exception DependentNotFoundError should be raised

Scenario: Calling with a dependent in dependents (query resources)
    Given the method _unwrap_dependent will return its one argument unchanged
    When I call the method with:
        a dependent in dependents
    Then the result should contain:
        a resource name
