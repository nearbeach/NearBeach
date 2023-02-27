describe("Test All Logins for each Test User", () => {
	//The following tests will make sure that every user can log in.

	//Before each - we need to make sure the users are logged out.
	beforeEach(() => {
		cy.visit("http://localhost:8000/logout");
	});

	//Admin user logs in
	it("Admin User Logs In", () => {
		//Go to the login page
		cy.visit("http://localhost:8000");
		cy.url().should("include", "/login");

		//Type in the user details
		cy.get("#id_username").type("admin");

		cy.get("#id_password").type("Test1234$");

		//Submit the form
		cy.get("form").submit();

		//Make sure the user is logged in
		cy.getCookie("sessionid").should("exist");
	});

	//Team Leader user logs in
	it("Team Leader Logs In", () => {
		//Go to the login page
		cy.visit("http://localhost:8000");
		cy.url().should("include", "/login");

		//Type in the user details
		cy.get("#id_username").type("team_leader");

		cy.get("#id_password").type("Test1234$");

		//Submit the form
		cy.get("form").submit();

		//Make sure the user is logged in
		cy.getCookie("sessionid").should("exist");
	});

	//team_member user logs in
	it("Team Member User Logs In", () => {
		//Go to the login page
		cy.visit("http://localhost:8000");
		cy.url().should("include", "/login");

		//Type in the user details
		cy.get("#id_username").type("team_member");

		cy.get("#id_password").type("Test1234$");

		//Submit the form
		cy.get("form").submit();

		//Make sure the user is logged in
		cy.getCookie("sessionid").should("exist");
	});

	// Team Intern
	it("Team Intern User Logs In", () => {
		//Go to the login page
		cy.visit("http://localhost:8000");
		cy.url().should("include", "/login");

		//Type in the user details
		cy.get("#id_username").type("team_intern");

		cy.get("#id_password").type("Test1234$");

		//Submit the form
		cy.get("form").submit();

		//Make sure the user is logged in
		cy.getCookie("sessionid").should("exist");
	});

	// Read Only
	it("Read Only User Logs In", () => {
		//Go to the login page
		cy.visit("http://localhost:8000");
		cy.url().should("include", "/login");

		//Type in the user details
		cy.get("#id_username").type("read_only");

		cy.get("#id_password").type("Test1234$");

		//Submit the form
		cy.get("form").submit();

		//Make sure the user is logged in
		cy.getCookie("sessionid").should("exist");
	});
});
