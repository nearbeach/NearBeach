// The following tests will test to make sure the admin can edit groups

describe("Shakeout Group -> as Admin", () => {
  // Before running tests - we have to make sure the admin user is logged in
  before(() => {
    cy.login('admin','Test1234$');

    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
  });

  //Making sure we still have the sessionid and csrftoken
  beforeEach(() => {
    Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
  });

  it("Go to the Group Search", () => {
    cy.visit('http://localhost:8000/search/group/');

    cy.get("h1").should('have.text','Search Groups');
  });

  it("Search for 'Empty Group' -> make sure it is the only group left", () => {
    cy.get('.form-group > .form-control').type("Empty Group");

    cy.wait(1000);

      cy.get('.card-body').should('contain','Empty Group');
      cy.get('.card-body').should('not.contain','Administration');
      cy.get('.card-body').should('not.contain','QA Team');
    });

  it("Clear the search -> add groups should appear", () => {
    cy.get('.form-group > .form-control').clear();

    cy.wait(1000);

    cy.get('.card-body').should('contain','Empty Group');
    cy.get('.card-body').should('contain','Administration');
    cy.get('.card-body').should('contain','QA Team');
  });

  it("Click on the 'Add Group' button and start adding a new group", () => {
    cy.get('.col-md-12 > .btn').click();
    cy.url().should('contain', '/new_group/');

    // User enters in an existing group name
    cy.get('.col-md-8 > :nth-child(1) > .form-control').type('QA Team');
    cy.wait(1000);

    // User is informed that that group name already exists
    cy.get('.error').should('contain','Please supply a unique name');

    // User enters in an existing group name -> different permutation
    cy.get('.col-md-8 > :nth-child(1) > .form-control').clear().type('qa tEAM');
    cy.wait(1000);

    // User is informed that that group name already exists
    cy.get('.error').should('contain','Please supply a unique name');

    // User is determined to create the group - but is rejected by the system
    cy.get('.col-md-12 > .btn').click();

    // User is shown an error modal
    cy.get('#errorModalContent')
      .should(
        'contain',
        'FORM ISSUE: Sorry, but can you please fill out the form completely.'
      );
    cy.wait(200);

    // User closes the error modal
    cy.get('.modal-footer > .btn').click().click();

    // User is now determined to user a new unique name
    let group_name = `A Unique Named Group ${Math.random().toString().substr(2, 8)}`;
    cy.get('.col-md-8 > :nth-child(1) > .form-control')
      .clear()
      .type(group_name);
    
    cy.wait(1000);

    // User decides to add 'QA Team' as the parent
    cy.get('.vs__search').type('QA Team{enter}');
    cy.wait(100);

    //User can now create the group
    cy.get('.col-md-12 > .btn').click();

    cy.url().should('contain','group_information');

    // User checks the values of the group name and parent group
    cy.get('.col-md-8 > :nth-child(1) > .form-control')
      .should('have.value',group_name);

    cy.get('.col-md-8 > :nth-child(2) > .v-select')
      .should('contain','QA Team');
  });
});
