Feature: DependencyRegister.__init__
    Initialisation of a new DependencyRegister instance

Background:
    Given I am testing the creation of a new DependencyRegister instance

Scenario: dependents attribute is initialised
    When a new instance is created
    Then the dependents attribute should be empty
