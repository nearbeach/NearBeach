<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body task-border">
				<h1>Task Information</h1>
				<hr/>

				<div v-if="taskIsClosed"
					 class="alert alert-info"
				>
					Task is currently closed
				</div>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							To create a new task, fill out the form and submit at
							the bottom of the page.
						</p>
					</div>

					<!-- Task FORM -->
					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<!-- TASK NAME -->
						<div class="form-group">
							<label
							>Task Short Description:
								<validation-rendering
									v-bind:error-list="v$.taskShortDescriptionModel.$errors"
								></validation-rendering>
							</label>
							<input
								type="text"
								v-model="taskShortDescriptionModel"
								v-bind:disabled="isReadOnly"
								class="form-control"
							/>
						</div>
						<br/>

						<!-- TASK DESCRIPTION -->
						<label>
							Task Long Description:
							<validation-rendering
								v-bind:error-list="v$.taskDescriptionModel.$errors"
							></validation-rendering>
						</label>
						<br/>
						<img
							v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
							class="loader-image"
							alt="loading image for Tinymce"
						/>
						<editor
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
							skin: `${this.skin}`,
							content_css: `${this.contentCss}`,
							relative_urls: false,
						}"
							v-bind:disabled="isReadOnly"
							v-model="taskDescriptionModel"
						/>
					</div>
				</div>

				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<stakeholder-information
					v-bind:organisation-results="organisationResults"
					v-bind:default-stakeholder-image="defaultStakeholderImage"
				></stakeholder-information>

				<!-- TASK STATUS AND PRIORITY -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Task Status and Priority</strong>
						<p class="text-instructions">
							Please update the task's status and priority to reflect it's current
							status/priority. Then click on the "Update Task" button to save
							the change.
						</p>
					</div>
					<div class="col-md-4">
						<label>Task Status</label>
						<n-select
							v-bind:options="statusOptions"
							v-bind:disabled="userLevel <= 2"
							v-model:value="taskStatusModel"
						></n-select>
					</div>
					<div class="col-md-4">
						<label>Task Priority</label>
						<n-select
							v-bind:options="priorityOptions"
							v-bind:disabled="userLevel <= 2"
							v-model:value="taskPriorityModel"
						></n-select>
					</div>
				</div>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="task"
					v-on:update_dates="updateDates($event)"
					v-bind:start-date-model="taskStartDateModel.getTime()"
					v-bind:end-date-model="taskEndDateModel.getTime()"
					v-bind:is-read-only="isReadOnly"
				></between-dates>

				<!-- STORY POINTS-->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Story Points</strong>
						<p class="text-instructions">
							A story point reflects how complicated and time consuming a single task will take. The
							larger the number, the larger the complexity and time.
						</p>
					</div>
					<div class="col-md-8">
						<label>Story Points</label>
						<n-input-number
							v-model:value="taskStoryPointModel"
							placeholder="Min"
							:min="1"
							:max="10"
							style="max-width: 150px;"
						/>
					</div>
				</div>

				<!-- Submit Button -->
				<hr v-if="!isReadOnly"/>
				<div
					class="row submit-row"
					v-if="!isReadOnly"
				>
					<div class="col-md-12">
						<!-- Update Task -->
						<button class="btn btn-primary save-changes"
								v-on:click="updateTask"
						>
							Update task
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";
import Editor from "@tinymce/tinymce-vue";
import {NSelect, NInputNumber } from "naive-ui";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";
import BetweenDates from "../dates/BetweenDates.vue";

//VueX
import {mapGetters} from "vuex";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useUploadImage} from "../../composables/uploads/useUploadImage";

export default {
	name: "TaskInformation",
	setup() {
		return {v$: useVuelidate()};
	},
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
			default: "/",
		},
		taskResults: {
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
		statusOptions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		taskIsClosed: {
			type: Boolean,
			default: false,
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
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
		}),
	},
	watch: {
		async taskStatusModel() {
			//Escape condition 1 - if the task is NOT already closed
			if (!this.taskIsClosed) return;

			//Escape condition 2 - if the NEW status is closed
			if (this.checkStatusIsClosed()) return;

			//Method - we want to resave the data and then reload
			await this.updateTask();
			window.location.reload();
		},
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
			taskDescriptionModel: this.taskResults[0].fields.task_long_description,
			taskEndDateModel: new Date(
				this.taskResults[0].fields.task_end_date
			),
			taskPriorityModel: this.taskResults[0].fields.task_priority,
			taskShortDescriptionModel: this.taskResults[0].fields.task_short_description,
			taskStartDateModel: new Date(
				this.taskResults[0].fields.task_start_date
			),
			taskStatusModel: this.taskResults[0].fields.task_status,
			taskStoryPointModel: this.taskResults[0].fields.task_story_point,
		};
	},
	validations: {
		taskDescriptionModel: {
			required,
			maxLength: maxLength(630000),
		},
		taskEndDateModel: {
			required,
		},
		taskShortDescriptionModel: {
			required,
		},
		taskStartDateModel: {
			required,
		},
	},
	methods: {
		useUploadImage,
		useNBTheme,
		checkStatusIsClosed() {
			//Will filter the current status for the status - then check to see if it is closed
			const filtered_status = this.statusOptions.filter((row) => {
				return parseInt(row.value) === parseInt(this.taskStatusModel);
			});

			//If there are not matching status - return true. Assume closed
			if (filtered_status.length === 0) return true;

			//Use the first value
			return filtered_status[0].task_higher_order_status === "Closed";
		},
		setReadOnly() {
			//If the project is closed -> we state that is read only is true
			if (this.checkStatusIsClosed()) {
				this.isReadOnly = true;
				return;
			}

			if (this.userLevel <= 1) {
				this.isReadOnly = true;
			}
		},
		updateTask() {
			//Check validation
			this.v$.$touch();

			//If the form is not validated
			if (this.v$.$invalid) {
				this.$store.dispatch("newToast", {
					header: "Validation issues",
					message: "Please correct the validation issues before submitting",
					extra_classes: "bg-warning text-dark",
					unique_type: "save_task",
				});

				//User does not need to do anything else
				return;
			}

			this.$store.dispatch("newToast", {
				header: "Saving Task",
				message: "Please wait whilst saving task",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_task",
			})

			//Create the data_to_send array
			const data_to_send = new FormData();
			data_to_send.set(
				"task_long_description",
				this.taskDescriptionModel
			);
			data_to_send.set(
				"task_end_date",
				this.taskEndDateModel.toISOString()
			);
			data_to_send.set(
				"task_short_description",
				this.taskShortDescriptionModel
			);
			data_to_send.set(
				"task_start_date",
				this.taskStartDateModel.toISOString()
			);
			data_to_send.set("task_status", this.taskStatusModel);
			data_to_send.set("task_priority", this.taskPriorityModel);
			data_to_send.set("task_story_point", this.taskStoryPointModel);

			//Send data to backend
			this.axios.post(
				`${this.rootUrl}task_information/${this.taskResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				//Hide the loading modal
				this.$store.dispatch("newToast", {
					header: "Task Saved",
					message: "Task has successfully been saved",
					extra_classes: "bg-success",
					unique_type: "save_task",
				});

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
		updateDates(data) {
			this.taskEndDateModel = new Date(data.end_date);
			this.taskStartDateModel = new Date(data.start_date);
		},
		updateGroupModel(data) {
			this.groupModel = data;
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Set the read only on mount :)
		this.setReadOnly();

		this.$store.commit({
			type: "updateTitle",
			title: this.taskShortDescriptionModel,
		});
	},
};
</script>


