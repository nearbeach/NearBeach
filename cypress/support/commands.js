// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

Cypress.Commands.add('login', (username, password) => {
    //Make sure users are logged out first
    cy.visit("http://localhost:8000/logout");

    //Log the user in (user automatically directed to correct page)
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
          username: username,
          password: password,
        },
        headers: {
          "X-CSRFTOKEN": token,
        },
      });
    });

    cy.getCookie("sessionid").should("exist");
    cy.getCookie("csrftoken").should("exist");
})

Cypress.Commands.add('writeToTinymce', (element_location, text_to_enter) => {
    //The 'element_location' is the location of the iframe
    //i.e. `iframe[class=tox-edit-area__iframe]`
    //We use this to find the body, where we place our text.
    cy.get(element_location).then(iframe => {
        //Get the body inside the iframe
        const body = iframe.contents().find('body');

        //Type inside the body
        cy.wrap(body)
            .type(text_to_enter);
    });
})
