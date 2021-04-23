// The following will make sure the team_leader does not have access to certain menu items
// All menu items have been tested at the administration level

describe("Shakeout Menu", () => {
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

  //Make sure the administration menu does not exist
  it("Check no admin menu", () => {
      //Go to dashboard
      cy.visit('http://localhost:8000/');

      //Make sure the administration drop down does not exist
      cy.get('#administrationDropdown')
        .should('not.exist');
  })
})
