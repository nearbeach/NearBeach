<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
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
							:init="{
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: uploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
									 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${this.skin}`,
							content_css: `${this.contentCss}`,
						}"
							v-bind:disabled="isReadOnly"
							v-model="taskDescriptionModel"
						/>
					</div>
				</div>

				<!-- TASK STATUS -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Task Status</strong>
						<p class="text-instructions">
							Please update the task's status to reflect it's current
							status. Then click on the "Update Task" button to save
							the change.
						</p>
					</div>
					<div class="col-md-4">
						<n-select
							v-bind:options="statusOptions"
							v-bind:disabled="userLevel <= 2"
							v-model:value="taskStatusModel"
						></n-select>
					</div>
				</div>
				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<stakeholder-information
					v-bind:organisation-results="organisationResults"
					v-bind:default-stakeholder-image="defaultStakeholderImage"
				></stakeholder-information>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="task"
					v-on:update_dates="updateDates($event)"
					v-bind:start-date-model="taskStartDateModel.getTime()"
					v-bind:end-date-model="taskEndDateModel.getTime()"
					v-bind:is-read-only="isReadOnly"
				></between-dates>

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
import {NSelect} from "naive-ui";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";
import BetweenDates from "../dates/BetweenDates.vue";

//VueX
import {mapGetters} from "vuex";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import uploadMixin from "../../mixins/uploadMixin";

export default {
	name: "TaskInformation",
	setup() {
		return {v$: useVuelidate()};
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
			default: "/",
		},
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		stakeholderModel: {
			type: Array,
			default: () => {
				return [];
			},
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
			taskDescriptionModel:
			this.taskResults[0].fields.task_long_description,
			taskEndDateModel: new Date(
				this.taskResults[0].fields.task_end_date
			),
			taskShortDescriptionModel:
			this.taskResults[0].fields.task_short_description,
			taskStartDateModel: new Date(
				this.taskResults[0].fields.task_start_date
			),
			taskStatusModel: this.taskResults[0].fields.task_status,
		};
	},
	mixins: [getThemeMixin, uploadMixin],
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
	},
};
</script>

<style scoped></style>
