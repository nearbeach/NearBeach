<template>
	<h2>AssignedSprints</h2>
	<p class="text-instructions">
		Lists all sprints that contains this object.
	</p>

	<h3
		v-if="currentSprints.length > 0"
	>
		Current
	</h3>
	<render-sprint-card
		v-bind:sprint-results="currentSprints"
		v-on:confirm_remove_sprint="confirmRemoveSprintFunction($event)"
	></render-sprint-card>

	<h3
		v-if="finishedSprints.length > 0"
	>
		Finished
	</h3>
	<render-sprint-card
		v-bind:sprint-results="finishedSprints"
		v-on:confirm_remove_sprint="confirmRemoveSprintFunction($event)"
	></render-sprint-card>

	<div class="alert alert-info"
		v-if="currentSprints.length + finishedSprints.length === 0"
	>
		Currently this object has not been assigned to any sprints.
	</div>

	<div class="row submit-row">
		<div class="col-md-12">
			<button class="btn btn-primary save-changes"
					v-on:click="addToSprint"
					v-if="userLevel >= 2"
			>
				Add Object To Sprint
			</button>
		</div>
	</div>

	<add-sprint-wizard
		v-on:update_sprint_list="updateSprintList($event)"
	></add-sprint-wizard>

	<confirm-remove-sprint
		v-bind:confirm-remove-sprint="confirmRemoveSprint"
		v-on:update_sprint_list="updateSprintList($event)"
	></confirm-remove-sprint>
</template>

<script>
//vuex
import { mapGetters } from "vuex";

//Bootstrap
import { Modal } from "bootstrap";

//Components
import AddSprintWizard from "../wizards/AddSprintWizard.vue";
import RenderSprintCard from "./RenderSprintCard.vue";
import ConfirmRemoveSprint from "../wizards/ConfirmRemoveSprint.vue";

export default {
	name: "AssignedSprints",
	components: {
		ConfirmRemoveSprint,
		RenderSprintCard,
		AddSprintWizard,
	},
	data() {
		return {
			allowedObjects: [
				"requirement_item",
				"project",
				"task",
			],
			confirmRemoveSprint: {
				"sprint_id": 0,
				"sprint_name": "",
			},
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
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		addToSprint() {
			const modal = new Modal(document.getElementById("addSprintWizardModal"));
			modal.show();
		},
		confirmRemoveSprintFunction(data) {
			//Update data
			this.confirmRemoveSprint = data;

			//Open Modal
			const modal = new Modal(document.getElementById("confirmSprintRemoveModal"));
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
			if (this.allowedObjects.includes(this.destination)) {
				this.getAssignedSprints();
			}
		});
	},
}
</script>