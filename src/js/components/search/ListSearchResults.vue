<template>
	<div class="card search-card">
		<div class="card-body">
			<h2>{{ importVariables.header }} Search Results</h2>
			<hr/>

			<render-object-card v-bind:search-results="searchResults"
								v-bind:import-variables="importVariables"
								v-bind:destination="destination"
			></render-object-card>
		</div>
	</div>
</template>

<script>
//Components
import RenderObjectCard from "../render/RenderObjectCard.vue";

export default {
	name: "ListSearchResults",
	components: {
		RenderObjectCard,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		importVariables: {
			type: Object,
			default: () => {
				return {
					header: "",
					prefix: "",
					id: 0,
					title: "",
					status: "",
				};
			},
		}, // {header, prefix,id, title, status}
		searchResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
};
</script>

<style scoped></style>
