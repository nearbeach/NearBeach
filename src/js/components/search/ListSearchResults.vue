<template>
	<div class="card search-card">
		<div class="card-body">
			<h2>{{ importVariables.header }} Search Results</h2>
			<hr/>

			<render-object-card v-bind:search-results="searchResults"
								v-bind:import-variables="importVariables"
								v-bind:destination="destination"
			></render-object-card>

			<nav v-bind:aria-label="`Pagination for ${importVariables.header}`"
				v-if="number_of_pages > 1"
			>
				<ul class="pagination justify-content-center"
				>
					<li v-for="index in number_of_pages"
						v-bind:class="getClasses(index)"
					>
						<a v-if="parseInt(index) !== parseInt(current_page)"
							class="page-link"
						   	href="javascript:void(0)"
						   	v-on:click="changePage(index)"
						>
							{{ index }}
						</a>
						<span v-else
							  class="page-link"
						>
							{{ index }}
						</span>
					</li>
				</ul>
			</nav>
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
		current_page: {
			type: Number,
			default: 0,
		},
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
		},
		number_of_pages: {
			type: Number,
			default: 0,
		},
		// {header, prefix,id, title, status}
		searchResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	methods: {
		changePage(destination_page) {
			//Emit up the change for search
			this.$emit("get_search_results", {
				"array_of_objects": [this.destination],
				"destination_page": destination_page
			});
		},
		getClasses(index) {
			if (parseInt(index) === this.current_page) {
				return "page-item active";
			}

			return "page-item";
		}
	}
};
</script>


