Feature: DependencyRegister._register_dependent
    A method to register a dependent needing a named resource.

Scenario: Giving a dependent and a resource name
    Given I'm an author user
    And I have an article
    When I go to the article page
    And I press the publish button
    Then I should not see the error message
    And the article should be published  # Note: will query the database
