<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card card-body">
				<h1>New Scheduled Object</h1>
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
				<get-stakeholders
					v-on:update_stakeholder_model="updateStakeholderModel($event)"
					v-bind:is-dirty="v$.stakeholderModel.$dirty"
				></get-stakeholders>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="object"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<!-- Group Permissions -->
				<hr/>
				<group-permissions
					v-bind:display-group-permission-issue="displayGroupPermissionIssue"
					v-bind:group-results="groupResults"
					v-bind:user-group-permissions="userGroupPermissions"
					v-on:update_group_model="updateGroupModel($event)"
					v-bind:is-dirty="v$.groupModel.$dirty"
					destination="object"
				></group-permissions>

				<!-- Scheduler Frequency -->
				<hr/>
				<scheduler-frequency
					v-on:update_scheduler_frequency="updateSchedulerFrequency"
				></scheduler-frequency>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button class="btn btn-primary save-changes"
								v-on:click="submitNewScheduledObject"
						>
							Create New Scheduled Object
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
import { NSelect, NConfigProvider } from "naive-ui";
import BetweenDates from "../dates/BetweenDates.vue";
import GetStakeholders from "../organisations/GetStakeholders.vue";
import GroupPermissions from "../permissions/GroupPermissions.vue";
import SchedulerFrequency from "./SchedulerFrequency.vue";

//Validations
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useNewObjectUploadImage} from "../../composables/uploads/useNewObjectUploadImage";

export default {
	name: "NewScheduledObject",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		BetweenDates,
		editor,
		GetStakeholders,
		GroupPermissions,
		NConfigProvider,
		NSelect,
		SchedulerFrequency,
		ValidationRendering,
	},
	props: {
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "light",
		},
		userGroupPermissions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		uuid: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			groupModel: {},
			groupModelValidation: true,
			displayGroupPermissionIssue: false,
			objectDescriptionModel: "",
			objectEndDateModel: "",
			objectStartDateModel: "",
			objectTitleModel: "",
			objectTypeModel: "",
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
			stakeholderModel: "",

			//Scheduler Frequency Data
			daysBeforeModel: 0,
			dayModel: [],
			endDateConditionModel: "no-end-date",
			endDateModel: 0,
			isFormValid: false,
			numberOfRepeats: 0,
			schedulerFrequencyModel: "Set Day of the Week",
			singleDayModel: "monday",
			startDateModel: 0,
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		}),
	},
	validations: {
		groupModel: {
			required,
		},
		objectDescriptionModel: {
			required,
		},
		objectTitleModel: {
			required,
		},
		objectTypeModel: {
			required,
		},
		stakeholderModel: {
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
		async submitNewScheduledObject() {
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
			data_to_send.set("organisation", this.stakeholderModel);
			data_to_send.set(
				"object_start_date",
				this.objectStartDateModel.toISOString()
			);
			data_to_send.set(
				"object_end_date",
				this.objectEndDateModel.toISOString()
			);
			data_to_send.set(
				"uuid",
				this.uuid,
			);

			// Insert a new row for each group list item
			this.groupModel.forEach((row) => {
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

			//Loop through dayModel and append to data to send
			this.dayModel.forEach((single_day) => {
				data_to_send.append("day", single_day);
			});

			this.axios.post(
				`${this.rootUrl}new_scheduled_object/save/`,
				data_to_send,
			).then((response) => {
				//Redirect to the scheduled object information page
				const id = response.data.scheduled_object_id;
				window.location.href = `${this.rootUrl}scheduled_object_information/${id}`;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error creating new scheduled object",
					message: `Sorry, we could not create this scheduled object for you. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateDates(data) {
			//Update both the start and end dates
			this.objectStartDateModel = new Date(data.start_date);
			this.objectEndDateModel = new Date(data.end_date);
		},
		updateGroupModel(data) {
			this.groupModel = data;

			//Calculate to see if the user's groups exist in the groupModel AND
			//Make sure the user has ENOUGH permissions.
			this.displayGroupPermissionIssue = this.userGroupPermissions.filter(row => {
				//Condition 1 - group model includes current group
				//Condition 2 - user has create permissions on group
				const condition_1 = this.groupModel.includes(row.group_id);
				const condition_2 = row.object_permission_value >= 3;

				return condition_1 && condition_2;
			}).length === 0;
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
		updateStakeholderModel(data) {
			this.stakeholderModel = data;
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
		const user_level = this.calculateUserLevel(this.userGroupPermissions);
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: user_level,
		});
	},
}
</script>