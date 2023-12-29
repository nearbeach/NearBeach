<template>
	<list-tags-module></list-tags-module>

	<hr>

	<list-public-links></list-public-links>
</template>

<script>
// JavaScript Libraries
import ListPublicLinks from "./ListPublicLinks.vue";
import ListTagsModule from "./ListTagsModule.vue";

export default {
	name: "MiscModule",
	components: {
		ListPublicLinks,
		ListTagsModule,
	},
};
</script>

<style scoped></style>
