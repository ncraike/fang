Feature: DependencyRegister.query_resources
    A method to query the resources needed by a dependent

Background:
    Given I am testing the query_resources method of DependencyRegister

Scenario: Calling with dependent (should call _unwrap_dependent)
    Given I am ignoring all exceptions during the method call
    When I call the method with:
        a fake dependent
    Then the method _unwrap_dependent should be called with:
        a fake dependent
