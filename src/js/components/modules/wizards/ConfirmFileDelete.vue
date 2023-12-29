<template>
	<div
		class="modal fade"
		id="confirmFileDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmFileDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmFileDelete"
					>
						Please confirm File Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmFileDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the file?
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
						v-on:click="deleteFile"
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
	name: "ConfirmFileDelete",
	props: {
		documentKey: {
			type: String,
			default: "",
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteFile() {
			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("document_key", this.documentKey);

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/remove/`,
				data_to_send,
			).then(() => {
				this.$emit("remove_document", {
					document_key: this.documentKey,
				});
			}).catch((error) => {
				// this.showErrorModal(error, this.destination);
			});

			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmFileDeleteButton").click();
		}
	},
}
</script>
