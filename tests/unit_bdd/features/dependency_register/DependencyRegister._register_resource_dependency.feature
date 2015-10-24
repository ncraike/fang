Feature: DependencyRegister._register_resource_dependency
    A method to register that named resource is needed by a dependent

Background:
    Given I am testing the _register_resource_dependency method of DependencyRegister

Scenario: Giving a dependent and a resource name
    When I call the method with:
        a fake resource name
        a fake dependent
    Then it should succeed
