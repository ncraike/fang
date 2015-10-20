Feature: DependencyRegister._register_dependent
    A method to register a dependent needing a named resource.

Scenario: Giving a dependent and a resource name
    Given I am testing the _register_dependent method of DependencyRegister
    And I have a fake dependent
    And I have a fake resource name
    When I call the method
    Then it should succeed
