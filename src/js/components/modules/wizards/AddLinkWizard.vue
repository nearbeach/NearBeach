<template>
	<div
		class="modal fade"
		id="addLinkModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.userIcon"></Icon>
						Add Link
						Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addLinkCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Add Link</strong>
							<p class="text-instruction">
								Add hyperlinks to other documents and sources
								located in on the internet/cloud.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label for="document_description">
									Document Description
									<validation-rendering
										v-bind:error-list="v$.documentDescriptionModel.$errors"
									></validation-rendering>
									<span
										class="error"
										v-if="duplicateDescription"
									>
										Sorry - but this is a duplicated
										description.</span
									>
								</label>
								<input
									id="document_description"
									v-model="documentDescriptionModel"
									class="form-control"
									maxlength="50"
									placeholder="NearBeach Homepage"
								/>
							</div>
							<div class="form-group">
								<label for="document_url_location">
									Document URL
									<validation-rendering
										v-bind:error-list="v$.documentUrlLocationModel.$errors"
									></validation-rendering>
								</label>
								<input
									id="document_url_location"
									v-model="documentUrlLocationModel"
									class="form-control"
									placeholder="https://nearbeach.org"
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
						v-on:click="addLink"
						v-bind:disabled="disableAddButton"
					>
						Add Link
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";

//VueX
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../../mixins/iconMixin";
import reopenCardInformation from "../../../mixins/reopenCardInformation"

//Validation
import useVuelidate from "@vuelidate/core";
import {required, url} from "@vuelidate/validators";
import ValidationRendering from "../../validation/ValidationRendering.vue";
import {Modal} from "bootstrap";

export default {
	name: "AddLinkWizard",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		Icon,
		ValidationRendering,
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
	mixins: [
      iconMixin,
      reopenCardInformation,
  ],
	data() {
		return {
			linkModel: "",
			disableAddButton: true,
			documentDescriptionModel: "",
			documentUrlLocationModel: "",
			duplicateDescription: false,
		};
	},
	validations: {
		documentDescriptionModel: {
			required,
		},
		documentUrlLocationModel: {
			required,
			url,
		},
	},
	computed: {
		...mapGetters({
			currentFolder: "getCurrentFolder",
			excludeDocuments: "getDocumentFilteredList",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addLink() {
			const data_to_send = new FormData();
			data_to_send.set(
				"document_description",
				this.documentDescriptionModel
			);
			data_to_send.set(
				"document_url_location",
				this.documentUrlLocationModel
			);

			//Only set the parent folder variable if there exists a variable in current folder
			if (this.currentFolder > 0) {
				data_to_send.set("parent_folder", this.currentFolder);
			}

			this.axios.post(
				`${this.rootUrl}documentation/${this.destination}/${this.locationId}/add_link/`,
				data_to_send
			).then((response) => {
				//Append something to document List
				this.$store.dispatch("appendDocumentList", {
					documentList: response.data[0],
				});

				//Clear the data
				this.documentDescriptionModel = "";
				this.documentUrlLocationModel = "";

				//Close the modal
				document.getElementById("addLinkCloseButton").click();

				//Reshow the card information modal if exists
				this.reopenCardInformation();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Adding Link",
					message: `Sorry, could not add the link for you. Error - ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	updated() {
		//We need to make sure both fields are not blank & to make sure the description is not duplicated
		const match = this.excludeDocuments.filter((row) => {
			return (
				row.document_key__document_description ===
				this.documentDescriptionModel
			);
		});

		//Notify the user of duplicate descriptions (if there is any)
		this.duplicateDescription = match.length > 0;

		// Check the validation
		this.v$.$touch();

		//Disable the button (if it does not meet our standards)
		this.disableAddButton = this.v$.$invalid || match.length > 0;
	},
};
</script>

<style scoped></style>
