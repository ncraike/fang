Feature: DependencyRegister._register_dependent
    A method to register that a dependent needs a named resource.

Background:
    Given I am testing the _register_dependent method of DependencyRegister

Scenario: Giving a dependent and a resource name
    When I call the method with:
        a dependent
        a resource name
    Then it should succeed

Scenario: Registering for a dependent not in dependents, dependent should be added
    When I call the method with:
        a dependent not in dependents
        a resource name
    Then the dependent should be in dependents

Scenario: Registering for a dependent not in dependents, resource should be added
    When I call the method with:
        a dependent not in dependents
        a resource name
    Then the resource name should be registered for the dependent

Scenario: Registering for a dependent already in dependents, resource should be added
    When I call the method with:
        a dependent in dependents
        a resource name
    Then the resource name should be registered for the dependent
