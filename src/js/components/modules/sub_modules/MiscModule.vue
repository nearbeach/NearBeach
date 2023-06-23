<template>
	<div>
		<list-tags-module
			v-bind:destination="destination"
			v-bind:location-id="locationId"
		></list-tags-module>
	</div>
</template>

<script>
	// JavaScript Libraries
	import ListTagsModule from "./ListTagsModule.vue";

	export default {
		name: "MiscModule",
		components: {
			ListTagsModule,
		},
		props: {
			destination: {
				type: String,
				default: "",
			},
			locationId: {
				type: Number,
				default: 0,
			},
		},
		mixins: [],
		computed: {},
		data() {
			return {
				noteHistoryResults: [],
			};
		},
		methods: {},
		mounted() {},
	};
</script>

<style scoped></style>
