Feature: DependencyRegister._unwrap_dependent
    An internal class method to help unwrap decorators, etc for given dependents

Background:
    Given I am testing the _unwrap_dependent class-method of DependencyRegister

Scenario: Calling with class dependent
    When I call the method with:
        a fake dependent which is a class
    Then the result should be a fake dependent which is a class
