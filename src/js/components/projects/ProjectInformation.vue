<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body project-border">
				<h1>Project Information</h1>
				<hr/>

				<div
v-if="projectIsClosed"
					 class="alert alert-info"
				>
					Project is currently closed
				</div>

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
									:error-list="v$.projectNameModel.$errors"
								></validation-rendering>
							</label>
							<input
								v-model="projectNameModel"
								type="text"
								class="form-control"
								:disabled="isReadOnly"
							/>
						</div>
						<br/>

						<!-- PROJECT DESCRIPTION -->
						<label>
							Project Description:
							<validation-rendering
								:error-list="v$.projectDescriptionModel.$errors"
							></validation-rendering>
						</label>
						<br/>
						<img
							:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
							class="loader-image"
							alt="loading image for Tinymce"
						/>
						<editor
							v-model="projectDescriptionModel"
							license-key="gpl"
							:init="{
							license_key: 'gpl',
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: useUploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 				 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${skin}`,
							content_css: `${contentCss}`,
							relative_urls: false,
						}"
							:disabled="isReadOnly"
						/>
					</div>
				</div>

				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<stakeholder-information
					:organisation-results="organisationResults"
					:default-stakeholder-image="defaultStakeholderImage"
				></stakeholder-information>

				<!-- PROJECT STATUS AND PRIORITY -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Project Status and Priority</strong>
						<p class="text-instructions">
							Please update the project's status and priority to reflect it's current
							status/priority. Then click on the "Update Project" button to
							save the change.
						</p>
					</div>
					<div class="col-md-4">
						<label>Project Status</label>
						<n-select
							v-model:value="projectStatusModel"
							:options="statusOptions"
							:disabled="userLevel<=1"
						></n-select>
					</div>
					<div class="col-md-4">
						<label>Project Priority</label>
						<n-select
							v-model:value="projectPriorityModel"
							:options="priorityOptions"
							:disabled="userLevel<=1"
						></n-select>
					</div>
				</div>

				<!-- STORY POINTS-->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Story Points</strong>
						<p class="text-instructions">
							A story point reflects how complicated and time consuming a single project will take. The
							larger the number, the larger the complexity and time.
						</p>
					</div>
					<div class="col-md-8">
						<label>Story Points</label>
						<n-input-number
							v-model:value="projectStoryPointModel"
							:disabled="isReadOnly"
							placeholder="Min"
							:min="1"
							:max="10"
							style="max-width: 150px;"
						/>
						<div
v-if="projectStoryPointModel > 5"
							 class="alert alert-info mt-3"
							 role="alert"
						>
							INFO: This is a large project. It is best to break this up into smaller tasks.
						</div>
					</div>
				</div>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="project"
					:is-read-only="isReadOnly"
					:end-date-model="projectEndDateModel.getTime()"
					:start-date-model="projectStartDateModel.getTime()"
					@update_dates="updateDates($event)"
				></between-dates>

				<!-- Submit and Close Button -->
				<hr v-if="!isReadOnly"/>
				<div
					v-if="!isReadOnly"
					class="row submit-row"
				>
					<div class="col-md-12">
						<!-- Update Project -->
						<button
class="btn btn-primary save-changes"
							@click="updateProject"
						>
							Update Project
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NSelect, NInputNumber} from "naive-ui";
import BetweenDates from "Components/dates/BetweenDates.vue";
import StakeholderInformation from "Components/organisations/StakeholderInformation.vue";
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "Components/validation/ValidationRendering.vue";

//Composables
import {useNBTheme} from "Composables/theme/useNBTheme";
import {useUploadImage} from "Composables/uploads/useUploadImage";

export default {
	name: "ProjectInformation",
	components: {
		BetweenDates,
		editor: Editor,
		NInputNumber,
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
		projectIsClosed: {
			type: Boolean,
			default: false,
		},
		projectResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		statusOptions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
			type: Number,
			default: 1,
		},
	},
	setup() {
		return {v$: useVuelidate()};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
		}),
	},
	data() {
		return {
			isReadOnly: false,
			priorityOptions: [
				{ value: 0, label: "Highest" },
				{ value: 1, label: "High" },
				{ value: 2, label: "Normal" },
				{ value: 3, label: "Low" },
				{ value: 4, label: "Lowest" },
			],
			projectDescriptionModel: this.projectResults[0].fields.project_description,
			projectEndDateModel: new Date(
				this.projectResults[0].fields.project_end_date
			),
			projectNameModel: this.projectResults[0].fields.project_name,
			projectPriorityModel: this.projectResults[0].fields.project_priority,
			projectStartDateModel: new Date(
				this.projectResults[0].fields.project_start_date
			),
			projectStatusModel: this.projectResults[0].fields.project_status,
			projectStoryPointModel: this.projectResults[0].fields.project_story_point,
		};
	},
	watch: {
		async projectStatusModel() {
			//Escape condition 1 - if the project is NOT already closed
			if (!this.projectIsClosed) return;

			//Escape condition 2 - if the NEW status is closed
			if (this.checkStatusIsClosed()) return;

			//Method - we want to resave the data and then reload
			await this.updateProject();
			window.location.reload();
		},
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
			maxLength: maxLength(255),
			required,
		},
		projectStartDateModel: {
			required,
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Set the read only status
		this.setReadOnly();

		this.$store.commit({
			type: "updateTitle",
			title: this.projectNameModel,
		});
	},
	methods: {
		useUploadImage,
		useNBTheme,
		checkStatusIsClosed() {
			//Will filter the current status for the status - then check to see if it is closed
			const filtered_status = this.statusOptions.filter((row) => {
				return parseInt(row.value) === parseInt(this.projectStatusModel);
			});

			//If there are not matching status - return true. Assume closed
			if (filtered_status.length === 0) return true;

			//Use the first value
			return filtered_status[0].project_higher_order_status === "Closed";
		},
		setReadOnly() {
			//If the project status is closed => set the isReadOnly to true
			if (this.checkStatusIsClosed()) {
				this.isReadOnly = true;
				return;
			}

			//If the user level is 1 or below
			if (this.userLevel <= 1) {
				this.isReadOnly = true;
			}
		},
		updateDates(data) {
			this.projectEndDateModel = new Date(data.end_date);
			this.projectStartDateModel = new Date(data.start_date);
		},
		async updateProject() {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
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
			data_to_send.set("project_priority", this.projectPriorityModel);
			data_to_send.set("project_story_point", this.projectStoryPointModel);

			//Notify user of attempting to save
			this.$store.dispatch("newToast", {
				header: "Project Currently Saving",
				message: "Please wait whilst we save the project",
				extra_classes: "bg-warning text-dark",
				unique_type: "save",
				delay: 0,
			});

			//Use axios to send data
			this.axios.post(
				`${this.rootUrl}project_information/${this.projectResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				//Notify user of success update
				this.$store.dispatch("newToast", {
					header: "Project Saved",
					message: "Project Saved",
					extra_classes: "bg-success",
					unique_type: "save",
				});

				//Reload the page IF the status is closed
				if (this.checkStatusIsClosed()) {
					window.location.reload();
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Project Could not save",
					message: `There was an error saving the project. Error -> ${error}`,
					extra_classes: "bg-danger",
					unique_type: "save",
					delay: 0,
				});
			});
		},
	},
};
</script>


