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
			v-if="localSearchResults.length > 0"
			v-bind:search-results="localSearchResults"
			v-bind:import-variables="sprintVariables"
			v-bind:destination="'sprint'"
		></list-search-results>

		<!-- WHEN THERE ARE NO RESULTS -->
		<div
			v-if="localSearchResults.length === 0"
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
		includeClosed: {
			type: Boolean,
			default: false,
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		searchInput: {
			type: String,
			required: false,
			default: "",
		},
		searchResults: {
			type: Array,
			required: true,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			includeClosedObjectsModel: this.includeClosed,
			sprintVariables: {
				header: "Sprint",
				prefix: "spr",
				id: "sprint_id",
				title: "sprint_name",
				status: "sprint_status",
			},
			localSearchResults: this.searchResults,
			searchModel: this.searchInput,
			searchTimeout: "",
		};
	},
	methods: {
		getSearchResults() {
			// Setup the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);
			data_to_send.set(
				"include_closed",
				this.includeClosedObjectsModel
			);

			//Use axios to request data
			this.axios.post(
				`${this.rootUrl}search/sprint/data/`,
				data_to_send
			).then((response) => {
				//Update the localSearchResults with the data
				this.localSearchResults = response.data;
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

<style scoped></style>
