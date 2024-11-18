<template>
	<div>
		<h2>
			Documents
		</h2>
		<p class="text-instructions">
			The following is a folder structure of all documents uploaded to
			this {{ this.getDestination() }}
		</p>

		<!-- DOCUMENT FOLDER TREE -->
		<div
			v-if="parseInt(documentObjectCount) === 0"
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
				v-if="this.currentFolder !== 0"
				v-on:click="goToParentDirectory()"
				class="document--child"
				@dragover.prevent
				@dragenter.prevent
				@drop="drop($event, currentParentFolder)"
			>
				<carbon-arrow-up
					height="80px"
					width="80px"
				></carbon-arrow-up>
				<p class="text-instructions">Go to Parent Directory...</p>
			</div>

			<!-- RENDER THE FOLDERS -->
			<div
				v-for="folder in folderFilteredList"
				:key="folder.pk"
				class="document--child"
				@dragover.prevent
				@dragenter.prevent
				@drop="drop($event, folder.pk)"
				@dragstart="dragFolderStart($event, folder.pk)"
				draggable="true"
			>
				<a
					href="javascript:void(0)"
					v-on:click="updateCurrentFolder(folder.pk)"
				>
					<carbon-folder
						width="80px"
						height="80px"
					></carbon-folder>
					<p class="text-instructions">
						{{ shortName(folder.fields.folder_description) }}
					</p>
				</a>

				<!-- REMOVE FOLDER -->
				<div
					class="document--remove"
					v-if="userLevel >= 2"
				>
					<carbon-trash-can
						v-on:click="confirmFolderDelete(folder.pk)"
					></carbon-trash-can>
				</div>
			</div>

			<!-- RENDER THE FILES -->
			<div
				v-for="document in documentFilteredList"
				:key="document.document_key_id"
				class="document--child"
				@dragstart="dragDocumentStart($event, document.document_key_id)"
				draggable="true"
			>
				<a
					v-bind:href="`/private/${document.document_key_id}/`"
					rel="noopener noreferrer"
					target="_blank"
				>
					<component
						v-bind:is="getIcon(document)"
						width="80px"
						height="80px"
					></component>
					<p class="text-instructions">
						{{ shortName(document.document_key__document_description) }}
					</p>
				</a>

				<!-- REMOVE DOCUMENT -->
				<div
					class="document--remove"
					v-if="userLevel >= 2"
				>
					<carbon-trash-can
						v-on:click="confirmFileDelete(document.document_key_id)"
					></carbon-trash-can>
				</div>
			</div>
		</div>

		<!-- ADD DOCUMENTS AND FOLDER BUTTON -->
		<hr v-if="userLevel > 1 || hasDocumentPermission" />
		<div class="btn-group save-changes"
			 v-if="readOnly === false"
		>
			<button
				class="btn btn-primary dropdown-toggle"
				type="button"
				data-bs-toggle="dropdown"
				aria-expanded="false"
				v-if="userLevel > 1 || hasDocumentPermission"
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
	</div>
</template>

<script>
import {Modal} from "bootstrap";

//Icons
import CarbonArrowUp from "../../icons/CarbonArrowUp.vue";
import CarbonDocument from "../../icons/CarbonDocument.vue";
import CarbonDocumentPdf from "../../icons/CarbonDocumentPdf.vue"
import CarbonFolder from "../../icons/CarbonFolder.vue";
import CarbonImage from "../../icons/CarbonImage.vue";
import MdiMicrosoftExcel from "../../icons/MdiMicrosoftExcel.vue";
import MdiMicrosoftPowerPoint from "../../icons/MdiMicrosoftPowerPoint.vue";
import MdiMicrosoftWord from "../../icons/MdiMicrosoftWord.vue";

//VueX
import {mapGetters} from "vuex";
import {CarbonTrashCan} from "../../../components";

export default {
	name: "DocumentsModule",
	components: {
		CarbonArrowUp,
		CarbonDocument,
		CarbonDocumentPdf,
		CarbonFolder,
		CarbonImage,
		CarbonTrashCan,
		MdiMicrosoftExcel,
		MdiMicrosoftPowerPoint,
		MdiMicrosoftWord,
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
		readOnly: {
			type: Boolean,
			default: false,
		},
	},
	computed: {
		...mapGetters({
			currentFolder: "getCurrentFolder",
			currentParentFolder: "getCurrentParentFolder",
			destination: "getDestination",
			documentFilteredList: "getDocumentFilteredList",
			documentObjectCount: "getDocumentObjectCount",
			folderFilteredList: "getFolderFilteredList",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
		...mapGetters([
			"getUserExtraPermission",
		]),
		hasDocumentPermission() {
      		return this.getUserExtraPermission("document");
    	},
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
			//Close the card modal if exists
			const cardModal = document.getElementById("cardInformationModalCloseButton");
			if (cardModal !== null)
			{
				cardModal.click();
			}

			const addFolderModal = new Modal(
				document.getElementById("addFolderModal")
			);
			addFolderModal.show();
		},
		addLink() {
			//Close the card modal if exists
			const cardModal = document.getElementById("cardInformationModalCloseButton");
			if (cardModal !== null)
			{
				cardModal.click();
			}

			const addLinkModal = new Modal(
				document.getElementById("addLinkModal")
			);
			addLinkModal.show();
		},
		confirmFileDelete(document_key) {
			//Send the document key to VueX
			this.$store.commit({
				type: "updateDocumentRemoveKey",
				documentRemoveKey: document_key,
			});

			//Close the card modal if exists
			const cardModal = document.getElementById("cardInformationModalCloseButton");
			if (cardModal !== null)
			{
				cardModal.click();
			}

			//Open the modal
			const confirmFileDeleteModal = new Modal(
				document.getElementById("confirmFileDeleteModal")
			);
			confirmFileDeleteModal.show();

		},
		confirmFolderDelete(folder_id) {
			//Send the folder id to VueX
			this.$store.commit({
				type: "updateFolderRemoveId",
				folderRemoveId: folder_id,
			});

			//Close the card modal if exists
			const cardModal = document.getElementById("cardInformationModalCloseButton");
			if (cardModal !== null)
			{
				cardModal.click();
			}

			//Open the modal
			const confirmFolderDeleteModal = new Modal(
				document.getElementById("confirmFolderDeleteModal")
			);
			confirmFolderDeleteModal.show();
		},
		dragDocumentStart(event, moving_document_id) {
			event.dataTransfer.setData(
				"moving_document_id",
				moving_document_id
			);

			event.dataTransfer.setData(
				"object_type",
				"document"
			);
		},
		dragFolderStart(event, moving_folder_id) {
			event.dataTransfer.setData(
				"moving_folder_id",
				moving_folder_id
			);

			event.dataTransfer.setData(
				"object_type",
				"folder"
			);
		},
		drop(event, folder_id) {
			event.preventDefault();

			//Look up the object type and apply the correct movement
			const object_type = event.dataTransfer.getData("object_type");
			if (object_type === "folder") {
				//Handle the folder stuff
				this.handleFolderMove(event, folder_id);
			} else if (object_type === "document") {
				this.handleDocumentMove(event, folder_id);
			}
		},
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getDocumentList() {
			//If getLocationID === 0 - bail on axios
			if (this.getLocationId() === 0) return;

			this.axios.post(
				`${this.rootUrl}documentation/${this.getDestination()}/${this.getLocationId()}/list/files/`
			).then((response) => {
				// this.documentList = response.data;
				//
				// this.updateDocumentFilteredList();
				this.$store.commit({
					type: "updateDocumentList",
					documentList: response.data,
				})
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error getting Document List",
					message: `Can not retrieve document list. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getFolderList() {
			//If getLocationID === 0 - bail on axios
			if (this.getLocationId() === 0) return;

			this.axios.post(
				`${this.rootUrl}documentation/${this.getDestination()}/${this.getLocationId()}/list/folders/`
			).then((response) => {
				// this.folderList = response.data;
				//
				// this.updateFolderFilteredList();
				this.$store.commit({
					type: "updateFolderList",
					folderList: response.data,
				});
			});
		},
		getIcon(document) {
			//If the document is a weblink - just return the link image
			if (
				document.document_key__document_url_location !== "" &&
				document.document_key__document_url_location !== null
			) {
				return "CarbonLink";
			}

			//We know the document is not a link - now we use the suffix to the document name to determine the icon
			const split_document = document.document_key__document.split(".");

			//Get the last result
			const document_suffic = split_document[split_document.length - 1];

			switch (document_suffic) {
				case "jpg":
				case "png":
				case "bmp":
					return CarbonImage;
				case "doc":
				case "docx":
					return MdiMicrosoftWord;
				case "xls":
				case "xlsx":
					return MdiMicrosoftExcel;
				case "ppt":
				case "pptx":
					return MdiMicrosoftPowerPoint;
				case "pdf":
					return CarbonDocumentPdf;
				default:
					return CarbonDocument;
			}
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
		goToParentDirectory() {
			this.$store.commit("updateCurrentFolder", {
				currentFolder: this.currentParentFolder,
			});
		},
		handleDocumentMove(event, parent_folder_id) {
			//Get the document key id
			const document_key_id = event.dataTransfer.getData('moving_document_id');
			if (document_key_id === undefined) return;

			//If folder id == 0, make it null
			if (parseInt(parent_folder_id) === 0) parent_folder_id = null;

			//Update document folder id
			this.$store.dispatch("updateDocumentFolder", {
				document_key_id: document_key_id,
				parent_folder_id: parent_folder_id,
			});

			//Update the backend
			const data_to_send = new FormData();
			data_to_send.set("document_key", document_key_id);
			if (parent_folder_id !== undefined && parent_folder_id !== null) {
				data_to_send.set("parent_folder", parent_folder_id);
			}

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/update_document/`,
				data_to_send,
			).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Moving Document",
					message: `Sorry, there was an error moving your document. Please refresh page. Error -> ${error}`,
					delay: 0,
					extra_classes: "bg-danger",
				});
			});
		},
		handleFolderMove(event, parent_folder_id) {
			//Get the folder id of the moving folder
			const moving_folder_id = event.dataTransfer.getData("moving_folder_id");
			if (moving_folder_id === undefined) return;

			//If folder_id == 0, make it null
			if (parseInt(parent_folder_id) === 0) parent_folder_id = null;

			//Update the folder
			this.$store.dispatch("updateFolderParentFolder", {
				moving_folder_id: moving_folder_id,
				parent_folder_id: parent_folder_id,
			});

			//Update backend
			const data_to_send = new FormData();
			data_to_send.set("moving_folder", moving_folder_id);
			if (parent_folder_id !== undefined && parent_folder_id !== null && parseInt(parent_folder_id) !== 0) {
				data_to_send.set("parent_folder", parent_folder_id);
			}

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/update_folder/`,
				data_to_send,
			).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Moving Folder",
					message: `Sorry, there was an error moving your folder. Please refresh page. Error -> ${error}`,
					delay: 0,
					extra_classes: "bg-danger",
				});
			});
		},
		shortName(input_string) {
			//The following method will determine if we need an ellipsis (...) at the end of the file/folder name
			const max_string_length = 50;

			//If string is less than the max length, then just return the string
			if (input_string.length <= max_string_length) {
				return input_string;
			}

			//Now we split the string by max_string_length - 3 (3 for the ...)
			return `${input_string.substring(
				0,
				max_string_length - 3
			)}...`;
		},
		updateCurrentFolder(new_folder_id) {
			//Update the current folder id
			this.$store.commit({
				type: "updateCurrentFolder",
				currentFolder: new_folder_id,
			});
		},
		uploadDocument() {
			//Close the card modal if exists
			const cardModal = document.getElementById("cardInformationModalCloseButton");
			if (cardModal !== null)
			{
				cardModal.click();
			}

			//Open the upload document modal
			const uploadDocumentModal = new Modal(
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


