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
				class="document--child"
			>
				<a
					href="javascript:void(0)"
					v-on:click="updateCurrentFolder(folder.pk)"
				>
					<Icon
						v-bind:icon="icons.folderIcon"
						width="80px"
						height="80px"
					/>
					<p class="text-instructions">
						{{ shortName(folder.fields.folder_description) }}
					</p>
				</a>

				<!-- REMOVE FOLDER -->
				<div
					class="document--remove"
					v-if="userLevel >= 2"
				>
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="confirmFolderDelete(folder.pk)"
					/>
				</div>
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
						{{ shortName(document.document_key__document_description) }}
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
		<div class="btn-group save-changes"
			 v-if="readOnly === false"
		>
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
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "DocumentsModule",
	components: {
		Icon,
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
	mixins: [iconMixin],
	computed: {
		...mapGetters({
			currentFolder: "getCurrentFolder",
			destination: "getDestination",
			documentFilteredList: "getDocumentFilteredList",
			documentObjectCount: "getDocumentObjectCount",
			folderFilteredList: "getFolderFilteredList",
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
				return this.icons.linkOut;
			}

			//We know the document is not a link - now we use the suffix to the document name to determine the icon
			const split_document = document.document_key__document.split(".");

			//Get the last result
			const document_suffic = split_document[split_document.length - 1];

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
			this.$store.dispatch("goToParentDirectory",{});
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

<style scoped></style>
