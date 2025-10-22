<template>
	<div>
		<div class="card">
			<div class="card-body">
				<!-- HEADING -->
				<h1>Search</h1>
				<hr/>

				<!-- SEARCH FIELD -->
				<div class="form-row">
					<div class="form-group">
						<label>Search:</label>
						<input
							v-model="searchModel"
							type="text"
							class="form-control search-organisation"
							maxlength="250"
						/>
					</div>
					<div class="form-group">
						<input
							id="inlcudeClosedObjects"
							v-model="includeClosedObjectsModel"
							type="checkbox"
						/>
						<label for="inlcudeClosedObjects">
							Include Closed Objects</label
						>
					</div>
					<div
v-if="isSuperuser"
						 class="form-group"
					>
						<input
							id="includeAllGroups"
							v-model="includeAllGroupsModel"
							type="checkbox"
						/>
						<label for="includeAllGroups">
							Include All Groups</label
						>
					</div>
				</div>
			</div>
		</div>
		<br/>

		<!-- REQUEST FOR CHANGE RESULTS -->
		<list-search-results
			v-if="searchResults.request_for_change.length > 0"
			:current-page="searchResults.request_for_change_current_page"
			:search-results="searchResults.request_for_change"
			:import-variables="requestForChangeVariables"
			:number-of-pages="searchResults.request_for_change_number_of_pages"
			destination="rfc"
			@get_search_results="getSearchResults($event)"
		></list-search-results>

		<!-- REQUIREMENTS RESULTS -->
		<list-search-results
			v-if="searchResults.requirement.length > 0"
			:current-page="searchResults.requirement_current_page"
			:search-results="searchResults.requirement"
			:import-variables="requirementVariables"
			:number-of-pages="searchResults.requirement_number_of_pages"
			destination="requirement"
			@get_search_results="getSearchResults($event)"
		></list-search-results>

		<!-- PROJECT RESULTS -->
		<list-search-results
			v-if="searchResults.project.length > 0"
			:current-page="searchResults.project_current_page"
			:search-results="searchResults.project"
			:import-variables="projectVariables"
			:number-of-pages="searchResults.project_number_of_pages"
			destination="project"
			@get_search_results="getSearchResults($event)"
		></list-search-results>

		<!-- TASK RESULTS -->
		<list-search-results
			v-if="searchResults.task.length > 0"
			:current-page="searchResults.task_current_page"
			:search-results="searchResults.task"
			:import-variables="taskVariables"
			:number-of-pages="searchResults.task_number_of_pages"
			destination="task"
			@get_search_results="getSearchResults($event)"
		></list-search-results>

		<!-- KANBAN RESULTS -->
		<list-search-results
			v-if="searchResults.kanban_board.length > 0"
			:current-page="searchResults.kanban_board_current_page"
			:search-results="searchResults.kanban_board"
			:import-variables="kanbanVariables"
			:number-of-pages="searchResults.kanban_board_number_of_pages"
			destination="kanban_board"
			@get_search_results="getSearchResults($event)"
		></list-search-results>

		<!-- WHEN THERE ARE NO RESULTS -->
		<div
			v-if="showNoResults()"
			class="alert alert-warning"
		>
			Sorry - but there are no results for this search term. Please try
			searching for a different search term.
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
		isSuperuser: {
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
	},
	data() {
		return {
			allObjects: [
				"request_for_change",
				"requirement",
				"project",
				"task",
				"kanban_board",
			],
			includeAllGroupsModel: false,
			includeClosedObjectsModel: false,
			isCurrentlySearching: true,
			kanbanVariables: {
				header: "",
				prefix: "Kb",
				id: "id",
				title: "title",
				status: "status",
			},
			projectVariables: {
				header: "",
				prefix: "Pro",
				id: "id",
				title: "title",
				status: "status",
			},
			requestForChangeVariables: {
				header: "",
				prefix: "Rfc",
				id: "id",
				title: "title",
				status: "status",
			},
			requirementVariables: {
				header: "",
				prefix: "Req",
				id: "id",
				title: "title",
				status: "status",
			},
			searchModel: this.searchInput,
			searchResults: {
				"request_for_change": [],
				"requirement": [],
				"project": [],
				"task": [],
				"kanban_board": [],
			},
			searchTimeout: "",
			taskVariables: {
				header: "Tasks",
				prefix: "Task",
				id: "id",
				title: "title",
				status: "status",
			},
		};
	},
	watch: {
		includeAllGroupsModel() {
			//Stop the clock
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			//Get the search results - we don't need to wait for this case
			this.getSearchResults({
				"array_of_objects": this.allObjects,
				"destination_page": 1,
			});
		},
		includeClosedObjectsModel() {
			//Stop the clock
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			//Get the search results - we don't need to wait for this case
			this.getSearchResults({
				"array_of_objects": this.allObjects,
				"destination_page": 1,
			});
		},
		searchModel() {
			//Reset the timer if it exists
			if (this.searchTimeout !== "") {
				//Stop the clock!
				clearTimeout(this.searchTimeout);
			}

			this.searchTimeout = setTimeout(() => {
				this.getSearchResults({
					"array_of_objects": this.allObjects,
					"destination_page": 1,
				});
			}, 500);
		},
	},
	mounted() {
		//Send RootURL upstream
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		this.getSearchResults({
			"array_of_objects": this.allObjects,
			"destination_page": 1,
		});
	},
	methods: {
		getSearchResults(search_args) {
			this.isCurrentlySearching = true;

			// Setup the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);
			data_to_send.set(
				"include_closed",
				this.includeClosedObjectsModel
			);
			data_to_send.set(
				"include_all_groups",
				this.includeAllGroupsModel
			);
			data_to_send.set("destination_page", search_args.destination_page)

			//Array of Objects
			search_args.array_of_objects.forEach((row) => {
				data_to_send.append("array_of_objects", row);
			});

			//Use axios to request data
			this.axios.post(
				`${this.rootUrl}search/data/`, data_to_send
			).then((response) => {
				//Loop through all the objects, and check if they are defined. Then update
				this.allObjects.forEach((row) => {
					if (response.data[row] !== undefined) {
						//Data exists, update
						this.searchResults[row] = response.data[row];
						this.searchResults[`${row}_current_page`] = response.data[`${row}_current_page`];
						this.searchResults[`${row}_number_of_pages`] = response.data[`${row}_number_of_pages`];
					}
				});

				//Update the searchResults with the data
				// this.searchResults = response.data;
				this.isCurrentlySearching = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get search results",
					message: `Sorry, we failed to get your search results. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
				this.isCurrentlySearching = false;
			});
		},
		showNoResults() {
			//Only want this when there are no items to show, and search isnt currently happening
			const condition_1 = this.searchResults.requirement.length +
								this.searchResults.project.length +
								this.searchResults.task.length +
								this.searchResults.kanban_board.length +
								this.searchResults.request_for_change.length === 0;
			const condition_2 = !this.isCurrentlySearching;

			return condition_1 && condition_2;
		}
	},
};
</script>


