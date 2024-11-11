<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body requirement-border">
				<h1>New Requirement</h1>
				<hr/>
				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Place a basic bird's eye view of the requirement
							description here. You will be able to break the
							requirement down into smaller components called 'Items'
							on the next page.
						</p>
					</div>

					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<div class="form-group">
							<label for="id_requirement_title"
							>Requirement Title:
								<validation-rendering
									v-bind:error-list="v$.requirementTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="id_requirement_title"
								class="form-control"
								name="requirement_title"
								type="text"
								required="true"
								maxlength="255"
								v-model="requirementTitleModel"
							/>
						</div>

						<br/>
						<label>
							Requirement Scope:
							<validation-rendering
								v-bind:error-list="v$.requirementScopeModel.$errors"
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
							v-model="requirementScopeModel"
						/>
					</div>
				</div>

				<!-- Stakeholder Organisation -->
				<hr/>
				<get-stakeholders
					v-on:update_stakeholder_model="updateStakeholderModel($event)"
					v-bind:is-dirty="v$.stakeholderModel.$dirty"
				></get-stakeholders>

				<!-- Status -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Status</h2>
						<p class="text-instructions">
							Set the Requirement Status and Type here.
						</p>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Status
								<validation-rendering
									v-bind:error-list="v$.statusModel.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="statusFixList"
								label="status"
								v-model:value="statusModel"
							></n-select>
						</div>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Type
								<validation-rendering
									v-bind:error-list="v$.typeModel.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="typeFixList"
								label="type"
								v-model:value="typeModel"
							></n-select>
						</div>
					</div>
				</div>

				<!-- Group Permissions -->
				<hr/>
				<group-permissions
					v-bind:display-group-permission-issue="displayGroupPermissionIssue"
					v-bind:group-results="groupResults"
					v-bind:user-group-permissions="userGroupPermissions"
					v-on:update_group_model="updateGroupModel($event)"
					v-bind:is-dirty="v$.groupModel.$dirty"
					destination="requirement"
				></group-permissions>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="submitNewRequirement"
							v-bind:disabled="disableSubmitButton"
						>Create new Requirement</button
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//JavaScript Libraries

import Editor from "@tinymce/tinymce-vue";
import GetStakeholders from "../organisations/GetStakeholders.vue";
import GroupPermissions from "../permissions/GroupPermissions.vue";
import {NSelect} from "naive-ui";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useNewObjectUploadImage} from "../../composables/uploads/useNewObjectUploadImage";
import {useReplaceIncorrectImageUrl} from "../../composables/uploads/useReplaceIncorrectImageUrl";

export default {
	name: "NewRequirement",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		GetStakeholders,
		GroupPermissions,
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
		statusList: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: "",
		},
		typeList: {
			type: Array,
			default: () => {
				return [];
			},
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
			displayGroupPermissionIssue: false,
			disableSubmitButton: false,
			groupModel: "",
			requirementScopeModel: "",
			requirementTitleModel: "",
			stakeholderModel: "",
			statusFixList: [],
			statusModel: "",
			typeFixList: [],
			typeModel: "",
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
		requirementScopeModel: {
			required,
			maxLength: maxLength(630000),
		},
		requirementTitleModel: {
			required,
		},
		stakeholderModel: {
			required,
		},
		statusModel: {
			required,
		},
		typeModel: {
			required,
		},
	},
	methods: {
		useNewObjectUploadImage,
		useNBTheme,
		async submitNewRequirement() {
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

			// Set up the data object to send
			const data_to_send = new FormData();
			data_to_send.set(
				"requirement_title",
				this.requirementTitleModel
			);
			data_to_send.set(
				"requirement_scope",
				useReplaceIncorrectImageUrl(this.requirementScopeModel)
			);
			data_to_send.set("organisation", this.stakeholderModel);
			data_to_send.set("requirement_status", this.statusModel);
			data_to_send.set("requirement_type", this.typeModel);
			data_to_send.set("uuid", this.uuid);

			// Insert a new row for each group list item
			this.groupModel.forEach((row) => {
				data_to_send.append("group_list", row);
			});

			// Use Axion to send the data
			this.axios.post(
				"save/",
				data_to_send
			).then((response) => {
				// Use the result to go to the url
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error submitting new requirement",
					message: `Sorry, we could not submit the new requirement. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});

				this.disableSubmitButton = false;
			});
		},
		updateGroupModel(newGroupModel) {
			//Update the group model
			this.groupModel = newGroupModel;

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
		updateStakeholderModel(newStakeholderModel) {
			this.stakeholderModel = newStakeholderModel;
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//VueX
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//We need to map "fields" array from the statusList/typeList json data
		this.statusFixList = this.statusList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_status,
			};
		});

		this.typeFixList = this.typeList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_type,
			};
		});
	},
};
</script>


