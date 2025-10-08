<template>
	<div class="card search-card"
		 v-bind:style="cardClass"
		 ref="searchCard"
	>
	  	<div class="card-header">
			<h2>{{ importVariables.header }} Search Results</h2>
		</div>
		<div class="card-body">
			<render-object-card v-bind:search-results="localSearchResults"
								v-bind:import-variables="importVariables"
								v-bind:destination="destination"
			></render-object-card>
		</div>
		<div class="card-footer">
			<nav v-bind:aria-label="`Pagination for ${importVariables.header}`"
				v-if="setOfPages.length > 1"
			>
				<ul class="pagination justify-content-center m-0"
				>
					<li v-for="index in setOfPages"
						v-bind:key="index.destinationPage"
						v-bind:class="getClasses(index.destinationPage)"
					>
						<a v-if="parseInt(index.destinationPage) !== parseInt(currentPage)"
							class="page-link"
						   	href="javascript:void(0)"
						   	v-on:click="changePage(index.destinationPage)"
						>
							{{ index.text }}
						</a>
						<span v-else
							  class="page-link"
						>
							{{ index.text }}
						</span>
					</li>
				</ul>
			</nav>
		</div>
	</div>
</template>

<script>
//Components
import RenderObjectCard from "Components/render/RenderObjectCard.vue";

//Composable
import {getSetOfPages} from "Composables/pagintation/getSetOfPages";

export default {
	name: "ListSearchResults",
	components: {
		RenderObjectCard,
	},
	emits: [
		"get_search_results",
	],
	props: {
		currentPage: {
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
		numberOfPages: {
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
	watch: {
		searchResults: {
			handler(new_value) {
				// Update search results
				this.localSearchResults = new_value;

				// Remove the forced styling
				this.cardClass = "";

				// Update set of pages
				this.setOfPages = getSetOfPages(this.currentPage, this.numberOfPages);
			},
			deep: true,
		}
	},
	data() {
		return {
			cardClass: "",
			localSearchResults: this.searchResults,
			setOfPages: [],
		};
	},
	methods: {
		getSetOfPages,
		changePage(destination_page) {
			// Update the card class so the card does not collapse
			this.cardClass = `height: ${this.$refs.searchCard.offsetHeight}px`

			// Default search results to nothing
			this.localSearchResults = [];

			// Translate destination - rfc -> request_for_change
			const destination = this.destination === "rfc" ? "request_for_change" : this.destination;

			//Emit up the change for search
			this.$emit("get_search_results", {
				"array_of_objects": [destination],
				"destination_page": destination_page
			});

			// Apply the new set of pages
			this.setOfPages = this.getSetOfPages(destination_page, this.numberOfPages);
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
	},
	mounted() {
		// Sets the default array of pages
		this.setOfPages = getSetOfPages(1, this.numberOfPages);
	}
};
</script>


