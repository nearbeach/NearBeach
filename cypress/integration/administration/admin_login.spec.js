describe('My First Test', () => {
  it('finds the content "type"', () => {
    cy.visit('http://localhost:8000');

    cy.url().should('include', '/login');

    cy.get('#id_username')
        .type('admin')
        .should('have.value','admin');

    cy.get('#id_password')
        .type('Test1234')
        .should('have.value','Test1234');

    cy.get('.btn').click();
  })
})
