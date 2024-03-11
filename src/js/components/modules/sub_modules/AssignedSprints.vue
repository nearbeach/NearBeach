<template>
	<h2>AssignedSprints</h2>
	<p class="text-instructions">
		Lists all sprints that contains this object.
	</p>

	<render-object-card
		v-if="currentSprints.length > 0"
		v-bind:destination="'sprint'"
		v-bind:import-variables="currentImportVariables"
		v-bind:search-results="currentSprints"
	></render-object-card>

	<render-object-card
		v-if="finishedSprints.length > 0"
		v-bind:destination="'sprint'"
		v-bind:import-variables="finishedImportVariables"
		v-bind:search-results="finishedSprints"
	></render-object-card>

	<div class="alert alert-info"
		v-if="currentSprints.length + finishedSprints.length === 0"
	>
		Currently this object has not been assigned to any sprints.
	</div>

	<div class="row submit-row">
		<div class="col-md-12">
			<button class="btn btn-primary save-changes"
					v-on:click="addToSprint"
			>
				Add Object To Sprint
			</button>
		</div>
	</div>

	<add-sprint-wizard
		v-on:update_sprint_list="updateSprintList($event)"
	></add-sprint-wizard>
</template>

<script>
//vuex
import { mapGetters } from "vuex";

//Bootstrap
import { Modal } from "bootstrap";

//Components
import AddSprintWizard from "../wizards/AddSprintWizard.vue";
import RenderObjectCard from "../../render/RenderObjectCard.vue";

export default {
	name: "AssignedSprints",
	components: {
		RenderObjectCard,
		AddSprintWizard,
	},
	data() {
		return {
			currentImportVariables: {
				header: "List of Current Sprints",
				prefix: "sprint",
				id: "sprint_id",
				title: "sprint_name",
				status: "sprint_status",
			},
			currentSprints: [],
			finishedImportVariables: {
				header: "List of Finished Sprints",
				prefix: "sprint",
				id: "sprint_id",
				title: "sprint_name",
				status: "sprint_status",
			},
			finishedSprints: [],
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addToSprint() {
			const modal = new Modal(document.getElementById("addSprintWizardModal"));
			modal.show();
		},
		getAssignedSprints() {
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/sprint_list/assigned/`,
			).then((response) => {
				//Update local data
				this.updateSprintList(response.data);
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					headers: "Error fetching assigned sprints",
					message: `Could not get the data. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})
		},
		updateSprintList(data) {
		//Update local data
			this.currentSprints = data.filter((row) => {
				return row.sprint_status !== "Finished";
			});

			this.finishedSprints = data.filter((row) => {
				return row.sprint_status === "Finished";
			});
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getAssignedSprints();
		});
	},
}
</script>