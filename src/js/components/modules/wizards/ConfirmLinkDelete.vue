<template>
	<div
		class="modal fade"
		id="confirmLinkDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmLinkDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmLinkDelete"
					>
						Please confirm Link Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmLinkDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the link?
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
						v-on:click="deleteLink"
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
	name: "ConfirmLinkDelete",
	emits: [
		'update_link_results',
	],
	props: {},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			objectLink: "getObjectLink",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteLink() {
			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("link_id", this.objectLink.object_id);
			data_to_send.set(
				"link_connection",
				this.objectLink.object_type === this.destination ? "meta_object" : this.objectLink.object_type
			);

			//Send the data to the backend
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_link/`,
					data_to_send
				)
				.then(() => {
					//Update the data
					this.$emit("update_link_results", {});
				});

			//Close the modal
			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmLinkDeleteButton").click();
		}
	},
}
</script>
