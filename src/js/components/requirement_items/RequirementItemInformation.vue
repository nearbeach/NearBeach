<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Requirement Item Information</h1>
				<br/>
				<a
					v-bind:href="`${rootUrl}requirement_information/${requirementItemResults[0].fields.requirement}/`"
				>
					Go Back to requirement
				</a>
				<hr/>

				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Requirement Items should be detailed. They should only
							focus on one small section of the requirement.
						</p>
					</div>

					<!-- Requirement item information -->
					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<div class="form-group">
							<label for="requirement_item_title">
								Requirement Item Title:
								<validation-rendering
									v-bind:error-list="v$.requirementItemTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="requirement_item_title"
								v-model="requirementItemTitleModel"
								class="form-control"
								type="text"
								required="true"
								maxlength="255"
							/>
						</div>
						<div class="form-group">
							<label>
								Requirement Item Scope:
								<validation-rendering
									v-bind:error-list="v$.requirementItemScopeModel.$errors"
								></validation-rendering>
							</label>
							<br/>
							<img
								v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
								class="loader-image"
								alt="loading image for Tinymce"
							/>
							<editor
								:init="{
								file_picker_types: 'image',
								height: 500,
								images_upload_handler: uploadImage,
								menubar: false,
								paste_data_images: true,
								plugins: ['lists', 'image', 'codesample', 'table'],
								toolbar: [
									'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
									'bold italic strikethrough underline backcolor | table | ' +
										'bullist numlist outdent indent | removeformat | image codesample',
								],
								skin: `${this.skin}`,
								content_css: `${this.contentCss}`,
							}"
								v-model="requirementItemScopeModel"
							/>
						</div>
					</div>
				</div>

				<!-- Stakeholder Information -->
				<hr/>
				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Stakeholder</h2>
					</div>
					<div class="col-md-8 organisation-details">
						<img
							v-bind:src="getStakeholderImage"
							alt="Stakeholder Logo"
							class="organisation-image"
						/>
						<div class="organisation-name">
							{{ stakeholderModel.organisation_name }}
						</div>
						<div class="organisation-link">
							<Icon v-bind:icon="icons.linkOut"></Icon>
							Website:
							<a
								v-bind:href="stakeholderModel.organisation_website"
								target="_blank"
								rel="noopener noreferrer"
							>
								{{ stakeholderModel.organisation_website }}
							</a>
						</div>
						<div class="organisation-email">
							<Icon v-bind:icon="icons.mailIcon"></Icon>
							Email:
							<a
								v-bind:href="`mailto:${stakeholderModel.organisation_email}`"
							>
								{{ stakeholderModel.organisation_email }}
							</a>
						</div>
					</div>
				</div>

				<!-- Status -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Status</h2>
						<p class="text-instructions">
							Set the Requirement Status and Type here.
						</p>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Status
								<validation-rendering
									v-bind:error-list="v$.statusFixList.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="statusFixList"
								label="status"
								v-model:value="statusModel"
							></n-select>
						</div>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Type
								<validation-rendering
									v-bind:error-list="v$.typeModel.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="typeFixList"
								label="type"
								v-model:value="typeModel"
							></n-select>
						</div>
					</div>
				</div>

				<!-- Submit Button -->
				<hr v-if="userLevel > 1"/>
				<div
					v-if="userLevel > 1"
					class="row submit-row"
				>
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="updateRequirementItem"
						>Update Requirement</a
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//JavaScript Libraries
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";
import axios from "axios";
import Editor from "@tinymce/tinymce-vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import iconMixin from "../../mixins/iconMixin";
import uploadMixin from "../../mixins/uploadMixin";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "RequirementItemInformation.vue",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		Icon,
		NSelect,
		ValidationRendering,
	},
	props: {
		requirementItemResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		defaultStakeholderImage: {
			type: String,
			default: "/",
		},
		statusList: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: ""
		},
		typeList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
		getStakeholderImage() {
			const image =
				this.stakeholderModel.organisation_profile_picture;
			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultStakeholderImage;
			}
			return `${this.rootUrl}private/${this.stakeholderModel.organisation_profile_picture}`;
		},
	},
	mixins: [getThemeMixin, iconMixin, uploadMixin],
	data() {
		return {
			requirementItemScopeModel: "",
			requirementItemTitleModel: "",
			stakeholderModel: "",

			statusFixList: [],
			statusModel: "",
			typeFixList: [],
			typeModel: "",
		};
	},
	validations: {
		requirementItemScopeModel: {
			required,
			maxLength: maxLength(630000),
		},
		requirementItemTitleModel: {
			required,
		},
		statusFixList: {
			required,
		},
		statusModel: {
			required,
		},
		typeModel: {
			required,
		},
	},
	methods: {
		updateRequirementItem() {
			// Check the validation first
			this.v$.$touch();

			if (this.v$.$invalid) {
				//Show the error dialog and notify to the user that there were field missing.
				var elem_cont =
					document.getElementById("errorModalContent");

				// Update the content
				elem_cont.innerHTML = `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

				// Show the modal
				var errorModal = new Modal(
					document.getElementById("errorModal")
				);
				errorModal.show();

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Open up the loading modal
			var loadingModal = new Modal(
				document.getElementById("loadingModal")
			);
			loadingModal.show();

			//Update message in loading modal
			document.getElementById(
				"loadingModalContent"
			).innerHTML = `Updating your Requirement Item details`;

			// Set up the data object to send
			const data_to_send = new FormData();
			data_to_send.set(
				"requirement_item_title",
				this.requirementItemTitleModel
			);
			data_to_send.set(
				"requirement_item_scope",
				this.requirementItemScopeModel
			);
			data_to_send.set("requirement_item_status", this.statusModel);
			data_to_send.set("requirement_item_type", this.typeModel);

			// Use Axion to send the data
			axios
				.post("save/", data_to_send)
				.then((response) => {
					//Update the message in the loading modal
					document.getElementById(
						"loadingModalContent"
					).innerHTML = `UPDATED SUCCESSFULLY`;

					//Close after 1 second
					setTimeout(() => {
						loadingModal.hide();
					}, 1000);
				})
				.catch((error) => {
					//Hide the loading modal
					loadingModal.hide();

					// Get the error modal
					var elem_cont =
						document.getElementById("errorModalContent");

					// Update the content
					elem_cont.innerHTML = `<strong>HTML ISSUE:</strong> We could not save the new requirement item<hr>${error}`;

					// Show the modal
					var errorModal = new Modal(
						document.getElementById("errorModal")
					);
					errorModal.show();
				});
		},
	},
	mounted() {
		//Get data from the requirementResults and delegate to the Models
		var requirement_item_results =
			this.requirementItemResults[0].fields;

		this.requirementItemScopeModel =
			requirement_item_results.requirement_item_scope;
		this.requirementItemTitleModel =
			requirement_item_results.requirement_item_title;

		//Extract the organisation results directly
		this.stakeholderModel = this.organisationResults[0].fields;

		//Map the original lists to something NSelect can read
		this.statusFixList = this.statusList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_status,
			};
		});

		this.typeFixList = this.typeList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_type,
			};
		});

		//Set the status and type models
		this.statusModel = requirement_item_results.requirement_item_status;
		this.typeModel = requirement_item_results.requirement_item_type;
	},
};
</script>

<style scoped></style>
