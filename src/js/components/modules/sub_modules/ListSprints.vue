<template>
	<h2>List Sprints</h2>
	<p class="text-instructions">
		Lists out all the sprints associated with this particular object.
	</p>

	<child-sprints></child-sprints>

	<assigned-sprints></assigned-sprints>
</template>

<script>
//Import components
import ChildSprints from "./ChildSprints.vue";
import AssignedSprints from "./AssignedSprints.vue";

export default {
	name: "ListSprints",
	components: {
		AssignedSprints,
		ChildSprints,
	},
}
</script>