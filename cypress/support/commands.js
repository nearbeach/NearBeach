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
