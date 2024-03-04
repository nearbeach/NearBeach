<template>
	<list-tags-module></list-tags-module>

	<hr>

	<list-public-links></list-public-links>

	<hr v-if="['project', 'task', 'requirement'].includes(this.destination)">

	<bugs-module
		v-if="['project', 'task', 'requirement'].includes(this.destination)"
	></bugs-module>
</template>

<script>
// JavaScript Libraries
import BugsModule from "./BugsModule.vue";
import ListPublicLinks from "./ListPublicLinks.vue";
import ListTagsModule from "./ListTagsModule.vue";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "MiscModule",
	components: {
		BugsModule,
		ListPublicLinks,
		ListTagsModule,
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
		}),
	},
};
</script>

<style scoped></style>
