<template>
	<div class="row">
		<div v-if="status==='loading'"
			class="alert alert-info"
		>
			Please wait. Fetching data.
		</div>

		<div v-if="status!=='loading'"
			 class="row"
		>
			<div class="col-md-4">
				<strong>User Action Required</strong>
				<p class="text-instructions">
					Please note the following data will need to be reviewed by a human. There can be false positives within
					this data where the text in the description can be over-written. Please uncheck if you do not want this
					data over-written.
				</p>
				<p class="text-instructions">
					Alternatively, you can go to the object and manually edit the data. Please untick the row if you would
					like to take this step.
				</p>
				<p class="text-instructions">
					Best practise is to review each of these action required, as there could be false positives.
				</p>
			</div>
			<div class="col-md-8">
				<render-object-card-checkbox v-bind:search-results="projectResults.userActionRequired"
											 v-bind:import-variables="projectVariables"
											 destination="project"
											 model-target="project"
											 target="_blank"
											 v-on:update_checkbox_model="updateCheckboxModel"
											 v-if="projectResults.userActionRequired.length > 0"
				></render-object-card-checkbox>

				<render-object-card-checkbox v-bind:search-results="requirementResults.userActionRequired"
											 v-bind:import-variables="requirementVariables"
											 destination="requirement"
											 model-target="requirement"
											 target="_blank"
											 v-on:update_checkbox_model="updateCheckboxModel"
											 v-if="requirementResults.userActionRequired.length > 0"
				></render-object-card-checkbox>

				<render-object-card-checkbox v-bind:search-results="requirementItemResults.userActionRequired"
											 v-bind:import-variables="requirementItemVariables"
											 destination="requirement_item"
											 model-target="requirement_item"
											 target="_blank"
											 v-on:update_checkbox_model="updateCheckboxModel"
											 v-if="requirementItemResults.userActionRequired.length > 0"
				></render-object-card-checkbox>

				<render-object-card-checkbox v-bind:search-results="taskResults.userActionRequired"
											 v-bind:import-variables="taskVariables"
											 destination="task"
											 model-target="task"
											 target="_blank"
											 v-on:update_checkbox_model="updateCheckboxModel"
											 v-if="taskResults.userActionRequired.length > 0"
				></render-object-card-checkbox>
			</div>
			<div class="spacer"></div>
		</div>

		<div class="spacer"></div>
		<hr/>
		<div v-if="status!=='loading'"
			 class="row"
		>
			<div class="col-md-4">
				<strong>Data to be removed</strong>
				<p v-if="gdprObjectType === 'customer'"
				   class="text-instructions"
				>
					The following objects will have the customer removed from them. The objects will NOT be deleted,
					just the connection to the customer.
				</p>
			</div>
			<div class="col-md-8">
				<render-object-card v-bind:search-results="projectResults.dataToBeDeleted"
									v-bind:import-variables="projectVariables"
									destination="project"
									target="_blank"
									v-if="projectResults.dataToBeDeleted.length > 0"
				></render-object-card>

				<render-object-card v-bind:search-results="requirementResults.dataToBeDeleted"
									v-bind:import-variables="requirementVariables"
									destination="requirement"
									target="_blank"
									v-if="requirementResults.dataToBeDeleted.length > 0"
				></render-object-card>

				<render-object-card v-bind:search-results="requirementItemResults.dataToBeDeleted"
									v-bind:import-variables="requirementItemVariables"
									destination="requirement_item"
									target="_blank"
									v-if="requirementItemResults.dataToBeDeleted.length > 0"
				></render-object-card>

				<render-object-card v-bind:search-results="taskResults.dataToBeDeleted"
									v-bind:import-variables="taskVariables"
									destination="task"
									target="_blank"
									v-if="taskResults.dataToBeDeleted.length > 0"
				></render-object-card>
			</div>
		</div>
	</div>
</template>

<script>
// VueX
import { mapGetters } from "vuex";

// Components
import RenderObjectCard from "../../render/RenderObjectCard.vue";
import RenderObjectCardCheckbox from "../../render/RenderObjectCardCheckbox.vue";

export default {
	name: "GdprWizardDataVerification",
	components: {
		RenderObjectCard,
		RenderObjectCardCheckbox,
	},
	data() {
		return {
			status: "loading",
			projectModel: [],
			projectResults: {
				userActionRequired: [],
				dataToBeDeleted: []
			},
			projectVariables: {
				header: "Projects",
				prefix: "Pro",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			requirementModel: [],
			requirementResults: {
				userActionRequired: [],
				dataToBeDeleted: [],
			},
			requirementVariables: {
				header: "Requirements",
				prefix: "Req",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			requirementItemModel: [],
			requirementItemResults: {
				userActionRequired: [],
				dataToBeDeleted: [],
			},
			requirementItemVariables: {
				header: "Requirement Items",
				prefix: "Item",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			taskModel: [],
			taskResults: {
				userActionRequired: [],
				dataToBeDeleted: [],
			},
			taskVariables: {
				header: "Tasks",
				prefix: "Task",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
		}
	},
	computed: {
		...mapGetters({
			gdprObjectId: "getGdprObjectId",
			gdprObjectType: "getGdprObjectType",
			rootUrl: "getRootUrl",
		})
	},
	watch: {
		gdprObjectId() {
			//Do nothing if empty
			if (this.gdprObjectId === null || this.gdprObjectId === "") return;

			this.getData();
		}
	},
	methods: {
		getData() {
			//Tell user we are fetching data
			this.$store.dispatch("newToast", {
				header: "Fetching Data",
				message: "Please wait. Fetching Data",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "gdpr_wizard",
			})
			//Setup form data
			const data_to_send = new FormData();
			data_to_send.set("gdpr_object_type", this.gdprObjectType);
			data_to_send.set("gdpr_object_id", this.gdprObjectId);

			//Contact the backend
			this.axios.post(
				`${this.rootUrl}gdpr_wizard/get_data/`,
				data_to_send,
			).then(response => {
				this.$store.dispatch("newToast", {
					header: "Fetched Data",
					message: "Data has been fetched. Please move to Data Verification Tab to review",
					extra_classes: "bg-success",
					unique_type: "gdpr_wizard",
				});

				this.status = "loaded";

				//Load data into structure
				this.projectResults.dataToBeDeleted = response.data.data_to_be_deleted.project;
				this.projectResults.userActionRequired =response.data.user_action_required.project;
				this.requirementResults.dataToBeDeleted = response.data.data_to_be_deleted.requirement;
				this.requirementResults.userActionRequired = response.data.user_action_required.requirement;
				this.requirementItemResults.dataToBeDeleted = response.data.data_to_be_deleted.requirement_item;
				this.requirementItemResults.userActionRequired = response.data.user_action_required.requirement_item;
				this.taskResults.dataToBeDeleted = response.data.data_to_be_deleted.task;
				this.taskResults.userActionRequired = response.data.user_action_required.task;

				//Verifiy the tab
				this.$store.commit({
					type: "updateValidationData",
					tab_id: "tab_2",
					value: true,
				});
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Fetching Data",
					message: `Sorry, could not fetch the data we required. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "gdpr_wizard",
				});
			})
		},
		updateCheckboxModel(data) {
			this.$store.commit({
				type: "updateUserActionToRemove",
				modelTarget: data.modelTarget,
				value: data.value,
			});
		},
	}

}
</script>