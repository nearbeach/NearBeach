<template>
	<child-sprints
		v-if="childSprintsAllowedDestination.includes(destination)"
	></child-sprints>

	<assigned-sprints
		v-if="assignedSprintAllowedDestination.includes(destination)"
	></assigned-sprints>
</template>

<script>
//Import components
import ChildSprints from "./ChildSprints.vue";
import AssignedSprints from "./AssignedSprints.vue";

//vuex
import { mapGetters } from "vuex";

export default {
	name: "ListSprints",
	components: {
		AssignedSprints,
		ChildSprints,
	},
	data() {
		return {
			assignedSprintAllowedDestination: [
				"requirement_item",
				"project",
				"task",
			],
			childSprintsAllowedDestination: [
				"requirement",
				"project",
			],
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
		}),
	},
}
</script>