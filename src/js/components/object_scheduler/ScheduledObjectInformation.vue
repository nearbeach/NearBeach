<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card card-body">
				<h1>Scheduled Object Information</h1>
				<a v-bind:href="`${rootUrl}scheduled_objects/`">Back to Scheduled Object list</a>
				<hr>

				<div class="row">
					<div class="col-md-4">
						<h2>Object Type</h2>
						<p class="text-instructions">
							Please select if the object will be either a Project or Task.
						</p>
					</div>
					<div class="col-md-8">
						<label>
							Object Type
							<validation-rendering
								v-bind:error-list="v$.objectTypeModel.$errors"
							></validation-rendering>
						</label>
						<n-select
							v-model:value="objectTypeModel"
							:options="objectTypeOptions"
						/>
					</div>
				</div>

				<!-- OBJECT DESCRIPTION-->
				<hr>
				<div class="row">
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Please supply a suitable Title and Description for your object. This will be created exactly
							each time the object is created.
						</p>
					</div>

					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<div class="form-group">
							<label
							>Object Title
								<validation-rendering
									v-bind:error-list="v$.objectTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								type="text"
								v-model="objectTitleModel"
								class="form-control"
							/>
						</div>
						<br/>

						<!-- OBJECT DESCRIPTION -->
						<label>
							Object Description:
							<validation-rendering
								v-bind:error-list="v$.objectDescriptionModel.$errors"
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
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: useNewObjectUploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
									 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${this.skin}`,
							content_css: `${this.contentCss}`,
							relative_urls: false,
						}"
							v-model="objectDescriptionModel"
						/>
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
					destination="object"
					v-bind:end-date-model="objectEndDateModel.getTime()"
					v-bind:start-date-model="objectStartDateModel.getTime()"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<!-- Group Permissions -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Group Permissions</h2>
						<p class="text-instructions">
							Add or remove groups from this scheduled object. Adding a group
							will allow users from that group to access the constructed object.
						</p>
						<p class="text-instructions">
							Users who do not have access to this scheduled object, won't be able
							to edit/view this object, nor it's constructed object.
						</p>
					</div>
					<div class="col-md-8">
						<label>
							Group List
							<validation-rendering v-bind:error-list="v$.objectGroupModel.$errors"
							></validation-rendering>
						</label>
						<n-select
							:options="groupResults"
							label="group"
							v-model:value="objectGroupModel"
							v-on:update-value="checkObjectGroupModel"
							multiple
						></n-select>

<!--						 ALERT FOR WHEN USER GROUPS ARE NOT INCLUDED -->
						<br/>
						<div v-if="displayGroupPermissionIssue"
							 class="alert alert-warning"
						>
							None of your user groups were included. You will not have permissions to create this object. Please
							select one of your groups
						</div>
					</div>
				</div>

				<!-- Scheduler Frequency -->
				<hr/>
				<scheduler-frequency
					v-bind:days-before="daysBeforeModel"
					v-bind:day="dayModel"
					v-bind:end-date-condition="endDateConditionModel"
					v-bind:end-date="endDateModel"
					v-bind:number-of-repeats="numberOfRepeats"
					v-bind:scheduler-frequency="schedulerFrequencyModel"
					v-bind:single-day="singleDayModel"
					v-bind:start-date="startDateModel"
					v-on:update_scheduler_frequency="updateSchedulerFrequency"
				></scheduler-frequency>

				<!-- Is Active -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Is Active</h2>
						<p class="text-instructions">
							Toggle this scheduled object on or off. Please remember to save after toggling.
						</p>
					</div>
					<div class="col-md-8">
						<n-switch v-model:value="isActiveModel">
							<template #checked>
								Currently Active
							</template>
							<template #unchecked>
								Disabled
							</template>
						</n-switch>
					</div>
				</div>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button class="btn btn-primary save-changes"
								v-on:click="updateSchedulerObject"
						>
							Update Scheduled Object
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Components
import editor from "@tinymce/tinymce-vue";
import { NSelect, NConfigProvider, NSwitch } from "naive-ui";
import BetweenDates from "../dates/BetweenDates.vue";
import SchedulerFrequency from "./SchedulerFrequency.vue";

//Validations
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useNewObjectUploadImage} from "../../composables/uploads/useNewObjectUploadImage";

export default {
	name: "NewScheduledObject",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		StakeholderInformation,
		BetweenDates,
		editor,
		NConfigProvider,
		NSelect,
		NSwitch,
		SchedulerFrequency,
		ValidationRendering,
	},
	props: {
		defaultStakeholderImage: {
			type: String,
			default: "",
		},
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		objectTemplateResults: {
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
		rootUrl: {
			type: String,
			default: "/",
		},
		scheduledObjectResults: {
			type: Object,
			default: () => {
				return {
					"schedule_object_id": 0,
					"object_template_id": 0,
					"end_date": null,
					"frequency": "Set Day of the Week",
					"frequency_attribute": null,
					"is_active": true,
					"number_of_repeats": -1
				};
			},
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		templateGroupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: "light",
		},
		userGroupAndLevel: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userGroupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			groupModelValidation: true,
			displayGroupPermissionIssue: false,
			objectDescriptionModel: this.objectTemplateResults[0].object_template_json.object_description,
			objectEndDateModel: new Date(this.objectTemplateResults[0].object_template_json.object_end_date),
			objectGroupModel: this.templateGroupResults,
			objectStartDateModel: new Date(this.objectTemplateResults[0].object_template_json.object_start_date),
			objectTitleModel: this.objectTemplateResults[0].object_template_json.object_title,
			objectTypeModel: this.objectTemplateResults[0].object_template_type,
			objectTypeOptions: [
				{
					value: 0,
					label: "Project",
				},
				{
					value: 1,
					label: "Task",
				},
			],

			//Scheduler Frequency Data
			daysBeforeModel: this.getDaysBeforeModel(),
			dayModel: this.getDayModel(),
			endDateConditionModel: this.getEndDateConditionModel(),
			endDateModel: this.getEndDateModel(),
			isActiveModel: this.scheduledObjectResults.is_active,
			isFormValid: true,
			numberOfRepeats: this.scheduledObjectResults.number_of_repeats,
			schedulerFrequencyModel: this.scheduledObjectResults.frequency,
			singleDayModel: this.getSingleDayModel(),
			startDateModel: new Date(this.scheduledObjectResults.start_date).getTime(),
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		}),
	},
	validations: {
		objectDescriptionModel: {
			required,
		},
		objectGroupModel: {
			required,
		},
		objectTitleModel: {
			required,
		},
		objectTypeModel: {
			required,
		},
	},
	methods: {
		useNewObjectUploadImage,
		useNBTheme,
		calculateUserLevel(data) {
			//If there is no data to crunch, just return.
			if (data.length === 0) return 0;

			//Inside list we have two fields; project, and tasks. We want to grab the highest value from
			//both of those fields. Then we want to grab the highest values out of those two results. This will be our
			//user level.
			const user_level_project = data.reduce((prev, current) => {
				return (prev && prev.project_permission > current.project_permission) ? prev : current;
			}).project_permission;

			const user_level_task = data.reduce((prev, current) => {
				return (prev && prev.task_permission > current.task_permission) ? prev : current;
			}).task_permission;

			if (user_level_task > user_level_project) {
				return user_level_task;
			}
			return user_level_project;
		},
		checkObjectGroupModel() {
			//Calculate to see if the user's groups exist in the objectGroupModel
			this.displayGroupPermissionIssue = this.userGroupResults.filter(row => {
				return this.objectGroupModel.includes(row.group_id);
			}).length === 0;

			//Calculate to see if the user has create permission for any of the selected groups
			const filtered_user_and_group_level = this.userGroupAndLevel.filter((row) => {
				return this.objectGroupModel.includes(row.group_id);
			});

			//Calulate the boolean result. We need to make sure the user can create (3 - create)
			this.groupModelValidation = this.calculateUserLevel(filtered_user_and_group_level) >= 3;

			//As there is no validation yet, we'll use a toast to notify the user
			if (!this.groupModelValidation) {
				this.$store.dispatch("newToast", {
					header: "No CREATE permission for groups",
					message: "Please note - for the current groups selected, you do not have create permissions. Please add in a group you have create permission with.",
					extra_classes: "bg-danger",
					delay: 5000,
					unique_type: "group-model-validation",
				});
			}
		},
		getEndDateConditionModel() {
			//If number of repeats
			if (this.scheduledObjectResults.number_of_repeats >= 0) return "number-of-repeats";

			//If end date
			if (this.scheduledObjectResults.end_date !== null) return "end-date";

			return "no-end-date";
		},
		getDayModel() {
			//Default date is []
			if (this.scheduledObjectResults.frequency_attribute === undefined) return [];
			if (this.scheduledObjectResults.frequency_attribute.days_of_the_week === undefined) return [];

			return this.scheduledObjectResults.frequency_attribute.days_of_the_week;
		},
		getDaysBeforeModel() {
			if (this.scheduledObjectResults.frequency_attribute === undefined) return 0;
			if (this.scheduledObjectResults.frequency_attribute.days_before === undefined) return 0;

			return this.scheduledObjectResults.frequency_attribute.days_before;
		},
		getEndDateModel() {
			if (this.scheduledObjectResults.end_date === null) return 0;

			//Convert the end date
			const convert_date = new Date(this.scheduledObjectResults.end_date);
			return convert_date.getTime();
		},
		getSingleDayModel() {
			if (this.scheduledObjectResults.frequency_attribute === undefined) return "Monday";
			if (this.scheduledObjectResults.frequency_attribute.day_of_the_week === undefined) return "Monday";

			return this.scheduledObjectResults.frequency_attribute.day_of_the_week;
		},
		updateDates(data) {
			//Update both the start and end dates
			this.objectStartDateModel = new Date(data.start_date);
			this.objectEndDateModel = new Date(data.end_date);
		},
		updateSchedulerFrequency(data) {
			this.daysBeforeModel = data.daysBeforeModel;
			this.dayModel = data.dayModel;
			this.endDateConditionModel = data.endDateConditionModel;
			this.endDateModel = data.endDateModel;
			this.isFormValid = data.isFormValid;
			this.numberOfRepeats = data.numberOfRepeatsModel;
			this.schedulerFrequencyModel = data.schedulerFrequencyModel;
			this.singleDayModel = data.singleDayModel;
			this.startDateModel = data.startDateModel;
		},
		async updateSchedulerObject() {
			//Validate the data before sending
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect || this.displayGroupPermissionIssue || !this.isFormValid) {
                //Tell the user to fix the validation issues
                this.$store.dispatch("newToast", {
                    header: "Please check all validation",
                    message: "There are some fields that are filled in correctly. Please correct these mistakes.",
                    extra_classes: "bg-danger",
                    delay: 0,
                });

				return;
			}

			if (!this.groupModelValidation) {
				this.$store.dispatch("newToast", {
					header: "No CREATE permission for groups",
					message: "Please note - for the current groups selected, you do not have create permissions. Please add in a group you have create permission with.",
					extra_classes: "bg-danger",
					delay: 5000,
				});

				return;
			}

			//Create form data
			const data_to_send = new FormData()
			data_to_send.set("object_type", this.objectTypeModel);
			data_to_send.set("object_title", this.objectTitleModel);
			data_to_send.set("object_description", this.objectDescriptionModel);
			data_to_send.set(
				"object_start_date",
				this.objectStartDateModel.toISOString()
			);
			data_to_send.set(
				"object_end_date",
				this.objectEndDateModel.toISOString()
			);

			// Insert a new row for each group list item
			this.objectGroupModel.forEach((row) => {
				data_to_send.append("group_list", row);
			});

			//Convert the dates
			const offset = new Date().getTimezoneOffset();
			let scheduler_end_date = new Date(this.endDateModel - (offset * 60 * 1000));
			let scheduler_start_date = new Date(this.startDateModel - (offset * 60 * 1000));

			scheduler_end_date = scheduler_end_date.toISOString().split("T")[0];
			scheduler_start_date = scheduler_start_date.toISOString().split("T")[0];

			//Send the scheduler data
			data_to_send.set("days_before", this.daysBeforeModel);
			data_to_send.set("number_of_repeats", this.numberOfRepeats);
			data_to_send.set("scheduler_frequency", this.schedulerFrequencyModel);
			data_to_send.set("scheduler_end_date", scheduler_end_date);
			data_to_send.set("scheduler_start_date", scheduler_start_date);
			data_to_send.set("single_day", this.singleDayModel);
			data_to_send.set("end_date_condition", this.endDateConditionModel);
			data_to_send.set("is_active", this.isActiveModel);

			//Loop through dayModel and append to data to send
			this.dayModel.forEach((single_day) => {
				data_to_send.append("day", single_day);
			});

			this.axios.post(
				`${this.rootUrl}scheduled_object_information/${this.scheduledObjectResults.schedule_object_id}/save/`,
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Saved Scheduled Object",
					message: "Scheduled Object has been updated",
					extra_classes: "bg-success",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error creating new scheduled object",
					message: `Sorry, we could not create this scheduled object for you. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//Update user level
		const user_level = this.calculateUserLevel(this.userGroupAndLevel);
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: user_level,
		});
	},
}
</script>