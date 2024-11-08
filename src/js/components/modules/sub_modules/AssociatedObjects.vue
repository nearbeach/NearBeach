<template>
	<div>
		<h2>
			Associated Objects
		</h2>
		<p class="text-instructions">
			The following are current OPEN objects associated with the organisation.
		</p>
		<hr v-if="projectResults.length + taskResults.length + requirementResults.length > 0"/>

		<!-- Project Results -->
		<render-object-card v-bind:search-results="projectResults"
							v-bind:import-variables="projectVariables"
							destination="project"
							v-if="projectResults.length > 0"
		></render-object-card>


		<!-- Requirement Results -->
		<render-object-card v-bind:search-results="requirementResults"
							v-bind:import-variables="requirementVariables"
							destination="requirement"
							v-if="requirementResults.length > 0"
		></render-object-card>


		<!-- Task Results -->
		<render-object-card v-bind:search-results="taskResults"
							v-bind:import-variables="taskVariables"
							destination="task"
							v-if="taskResults.length > 0"
		></render-object-card>

		<!-- Only show when there are no associated tasks -->
		<div
			class="spacer"
			v-if="projectResults.length + taskResults.length + requirementResults.length === 0"
		></div>

		<div
			class="alert alert-info"
			v-if="projectResults.length + taskResults.length + requirementResults.length === 0"
		>
			There are currently no Objects associated with this Organisation.
			You can create some new objects by click on the "New Objects" menu
			item.
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

import RenderObjectCard from "../../render/RenderObjectCard.vue";

export default {
	name: "AssociatedObjects",
	components: {
		RenderObjectCard,
	},
	data() {
		return {
			projectResults: [],
			projectVariables: {
				header: "Projects",
				prefix: "Pro",
				id: "project_id",
				title: "project_name",
				status: "project_status_text",
			},
			requirementResults: [],
			requirementVariables: {
				header: "Requirements",
				prefix: "Req",
				id: "requirement_id",
				title: "requirement_title",
				status: "requirement_status__requirement_status",
			},
			taskResults: [],
			taskVariables: {
				header: "Tasks",
				prefix: "Task",
				id: "task_id",
				title: "task_short_description",
				status: "task_status_text",
			},
		};
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		getAssociatedObjectResults() {
			if (this.locationId === 0) {
				setTimeout(() => {
					this.getAssociatedObjectResults();
				}, 100);

				return;
			}

			//All is good - get the data
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/associated_objects/`
			).then((response) => {
				this.projectResults = response.data.project;
				this.requirementResults = response.data.requirement;
				this.taskResults = response.data.task;
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Associated Objects",
					message: `Sorry, we could not get associated objects. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getFriendlyDate(input_date) {
			const options = {
					weekday: "long",
					year: "numeric",
					month: "long",
					day: "numeric",
				},
				local_date = new Date(input_date);

			return local_date.toLocaleString("en-US", options);
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getAssociatedObjectResults();
		});
	},
};
</script>


