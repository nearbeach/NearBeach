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
import RenderObjectCard from "../render/RenderObjectCard.vue";

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
		changePage(destination_page) {
			// Update the card class so the card does not collapse
			this.cardClass = `height: ${this.$refs.searchCard.offsetHeight}px`

			// Default search results to nothing
			this.localSearchResults = [];

			//Emit up the change for search
			this.$emit("get_search_results", {
				"array_of_objects": [this.destination],
				"destination_page": destination_page
			});

			// Apply the new set of pages
			this.updateSetOfPages(destination_page);
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
		updateSetOfPages(destination_page) {
			if (this.numberOfPages <= 7)
			{
				// There are not enough blocks to add in the first/previous/next/last buttons
				// Array.from({length: 10}, (_, i) => i + 1)
				this.setOfPages = Array.from(
					{ length: this.numberOfPages },
					(_, index) => {
						return {
							destinationPage: index + 1,
							text: `${index + 1}`,
						}
					}
				)

				//Finished
				return;
			}

			if (destination_page <= 4)
			{
				// At the start of the pagination
				this.setOfPages = [
					{ destinationPage: 1, text: "1"},
					{ destinationPage: 2, text: "2"},
					{ destinationPage: 3, text: "3"},
					{ destinationPage: 4, text: "4"},
					{ destinationPage: 5, text: "5"},
					{ destinationPage: 6, text: ">"},
					{ destinationPage: this.numberOfPages, text: ">>"},
				]

				// Done
				return;
			}

			if (destination_page > this.numberOfPages - 4)
			{
				// At the end of the pagination
				this.setOfPages = [
					{ destinationPage: 1, text: "<<"},
					{ destinationPage: this.numberOfPages - 5, text: `<`},
					{ destinationPage: this.numberOfPages - 4, text: `${this.numberOfPages - 4}`},
					{ destinationPage: this.numberOfPages - 3, text: `${this.numberOfPages - 3}`},
					{ destinationPage: this.numberOfPages - 2, text: `${this.numberOfPages - 2}`},
					{ destinationPage: this.numberOfPages - 1, text: `${this.numberOfPages - 1}`},
					{ destinationPage: this.numberOfPages, text: `${this.numberOfPages}`},
				]

				// Done
				return;
			}

			this.setOfPages = [
				{ destinationPage: 1, text: "<<"},
				{ destinationPage: destination_page - 2, text: "<"},
				{ destinationPage: destination_page - 1, text: `${destination_page - 1}`},
				{ destinationPage: destination_page, text: `${destination_page}`},
				{ destinationPage: destination_page + 1, text: `${destination_page + 1}`},
				{ destinationPage: destination_page + 2, text: ">"},
				{ destinationPage: this.numberOfPages, text: ">>"},
			]
		}
	},
	mounted() {
		// Sets the default array of pages
		this.updateSetOfPages(1);
	}
};
</script>


