// Global Test Variables
let project_title = 'Automatic Project Creation - by administrator',
    project_description = `Automatic Testing with Cypress - writing in a simple description`;

describe("Shakeout Project", () => {
  // Before running tests - we have to make sure the admin user is logged in
  before(() => {
    cy.visit("http://localhost:8000/");
    cy.get("[name=csrfmiddlewaretoken]")
      .should("exist")
      .should("have.attr", "value")
      .as("csrfToken");

    cy.get("@csrfToken").then((token) => {
      cy.request({
        method: "POST",
        url: "/login",
        form: true,
        body: {
          username: "admin",
          password: "Test1234$",
        },
        headers: {
          "X-CSRFTOKEN": token,
        },
      });
    });

    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
  });

  //Making sure we still have the sessionid and csrftoken
  beforeEach(() => {
    Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
  });

  // NEW PROJECT TEST
  it("New Project Test", () => {
    // User goes to the dashboard
    cy.visit('http://localhost:8000/');

    //User navigates the menu #newObjectsDropdown
    cy.get('#newObjectsDropdown').click();
    cy.get(':nth-child(4) > .dropdown-item').click();

    //User confirms they are now at the correct place
    cy.url().should('include', '/new_project/');

    //User clicks on the "Create New Project" button
    cy.get('.col-md-12 > .btn')
        .type('Create New Project');

    //User checks to make sure they are given a warning
    cy.get('#errorModalContent')
        .contains('FORM ISSUE: Sorry, but can you please fill out the form completely.')

    //User closes the error modal
    cy.get('.modal-footer > .btn').click();

    //User now checks out all the errors on the page now
    cy.contains('Please suppy a title.');
    cy.contains('Please supply a description');
    cy.contains('Please search for a Stakeholder.');
    cy.contains('Please select at least one group.');

    //User starts to fill in the form
    cy.get('.form-group > .form-control')
        .type(project_title);

    //User fills out the iframe of tiny mouse.
    cy.get("iframe[class=tox-edit-area__iframe]").then(iframe => {
      const body = iframe.contents().find('body');
      cy.wrap(body)
          //The text is paste into tinymce as plaintext.
          .type(project_description);
    });

    // User searches for NearBeach in the organisation search bar
    cy.get('#vs1__combobox > .vs__selected-options > .vs__search')
        .type("NearBeach");

    // User selects first option (which should be NearBeach) from the dropdown box
    cy.get("#vs1__listbox").click();

    //Navigate through the start calendar options to find the correct date
    cy.get(':nth-child(2) > .form-group > .vdatetime > .vdatetime-input').click();
    cy.get('.vdatetime-popup__year').click();
    cy.get(':nth-child(100)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get('.vdatetime-popup__date').click();
    cy.get('.vdatetime-month-picker__list > :nth-child(1)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get(':nth-child(10) > :nth-child(1) > span').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get('.vdatetime-time-picker__list--hours > :nth-child(9)').click();
    cy.get('.vdatetime-time-picker__list--minutes > :nth-child(7)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();

    //Check to make sure the dates are correct
    cy.get(':nth-child(2) > .form-group > .vdatetime > .vdatetime-input')
        .should('have.value','1 Jan 2020, 08:30');

    //TODO: Need to find out how to check the time value.
    //Navigate through the end calendar options to find the correct date
    cy.get(':nth-child(3) > .form-group > .vdatetime > .vdatetime-input').click();
    cy.get('.vdatetime-popup__year').click();
    cy.get(':nth-child(100)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get('.vdatetime-popup__date').click();
    cy.get('.vdatetime-month-picker__list > :nth-child(12)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get(':nth-child(39) > :nth-child(1) > span').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();
    cy.get('.vdatetime-time-picker__list--hours > :nth-child(18)').click();
    cy.get('.vdatetime-time-picker__list--minutes > :nth-child(1)').click();
    cy.get('.vdatetime-popup__actions__button--confirm').click();

    cy.get(':nth-child(3) > .form-group > .vdatetime > .vdatetime-input')
        .should('have.value', '31 Dec 2020, 17:00');

    //Get the group lists
    cy.get('#vs2__combobox > .vs__selected-options > .vs__search')
        .type('QA Team{enter}Admin{enter}');

    //Save the data
    cy.get('.save-changes').click();
  })

  // Check the data created in the previous step
  it("Read the current project", () => {
    //User confirms they are now at the correct place
    cy.url().should('include', '/project_information/');

    //Now check the fields
    cy.get(':nth-child(3) > .col-md-8 > .form-group > .form-control')
        .should('have.value', project_title);

    //Check to make sure the project status is NEW
    //cy.get('.vs__selected')
    cy.get('#vs1__combobox')
        .contains('New');
        // .should('have.text', '\n New\n           ');

    // cy.get('.organisation_name')
    cy.get('.organisation-name > a')
        .contains('NearBeach Organisation')

    cy.get(':nth-child(2) > .form-group > .vdatetime > .vdatetime-input')
        .should('have.value', '1 Jan 2020, 08:30');

    cy.get(':nth-child(3) > .form-group > .vdatetime > .vdatetime-input')
        .should('have.value', '31 Dec 2020, 17:00');
  })
});


