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
			</div>
			<div class="col-md-8">
				<render-object-card v-bind:search-results="projectResults"
									v-bind:import-variables="projectVariables"
									destination="project"
									target="_blank"
									v-if="projectResults.length > 0"
				></render-object-card>
			</div>
			<div class="spacer"></div>
		</div>

		<div v-if="status!=='loading'"
			 class="row"
		>
			<div class="col-md-4">
				<strong>Data to be removed</strong>
			</div>
			<div class="col-md-8">
				ADD DATA
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
import RenderObjectCard from "../../render/RenderObjectCard.vue";

export default {
	name: "GdprWizardDataVerification",
	components: {RenderObjectCard},
	data() {
		return {
			status: "loading",
			projectResults: [],
			projectVariables: {
				header: "Projects",
				prefix: "Pro",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			requirementResults: [],
			requirementVariables: {
				header: "Requirements",
				prefix: "Req",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			requirementItemResults: [],
			requirementItemVariables: {
				header: "Requirement Items",
				prefix: "Item",
				id: "object_id",
				title: "object_title",
				status: "object_status",
			},
			taskResults: [],
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
				this.projectResults = response.data.user_action_required.project;
				this.requirementResults = response.data.user_action_required.requirement;
				this.requirementItemResults = response.data.user_action_required.requirement_item;
				this.taskResults = response.data.user_action_required.task;

				//ADD CODE
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Fetching Data",
					message: `Sorry, could not fetch the data we required. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "gdpr_wizard",
				});
			})
		}
	}

}
</script>