//The following tests will get the user to click on every menu item

describe("Shakeout Menu -> as Admin", () => {
	// Before running tests - we have to make sure the admin user is logged in
	before(() => {
		cy.login("admin", "Test1234$");

		cy.getCookie("sessionid").should("exist");
		cy.getCookie("csrftoken").should("exist");
	});

	//Making sure we still have the sessionid and csrftoken
	beforeEach(() => {
		Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
	});

	it("Click NearBeach Logo", () => {
		//Go to dashboard
		cy.visit("http://localhost:8000/");

		//Click the NearBeach logo
		cy.get(".navbar-brand").click();

		//Check to make sure we are at the dashboard
		cy.url().should("eq", "http://localhost:8000/");
	});

	it("New Object - items work correctly", () => {
		//Click on "New Objects" - then "New Customer"
		cy.get("#newObjectsDropdown").click();
		cy.get(":nth-child(1) > .dropdown-item").click();
		cy.url().should("contain", "/new_customer/");

		//Click on "New Objects" - then "New Kanban Board"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(2) > .dropdown-item").click();
		cy.url().should("contain", "/new_kanban/");

		//Click on "New Objects" - then "New Organisation"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(3) > .dropdown-item").click();
		cy.url().should("contain", "/new_organisation/");

		//Click on "New Objects" - then "New Project"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(4) > .dropdown-item").click();
		cy.url().should("contain", "/new_project/");

		//Click on "New Objects" - then "New Request for Change"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(5) > .dropdown-item").click();
		cy.url().should("contain", "/new_request_for_change/");

		//Click on "New Objects" - then "New Requirement"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(6) > .dropdown-item").click();
		cy.url().should("contain", "/new_requirement/");

		//Click on "New Objects" - then "New Task"
		cy.get("#newObjectsDropdown").click();
		cy.get(".dropdown-menu > :nth-child(7) > .dropdown-item").click();
		cy.url().should("contain", "/new_task/");
	});

	it("Find Objects", () => {
		//Click on "Find Objects" - then "Find All"
		cy.get("#findObjectsDropdown").click();
		cy.get('[href="/search/"]').click();
		cy.url().should("contain", "/search/");

		//Click on "Find Objects" - then "Find All"
		cy.get("#findObjectsDropdown").click();
		cy.get('[href="/search/customer/"]').click();
		cy.url().should("contain", "/search/customer/");

		//Click on "Find Objects" - then "Find All"
		cy.get("#findObjectsDropdown").click();
		cy.get('[href="/search/organisation/"]').click();
		cy.url().should("contain", "/search/organisation/");
	});

	it("Administration", () => {
		//Click on "Find Objects" - then "Find All"
		cy.get("#administrationDropdown").click();
		cy.get('[href="/search/group/"]').click();
		cy.url().should("contain", "/search/group/");

		//Click on "Find Objects" - then "Find All"
		cy.get("#administrationDropdown").click();
		cy.get('[href="/search/permission_set/"]').click();
		cy.url().should("contain", "/search/permission_set/");

		//Click on "Find Objects" - then "Find All"
		cy.get("#administrationDropdown").click();
		cy.get('[href="/search/user/"]').click();
		cy.url().should("contain", "/search/user/");
	});

	it("Search", () => {
		cy.get("#id_search").type("test{enter}");
		cy.url().should("contain", "/search/");
	});

	it("User", () => {
		//Click on the "User" - then "Logout"
		cy.get("#userDropdown").click();
		cy.get('[href="/logout"]').click();
		cy.url().should("contain", "/login");
	});
});
