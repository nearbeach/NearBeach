<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body project-border">
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
							images_upload_handler: useNewObjectUploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
									 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${skin}`,
							content_css: `${contentCss}`,
							relative_urls: false,
						}"
						/>
					</div>
				</div>

				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<get-stakeholders
					:is-dirty="v$.stakeholderModel.$dirty"
					@update_stakeholder_model="updateStakeholderModel($event)"
				></get-stakeholders>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="project"
					@update_dates="updateDates($event)"
				></between-dates>

				<!-- Group Permissions -->
				<hr/>
				<group-permissions
					:display-group-permission-issue="displayGroupPermissionIssue"
					:group-results="groupResults"
					:user-group-permissions="userGroupPermissions"
					:is-dirty="v$.groupModel.$dirty"
					destination="project"
					@update_group_model="updateGroupModel($event)"
				></group-permissions>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							:disabled="disableSubmitButton"
							@click="submitNewProject"
						>Create new Project</button
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
import BetweenDates from "Components/dates/BetweenDates.vue";
import GroupPermissions from "Components/permissions/GroupPermissions.vue";
import GetStakeholders from "Components/organisations/GetStakeholders.vue";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "Components/validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";
import {useNBTheme} from "Composables/theme/useNBTheme";
import {useNewObjectUploadImage} from "Composables/uploads/useNewObjectUploadImage";
import {useReplaceIncorrectImageUrl} from "Composables/uploads/useReplaceIncorrectImageUrl";

export default {
	name: "NewProject",
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
		// userGroupResults: {
		// 	type: Array,
		// 	default: () => {
		// 		return [];
		// 	},
		// },
		userGroupPermissions: {
			type: Array,
			default: () => {
				return [];
			}
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
	setup() {
		return {v$: useVuelidate()};
	},
	data() {
		return {
			displayGroupPermissionIssue: false,
			disableSubmitButton: false,
			groupModel: {},
			projectDescriptionModel: "",
			projectEndDateModel: "",
			projectNameModel: "",
			projectStartDateModel: "",
			stakeholderModel: {},
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
	methods: {
		useNewObjectUploadImage,
		useNBTheme,
		async submitNewProject() {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect || this.displayGroupPermissionIssue) {
                //Tell the user to fix the validation issues
                this.$store.dispatch("newToast", {
                    header: "Please check all validation",
                    message: "There are some fields that are filled in incorrectly. Please correct these mistakes.",
                    extra_classes: "bg-danger",
                    delay: 0,
                });

				return;
			}

			this.disableSubmitButton = true;

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("project_name", this.projectNameModel);
			data_to_send.set(
				"project_description",
				useReplaceIncorrectImageUrl(this.projectDescriptionModel)
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
			this.groupModel.forEach((row) => {
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

				this.disableSubmitButton = false;
			});
		},
		updateDates(data) {
			//Update both the start and end dates
			this.projectStartDateModel = new Date(data.start_date);
			this.projectEndDateModel = new Date(data.end_date);
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
		updateStakeholderModel(data) {
			this.stakeholderModel = data;
		},
	},
};
</script>


