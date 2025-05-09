<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<!-- HEADER -->
				<h1>New Customer</h1>
				<hr/>

				New Customer Form
				<new-customer-form
					v-bind:organisation-name="organisationName"
					v-bind:title-list="titleList"
					v-bind:flag-validation-check="flagValidationCheck"
					v-on:update_customer_data="updateCustomerData($event)"
				></new-customer-form>

				<!-- CUSTOMER ORGANISATION -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Customer Organisation</strong>
						<p class="text-instructions">
							A customer will require an Organisation. If the customer
							does not have any organisations, i.e. a sole trader, we
							recommend creating the customer as an organisation instead.
						</p>
					</div>
					<div class="col-md-8">
						<div class="form-group col-sm-8">
							<label>
								Organisation:
								<validation-rendering
									v-bind:error-list="v$.organisationModel.$errors"
								></validation-rendering>
							</label>
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
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="submitNewCustomer"
							v-bind:disabled="disableSubmitButton"
						>Submit Customer</button
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Validation
import useVuelidate from "@vuelidate/core";
import {required, email} from "@vuelidate/validators";

//Components
import NewCustomerForm from "./NewCustomerForm.vue";
import {NSelect} from "naive-ui";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "NewCustomer",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		ValidationRendering,
		NewCustomerForm,
		NSelect,
	},
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
	data() {
		return {
			customerEmailModel: "",
			customerFirstNameModel: "",
			customerLastNameModel: "",
			disableSubmitButton: false,
			flagValidationCheck: false,
			organisationFixList: [],
			organisationModel: "",
			searchTimeout: "",
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
			organisationModel: {
				required,
			},
			titleModel: {
				required,
			},
		};
	},
	methods: {
		useNBTheme,
		fetchOptions(search, loading) {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (search.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getOrganisationData(search, loading);
				}, 500);
			}
		},
		getOrganisationData(search) {
			// Save the seach data in FormData
			const data_to_send = new FormData();
			data_to_send.set("search", search);

			// Now that the timer has run out, lets use AJAX to get the organisations.
			this.axios.post(
				`${this.rootUrl}search/organisation/data/`,
				data_to_send
			).then((response) => {
				//Extract the required JSON data
				const extracted_data = response.data;

				//Look through the extracted data - and map the required fields into stakeholder fix list
				this.organisationFixList = extracted_data.map((row) => {
					//Create the creation object
					return {
						value: row.pk,
						label: row.fields.organisation_name,
					};
			});
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Getting Organisation Data",
						message: `Error getting organisation data. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
			});
		},
		async submitNewCustomer() {
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
				//Show error modal
				this.$store.dispatch("newToast", {
					header: "Error submitting new customer",
					message: `Sorry, we had an submitting new customer. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Disble submit button
			this.disableSubmitButton = true;

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
			this.axios
				.post(`${this.rootUrl}new_customer/save/`, data_to_send)
				.then((response) => {
					//Go to the new customer page
					window.location.href = response.data;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error submitting new customer",
						message: `Sorry, we had an submitting new customer. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});

					//Enable users to submit again
					this.disableSubmitButton = false;
				});
		},
		updateCustomerData(data) {
			//Update the modal field with the value data
			this[data.field] = data.value;
		},
	},
	mounted() {
		//Get a default list when mounted
		this.$nextTick(() => {
			this.getOrganisationData("", "");
		});
	},
};
</script>


