<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Permission Information</h1>
				<br/>
				<a :href="`${rootUrl}search/permission_set/`"
				>Go back to permission list</a
				>
				<hr/>

				<div
					v-if="permissionSetResults[0].pk === 1"
					class="alert alert-danger"
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
							v-model="permissionSetNameModel"
							type="text"
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
							:property-value="administrationAssignUserToGroupModel"
							:list-of-choices="permissionLevel"
							property="administrationAssignUserToGroupModel"
							property-label="Assign User To Group Model"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="administrationCreateGroupModel"
							:list-of-choices="permissionLevel"
							property="administrationCreateGroupModel"
							property-label="Create Groups"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="administrationCreatePermissionSetModel"
							:list-of-choices="permissionLevel"
							property-label="Create Permission Sets"
							property="administrationCreatePermissionSetModel"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="administrationCreateUserModel"
							:list-of-choices="permissionLevel"
							property="administrationCreateUserModel"
							property-label="Create Users"
							@update_property_value="updatePropertyValue($event)"
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
							:property-value="customerModel"
							:list-of-choices="permissionLevel"
							property="customerModel"
							property-label="Customers"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="organisationModel"
							:list-of-choices="permissionLevel"
							property="organisationModel"
							property-label="Organisations"
							@update_property_value="updatePropertyValue($event)"
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
							:property-value="kanbanModel"
							:list-of-choices="permissionLevel"
							property="kanbanModel"
							property-label="Kanban Boards"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="kanbanCardModel"
							:list-of-choices="permissionLevel"
							property="kanbanCardModel"
							property-label="Kanban Cards"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="projectModel"
							:list-of-choices="permissionLevel"
							property="projectModel"
							property-label="Projects"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="taskModel"
							:list-of-choices="permissionLevel"
							property="taskModel"
							property-label="Tasks"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="requestForChangeModel"
							:list-of-choices="permissionLevel"
							property="requestForChangeModel"
							property-label="Request for Change"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="requirementModel"
							:list-of-choices="permissionLevel"
							property="requirementModel"
							property-label="Requirements"
							@update_property_value="updatePropertyValue($event)"
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
							:property-value="documentModel"
							:list-of-choices="permissionBoolean"
							property="documentModel"
							property-label="Grants upload ability"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="kanbanNoteModel"
							:list-of-choices="permissionBoolean"
							property="kanbanNoteModel"
							property-label="Grants notes on Kanban Boards"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="organisationNoteModel"
							:list-of-choices="permissionBoolean"
							property="organisationNoteModel"
							property-label="Grants notes on Organisations"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="projectNoteModel"
							:list-of-choices="permissionBoolean"
							property="projectNoteModel"
							property-label="Grants notes on Projects"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="requirementNoteModel"
							:list-of-choices="permissionBoolean"
							property="requirementNoteModel"
							property-label="Grants notes on Requirements"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="requirementItemNoteModel"
							:list-of-choices="permissionBoolean"
							property="requirementItemNoteModel"
							property-label="Grants notes on Requirement Items"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="taskNoteModel"
							:list-of-choices="permissionBoolean"
							property="taskNoteModel"
							property-label="Grants notes on Tasks"
							@update_property_value="updatePropertyValue($event)"
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
							:property-value="bugClientModel"
							:list-of-choices="permissionLevel"
							property="bugClientModel"
							property-label="Configure bug clients"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="tagModel"
							:list-of-choices="permissionLevel"
							property="tagModel"
							property-label="Configure tags"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>

						<single-permission-properties
							:property-value="scheduleObjectModel"
							:list-of-choices="permissionLevel"
							property="scheduleObjectModel"
							property-label="Configure Schedule Object"
							@update_property_value="updatePropertyValue($event)"
						></single-permission-properties>
					</div>
				</div>

				<!-- Save Changes -->
				<!-- Don't show if we are looking at admin -->
				<hr v-if="permissionSetResults[0].pk !== 1"/>
				<div
					v-if="permissionSetResults[0].pk !== 1"
					class="row submit-row"
				>
					<div class="col-md-12">
						<button
							class="btn btn-danger"
							@click="confirmDelete"
						>
							Delete Permission Set
						</button>
						<button
							class="btn btn-primary save-changes"
							@click="saveChanges"
						>
							Save Permission Set
						</button>
					</div>
				</div>
			</div>
		</div>

		<confirm-permission-set-delete
			:permission-set-id="permissionSetResults[0].pk"
		></confirm-permission-set-delete>
	</n-config-provider>
</template>

<script>
import SinglePermissionProperties from "./SinglePermissionProperties.vue";
import ConfirmPermissionSetDelete from "./ConfirmPermissionSetDelete.vue";

//Modal
import { Modal } from "bootstrap";

//Composable
import {useNBTheme} from "Composables/theme/useNBTheme";

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
			permissionSetNameModel: this.permissionSetResults[0].fields.permission_set_name,
			administrationAssignUserToGroupModel: this.permissionSetResults[0].fields.administration_assign_user_to_group,
			administrationCreateGroupModel: this.permissionSetResults[0].fields.administration_create_group,
			administrationCreatePermissionSetModel: this.permissionSetResults[0].fields.administration_create_permission_set,
			administrationCreateUserModel: this.permissionSetResults[0].fields.administration_create_user,
			bugClientModel: this.permissionSetResults[0].fields.bug_client,
			customerModel: this.permissionSetResults[0].fields.customer,
			kanbanModel: this.permissionSetResults[0].fields.kanban_board,
			kanbanCardModel: this.permissionSetResults[0].fields.kanban_card,
			organisationModel: this.permissionSetResults[0].fields.organisation,
			projectModel: this.permissionSetResults[0].fields.project, 
			requestForChangeModel: this.permissionSetResults[0].fields.request_for_change,
			requirementModel: this.permissionSetResults[0].fields.requirement,
			tagModel: this.permissionSetResults[0].fields.tag,
			taskModel: this.permissionSetResults[0].fields.task,
			documentModel: this.permissionSetResults[0].fields.document,
			kanbanNoteModel: this.permissionSetResults[0].fields.kanban_note,
			projectNoteModel: this.permissionSetResults[0].fields.project_note,
			scheduleObjectModel: this.permissionSetResults[0].fields.schedule_object,
			taskNoteModel: this.permissionSetResults[0].fields.task_note,
			requirementNoteModel: this.permissionSetResults[0].fields.requirement_note,
			requirementItemNoteModel: this.permissionSetResults[0].fields.requirement_item_note,
			organisationNoteModel: this.permissionSetResults[0].fields.organisation_note,

		};
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});

		this.$store.commit({
			type: "updateTitle",
			title: this.permissionSetNameModel,
		});
	},
	methods: {
		useNBTheme,
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
			data_to_send.set("kanban_note", this.kanbanNoteModel);
			data_to_send.set("project_note", this.projectNoteModel);
			data_to_send.set("schedule_object", this.scheduleObjectModel);
			data_to_send.set("task_note", this.taskNoteModel);
			data_to_send.set("requirement_note", this.requirementNoteModel);
			data_to_send.set("requirement_item_note", this.requirementItemNoteModel);
			data_to_send.set("organisation_note", this.organisationNoteModel);
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
};
</script>


