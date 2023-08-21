// The following test will make sure that the team_leader can;
// 1. Create a new organisation
// 2. Edit an existing organisation

describe("Team Leader - Shakeout Organisation", () => {
	// Before running tests - we have to make sure the admin user is logged in
	before(() => {
		cy.login("team_leader", "Test1234$");

		cy.getCookie("sessionid").should("exist");
		cy.getCookie("csrftoken").should("exist");
	});

	//Making sure we still have the sessionid and csrftoken
	beforeEach(() => {
		Cypress.Cookies.preserveOnce("sessionid", "csrftoken");
	});

	//Go to the new_organisation page
	it("Team Leader goes to the new organisation page", () => {
		cy.visit("http://localhost:8000/new_organisation/");
		cy.get("h1").should("have.text", "New Organisation");
	});

	it("Team Leader can not submit blank results", () => {
		//User clicks on the submit button
		cy.get(".col-md-12 > .btn").click();

		//User checks to make sure they are given a warning
		cy.get("#errorModalContent").contains(
			"FORM ISSUE: Sorry, but can you please fill out the form completely."
		);

		//Wait a fraction of a second, then close the modal
		cy.wait(500);
		cy.get(".modal-footer > .btn").click();

		//User checks to make sure all errors are present
		cy.get(".col-md-8 > :nth-child(1) > label > .error")
			.invoke("html")
			.should("contain", " Please suppy a title");

		cy.get(".row > :nth-child(1) > label > .error")
			.invoke("html")
			.should("contains", "Please supply");

		cy.get(":nth-child(2) > label > .error")
			.invoke("html")
			.should("contains", "Please supply");
	});

	it("Team Leader will fill out all fields with the word 'NearBeach'", () => {
		//User types in Jargon for all fields
		cy.get("#id_organisation_name").type("NearBeach");
		cy.get("#id_organisation_website").type("NearBeach");
		cy.get("#id_organisation_email").type("NearBeach");

		//Check to make sure team leader gets errors for both Website + Email
		cy.get(".row > :nth-child(1) > label > .error")
			.invoke("html")
			.should("contains", "Please format at URL");

		cy.get(":nth-child(2) > label > .error")
			.invoke("html")
			.should("contains", "Please format as Email");
	});

	it("Team Leader will please in correct information into fields", () => {
		cy.get("#id_organisation_website")
			.clear()
			.type("https://nearbeach.org");
		cy.get("#id_organisation_email").clear().type("support@nearbeach.org");

		//Test to make sure the errors no longer exist
		cy.get(".row > :nth-child(1) > label > .error").should("not.exist");

		cy.get(":nth-child(2) > label > .error").should("not.exist");
	});

	it("The Team Leader will submit the organisation and be notified about the duplicate", () => {
		cy.get(".col-md-12 > .btn").click();

		//Wait a fraction of a section
		cy.wait(1000);

		//Check to make sure there is the duplicate card system
		cy.get(".card-body")
			.invoke("html")
			.should("contains", "Potential Duplication");
	});

	it("The Team Leader will now modify the form - and submit", () => {
		cy.get("#id_organisation_name").clear().type("Example Organisation");

		cy.get("#id_organisation_website").clear().type("https://example.com");

		cy.get("#id_organisation_email").clear().type("contact@example.com");

		//User submits organisation and waits for page to load
		cy.get(".col-md-12 > .btn").click();
		cy.wait(1000);
		cy.wait(200);

		//User checks the URL for organisation_information
		cy.url().should("contain", "/organisation_information/");
	});

	it("Team Leader appends data onto the attributes of the Organisation", () => {
		cy.get("#id_organisation_name").type(" EDIT");

		cy.get("#id_organisation_website").type(".edit");

		cy.get("#id_organisation_email").type(".edit");

		//User submits organisation and waits for page to load
		cy.get(".card-body > .submit-row > .col-md-12 > .btn").click();
		cy.get("#loadingModal").click();
		cy.wait(1000);
		cy.reload();

		//User checks the results
		cy.get("#id_organisation_name").should(
			"have.value",
			"Example Organisation EDIT"
		);

		cy.get("#id_organisation_website").should(
			"have.value",
			"https://example.com.edit"
		);

		cy.get("#id_organisation_email").should(
			"have.value",
			"contact@example.com.edit"
		);
	});

	it("Team Leader will add a note to the organisation", () => {
		//User will reload the page
		cy.reload();

		//User will click on the "Misc" button below
		cy.get("#misc-modules-tab").click();

		//User will click on the "Add Note" button
		cy.get(
			'#misc-modules > [data-v-ce8eeb0a=""] > .row > .col-md-12 > .btn'
		).click();
		cy.wait(500);

		//User fills out the iframe of tiny mouse.
		cy.get("iframe[class=tox-edit-area__iframe]").then((iframe) => {
			const body = iframe.contents().find("body");
			cy.wrap(body)
				//The text is paste into tinymce as plaintext.
				.type("This is a simple note");
		});

		//User click on the "Submit" button to submit the note
		cy.get(
			"#newNoteModal > .modal-dialog > .modal-content > .modal-footer > .btn-primary"
		).click();

		//User checks to make sure the note was saved
		cy.get("#misc-modules")
			.invoke("html")
			.should("contains", "This is a simple note");
	});

	it("Team Leader will create a new contact on the organisation information page", () => {
		//User click on the "Organisation Contacts" tab
		cy.get("#organisation-contacts-tab").click();

		//User click on the "Add Contact" button
		cy.get("#organisation-contacts > .row > .col-md-12 > .btn").click();
		cy.wait(500);

		//NOTE TO DO - SELECT TITLE
		//User will search for the title Mx - and select it
		cy.get("#vs1__combobox > .vs__selected-options > .vs__search").type(
			"Mx{enter}"
		);

		cy.get(".col-sm-4 > .form-control").type("Contact");
		cy.get(".col-sm-5 > .form-control").type("Example");
		cy.get(".col-sm-8 > .form-control").type("contact.example@example.com");

		//User click on the submit button
		cy.get(
			"#addCustomerModal > .modal-dialog > .modal-content > .modal-footer > .btn-primary"
		).click();
		cy.wait(1000);

		//Check that the URL contains customer_information
		cy.url().should("contains", "/customer_information/");
	});
});
