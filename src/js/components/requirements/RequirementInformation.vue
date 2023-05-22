<template>
	<div class="card">
		<div class="card-body">
			<h1>Requirement Information</h1>
			<hr />

			<div class="row">
				<!-- Description -->
				<div class="col-md-4">
					<h2>Description</h2>
					<p class="text-instructions">
						Place a basic bird's eye view of the requirement
						description here. You will be able to break the
						requirement down into smaller components called 'Items'
						below in the 'Requirement Item' section.
					</p>
				</div>

				<div
					class="col-md-8"
					style="min-height: 610px"
				>
					<div class="form-group">
						<label for="id_requirement_title"
							>Requirement Title:
							<validation-rendering
								v-bind:error-list="v$.requirementTitleModel.$errors"
							></validation-rendering>
						</label>
						<input
							id="id_requirement_title"
							class="form-control"
							name="requirement_title"
							type="text"
							required="true"
							maxlength="255"
							v-model="requirementTitleModel"
						/>
					</div>

					<br />
					<label>
						Requirement Scope:
						<validation-rendering
							v-bind:error-list="v$.requirementScopeModel.$errors"
						></validation-rendering>
					</label>
					<br />
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
						}"
						v-bind:content_css="false"
						v-bind:disabled="isReadOnly"
						v-bind:skin="false"
						v-model="requirementScopeModel"
					/>
				</div>
			</div>

			<!-- Stakeholder Information -->
			<hr />
			<stakeholder-information
				v-bind:organisation-results="organisationResults"
				v-bind:default-stakeholder-image="defaultStakeholderImage"
			></stakeholder-information>

			<!-- Status -->
			<hr />
			<div class="row">
				<div class="col-md-4">
					<h2>Status</h2>
					<p class="text-instructions">
						Set the Requirement Status and Type here.
					</p>
				</div>
				<div class="col-md-8">
					<div
						class="col-md-12"
						v-if="!statusModel.status_closed"
					>
						<div class="row">
							<div class="col-md-6">
								<div class="form-group">
									<label
										>Requirement Status
										<validation-rendering
											v-bind:error-list="v$.statusModel.$errors"
										></validation-rendering>
									</label>
									<n-select
										:options="statusFixList"
										v-bind:clearable="false"
										label="status"
										v-model:value="statusModel"
									></n-select>
								</div>
							</div>
							<div class="col-md-6">
								<div
									class="alert alert-danger"
									v-if="statusModel.status_closed"
								>
									Please note - saving the requirement with
									this status will close the requirement.
								</div>
							</div>
						</div>
					</div>
					<div
						class="col-md-12"
						v-else
					>
						<div class="alert alert-info">
							Please note - this requirement is closed.
						</div>
					</div>
					<div class="row">
						<div class="col-md-6">
							<div class="form-group">
								<label
									>Requirement Type
									<validation-rendering
										v-bind:error-list="v$.typeModel.$errors"
									></validation-rendering>
								</label>
								<n-select
									:options="typeFixList"
									v-bind:disabled="isReadOnly"
									v-bind:clearable="false"
									label="type"
									v-model:value="typeModel"
								></n-select>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Submit Button -->
			<hr />
			<div
				class="row submit-row"
				v-if="userLevel > 1"
			>
				<div class="col-md-12">
					<a
						href="javascript:void(0)"
						class="btn btn-primary save-changes"
						v-on:click="updateRequirement"
						>Update Requirement</a
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	//JavaScript Libraries
	const axios = require("axios");
	import Editor from "@tinymce/tinymce-vue";
	import { NSelect } from "naive-ui";
	import StakeholderInformation from "../organisations/StakeholderInformation.vue";

	//VueX
	import { mapGetters } from "vuex";

	//Validation
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";
	import ValidationRendering from "../validation/ValidationRendering.vue";

	//Mixins
	import errorModalMixin from "../../mixins/errorModalMixin.js";
	import loadingModalMixin from "../../mixins/loadingModalMixin.js";
	import uploadMixin from "../../mixins/uploadMixin";

	export default {
		name: "RequirementInformation",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			editor: Editor,
			NSelect,
			StakeholderInformation,
			ValidationRendering,
		},
		props: {
			defaultStakeholderImage: {
				type: String,
				default: "",
			},
			organisationResults: {
				type: Array,
				default() {
					return [];
				},
			},
			requirementResults: {
				type: Array,
				default() {
					return [];
				},
			},
			statusList: {
				type: Array,
				default() {
					return [];
				},
			}, 
			typeList: {
				type: Array,
				default() {
					return [];
				},
			},
			userLevel:  {
				type: Number,
				default: 0
			},
		},
		computed: {
			...mapGetters({
				rootUrl: "getRootUrl",
				staticUrl: "getStaticUrl",
			}),
		},
		mixins: [errorModalMixin, loadingModalMixin, uploadMixin],
		data() {
			return {
				isReadOnly: false,
				requirementScopeModel: "",
				requirementTitleModel: "",
				stakeholderModel: "",
				statusFixList: [],
				statusModel: "",
				typeFixList: [],
				typeModel: "",
			};
		},
		validations: {
			requirementScopeModel: {
				required,
				maxLength: maxLength(630000),
			},
			requirementTitleModel: {
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
			updateRequirement() {
				// Check the validation first
				this.v$.$touch();

				if (this.v$.$invalid) {
					this.showValidationErrorModal();

					//Just return - as we do not need to do the rest of this function
					return;
				}

				this.showLoadingModal("Requirement");

				// Set up the data object to send
				const data_to_send = new FormData();
				data_to_send.set(
					"requirement_title",
					this.requirementTitleModel
				);
				data_to_send.set(
					"requirement_scope",
					this.requirementScopeModel
				);
				data_to_send.set("requirement_status", this.statusModel);
				data_to_send.set("requirement_type", this.typeModel);

				// Use Axion to send the data
				axios
					.post("save/", data_to_send)
					.then((response) => {
						this.closeLoadingModal();

						//If the status is closed - refresh the page
						if (this.statusModel.status_closed) {
							window.location.reload();
						}
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
		},
		mounted() {
			//Get data from the requirementResults and delegate to the Models
			var requirement_results = this.requirementResults[0].fields;

			this.requirementScopeModel = requirement_results.requirement_scope;
			this.requirementTitleModel = requirement_results.requirement_title;

			//We need to extract "fields" array from the statusList/typeList json data
			this.statusFixList = this.statusList.map((row) => {
				//Construct the object
				return {
					value: row.pk,
					label: row.fields.requirement_status,
				};
			});
			this.typeFixList = this.typeList.map((row) => {
				return {
					value: row.pk,
					label: row.fields.requirement_type,
				};
			});

			//Get the requirement status id from the requirement results
			this.statusModel = requirement_results.requirement_status;

			//Update type model
			this.typeModel = requirement_results.requirement_type;

			//Check for the read only
			if (this.statusModel.status_closed || this.userLevel === 1) {
				this.isReadOnly = true;
			}
		},
	};
</script>

<style scoped></style>
