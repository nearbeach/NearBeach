<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Kanban</h1>
				<hr/>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<strong>Please note</strong>
						<p class="text-instructions">Board names must be unique.</p>
					</div>

					<!-- BOARD NAME -->
					<div class="col-md-8">
						<div class="form-group">
							<label
							>Kanban Board Name
								<validation-rendering
									v-bind:error-list="v$.kanbanBoardNameModel.$errors"
								></validation-rendering>
								<span
									class="error"
									v-if="!uniqueKanbanBoardName"
								>
								Please supply a unique name</span
								>
								<span
									class="error"
									v-if="checkingKanbanBoardName"
								>
								Checking kanban name...</span
								>
							</label>
							<input
								type="text"
								class="form-control"
								v-model="kanbanBoardNameModel"
							/>
						</div>
					</div>
				</div>
				<hr/>

				<!-- Properties for the drag and drop coloumns/levels -->
				<div class="row">
					<div class="col-md-4">
						<h2>Columns & Levels</h2>
						<p class="text-instructions">
							Drag the cards around to sort out the columns how you
							want them.
						</p>
					</div>
					<div class="col-md-4">
						<kanban-property-order
							v-bind:property-list="columnModel"
							v-bind:is-dirty="v$.columnModel.$dirty"
							property-name="Column"
							source="columnModel"
							v-on:update_property_list="updatePropertyList($event)"
						></kanban-property-order>
					</div>
					<div class="d-block d-md-none d-lg-none d-xl-none d-xxl-none mt-3">
						<hr />
					</div>
					<div class="col-md-4">
						<kanban-property-order
							v-bind:property-list="levelModel"
							v-bind:is-dirty="v$.columnModel.$dirty"
							property-name="Level"
							source="levelModel"
							v-on:update_property_list="updatePropertyList($event)"
						></kanban-property-order>
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
					destination="kanban_board"
				></group-permissions>

				<!-- SAVE -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							class="btn btn-primary save-changes"
							v-on:click="addNewKanban"
							v-bind:disabled="disableSubmitButton"
						>
							Add Kanban
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import KanbanPropertyOrder from "./KanbanPropertyOrder.vue";
import GroupPermissions from "../permissions/GroupPermissions.vue";

// Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "NewKanban",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		GroupPermissions,
		KanbanPropertyOrder,
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
		theme: {
			type: String,
			default: "",
		},
		userGroupPermissions: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			checkingKanbanBoardName: false,
			columnModel: [
				{
					id: 0,
					property: "Normal",
					title: "Backlog",
				},
				{
					id: 1,
					property: "Blocked",
					title: "Blocked",
				},
				{
					id: 2,
					property: "Normal",
					title: "In Progress",
				},
				{
					id: 4,
					property: "Normal",
					title: "Review and QA",
				},
				{
					id: 5,
					property: "Closed",
					title: "Completed",
				},
			],
			disableSubmitButton: false,
			displayGroupPermissionIssue: false,
			groupModel: [],
			kanbanBoardNameModel: "",
			levelModel: [
				{
					id: 0,
					title: "Sprint 1",
				},
				{
					id: 1,
					title: "Sprint 2",
				},
			],
			searchTimeout: "",
			uniqueKanbanBoardName: true,
		};
	},
	validations: {
		columnModel: {
			required,
		},
		groupModel: {
			required,
		},
		kanbanBoardNameModel: {
			required,
		},
		levelModel: {
			required,
		},
	},
	watch: {
		kanbanBoardNameModel() {
			//Apply checking flag
			this.checkingKanbanBoardName = true;

			//Reset the timer if it exists
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			// If the obj.search is defined, we want to use the search Defined. Otherwise search undefined
			if (this.kanbanBoardNameModel === undefined) {
				// Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
				this.searchTimeout = setTimeout(
					this.checkKanbanBoardName,
					500
				);
			} else {
				// Reset the clock, to only search if there is an uninterupted 0.5s of no typing.
				if (this.kanbanBoardNameModel.length >= 3) {
					this.searchTimeout = setTimeout(
						this.checkKanbanBoardName,
						500,
						this.kanbanBoardNameModel,
						null
					);
				}
			}
		},
	},
	methods: {
		useNBTheme,
		addNewKanban() {
			//Check form validation
			this.v$.$touch();

			if (
				this.v$.$invalid ||
				!this.uniqueKanbanBoardName ||
				this.checkingKanbanBoardName ||
				this.displayGroupPermissionIssue
			) {
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Disable submit button
			this.disableSubmitButton = true;

			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set(
				"kanban_board_name",
				this.kanbanBoardNameModel
			);

			//Loop through all the column models
			this.columnModel.forEach((column) => {
				data_to_send.append("column_title", column.title);
				data_to_send.append("column_property", column.property);
			});

			this.levelModel.forEach((level) => {
				data_to_send.append("level_title", level.title);
			});

			this.groupModel.forEach((single_group) => {
				data_to_send.append("group_list", single_group);
			});

			//Use axios to send the data
			this.axios.post(
				`${this.rootUrl}new_kanban_save/`,
				data_to_send
			).then((response) => {
				//Go to that webpage
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Issue Creating new Kanban board",
					message: `Issues creating new kanban board -> Error ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				this.disableSubmitButton = false;
			});
		},
		checkKanbanBoardName() {
			//Send the Kanban board name to the backend - it will send back the results.
			const data_to_send = new FormData();
			data_to_send.set(
				"kanban_board_name",
				this.kanbanBoardNameModel
			);

			//Use axios to query the database
			this.axios.post(
				`${this.rootUrl}kanban_information/check_kanban_board_name/`,
				data_to_send
			).then((response) => {
				//If the data came back empty - then the kanban board name is unique
				this.uniqueKanbanBoardName = response.data.length === 0;

				//Checking kanban board name is finished
				this.checkingKanbanBoardName = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Issue checking Kanban board name",
					message: `Issues checking kanban board name -> Error ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});
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
		updatePropertyList(data) {
			this[data.source] = data.data;
		},
	},
};
</script>


