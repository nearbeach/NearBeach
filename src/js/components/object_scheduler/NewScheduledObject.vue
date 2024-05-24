<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card card-body">
				<h1>New Scheduled Object</h1>
				<hr>

				<div class="row">
					<div class="col-md-4">
						<h2>Object Type</h2>
						<p class="text-instructions">
							Please select if the object will be either a Project or Task.
						</p>
					</div>
					<div class="col-md-8">
						<label>Object Type</label>
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
				<get-stakeholders
					v-on:update_stakeholder_model="updateStakeholderModel($event)"
					v-bind:is-dirty="v$.stakeholderModel.$dirty"
				></get-stakeholders>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="project"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<!-- Group Permissions -->
				<hr/>
				<group-permissions
					v-bind:display-group-permission-issue="displayGroupPermissionIssue"
					v-bind:group-results="groupResults"
					v-bind:destination="'project'"
					v-bind:user-group-results="userGroupResults"
					v-on:update_group_model="updateGroupModel($event)"
					v-bind:is-dirty="v$.groupModel.$dirty"
				></group-permissions>

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

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import uploadMixin from "../../mixins/uploadMixin";

//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";

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
			displayGroupPermissionIssue: false,
			objectDescriptionModel: "",
			objectTitleModel: "",
			objectTypeModel: "",
			objectTypeOptions: [
				{
					value: "project",
					label: "Project",
				},
				{
					value: "task",
					label: "Task",
				},
			],
			stakeholderModel: "",
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
	mixins: [
		getThemeMixin,
		uploadMixin,
	],
	methods: {
		updateDates(data) {
			//Update both the start and end dates
			this.projectStartDateModel = new Date(data.start_date);
			this.projectEndDateModel = new Date(data.end_date);
		},
		updateGroupModel(data) {
			this.groupModel = data;

			//Calculate to see if the user's groups exist in the groupModel
			this.displayGroupPermissionIssue = this.userGroupResults.filter(row => {
				return this.groupModel.includes(row.group_id);
			}).length === 0;
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
	},
}
</script>