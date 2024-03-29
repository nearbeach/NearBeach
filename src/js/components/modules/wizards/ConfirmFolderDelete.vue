<template>
	<div
		class="modal fade"
		id="confirmFolderDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmFolderDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmFolderDelete"
					>
						Please confirm Folder Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmFolderDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the folder? All files under this folder will be deleted also.
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
						v-on:click="deleteFolder"
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
import {Modal} from "bootstrap";

//Mixins
import reopenCardInformation from "../../../mixins/reopenCardInformation";

export default {
	name: "ConfirmFolderDelete",
	mixins: [
		reopenCardInformation,
	],
	computed: {
		...mapGetters({
			destination: "getDestination",
			folderRemoveId: "getFolderRemoveId",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteFolder() {
			//Check to make sure it isn't blank
			if (this.folderRemoveId === "") {
				//We don't want to remove a blank file
				return;
			}

			//Axios is a promise. It is not guaranteed that the folderRemoveId will not be blanked out by the time
			//it has finished it's web query. Hence we cache this here. :)
			const cached_folder_remove_id = this.folderRemoveId;

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("folder_id", this.folderRemoveId);

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/remove_folder/`,
				data_to_send,
			).then(() => {
				//Update VueX - remove that document from the list
				this.$store.dispatch("removeFolder", {
					folder_id: cached_folder_remove_id,
				});

				//Close the modal
				this.closeModal();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing folder",
					message: `We could not remove your folder. Error - ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});

			this.closeModal();
		},
		closeModal() {
			//Zero out the document key (just in case)
			this.$store.commit({
				type: "updateFolderRemoveId",
				documentRemoveKey: "",
			});

			//Close the modal
			document.getElementById("confirmFolderDeleteButton").click();

			//Reshow the card information modal if exists
			this.reopenCardInformation();
		}
	},
}
</script>
