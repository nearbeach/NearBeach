<template>
	<list-tags-module></list-tags-module>

	<add-tag-wizard></add-tag-wizard>

	<hr>

	<list-public-links></list-public-links>

</template>

<script>
// JavaScript Libraries
import AddTagWizard from "../wizards/AddTagWizard.vue";
import ListPublicLinks from "./ListPublicLinks.vue";
import ListTagsModule from "./ListTagsModule.vue";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "MiscModule",
	components: {
		AddTagWizard,
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


