<template>
	<div
		class="modal fade"
		id="confirmCustomerRemoveModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmCustomerRemove"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmCustomerRemove"
					>
						Please confirm Customer Removal
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmCustomerRemoveButton"
					></button>
				</div>
				<div class="modal-body">
					<div class="customer-card--details">
						<div class="customer-card--name">
							<a
								v-bind:href="`${rootUrl}customer_information/${customerObject.customer_id}/`"
								target="_blank"
								rel="noopener noreferrer"
							>
								{{ customerObject.customer_first_name }}
								{{ customerObject.customer_last_name }}
							</a>
						</div>
						<div class="customer-card--email">
							{{ customerObject.customer_email }}
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="removeCustomer"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "ConfirmCustomerRemoval",
	emits: ["remove_customer"],
	props: {
		customerObject: {
			type: Object,
			default: () => {
				return {
					customer_id: 0,
					customer_email: "",
					customer_first_name: "",
					customer_last_name: "",
					customer_profile_picture: "",
				}
			}
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		closeModal() {
			document.getElementById("confirmCustomerRemoveButton").click();
		},
		removeCustomer() {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("customer_id", this.customerObject.customer_id);

			//Depending on the destination, depends on the URL
			let url = `${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_customer/`
			if (this.destination === "organisation") {
				url = `${this.rootUrl}customer_information/${this.locationId}/delete/`
			}

			this.axios.post(
				url,
				data_to_send,
			).then(() => {
				//Filter out the delete customer
				this.$emit("remove_customer", this.customerObject.customer_id);
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can't remove customer",
					message: `Sorry, could not remove customer. Error -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});

			this.closeModal();
		},
	},
}
</script>
