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
						<Icon v-bind:icon="icons.userIcon"></Icon> Add Customer
						Wizard
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
	import axios from "axios";
	import { Modal } from "bootstrap";
	import { Icon } from "@iconify/vue";
	import NewCustomerForm from "./NewCustomerForm.vue";

	//VueX
	import { mapGetters } from "vuex";

	//Validation
	import useVuelidate from "@vuelidate/core";
	import { required, email } from "@vuelidate/validators";

	//Mixin
	import iconMixin from "../../mixins/iconMixin";

	export default {
		name: "NewCustomerModal",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			Icon,
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
		mixins: [iconMixin],
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
			submitNewCustomer: async function () {
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
				data_to_send.set("organisation", this.organisationId);

				//Send the data using axios
				axios
					.post(`${this.rootUrl}new_customer/save/`, data_to_send)
					.then((response) => {
						//Go to the new customer page
						window.location.href = response.data;
					})
					.catch((error) => {});
			},
			updateCustomerData(data) {
				//Update the modal field with the value data
				this[data.field] = data.value;
			},
		},
	};
</script>

<style scoped></style>
