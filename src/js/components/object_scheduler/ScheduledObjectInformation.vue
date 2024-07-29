<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card card-body">
				<h1>Scheduled Object Information</h1>
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
							:init="{
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: newObjectUploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
									 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${this.skin}`,
							content_css: `${this.contentCss}`,
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
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<!-- Group Permissions -->
				<hr/>
				<group-permissions
					v-bind:display-group-permission-issue="displayGroupPermissionIssue"
					v-bind:group-results="groupResults"
					v-bind:destination="'object'"
					v-bind:user-group-results="userGroupResults"
					v-on:update_group_model="updateGroupModel($event)"
					v-bind:is-dirty="v$.groupModel.$dirty"
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
						ADD CODE - BUTTONS
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

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import uploadMixin from "../../mixins/uploadMixin";

//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";

export default {
	name: "NewScheduledObject",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		StakeholderInformation,
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
		scheduledObjectId: {
			type: Number,
			default: 0,
		},
		scheduledObjectResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		staticUrl: {
			type: String,
			default: "/",
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
	},
	mixins: [
		getThemeMixin,
		uploadMixin,
	],
	methods: {
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
		updateDates(data) {
			//Update both the start and end dates
			this.objectStartDateModel = new Date(data.start_date);
			this.objectEndDateModel = new Date(data.end_date);
		},
		updateGroupModel(data) {
			this.groupModel = data;

			//Calculate to see if the user's groups exist in the groupModel
			this.displayGroupPermissionIssue = this.userGroupResults.filter(row => {
				return this.groupModel.includes(row.group_id);
			}).length === 0;

			//Calculate to see if the user has create permission for any of the selected groups
			const filtered_user_and_group_level = this.userGroupAndLevel.filter((row) => {
				return data.includes(row.group_id);
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
		updateScheduledObject() {
			//ADD CODE
		},
		updateSchedulerFrequency(data) {
			this.daysBeforeModel = data.daysBeforeModel;
			this.dayModel = data.dayModel;
			this.endDateConditionModel = data.endDateConditionModel;
			this.endDateModel = data.endDateModel;
			this.isFormValid = data.isFormValid;
			this.numberOfRepeats = data.numberOfRepeats;
			this.schedulerFrequencyModel = data.schedulerFrequencyModel;
			this.singleDayModel = data.singleDayModel;
			this.startDateModel = data.startDateModel;
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