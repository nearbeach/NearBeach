<template>
	<div
		class="modal fade"
		id="confirmPublicLinkDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmPublicLinkDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmPublicLinkDelete"
					>
						Please confirm Private Link Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmPublicLinkDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the private link?
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
						v-on:click="deletePrivateLink"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

//Composers
import {useReopenCardInformation} from "../../../composables/card_information/useReopenCardinformation";

export default {
	name: "confirmPublicLinkDelete",
	emits: [
		'update_link_results',
	],
	props: {
		overrideDestination: {
			type: String,
			default: "",
		},
		overrideLocationId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			publicLinkRemoveKey: "getPublicLinkRemoveKey",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		useReopenCardInformation,
		deletePrivateLink() {
			//Construct data to send
			const data_to_send = new FormData();
			data_to_send.set("public_link_id", this.publicLinkRemoveKey);

			//Notify user we are deleting the data
			this.$store.dispatch("newToast", {
				header: "Deleting Public Link",
				message: "Deleting Public Link",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "public_link_delete",
			});

			//Use axios
			this.axios.post(
				`${this.rootUrl}public_data/${this.getDestination()}/${this.getLocationId()}/delete/`,
				data_to_send,
			).then(() => {
				//Remove the row
				this.$store.dispatch("removePublicLink", {
					public_link_id: this.publicLinkRemoveKey,
				});

				this.$store.dispatch("newToast", {
					header: "Successfully Deleted Public Link",
					message: "Successfully Deleted Public Link",
					extra_classes: "bg-success",
					unique_type: "public_link_delete",
				});

				this.closeModal();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Deleting Public Link",
					message: `Error - could not delete link. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "public_link_delete",
				});
			});
		},
		closeModal() {
			//Zero out the public key (just in case)
			this.$store.commit({
				type: "updatePublicLinkRemoveKey",
				publicLinkRemoveKey: "",
			});

			//Close the modal
			document.getElementById("confirmPublicLinkDeleteButton").click();

			//Reshow the card information modal if exists
			useReopenCardInformation();
		},
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
	},
}
</script>
