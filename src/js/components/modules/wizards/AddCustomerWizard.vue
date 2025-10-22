<template>
	<div
		id="addCustomerModal"
		class="modal fade"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Customers Wizard
					</h2>
					<button
						id="addCustomerCloseButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div
						v-if="customerFixList.length > 0"
						class="row"
					>
						<div class="col-md-4">
							<strong>Select Customer</strong>
							<p class="text-instructions">
								Search for a customer who has not been added to
								this {{ destination }}. If the search is blank
								there are either no customers that match that
								search, or all customer have already been added
								to the {{ destination }}.
							</p>
						</div>
						<div class="col-md-8">
							<n-select
								v-model:value="customerModel"
								:options="customerFixList"
								label="customerName"
							></n-select>
						</div>
					</div>
					<div
						v-else
						class="row"
					>
						<div class="col-md-6">
							<strong>Sorry - no results</strong>
							<p class="text-instructions">
								This could be because
							</p>
							<ul class="text-instructions">
								<li>There are no more customers left to add</li>
								<li>
									There are no customers for this organisation
								</li>
							</ul>
						</div>
						<div class="col-md-6 no-search">
							<img
								:src="`${staticUrl}NearBeach/images/placeholder/questions.svg`"
								alt="Sorry - there are no results"
							/>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						:diabled="customerModel == ''"
						@click="addCustomer"
					>
						Save changes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "AddCustomerWizard",
	components: {
		NSelect,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
		excludeCustomers: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	emits: [
		'update_customer_results',
	],
	data() {
		return {
			customerModel: "",
			customerList: [],
			customerFixList: [],
		};
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	watch: {
		excludeCustomers() {
			this.updateCustomerFixList();
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (!escape_array.indexOf(this.locationId) < 0) return;

		//Wait 200ms before getting data
		this.$nextTick(() => {
			this.getCustomerList();
		});
	},
	methods: {
		addCustomer() {
			// Set up the data object to send
			const data_to_send = new FormData();
			data_to_send.set("customer", this.customerModel);

			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_customer/`,
					data_to_send
				)
				.then((response) => {
					//Send the new data up stream
					this.$emit("update_customer_results", response.data);

					//Clear the model
					this.customerModel = "";

					//Close the modal
					document.getElementById("addCustomerCloseButton").click();
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Adding Customer",
						message: `We had an issue adding customers. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		getCustomerList() {
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/customer_list_all/`
				)
				.then((response) => {
					//Place all the data into the "CustomerList" array.
					this.customerList = response.data;

					//Update the fixed list
					this.updateCustomerFixList();
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Getting Customer List",
						message: `We had an issue getting customer list. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		updateCustomerFixList() {
			//If no customer list result - just exit
			if (this.customerList.length === 0) return;

			//Create an array of ids we should be excluding
			const exclude_array = [];
			this.excludeCustomers.forEach((row) => {
				exclude_array.push(row.pk);
			});

			//Set the customerFixList
			this.customerFixList = this.customerList
				.filter((row) => {
					return !exclude_array.includes(row.pk);
				})
				.map((row) => {
					return {
						value: row.pk,
						label: `${row.fields.customer_first_name} ${row.fields.customer_last_name}`,
					};
				});
		},
	},
};
</script>


