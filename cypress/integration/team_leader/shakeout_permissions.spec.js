/*This test will visit pages that
1. Team Leader CAN access
2. Team Leader CAN NOT access
And we want to see the outcome
*/

describe("Shakeout Project", () => {
  // Before running tests - we have to make sure the admin user is logged in
  before(() => {
    cy.login('team_leader','Test1234$');

    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
  });

  //Making sure we still have the sessionid and csrftoken
  beforeEach(() => {
    Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
  });

  it('Permission Checking on Projects', () => {
    //User goes to Project 1 -> is allowed access
    cy.visit('http://localhost:8000/project_information/1');
    cy.get('h1').should('have.text','Project Information');

    //User goes to Project 2 -> is denied access
    cy.visit('http://localhost:8000/project_information/2/', {
      failOnStatusCode: false,
    });
    cy.get('h1').should('have.text','403 - Access Denied');
  });

  it('Permission Checking on Tasks', () => {
    //User goes to Task 1 -> is allowed access
    cy.visit('http://localhost:8000/task_information/1/');
    cy.get('h1').should('have.text','Task Information');

    //User goes to Task 2 -> is denied access
    cy.visit('http://localhost:8000/task_information/2/', {
      failOnStatusCode: false,
    });
    cy.get('h1').should('have.text','403 - Access Denied');
  })

  it('Permission Checking on Requirements', () => {
    //User goes to Requirement 1 -> is allowed access
    cy.visit('http://localhost:8000/requirement_information/1/');
    cy.get('h1').should('have.text', 'Requirement Information');

    //User goes to Requirement 2 -> is denied access
    cy.visit('http://localhost:8000/requirement_information/2/', {
      failOnStatusCode: false,
    });
    cy.get('h1').should('have.text','403 - Access Denied');
  });

  it('Permission Checking on RFC', () => {
    //User goes to Requirement 1 -> is allowed access
    cy.visit('http://localhost:8000/rfc_information/1/');
    cy.get('h1').should('have.text', 'Requirement Information');

    //User goes to Requirement 2 -> is denied access
    cy.visit('http://localhost:8000/rfc_information/2/', {
      failOnStatusCode: false,
    });
    cy.get('h1').should('have.text','403 - Access Denied');
  });

  it('Permission Checking on Kanban', () => {
    //User goes to Kanban 1 -> is allowed access
    cy.visit('http://localhost:8000/kanban_information/1/')
    cy.get('h1').should('have.text','QA Team Kanban Board');

    //User goes to Kanban 2 -> is denied access
    cy.visit('http://localhost:8000/kanban_information/2/', {
      failOnStatusCode: false,
    });
    cy.get('h1').should('have.text','403 - Access Denied');
  });
});
