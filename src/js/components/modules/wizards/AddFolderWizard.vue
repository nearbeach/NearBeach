<template>
	<div
		class="modal fade"
		id="addFolderModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Folder Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addFolderCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Creating a folder</strong>
							<p class="text-instructions">
								Give the folder an appropriate name. When done,
								click on the "Save" button. It will be added to
								the current folder.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label for="folder_description"
								>Folder Name</label
								>
								<input
									type="text"
									v-model="folderDescriptionModel"
									class="form-control"
									id="folder_description"
									maxlength="50"
								/>
							</div>
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
						v-bind:disabled="disableAddFolderButton"
						v-on:click="addFolder"
					>
						Add Folder
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";
import {useReopenCardInformation} from "../../../composables/card_information/useReopenCardinformation";

export default {
	name: "AddFolderWizard",
	components: {
	},
	props: {
		destination: {
			type: String,
			default: "/",
		},
		locationId: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			disableAddFolderButton: true,
			folderDescriptionModel: "",
		};
	},
	computed: {
		...mapGetters({
			existingFolders: "getFolderFilteredList",
			currentFolder: "getCurrentFolder",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		useReopenCardInformation,
		addFolder() {
			//Construct the data to send
			const data_to_send = new FormData();
			data_to_send.set(
				"folder_description",
				this.folderDescriptionModel
			);

			if (this.currentFolder > 0) {
				data_to_send.set("parent_folder", this.currentFolder);
			}

			//Send the data in POST
			this.axios
				.post(
					`${this.rootUrl}documentation/${this.destination}/${this.locationId}/add_folder/`,
					data_to_send
				)
				.then((response) => {
					//Update the Folder List in VueX
					this.$store.dispatch("appendFolderList", {
						folderList: response.data[0],
					});

					//Clear the model
					this.folderDescriptionModel = "";

					//Close the modal
					document.getElementById("addFolderCloseButton").click();

					//Reshow the card information modal if exists
					useReopenCardInformation();
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Failed to add folder",
						message: `Failed to add folder. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
	},
	updated() {
		/*If there is no folder description OR the folder description already exists - we want to disable the add
		button.*/
		const match = this.existingFolders.filter((row) => {
			return (
				row.fields.folder_description === this.folderDescriptionModel
			);
		});

		this.disableAddFolderButton =
			match.length > 0 || this.folderDescriptionModel === "" || this.folderDescriptionModel === null;
	},
};
</script>


