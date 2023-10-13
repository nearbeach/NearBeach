<template>
	<div>
		<h2>
			<Icon :icon="icons.bxBriefcase"/>
			Documents
		</h2>
		<p class="text-instructions">
			The following is a folder structure of all documents uploaded to
			this {{ this.getDestination() }}
		</p>

		<!-- DOCUMENT FOLDER TREE -->
		<div
			v-if="documentList.length + folderList.length == 0"
			class="module-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no documents or folders uploaded.
			</div>
		</div>
		<div
			v-else
			class="document--widget"
		>
			<!-- GO TO PARENT DIRECTORY -->
			<div
				v-if="this.currentFolder != null"
				v-on:click="goToParentDirectory()"
				class="document--child"
			>
				<Icon
					v-bind:icon="icons.arrowUp"
					width="80px"
					height="80px"
				/>
				<p class="text-instructions">Go to Parent Directory...</p>
			</div>

			<!-- RENDER THE FOLDERS -->
			<div
				v-for="folder in folderFilteredList"
				:key="folder.pk"
				v-on:click="updateCurrentFolder(folder.pk)"
				class="document--child"
			>
				<Icon
					v-bind:icon="icons.folderIcon"
					width="80px"
					height="80px"
				/>
				<p class="text-instructions">
					{{ shortName(folder.fields.folder_description) }}
				</p>
			</div>

			<!-- RENDER THE FILES -->
			<div
				v-for="document in documentFilteredList"
				:key="document.document_key_id"
				class="document--child"
			>
				<a
					v-bind:href="`/private/${document.document_key_id}/`"
					rel="noopener noreferrer"
					target="_blank"
				>
					<Icon
						v-bind:icon="getIcon(document)"
						width="80px"
						height="80px"
					/>
					<p class="text-instructions">
						{{
							shortName(
								document.document_key__document_description
							)
						}}
					</p>
				</a>

				<!-- REMOVE DOCUMENT -->
				<div
					class="document--remove"
					v-if="userLevel >= 2"
				>
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="confirmFileDelete(document.document_key_id)"
					/>
				</div>
			</div>
		</div>

		<!-- ADD DOCUMENTS AND FOLDER BUTTON -->
		<hr/>
		<div class="btn-group save-changes">
			<button
				class="btn btn-primary dropdown-toggle"
				type="button"
				data-bs-toggle="dropdown"
				aria-expanded="false"
				v-if="userLevel > 1"
			>
				New Document/File
			</button>
			<ul class="dropdown-menu">
				<li>
					<a
						class="dropdown-item"
						href="javascript:void(0)"
						v-on:click="uploadDocument"
					>
						Upload Document
					</a>
				</li>
				<li>
					<a
						class="dropdown-item"
						href="javascript:void(0)"
						v-on:click="addLink"
					>
						Add Link
					</a>
				</li>
				<li>
					<a
						class="dropdown-item"
						href="javascript:void(0)"
						v-on:click="addFolder"
					>
						Add Folder
					</a>
				</li>
			</ul>
		</div>

		<!-- MODALS -->
		<!-- ADD FOLDER ID -->
		<add-folder-wizard
			v-bind:destination="getDestination()"
			v-bind:location-id="locationId"
			v-bind:current-folder="currentFolder"
			v-bind:existing-folders="folderFilteredList"
			v-on:update_folder_list="updateFolderList($event)"
		></add-folder-wizard>

		<!-- ADD LINK WIZARD -->
		<add-link-wizard
			v-bind:destination="getDestination()"
			v-bind:location-id="locationId"
			v-bind:current-folder="currentFolder"
			v-bind:exclude-documents="documentFilteredList"
			v-on:update_document_list="updateDocumentList($event)"
		></add-link-wizard>

		<!-- CONFIRM DOCUMENT DELETE -->
		<confirm-file-delete-vue
			v-bind:document-key="removeDocumentKey"
			v-on:remove_document="removeDocument($event)"
		></confirm-file-delete-vue>

		<!-- UPLOAD DOCUMENT WIZARD -->
		<upload-document-wizard
			v-bind:destination="getDestination()"
			v-bind:location-id="locationId"
			v-bind:current-folder="currentFolder"
			v-bind:exclude-documents="documentFilteredList"
			v-on:update_document_list="updateDocumentList($event)"
		></upload-document-wizard>
	</div>
</template>

<script>
import axios from "axios";
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";
import AddFolderWizard from "../wizards/AddFolderWizard.vue";
import AddLinkWizard from "../wizards/AddLinkWizard.vue";
import ConfirmFileDeleteVue from "../wizards/ConfirmFileDelete.vue";
import UploadDocumentWizard from "../wizards/UploadDocumentWizard.vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "DocumentsModule",
	components: {
		AddFolderWizard,
		AddLinkWizard,
		ConfirmFileDeleteVue,
		Icon,
		UploadDocumentWizard,
	},
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
	data() {
		return {
			currentFolder: null,
			documentList: [],
			documentFilteredList: [],
			folderList: [],
			folderFilteredList: [],
			removeDocumentKey: "",
		};
	},
	mixins: [iconMixin],
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			userLevel: "getUserLevel",
			rootUrl: "getRootUrl",
		}),
	},
	watch: {
		overrideLocationId() {
			//Update the data
			this.getDocumentList();
			this.getFolderList();
		},
	},
	methods: {
		addFolder() {
			var addFolderModal = new Modal(
				document.getElementById("addFolderModal")
			);
			addFolderModal.show();
		},
		addLink() {
			var addLinkModal = new Modal(
				document.getElementById("addLinkModal")
			);
			addLinkModal.show();
		},
		confirmFileDelete(document_key) {
			//Send data downstream
			this.removeDocumentKey = document_key;

			//Open the modal
			var confirmFileDeleteModal = new Modal(
				document.getElementById("confirmFileDeleteModal")
			);
			confirmFileDeleteModal.show();

		},
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getDocumentList() {
			//If getLocationID === 0 - bail on axios
			if (this.getLocationId() === 0) return;

			axios
				.post(
					`${this.rootUrl}documentation/${this.getDestination()}/${this.getLocationId()}/list/files/`
				)
				.then((response) => {
					this.documentList = response.data;

					this.updateDocumentFilteredList();
				});
		},
		getFolderList() {
			//If getLocationID === 0 - bail on axios
			if (this.getLocationId() === 0) return;

			axios
				.post(
					`${this.rootUrl}documentation/${this.getDestination()}/${this.getLocationId()}/list/folders/`
				)
				.then((response) => {
					this.folderList = response.data;

					this.updateFolderFilteredList();
				});
		},
		getIcon(document) {
			//If the document is a weblink - just return the link image
			if (
				document.document_key__document_url_location != "" &&
				document.document_key__document_url_location !== null
			) {
				return this.icons.linkOut;
			}

			//We know the document is not a link - now we use the suffix to the document name to determine the icon
			var split_document = document.document_key__document.split(".");

			//Get the last result
			var document_suffic = split_document[split_document.length - 1];

			switch (document_suffic) {
				case "jpg":
				case "png":
				case "bmp":
					return this.icons.imageIcon;
				case "doc":
				case "docx":
					return this.icons.microsoftWord;
				case "xls":
				case "xlsx":
					return this.icons.microsoftExcel;
				case "ppt":
				case "pptx":
					return this.icons.microsoftPowerpoint;
				case "pdf":
					return this.icons.documentPdf;
				default:
					return this.icons.documentText;
			}
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
		goToParentDirectory() {
			//Filter for the directory - then obtain it's parent directory variable.
			var filtered_data = this.folderList.filter((row) => {
				return row.pk == this.currentFolder;
			})[0];

			//Update the current directory to the parent folder
			this.updateCurrentFolder(filtered_data.fields.parent_folder);
		},
		removeDocument(event) {
			this.documentList = this.documentList.filter((row) => {
				return row.document_key_id !== event.document_key;
			});

			this.updateDocumentFilteredList();
		},
		shortName(input_string) {
			//The following method will determine if we need an ellipsis (...) at the end of the file/folder name
			const max_string_length = 50;

			//If string is less than the max length, then just return the string
			if (input_string.length <= max_string_length) {
				return input_string;
			}

			//Now we split the string by max_string_length - 3 (3 for the ...)
			var new_string = `${input_string.substring(
				0,
				max_string_length - 3
			)}...`;

			//Return the new string
			return new_string;
		},
		updateCurrentFolder(new_folder_id) {
			//Update the current folder id
			this.currentFolder = new_folder_id;

			//Update the filtered lists
			this.updateDocumentFilteredList();
			this.updateFolderFilteredList();
		},
		updateDocumentList(data) {
			//Add data to the docuemnt List
			this.documentList.push(data[0]);

			//Update the filtered list
			this.updateDocumentFilteredList();
		},
		updateDocumentFilteredList() {
			//Filter the results to contain only the documents in the current folder
			this.documentFilteredList = this.documentList.filter((row) => {
				return row.folder == this.currentFolder;
			}).sort((a, b) => {
				return a.document_key__document_description > b.document_key__document_description;
			});

		},
		updateFolderList(data) {
			//Append the first row of the data (there will always be one row)
			this.folderList.push(data[0]);

			//Update the folder filtered list
			this.updateFolderFilteredList();
		},
		updateFolderFilteredList() {
			//Filter the results to contain only the folders in the current folder
			this.folderFilteredList = this.folderList.filter((row) => {
				return row.fields.parent_folder == this.currentFolder;
			}).sort((a, b) => {
				return a.fields.folder_description > b.fields.folder_description;
			});
		},
		uploadDocument() {
			var uploadDocumentModal = new Modal(
				document.getElementById("uploadDocumentModal")
			);
			uploadDocumentModal.show();
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getDocumentList();
			this.getFolderList();
		});
	},
};
</script>

<style scoped></style>
