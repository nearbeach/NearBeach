<template>
	<div class="card">
		<div class="card-body">
			<h1>Project Information</h1>
			<hr />

			<div class="row">
				<!-- DESCRIPTION -->
				<div class="col-md-4">
					<h2>Description</h2>
					<p class="text-instructions">
						Edit the project information and then click the "Update
						Project" button at the bottom of the page
					</p>
				</div>

				<!-- PROJECT FORM -->
				<div
					class="col-md-8"
					style="min-height: 610px"
				>
					<!-- PROJECT NAME -->
					<div class="form-group">
						<label
							>Project Name
							<validation-rendering
								v-bind:error-list="v$.projectNameModel.$errors"
							></validation-rendering>
						</label>
						<input
							type="text"
							v-model="projectNameModel"
							class="form-control"
						/>
					</div>
					<br />

					<!-- PROJECT DESCRIPTION -->
					<label>
						Project Description:
						<validation-rendering
							v-bind:error-list="v$.projectDescriptionModel.$errors"
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
							plugins: ['lists', 'paste', 'table'],
							toolbar: [
								'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
								'bold italic strikethrough underline backcolor | table | ' +
									'bullist numlist outdent indent | removeformat',
							],
						}"
						v-bind:content_css="false"
						v-bind:skin="false"
						v-bind:disabled="isReadOnly"
						v-model="projectDescriptionModel"
					/>
				</div>
			</div>

			<!-- PROJECT STATUS -->
			<hr />
			<div class="row">
				<div class="col-md-4">
					<strong>Project Status</strong>
					<p class="text-instructions">
						Please update the project's task to reflect it's current
						status. Then click on the "Update Project" button to
						save the change.
					</p>
				</div>
				<div
					class="col-md-4"
					v-if="!isReadOnly"
				>
					<n-select
						v-bind:options="statusOptions"
						v-model:value="projectStatusModel"
					></n-select>
				</div>
				<div
					class="col-md-4"
					v-if="!isReadOnly"
				>
					<div
						class="alert alert-danger"
						v-if="projectStatusModel === 'Closed'"
					>
						Saving the project with this status will close the
						project.
					</div>
				</div>
				<div
					class="col-md-4"
					v-if="isReadOnly"
				>
					<div
						class="alert alert-info"
						v-if="projectStatusModel === 'Closed'"
					>
						Project has been closed.
					</div>
				</div>
			</div>

			<!-- STAKEHOLDER ORGANISATION -->
			<hr />
			<stakeholder-information
				v-bind:organisation-results="organisationResults"
				v-bind:default-stakeholder-image="defaultStakeholderImage"
			></stakeholder-information>

			<!-- START DATE & END DATE -->
			<hr />
			<between-dates
				destination="project"
				v-on:update_dates="updateDates($event)"
				v-bind:end-date-model="projectEndDateModel.getTime()"
				v-bind:start-date-model="projectStartDateModel.getTime()"
			></between-dates>

			<!-- Submit and Close Button -->
			<hr v-if="userLevel >= 2 && !isReadOnly" />
			<div
				class="row submit-row"
				v-if="!isReadOnly"
			>
				<div class="col-md-12">
					<!-- Close Project -->
					<a
						href="javascript:void(0)"
						v-if="userLevel >= 3"
						class="btn btn-danger"
						v-on:click="closeProject"
						>Close Project</a
					>

					<!-- Update Project -->
					<a
						href="javascript:void(0)"
						v-if="userLevel >= 2"
						class="btn btn-primary save-changes"
						v-on:click="updateProject"
						>Update Project</a
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");
	import { NSelect } from "naive-ui";
	import BetweenDates from "../dates/BetweenDates.vue";
	import StakeholderInformation from "../organisations/StakeholderInformation.vue";
	import Editor from "@tinymce/tinymce-vue";

	//VueX
	import { mapGetters } from "vuex";

	//Validations
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";
	import ValidationRendering from "../validation/ValidationRendering.vue";

	//Mixins
	import errorModalMixin from "../../mixins/errorModalMixin";
	import loadingModalMixin from "../../mixins/loadingModalMixin";
	import uploadMixin from "../../mixins/uploadMixin";

	export default {
		name: "ProjectInformation",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			BetweenDates,
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
				default: () => {
					return [];
				},
			},
			projectResults: {
				type: Array,
				default: () => {
					return [];
				},
			},
			userLevel: {
				type: Number,
				default: 1,
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
				projectDescriptionModel:
					this.projectResults[0].fields.project_description,
				projectEndDateModel: new Date(
					this.projectResults[0].fields.project_end_date
				),
				projectNameModel: this.projectResults[0].fields.project_name,
				projectStartDateModel: new Date(
					this.projectResults[0].fields.project_start_date
				),
				projectStatusModel:
					this.projectResults[0].fields.project_status,
				statusOptions: [
					{ value: "Backlog", label: "Backlog" },
					{ value: "Blocked", label: "Blocked" },
					{ value: "In Progress", label: "In Progress" },
					{ value: "Test/Review", label: "Test/Review" },
				],
			};
		},
		validations: {
			projectDescriptionModel: {
				required,
				maxLength: maxLength(630000),
			},
			projectEndDateModel: {
				required,
			},
			projectNameModel: {
				required,
			},
			projectStartDateModel: {
				required,
			},
		},
		methods: {
			closeProject() {
				//Set the project status to Closed
				this.projectStatusModel = "Closed";

				//Update the project
				this.updateProject();
			},
			updateDates(data) {
				this.projectEndDateModel = new Date(data.end_date);
				this.projectStartDateModel = new Date(data.start_date);
			},
			updateProject() {
				// Check the validation first
				this.v$.$touch();

				if (this.v$.$invalid) {
					this.showValidationErrorModal();

					//Just return - as we do not need to do the rest of this function
					return;
				}

				//Construct data_to_send to backend
				const data_to_send = new FormData();
				data_to_send.set(
					"project_description",
					this.projectDescriptionModel
				);
				data_to_send.set(
					"project_end_date",
					this.projectEndDateModel.toISOString()
				);
				data_to_send.set("project_name", this.projectNameModel);
				data_to_send.set(
					"project_start_date",
					this.projectStartDateModel.toISOString()
				);
				data_to_send.set("project_status", this.projectStatusModel);

				//Open up the loading modal
				this.showLoadingModal("Project");

				//Use axios to send data
				axios
					.post(
						`${this.rootUrl}project_information/${this.projectResults[0].pk}/save/`,
						data_to_send
					)
					.then((response) => {
						//Notify user of success update
						this.closeLoadingModal();

						//Reload the page IF the status is closed
						if (this.projectStatusModel === "Closed")
							window.location.reload(true);
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
		},
		mounted() {
			//If users have enough permissions add in the "Closed" functionaly
			if (this.userLevel >= 3) {
				this.statusOptions.push("Closed");
			}

			//If the project status is closed => set the isReadOnly to true
			this.isReadOnly =
				this.projectResults[0].fields.project_status === "Closed";
		},
	};
</script>

<style scoped></style>
