Feature: DependencyRegister._register_resource_dependency
    A method to register that named resource is needed by a dependent

Background:
    Given I am testing the _register_resource_dependency method of DependencyRegister

Scenario: Giving resource name and a dependent
    When I call the method with:
        a fake resource name
        a fake dependent
    Then it should succeed

Scenario: Registering a resource name not in resources, resource should be added
    When I call the method with:
        a fake resource name not in resources
        a fake dependent
    Then the fake resource name should be in resources

Scenario: Registering a resource name not in resources, dependent should be added
    When I call the method with:
        a fake resource name not in resources
        a fake dependent
    Then the fake dependent should be registered as needing the fake resource

Scenario: Registering for a resource already in resources, dependent should be added
    When I call the method with:
        a fake resource name in resources
        a fake dependent
    Then the fake dependent should be registered as needing the fake resource
