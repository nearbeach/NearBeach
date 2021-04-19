describe("Authenticated sections", () => {
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
          username: "team_leader",
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

  beforeEach(() => {
    Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
  });

  it("should do something", () => {
    cy.visit('http://localhost:8000/new_project');

    cy.url().should('include', '/new_project/');
  });

  it("should do something", () => {
    cy.visit('http://localhost:8000/new_task');

    cy.url().should('include', '/new_task/');
  });

  it("Should not be able to go to projects 2", () => {
    cy.request({
      url: 'http://localhost:8000/project_information/2/',
      failOnStatusCode: false
    }).then((response) => {
      expect(response.status).to.eq(403)
    });
  })
});