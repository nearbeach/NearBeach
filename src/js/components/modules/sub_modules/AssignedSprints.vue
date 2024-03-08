<template>
	<h2>AssignedSprints</h2>
	<p class="text-instructions">
		Lists all sprints that contains this object.
	</p>

	<h3 v-if="currentSprints.length !== 0">Current Sprints</h3>
	<div v-if="currentSprints.length !== 0"></div>

	<h3 v-if="finishedSprints.length !== 0">Finished Sprints</h3>
	<div v-if="finishedSprints.length !== 0"></div>

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
</template>

<script>
//vuex
import { mapGetters } from "vuex";

export default {
	name: "AssignedSprints",
	data() {
		return {
			currentSprints: [],
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
		addToSprint() {},
		getAssignedSprints() {}
	},
	mounted() {
		this.$nextTick(() => {
			this.getAssignedSprints();
		});
	},
}
</script>