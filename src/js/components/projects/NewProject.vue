<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Project</h1>
				<hr/>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							To create a new project, fill out the form and submit at
							the bottom of the page.
						</p>
						<p class="text-instructions">
							<strong>Note: </strong>Media files can not be uploaded
							until AFTER you save. This is a security feature.
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
						<br/>

						<!-- PROJECT DESCRIPTION -->
						<label>
							Project Description:
							<validation-rendering
								v-bind:error-list="v$.projectDescriptionModel.$errors"
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
							v-model="projectDescriptionModel"
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

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="submitNewProject"
						>Create new Project</a
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";

//Components
import BetweenDates from "../dates/BetweenDates.vue";
import GroupPermissions from "../permissions/GroupPermissions.vue";
import GetStakeholders from "../organisations/GetStakeholders.vue";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import newObjectUploadMixin from "../../mixins/newObjectUploadMixin";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "NewProject",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		BetweenDates,
		editor: Editor,
		GetStakeholders,
		GroupPermissions,
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
			default: "",
		},
		userGroupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userLevel: {
			type: Number,
			default: 1,
		},
		uuid: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		}),
	},
	mixins: [getThemeMixin, newObjectUploadMixin],
	data() {
		return {
			displayGroupPermissionIssue: false,
			groupModel: {},
			projectDescriptionModel: "",
			projectEndDateModel: "",
			projectNameModel: "",
			projectStartDateModel: "",
			stakeholderModel: {},
		};
	},
	validations: {
		groupModel: {
			required,
		},
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
		stakeholderModel: {
			required,
		},
	},
	methods: {
		submitNewProject: async function () {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect || this.displayGroupPermissionIssue) {
				return;
			}

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("project_name", this.projectNameModel);
			data_to_send.set(
				"project_description",
				this.replaceIncorrectImageUrl(this.projectDescriptionModel)
				//this.projectDescriptionModel
			);
			data_to_send.set("organisation", this.stakeholderModel);
			data_to_send.set(
				"project_start_date",
				this.projectStartDateModel.toISOString()
			);
			data_to_send.set(
				"project_end_date",
				this.projectEndDateModel.toISOString()
			);
			data_to_send.set(
				"uuid",
				this.uuid,
			);

			// Insert a new row for each group list item
			this.groupModel.forEach((row, index) => {
				data_to_send.append("group_list", row);
			});

			//Send data to backend
			this.axios.post(
				`${this.rootUrl}new_project/save/`,
				data_to_send
			).then((response) => {
				//Go to the new project
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error submitting new project",
					message: `Sorry, we could not submit new project. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
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

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});
	},
};
</script>

<style scoped></style>
