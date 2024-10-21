<template>
	<div class="card">
		<div class="card-body">
			<h1>Unassigned Objects</h1>
			<hr/>

			<div
				class="alert alert-dark"
				v-if="!isLoaded"
			>
				Still obtaining a list of assigned objects
			</div>

			<!-- Requirements -->
			<render-object-card
				v-if="objectResults.requirement.length > 0"
				v-bind:search-results="objectResults.requirement"
				v-bind:import-variables="requirementVariables"
				destination="requirement"
			></render-object-card>

			<!-- Projects -->
			<render-object-card
				v-if="objectResults.project.length > 0"
				v-bind:search-results="objectResults.project"
				v-bind:import-variables="projectVariables"
				destination="project"
			></render-object-card>

			<!-- Tasks -->
			<render-object-card
				v-if="objectResults.task.length > 0"
				v-bind:search-results="objectResults.task"
				v-bind:import-variables="taskVariables"
				destination="task"
			></render-object-card>

			<!-- If there are no objects -->
			<div
				v-if="countObjects === 0 && isLoaded"
				class="alert alert-primary"
			>
				Good Work - all objects have been assigned to at least one user.
			</div>
		</div>
	</div>
</template>

<script>
//Components
import RenderObjectCard from '../render/RenderObjectCard.vue';

export default {
	name: "DashboardUnassignedObjects",
	components: {
		RenderObjectCard,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			isLoaded: false,
			objectResults: {
				requirement: [],
				project: [],
				task: [],
			},
			projectVariables: {
				header: "Projects",
				prefix: "Pro",
				id: "project_id",
				title: "project_name",
				status: "project_status__project_status",
				end_date: "project_end_date",
			},
			requirementVariables: {
				header: "Your Requirements",
				prefix: "Req",
				id: "requirement_id",
				title: "requirement_title",
				status: "requirement_status__requirement_status",
				end_date: "",
			},
			taskVariables: {
				header: "Tasks",
				prefix: "Task",
				id: "task_id",
				title: "task_short_description",
				status: "task_status__task_status",
				end_date: "task_end_date",
			},
		};
	},
	methods: {
		getMyObjects() {
			//Use axios to get the objects assigned to me
			this.axios
				.post(`${this.rootUrl}dashboard/get/unassigned_objects/`)
				.then((response) => {
					this.objectResults = response.data;

					//Update loading status
					this.isLoaded = true;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Getting Dashboard Data",
						message: `Can't get data for My Objects. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
	},
	computed: {
		countObjects() {
			return (
				this.objectResults.requirement.length +
				this.objectResults.project.length +
				this.objectResults.task.length
			);
		},
	},
	mounted() {
		//Get the data we want
		this.getMyObjects();

		//Update the state management
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		})
	},
};
</script>
