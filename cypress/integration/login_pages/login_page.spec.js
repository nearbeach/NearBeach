describe('Go to the login page', () => {
    it('User goes to the login page - keys in the login details - gets logged in', () => {
        cy.visit('http://localhost:8000');

        cy.url().should('include', '/login');

        cy.get('#id_username')
            .type('admin');

        cy.get('#id_password')
            .type('Test1234$');

        cy.get("form").submit();

        cy.getCookie("sessionid").should("exist");
    });
})