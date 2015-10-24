Feature: DependencyRegister._register_dependent
    A method to register a dependent needing a named resource.

Scenario: Giving a dependent and a resource name
    Given I am testing the _register_dependent method of DependencyRegister
    When I call the method with:
        a fake dependent
        a fake resource name
    Then it should succeed

Scenario: Giving a dependent not in dependents
    Given I am testing the _register_dependent method of DependencyRegister
    When I call the method with:
        a fake dependent not in dependents
        a fake resource name
    Then the fake dependent should be in dependents
