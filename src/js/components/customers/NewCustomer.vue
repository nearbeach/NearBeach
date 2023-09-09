<template>
  <n-config-provider :theme="getTheme(theme)">
	<div class="card">
		<div class="card-body">
			<!-- HEADER -->
			<h1>New Customer</h1>
			<hr />

			New Customer Form
			<new-customer-form
				v-bind:organisation-name="organisationName"
				v-bind:title-list="titleList"
				v-bind:flag-validation-check="flagValidationCheck"
				v-on:update_customer_data="updateCustomerData($event)"
			></new-customer-form>

			<!-- CUSTOMER ORGANISATION -->
			<hr />
			<div class="row">
				<div class="col-md-4">
					<strong>Customer Organisation</strong>
					<p class="text-instructions">
						This field is optional. If this customer does not have
						any organisations attached, it will treat this customer
						as a freelancer.
					</p>
				</div>
				<div class="col-md-8">
					<div class="form-group col-sm-8">
						<label>Organisation:</label>
						<n-select
							:options="organisationFixList"
							filterable
							placeholder="Search Organisations"
							@search="fetchOptions"
							v-model:value="organisationModel"
							label="organisation_name"
							class="get-stakeholders"
						/>
					</div>
				</div>
			</div>

			<!-- REMEMBER TO ADD IN USER PERMISSIONS HERE!! -->
			<!-- Submit Button -->
			<hr />
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						href="javascript:void(0)"
						class="btn btn-primary save-changes"
						v-on:click="submitNewCustomer"
						>Submit Customer</a
					>
				</div>
			</div>
		</div>
	</div>
  </n-config-provider>
</template>

<script>
	import axios from "axios";
	import { Modal } from "bootstrap";

	//Validation
	import useVuelidate from "@vuelidate/core";
	import { required, email } from "@vuelidate/validators";

	//Mixins
	import errorModalMixin from "../../mixins/errorModalMixin";
  import getThemeMixin from "../../mixins/getThemeMixin";
	import searchMixin from "../../mixins/searchMixin";

	//Components
	import NewCustomerForm from "./NewCustomerForm.vue";
	import { NSelect } from "naive-ui";

	export default {
		name: "NewCustomer",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			NewCustomerForm,
			NSelect,
		},
		inject: [
			'nextTick',
		],
		props: {
			organisationName: {
				type: String,
				default: "",
			},
			rootUrl: {
				type: String,
				default: "/",
			},
      theme: {
        type: String,
        default: "",
      },
			titleList: {
				type: Array,
				default() {
					return [];
				},
			},
		},
		mixins: [errorModalMixin, getThemeMixin, searchMixin],
		data() {
			return {
				customerEmailModel: "",
				customerFirstNameModel: "",
				customerLastNameModel: "",
				flagValidationCheck: false,
				organisationFixList: [],
				organisationModel: "",
				titleModel: [],
			};
		},
		validations() {
			return {
				customerEmailModel: {
					required,
					email,
				},
				customerFirstNameModel: {
					required,
				},
				customerLastNameModel: {
					required,
				},
				titleModel: {
					required,
				},
			};
		},
		methods: {
			fetchOptions(search, loading) {
				this.searchTrigger({
					return_function: this.getOrganisationData,
					searchTimeout: this.searchTimeout,
					search: search,
					loading: loading,
				});
			},
			getOrganisationData(search, loading) {
				// Save the seach data in FormData
				const data_to_send = new FormData();
				data_to_send.set("search", search);

				// Now that the timer has run out, lets use AJAX to get the organisations.
				axios
					.post(
						`${this.rootUrl}search/organisation/data/`,
						data_to_send
					)
					.then((response) => {
						//Extract the required JSON data
						var extracted_data = response.data;

						//Look through the extracted data - and map the required fields into stakeholder fix list
						this.organisationFixList = extracted_data.map((row) => {
							//Create the creation object
							return {
								value: row.pk,
								label: row.fields.organisation_name,
							};
						});
					})
					.catch(function (error) {
						// Get the error modal
						var elem_cont =
							document.getElementById("errorModalContent");

						// Update the content
						elem_cont.innerHTML = `<strong>Search Organisation Issue:</strong><br/>${error}`;

						// Show the modal
						var errorModal = new Modal(
							document.getElementById("errorModal"),
							{
								keyboard: false,
							}
						);
						errorModal.show();

						// Hide the loader
						var loader_element = document.getElementById("loader");
						loader_element.style.display = "none";
					});
			},
			submitNewCustomer: async function () {
				//Flag downstream to check validation
				this.flagValidationCheck = true;

				//Reset this check after 100ms
				setTimeout(() => {
					this.flagValidationCheck = false;
				}, 100);

				// Check the validation at this level
				this.v$.$touch();

				// Check the validation at this level
				const hasFormErrors = await this.v$.$validate();

				//NEED TO USE MIXIN FOR THIS SECTION
				if (!hasFormErrors) {
					//Show the error dialog and notify to the user that there were field missing.
					var elem_cont =
						document.getElementById("errorModalContent");

					// Update the content
					elem_cont.innerHTML = `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

					// Show the modal
					var errorModal = new Modal(
						document.getElementById("errorModal")
					);
					errorModal.show();

					//Just return - as we do not need to do the rest of this function
					return;
				}

				//Create the data_to_send
				const data_to_send = new FormData();
				data_to_send.set("customer_title", this.titleModel);
				data_to_send.set(
					"customer_first_name",
					this.customerFirstNameModel
				);
				data_to_send.set(
					"customer_last_name",
					this.customerLastNameModel
				);
				data_to_send.set("customer_email", this.customerEmailModel);

				//If there is an organisation in the model - send it
				if (
					this.organisationModel !== "" &&
					this.organisationModel !== null
				) {
					data_to_send.set("organisation", this.organisationModel);
				}

				//Send the data using axios
				axios
					.post(`${this.rootUrl}new_customer/save/`, data_to_send)
					.then((response) => {
						//Go to the new customer page
						window.location.href = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, "customer", "");
					});
			},
			updateCustomerData(data) {
				//Update the modal field with the value data
				this[data.field] = data.value;
			},
		},
		mounted() {
			//Get a default list when mounted
			this.nextTick(() => {
				this.getOrganisationData("", "");
			});
		},
	};
</script>

<style scoped></style>
