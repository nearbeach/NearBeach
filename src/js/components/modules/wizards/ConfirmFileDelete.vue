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
import {useReopenCardInformation} from "../../../composables/card_information/useReopenCardinformation";

export default {
	name: "ConfirmFileDelete",
	computed: {
		...mapGetters({
			destination: "getDestination",
			documentRemoveKey: "getDocumentRemoveKey",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		useReopenCardInformation,
		deleteFile() {
			//Check to make sure it isn't blank
			if (this.documentRemoveKey === "") {
				//We don't want to remove a blank file
				return;
			}

			//Axios is a promise. It is not guaranteed that the documentRemoveKey will not be blanked out by the time
			//it has finished it's web query. Hence we cache this here. :)
			const cached_document_remove_key = this.documentRemoveKey;

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("document_key", this.documentRemoveKey);

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/remove/`,
				data_to_send,
			).then(() => {
				//Update VueX - remove that document from the list
				this.$store.dispatch("removeDocument", {
					document_key: cached_document_remove_key,
				});

				//Close the modal
				this.closeModal();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing file",
					message: `We could not remove your file. Error - ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});

			this.closeModal();
		},
		closeModal() {
			//Zero out the document key (just in case)
			this.$store.commit({
				type: "updateDocumentRemoveKey",
				documentRemoveKey: "",
			});

			//Close the modal
			document.getElementById("confirmFileDeleteButton").click();

			//Reshow the card information modal if exists
			useReopenCardInformation();
		}
	},
}
</script>
