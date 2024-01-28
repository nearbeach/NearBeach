<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.userIcon"></Icon>
			Customers
		</h2>
		<p class="text-instructions">
			Below are a list of customers who are stakeholders to this
			{{ destination }}.
		</p>

		<!-- CUSTOMER RESULTS CARDS -->
		<div v-if="customerResults.length == 0">
			<div class="customers-module-spacer">
				<div class="alert alert-dark">
					Sorry - there are no customers. Please add them by clicking
					on the button below
				</div>
			</div>
		</div>
		<div v-else>
			<customers-list-module
				v-bind:customer-results="customerResults"
				v-on:remove_customer="removeCustomer($event)"
			></customers-list-module>
		</div>

		<!-- ADD CUSTOMER BUTTON -->
		<hr/>
		<div class="row submit-row">
			<div class="col-md-12">
				<button
					class="btn btn-primary save-changes"
					v-on:click="addNewCustomer"
					v-if="userLevel > 1"
				>
					Add Customer
				</button>
			</div>
		</div>

		<!-- MODALS -->
		<add-customer-wizard
			v-bind:location-id="locationId"
			v-bind:destination="destination"
			v-bind:exclude-customers="customerResults"
			v-on:update_customer_results="updateCustomerResults($event)"
		></add-customer-wizard>
	</div>
</template>

<script>
//JavaScript components
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import CustomersListModule from "./CustomersListModule.vue";
import AddCustomerWizard from "../wizards/AddCustomerWizard.vue";
import {Modal} from "bootstrap";

//VueX
import {mapGetters} from "vuex";


export default {
	name: "CustomersModule",
	components: {
		AddCustomerWizard,
		CustomersListModule,
		Icon,
	},
	mixins: [iconMixin],
	data() {
		return {
			customerResults: [],
		};
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			userLevel: "getUserLevel",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addNewCustomer() {
			const addCustomerModal = new Modal(
				document.getElementById("addCustomerModal")
			);
			addCustomerModal.show();
		},
		loadCustomerResults() {
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/customer_list/`
				)
				.then((response) => {
					this.customerResults = response.data;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Loading Customer Results",
						message: `We had an issue loading customer results. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		removeCustomer(customer_id) {
			this.customerResults = this.customerResults.filter((row) => {
				return row.pk !== customer_id;
			});
		},
		updateCustomerResults(data) {
			this.customerResults = data;
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (escape_array.indexOf(this.destination) >= 0) return;

		//Wait 200ms before getting data
		this.$nextTick(() => {
			this.loadCustomerResults();
		});
	},
};
</script>

<style scoped></style>
