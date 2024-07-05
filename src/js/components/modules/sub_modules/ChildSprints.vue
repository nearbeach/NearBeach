<template>
	<h2>List Sprints</h2>
	<p class="text-instructions">
		Lists out all the sprints associated with this particular object.
	</p>

	<div v-if="allowedObjects.includes(destination)">
		<div v-if="sprintResults.length === 0"
			 class="alert alert-info"
		>
			Currently there are no current sprints.
		</div>

		<!-- CURRENT SPRINTS-->
		<render-sprint-card
			v-bind:sprint-results="sprintResults"
			v-bind:can-delete="false"
		></render-sprint-card>

		<!-- BUTTONS-->
		<div class="row submit-row"
			v-if="userLevel >= 2"
		>
			<div class="col-md-12">
				<button class="btn btn-primary save-changes"
					v-on:click="openCreateModal"
				>
					Create New Sprint
				</button>
			</div>
		</div>
		<hr v-if="destination === 'project'" class="mt-4">
	</div>

	<new-sprint-wizard
		v-if="allowedObjects.includes(destination)"
		v-bind:sprint-results-length="sprintResults.length"
	></new-sprint-wizard>
</template>

<script>
//vuex
import { mapGetters } from "vuex";

//Bootstrap
import { Modal } from "bootstrap";

//Components
import NewSprintWizard from "../wizards/NewSprintWizard.vue";
import RenderSprintCard from "./RenderSprintCard.vue";

export default {
	name: "ChildSprints",
	components: {
		RenderSprintCard,
		NewSprintWizard,
	},
	data() {
		return {
			allowedObjects: [
				"project",
				"requirement",
			],
			sprintResults: [],
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
		closeModal() {
			document.getElementById("createNewSprintButton").click();
		},
		getSprints() {
			const url = `${this.rootUrl}object_data/${this.destination}/${this.locationId}/sprint_list/child/`;

			this.axios.post(
				url,
			).then((response) => {
				//Update the data
				this.sprintResults = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Sprint List",
					message: `Sorry, could not get child sprints. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		openCreateModal() {
			const modal = new Modal(document.getElementById("createNewSprintModal"));
			modal.show();
		},
	},
	mounted() {
		this.$nextTick(() => {
			//Only run the get sprints if the destination is correct
			if (this.allowedObjects.includes(this.destination)) {
				this.getSprints();
			}
		});
	},
}
</script>