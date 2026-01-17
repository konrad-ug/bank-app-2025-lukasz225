Feature: Account registry

  Background:
    Given The account registry is empty

  Scenario: User is able to create 2 accounts
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101012345"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101012345" exists in registry

  Scenario: User is able to update surname of already created account
    Given I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  Scenario: User is able to update name of already created account
    Given I create an account using name: "jan", last name: "kowalski", pesel: "12345678901"
    When I update "name" of account with pesel: "12345678901" to "adam"
    Then Account with pesel "12345678901" has "name" equal to "adam"

  Scenario: Created account has all fields correctly set
    When I create an account using name: "elvis", last name: "presley", pesel: "55010800000"
    Then Account with pesel "55010800000" exists in registry
    And Account with pesel "55010800000" has "name" equal to "elvis"
    And Account with pesel "55010800000" has "surname" equal to "presley"
    And Account with pesel "55010800000" has "balance" equal to "0"

  Scenario: User is able to delete created account
    Given I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: Incoming transfer increases balance
    Given I create an account using name: "elon", last name: "musk", pesel: "88888888888"
    When I make an incoming transfer of "1000" to account with pesel: "88888888888"
    Then Account with pesel "88888888888" has "balance" equal to "1000"

  Scenario: Outgoing transfer decreases balance
    Given I create an account using name: "jeff", last name: "bezos", pesel: "99999999999"
    And I make an incoming transfer of "500" to account with pesel: "99999999999"
    When I make an outgoing transfer of "200" from account with pesel: "99999999999"
    Then Account with pesel "99999999999" has "balance" equal to "300"