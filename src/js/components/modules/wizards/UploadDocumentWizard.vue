<template>
	<div
		class="modal fade"
		id="uploadDocumentModal"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Upload Document Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="uploadDocumentCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Uploading File</strong>
							<p class="text-instructions">
								You will be able to upload a file against this
								{{ getDestination }}. It will appear in the current
								folder.
							</p>
							<p v-if="documentModel.length === 0">
								1. Please click on "Upload File" button to
								upload a file
							</p>
							<p v-else-if="uploadPercentage === ''">
								2. Please modify the document descript to be
								more human readable. Or click the "Reset" button
								to remove the uploaded file.
							</p>
							<p v-else>
								3. Document is currently uploading. Please be
								patient.
							</p>
						</div>
						<div class="col-md-8">
							<div
								class="form-file"
								v-if="documentModel.length === 0"
							>
								<div class="mb-3">
									<label
										for="document"
										class="form-label"
									>
										Please upload a file<br/>
										{{ maxUploadString }}
										<div
											class="alert alert-warning"
											v-if="maxUploadWarning"
										>
											Sorry - file too large
										</div>
									</label>
									<input
										type="file"
										class="form-control"
										id="document"
										v-bind:accept="acceptedDocuments"
										v-on:change="
											handleFileUploads(
												$event.target.files
											)
										"
									/>
								</div>
							</div>
							<div
								class="form-group"
								v-else-if="uploadPercentage == ''"
							>
								<!-- DOCUMENT DESCRIPTION -->
								<div class="form-group">
									<label for="documentDescription"
									>Document Description</label
									>
									<input
										id="documentDescription"
										v-model="documentDescriptionModel"
										type="text"
										class="form-control"
									/>
								</div>

								<!-- RESET FORM BUTTON -->
								<div class="form-row mt-4">
									<button
										v-on:click="resetForm"
										class="btn btn-warning"
									>
										Reset Form
									</button>
								</div>
							</div>
							<div v-else>
								<!-- THE UPLOAD SPINNER -->
								<div
									v-if="
										parseFloat(uploadPercentage).toFixed(
											0
										) < 1
									"
									class="alert alert-warning"
								>
									Uploading
									{{
										(
											parseFloat(uploadPercentage) * 100
										).toFixed(2)
									}}%
									<div
										class="spinner-border text-primary"
										role="status"
									>
										<span class="sr-only"></span>
									</div>
								</div>

								<!-- THE FINAL WRITING -->
								<div
									v-else
									class="alert alert-success"
								>
									The document has been uploaded. The server
									is currently writing the file to disk.
									Please be patient - this modal will close
									automatically. Thank you
								</div>
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
						v-bind:disabled="disableUploadButton"
						v-on:click="uploadFile"
					>
						Upload File
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
	name: "UploadDocumentWizard",
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
			disableUploadButton: true,
			documentModel: [],
			documentDescriptionModel: "",
			uploadPercentage: "",
			maxUploadSize: 0,
			maxUploadString: "No Upload Limit",
			maxUploadWarning: false,
		};
	},
	computed: {
		...mapGetters({
			acceptedDocuments: "getAcceptedDocuments",
			currentFolder: "getCurrentFolder",
			destination: "getDestination",
			excludeDocuments: "getDocumentFilteredList",
			locationId: "getLocationId",
			staticUrl: "getStaticUrl",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		useReopenCardInformation,
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
		handleFileUploads(fileList) {
			/*Check that the size of the fileList is not too big
			  The boolean (0!=this.maxUploadSize) will product a 0 result when maxUploadSize is 0. Thus negating
			  the need for an extra if statement*/
			if (
				fileList[0].size * (this.maxUploadSize !== 0) >
				this.maxUploadSize
			) {
				this.maxUploadWarning = true;

				//Just return
				return;
			}

			//Remove maxUploadWarning
			this.maxUploadWarning = false;

			//Update the document modal
			this.documentModel = fileList[0];

			//Extract the file name and place into the document description for the user
			this.documentDescriptionModel = fileList[0].name;
		},
		resetForm() {
			//Blank out all the models
			this.documentModel = "";
			this.documentDescriptionModel = "";
			this.uploadPercentage = "";
		},
		uploadFile() {
			//Create the data to send
			const data_to_send = new FormData();
			data_to_send.set(
				"document",
				this.documentModel,
				this.documentDescriptionModel
			);
			data_to_send.set(
				"document_description",
				this.documentDescriptionModel
			);

			//If there is a current/partent folder - then add it to the data to send
			if (this.currentFolder > 0) {
				data_to_send.set("parent_folder", this.currentFolder);
			}

			//Configuration for axios
			const config = {
				onUploadProgress: (progressEvent) => {
					//As the document gets uploaded - we want to update the upload Percentage
					this.uploadPercentage =
						parseFloat(progressEvent.loaded) /
						parseFloat(progressEvent.total);
				},
			};

			//Use axios to send it to the backend
			this.axios.post(
				`${this.rootUrl}documentation/${this.getDestination()}/${this.getLocationId()}/upload/`,
				data_to_send,
				config
			).then((response) => {
				//Append the new document to the existing document list
				this.$store.dispatch("appendDocumentList", {
					documentList: response.data[0],
				});

				//Close the modal
				document.getElementById("uploadDocumentCloseButton").click();

				//Reset the document
				this.resetForm();

				//Reshow the card information modal if exists
				useReopenCardInformation();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to upload documentation",
					message: `Can not upload the documentation. ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	watch: {
		maxUploadSize() {
			//If the user has set 0 -> just say "No Upload Limit"
			if (this.maxUploadSize === 0) {
				return "No Upload Limit";
			}

			//Define the constants we wish to use
			const k = 1024;
			const sizes = [
				"Bytes",
				"KB",
				"MB",
				"GB",
				"TB",
				"PB",
				"EB",
				"ZB",
				"YB",
			];

			//Use math to find out which array section we are going to use from sizes
			const i = Math.floor(
				Math.log(this.maxUploadSize) / Math.log(k)
			);

			this.maxUploadString = `Max Upload Size: ${parseFloat(
				(this.maxUploadSize / Math.pow(k, i)).toFixed(2)
			)} ${sizes[i]}`;

			return "";
		},
	},
	updated() {
		const match = this.excludeDocuments.filter((row) => {
			return (
				row.document_key__document_description ===
				this.documentDescriptionModel
			);
		});

		this.disableUploadButton =
			this.documentModel === "" ||
			this.documentDescriptionModel.length === 0 ||
			match.length > 0;
	},
	mounted() {
		//Wait a few seconds before getting the max file upload size
		this.$nextTick(() => {
			//Get the max file upload size
			this.axios.post(
				`${this.rootUrl}documentation/get/max_upload/`
			).then((response) => {
				//Set the value
				this.maxUploadSize = response.data.max_upload_size;
			}).catch(() => {
				this.$store.dispatch("newToast", {
					header: "Failed to get the max upload size",
					message: `Had an issue getting data from backend. ${this.maxUploadString}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		});
	},
};
</script>


