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
		:sprint-results="currentSprints"
		@confirm_remove_sprint="confirmRemoveSprintFunction($event)"
	></render-sprint-card>

	<h3
		v-if="finishedSprints.length > 0"
	>
		Finished
	</h3>
	<render-sprint-card
		:sprint-results="finishedSprints"
		@confirm_remove_sprint="confirmRemoveSprintFunction($event)"
	></render-sprint-card>

	<div
v-if="currentSprints.length + finishedSprints.length === 0"
		class="alert alert-info"
	>
		Currently this object has not been assigned to any sprints.
	</div>

	<div class="row submit-row">
		<div class="col-md-12">
			<button
v-if="userLevel >= 2"
					class="btn btn-primary save-changes"
					@click="addToSprint"
			>
				Add Object To Sprint
			</button>
		</div>
	</div>

	<add-sprint-wizard
		@update_sprint_list="updateSprintList($event)"
	></add-sprint-wizard>

	<confirm-remove-sprint
		:confirm-remove-sprint="confirmRemoveSprint"
		@update_sprint_list="updateSprintList($event)"
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
	mounted() {
		this.$nextTick(() => {
			if (this.allowedObjects.includes(this.destination)) {
				this.getAssignedSprints();
			}
		});
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
}
</script>