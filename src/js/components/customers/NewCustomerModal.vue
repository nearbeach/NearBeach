<template>
	<div
		class="modal fade"
		id="addCustomerModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-xl-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Customer Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addCustomerCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<new-customer-form
						v-bind:title-list="titleList"
						v-bind:flag-validation-check="flagValidationCheck"
						v-on:update_customer_data="updateCustomerData($event)"
					></new-customer-form>
				</div>
				<div class="modal-footer">
					<a
						href="javascript:void(0)"
						class="btn btn-primary"
						v-on:click="submitNewCustomer"
					>Add Contact</a
					>

					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import NewCustomerForm from "./NewCustomerForm.vue";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, email} from "@vuelidate/validators";

export default {
	name: "NewCustomerModal",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NewCustomerForm,
	},
	props: {
		organisationId: {
			type: Number,
			default: 0,
		},
		titleList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			customerEmailModel: "",
			customerFirstNameModel: "",
			customerLastNameModel: "",
			flagValidationCheck: false,
			organisationModel: {},
			titleModel: [],
		};
	},
	validations: {
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
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		async submitNewCustomer() {
			//Flag downstream to check validation
			this.flagValidationCheck = true;

			//Reset this check after 100ms
			setTimeout(() => {
				this.flagValidationCheck = false;
			}, 100);

			// Check the validation at this level
			const isFormCorrect = await this.v$.$validate();

			//NEED TO USE MIXIN FOR THIS SECTION
			if (!isFormCorrect) {
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

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
			data_to_send.set("organisation", this.organisationId);

			//Send the data using axios
			this.axios.post(
				`${this.rootUrl}new_customer/save/`,
				data_to_send
			).then((response) => {
				//Go to the new customer page
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Could not save customer",
					message: `Sorry, could not save the customer. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateCustomerData(data) {
			//Update the modal field with the value data
			this[data.field] = data.value;
		},
	},
};
</script>


