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
						<Icon v-bind:icon="icons.userIcon"></Icon> Add Folder
						Wizard
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
	import axios from "axios";
	import { Icon } from "@iconify/vue";

	//VueX
	import { mapGetters } from "vuex";

	//Mixins
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";

	export default {
		name: "AddFolderWizard",
		components: {
			Icon,
		},
		props: {
			currentFolder: {
				type: String,
				default: "/",
			},
			destination: {
				type: String,
				default: "/",
			},
			existingFolders: {
				type: Array,
				default: () => {
					return [];
				},
			},
			locationId: {
				type: Number,
				default: 0,
			},
		},
		mixins: [errorModalMixin, iconMixin],
		data() {
			return {
				disableAddFolderButton: true,
				folderDescriptionModel: "",
			};
		},
		computed: {
			...mapGetters({
				rootUrl: "getRootUrl",
			}),
		},
		methods: {
			addFolder() {
				//Construct the data to send
				const data_to_send = new FormData();
				data_to_send.set(
					"folder_description",
					this.folderDescriptionModel
				);

				if (this.currentFolder !== null && this.currentFolder !== "") {
					data_to_send.set("parent_folder", this.currentFolder);
				}

				//Send the data in POST
				axios
					.post(
						`${this.rootUrl}documentation/${this.destination}/${this.locationId}/add_folder/`,
						data_to_send
					)
					.then((response) => {
						//Send the data up stream to get appended
						this.$emit("update_folder_list", response.data);

						//Clear the model
						this.folderDescriptionModel = "";

						//Close the modal
						document.getElementById("addFolderCloseButton").click();
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
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

<style scoped></style>
