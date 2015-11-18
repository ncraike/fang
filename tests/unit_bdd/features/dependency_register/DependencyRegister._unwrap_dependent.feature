Feature: DependencyRegister._unwrap_dependent
    An internal class method to help unwrap decorators, etc for given dependents

Background:
    Given I am testing the _unwrap_dependent class-method of DependencyRegister

Scenario: Calling with class dependent
    When I call the method with:
        a fake dependent which is a class
    Then the result should be a fake dependent which is a class

Scenario: Calling with non-class dependent (should call _unwrap_func)
    When I call the method with:
        a fake dependent
    Then the method _unwrap_func should be called with:
        a fake dependent

Scenario: Calling with non-class dependent (should return _unwrap_func result)
    When I call the method with:
        a fake dependent
    Then the result should be the return value of method _unwrap_func
