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

		<!-- REQUEST FOR CHANGE RESULTS -->
		<list-search-results
			v-if="localSearchResults.request_for_change.length > 0"
			v-bind:search-results="localSearchResults.request_for_change"
			v-bind:import-variables="requestForChangeVariables"
			v-bind:destination="'rfc'"
		></list-search-results>

		<!-- REQUIREMENTS RESULTS -->
		<list-search-results
			v-if="localSearchResults.requirement.length > 0"
			v-bind:search-results="localSearchResults.requirement"
			v-bind:import-variables="requirementVariables"
			v-bind:destination="'requirement'"
		></list-search-results>

		<!-- PROJECT RESULTS -->
		<list-search-results
			v-if="localSearchResults.project.length > 0"
			v-bind:search-results="localSearchResults.project"
			v-bind:import-variables="projectVariables"
			v-bind:destination="'project'"
		></list-search-results>

		<!-- TASK RESULTS -->
		<list-search-results
			v-if="localSearchResults.task.length > 0"
			v-bind:search-results="localSearchResults.task"
			v-bind:import-variables="taskVariables"
			v-bind:destination="'task'"
		></list-search-results>

		<!-- KANBAN RESULTS -->
		<list-search-results
			v-if="localSearchResults.kanban.length > 0"
			v-bind:search-results="localSearchResults.kanban"
			v-bind:import-variables="kanbanVariables"
			v-bind:destination="'kanban'"
		></list-search-results>

		<!-- WHEN THERE ARE NO RESULTS -->
		<div
			v-if="
					localSearchResults.requirement.length +
					localSearchResults.project.length +
					localSearchResults.task.length +
					localSearchResults.kanban.length +
					localSearchResults.request_for_change.length === 0
			"
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
			type: Object,
			required: true,
			default: () => {
				return {};
			},
		},
	},
	data() {
		return {
			includeClosedObjectsModel: this.includeClosed,
			kanbanVariables: {
				header: "Kanban",
				prefix: "Kb",
				id: "kanban_board_id",
				title: "kanban_board_name",
				status: "kanban_board_status",
			},
			localSearchResults: this.searchResults,
			projectVariables: {
				header: "Projects",
				prefix: "Pro",
				id: "project_id",
				title: "project_name",
				status: "project_status_text",
			},
			requestForChangeVariables: {
				header: "Request for Change",
				prefix: "Rfc",
				id: "rfc_id",
				title: "rfc_title",
				status: "rfc_status__rfc_status",
			},
			requirementVariables: {
				header: "Requirements",
				prefix: "Req",
				id: "requirement_id",
				title: "requirement_title",
				status: "requirement_status__requirement_status",
			},
			searchModel: this.searchInput,
			searchTimeout: "",
			taskVariables: {
				header: "Tasks",
				prefix: "Task",
				id: "task_id",
				title: "task_short_description",
				status: "task_status_text",
			},
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
				`${this.rootUrl}search/data/`, data_to_send
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
