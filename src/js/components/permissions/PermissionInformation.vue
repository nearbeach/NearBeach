<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Permission Information</h1>
				<br/>
				<a v-bind:href="`${this.rootUrl}search/permission_set/`"
				>Go back to permission list</a
				>
				<hr/>

				<div
					class="alert alert-danger"
					v-if="this.permissionSetResults[0].pk === 1"
				>
					Can not edit administration permission set.
				</div>

				<!-- BASIC INFORMATION -->
				<div class="row">
					<div class="col-md-4">
						<strong>Permission Set Details</strong>
						<p class="text-instructions">
							Please supply a unique name for the permission set.
						</p>
					</div>
					<div class="col-md-8">
						<label>Permission Set Name</label>
						<input
							type="text"
							v-model="permissionSetNameModel"
							class="form-control"
						/>
					</div>
				</div>
				<hr/>

				<!-- ADMINISTRATION PERMISSIONS -->
				<div class="row">
					<div class="col-md-4">
						<strong>Administration Permissions</strong>
						<p class="text-instructions">
							The following are administration permissions. These
							should be only applied to permission sets where they are
							only granted to administrators.
						</p>
					</div>
					<div class="col-md-8">
						<single-permission-properties
							v-bind:property="'administrationAssignUserToGroupModel'"
							v-bind:property-label="'Assign User To Group Model'"
							v-bind:property-value="
							administrationAssignUserToGroupModel
						"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'administrationCreateGroupModel'"
							v-bind:property-label="'Create Groups'"
							v-bind:property-value="administrationCreateGroupModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'administrationCreatePermissionSetModel'"
							v-bind:property-label="'Create Permission Sets'"
							v-bind:property-value="
							administrationCreatePermissionSetModel
						"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'administrationCreateUserModel'"
							v-bind:property-label="'Create Users'"
							v-bind:property-value="administrationCreateUserModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>
				<hr/>

				<!-- Customers and Organisations -->
				<div class="row">
					<div class="col-md-4">
						<strong>Customers and Organisations</strong>
					</div>
					<div class="col-md-8">
						<single-permission-properties
							v-bind:property="'customerModel'"
							v-bind:property-label="'Customers'"
							v-bind:property-value="customerModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'organisationModel'"
							v-bind:property-label="'Organisations'"
							v-bind:property-value="organisationModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>
				<hr/>

				<!-- Object Permissions -->
				<div class="row">
					<div class="col-md-4">
						<strong>Object Permissions</strong>
					</div>
					<div class="col-md-8">
						<single-permission-properties
							v-bind:property="'kanbanModel'"
							v-bind:property-label="'Kanban Boards'"
							v-bind:property-value="kanbanModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'kanbanCardModel'"
							v-bind:property-label="'Kanban Cards'"
							v-bind:property-value="kanbanCardModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'projectModel'"
							v-bind:property-label="'Projects'"
							v-bind:property-value="projectModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'taskModel'"
							v-bind:property-label="'Tasks'"
							v-bind:property-value="taskModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'requestForChangeModel'"
							v-bind:property-label="'Request for Change'"
							v-bind:property-value="requestForChangeModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'requirementModel'"
							v-bind:property-label="'Requirements'"
							v-bind:property-value="requirementModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>
				<hr/>

				<!-- Extra Permissions -->
				<div class="row">
					<div class="col-md-4">
						<strong>Extra Permissions</strong>
						<p class="text-instructions">
							The following permissions are added permissions on top
							of any read only. For example, if a read only user
							requires the ability to upload documentation, then you
							will need to enable the "Document" permissions here.
						</p>
					</div>
					<div class="col-md-8">
						<single-permission-properties
							v-bind:property="'documentModel'"
							v-bind:property-label="'Grants upload ability'"
							v-bind:property-value="documentModel"
							v-bind:list-of-choices="permissionBoolean"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'kanbanCommentModel'"
							v-bind:property-label="'Grants comments on Kanban Boards'"
							v-bind:property-value="kanbanCommentModel"
							v-bind:list-of-choices="permissionBoolean"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'projectHistoryModel'"
							v-bind:property-label="'Grants comments on Projects'"
							v-bind:property-value="projectHistoryModel"
							v-bind:list-of-choices="permissionBoolean"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'taskHistoryModel'"
							v-bind:property-label="'Grants comments on Tasks'"
							v-bind:property-value="taskHistoryModel"
							v-bind:list-of-choices="permissionBoolean"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>
				<hr/>

				<!-- MISC -->
				<div class="row">
					<div class="col-md-4">
						<strong>Misc Permissions</strong>
						<p class="text-instructions"></p>
					</div>
					<div class="col-md-8">
						<single-permission-properties
							v-bind:property="'bugClientModel'"
							v-bind:property-label="'Configure bug clients'"
							v-bind:property-value="bugClientModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							v-bind:property="'tagModel'"
							v-bind:property-label="'Configure tags'"
							v-bind:property-value="tagModel"
							v-bind:list-of-choices="permissionLevel"
							v-on:update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>

				<!-- Save Changes -->
				<!-- Don't show if we are looking at admin -->
				<hr v-if="this.permissionSetResults[0].pk !== 1"/>
				<div
					class="row submit-row"
					v-if="this.permissionSetResults[0].pk !== 1"
				>
					<div class="col-md-12">
						<button
							class="btn btn-danger"
							v-on:click="confirmDelete"
						>
							Delete Permission Set
						</button>
						<button
							class="btn btn-primary save-changes"
							v-on:click="saveChanges"
						>
							Save Permission Set
						</button>
					</div>
				</div>
			</div>
		</div>

		<confirm-permission-set-delete
			v-bind:permission-set-id="permissionSetResults[0].pk"
		></confirm-permission-set-delete>
	</n-config-provider>
</template>

<script>
import SinglePermissionProperties from "./SinglePermissionProperties.vue";
import ConfirmPermissionSetDelete from "./ConfirmPermissionSetDelete.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

//Modal
import { Modal } from "bootstrap";

export default {
	name: "PermissionInformation",
	components: {
		ConfirmPermissionSetDelete,
		SinglePermissionProperties,
	},
	props: {
		permissionBoolean: {
			type: Array,
			default: () => {
				return [];
			},
		},
		permissionLevel: {
			type: Array,
			default: () => {
				return [];
			},
		},
		permissionSetResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			permissionSetNameModel:
			this.permissionSetResults[0].fields.permission_set_name,
			administrationAssignUserToGroupModel:
			this.permissionSetResults[0].fields
				.administration_assign_user_to_group,
			administrationCreateGroupModel:
			this.permissionSetResults[0].fields
				.administration_create_group,
			administrationCreatePermissionSetModel:
			this.permissionSetResults[0].fields
				.administration_create_permission_set,
			administrationCreateUserModel:
			this.permissionSetResults[0].fields
				.administration_create_user,
			bugClientModel: this.permissionSetResults[0].fields.bug_client,
			customerModel: this.permissionSetResults[0].fields.customer,
			kanbanModel: this.permissionSetResults[0].fields.kanban_board,
			kanbanCardModel:
			this.permissionSetResults[0].fields.kanban_card,
			organisationModel:
			this.permissionSetResults[0].fields.organisation,
			projectModel: this.permissionSetResults[0].fields.project,
			requestForChangeModel:
			this.permissionSetResults[0].fields.request_for_change,
			requirementModel:
			this.permissionSetResults[0].fields.requirement,
			tagModel: this.permissionSetResults[0].fields.tag,
			taskModel: this.permissionSetResults[0].fields.task,
			documentModel: this.permissionSetResults[0].fields.document,
			kanbanCommentModel:
			this.permissionSetResults[0].fields.kanban_comment,
			projectHistoryModel:
			this.permissionSetResults[0].fields.project_history,
			taskHistoryModel:
			this.permissionSetResults[0].fields.task_history,
		};
	},
	mixins: [getThemeMixin],
	methods: {
		confirmDelete() {
			//Open the modal
			const modal = new Modal(document.getElementById("confirmPermissionSetDeleteModal"));
			modal.show();
		},
		saveChanges() {
			//Tell user we are updating this permission set
			this.$store.dispatch("newToast", {
				header: "Updating Permission Set",
				message: "Please wait, whilst we update the permission set",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "update_permission_set",
			});

			//Setup the data we want to send to the backend
			const data_to_send = new FormData();
			data_to_send.set(
				"permission_set_id",
				this.permissionSetResults[0].pk
			);
			data_to_send.set(
				"permission_set_name",
				this.permissionSetNameModel
			);
			data_to_send.set(
				"administration_assign_user_to_group",
				this.administrationAssignUserToGroupModel
			);
			data_to_send.set(
				"administration_create_group",
				this.administrationCreateGroupModel
			);
			data_to_send.set(
				"administration_create_permission_set",
				this.administrationCreatePermissionSetModel
			);
			data_to_send.set(
				"administration_create_user",
				this.administrationCreateUserModel
			);
			data_to_send.set("bug_client", this.bugClientModel);
			data_to_send.set("customer", this.customerModel);
			data_to_send.set("kanban_board", this.kanbanModel);
			data_to_send.set("kanban_card", this.kanbanCardModel);
			data_to_send.set("organisation", this.organisationModel);
			data_to_send.set("project", this.projectModel);
			data_to_send.set("requirement", this.requirementModel);
			data_to_send.set(
				"request_for_change",
				this.requestForChangeModel
			);
			data_to_send.set("task", this.taskModel);
			data_to_send.set("document", this.documentModel);
			data_to_send.set("kanban_comment", this.kanbanCommentModel);
			data_to_send.set("project_history", this.projectHistoryModel);
			data_to_send.set("task_history", this.taskHistoryModel);
			data_to_send.set("tag", this.tagModel);

			//Send data
			this.axios.post(
				`${this.rootUrl}permission_set_information/${this.permissionSetResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Permission Set",
					message: "We have updated your permission set successfully",
					extra_classes: "bg-success",
					unique_type: "update_permission_set",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error saving changes",
					message: `Sorry, we could not save your changes. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_permission_set",
				});
			});
		},
		updatePropertyValue(data) {
			//Update the property with what we require
			this[data.property] = data.value;
		},
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});
	},
};
</script>

<style scoped></style>
