<template>
	<div>
		<div class="card">
			<div class="card-body">
				<!-- HEADING -->
				<h1>Search Sprints</h1>
				<hr/>

				<!-- SEARCH FIELD -->
				<div class="form-row">
					<div class="form-group">
						<label>Search:</label>
						<input
							type="text"
							class="form-control search-organisation"
							v-model="searchModel"
							maxlength="250"
						/>
					</div>
					<div class="form-group">
						<input
							type="checkbox"
							id="inlcudeClosedObjects"
							v-model="includeClosedObjectsModel"
						/>
						<label for="inlcudeClosedObjects">
							Include Closed Objects</label
						>
					</div>
				</div>
			</div>
		</div>
		<br/>

		<!-- SPRINTS -->
		<list-search-results
			v-if="searchResults.length > 0"
			v-bind:search-results="searchResults"
			v-bind:import-variables="sprintVariables"
			v-bind:number-of-pages="numberOfPages"
			v-bind:current-page="currentPage"
			v-on:get_search_results="changePage"
			destination="sprint"
		></list-search-results>

		<!-- WHEN THERE ARE NO RESULTS -->
		<div
			v-if="searchResults.length === 0"
			class="alert alert-warning"
		>
			Sorry - but there are currently no sprints matching the search terms
		</div>
	</div>
</template>

<script>
//Vue Components
import ListSearchResults from "./ListSearchResults.vue";

export default {
	name: "SearchObjects",
	components: {
		ListSearchResults,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			currentPage: 1,
			includeClosedObjectsModel: this.includeClosed,
			numberOfPages: 1,
			sprintVariables: {
				header: "Sprint",
				prefix: "spr",
				id: "sprint_id",
				title: "sprint_name",
				status: "sprint_status",
			},
			searchModel: "",
			searchResults: [],
			searchTimeout: "",
		};
	},
	methods: {
		changePage(data) {
			this.currentPage = data.destination_page;
			this.getSearchResults();
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
		getSearchResults() {
			// Setup the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);
			data_to_send.set("include_closed", this.includeClosedObjectsModel);
			data_to_send.set("array_of_objects", "sprint");
			data_to_send.set("destination_page", this.currentPage);

			//Use axios to request data
			this.axios.post(
				`${this.rootUrl}search/sprint/data/`,
				data_to_send
			).then((response) => {
				//Update the searchResults with the data
				this.searchResults = response.data.sprint;
				this.numberOfPages = response.data.sprint_number_of_pages;
				this.currentPage = response.data.sprint_current_page;


			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get search results",
					message: `Sorry, we failed to get your search results. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	watch: {
		includeClosedObjectsModel() {
			//Stop the clock
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			//Get the search results - we don't need to wait for this case
			this.getSearchResults();
		},
		searchModel() {
			//Reset the timer if it exists
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			this.searchTimeout = setTimeout(
				this.getSearchResults,
				500
			);
		},
	},
	mounted() {
		//Send RootURL upstream
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//If the include closed is undefined - then we want to define it
		if (this.includeClosed === undefined) {
			this.includeClosedObjectsModel = false;
		}
	},
};
</script>


