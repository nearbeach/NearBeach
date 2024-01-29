<template>
	<div class="card">
		<div class="card-body">
			<!-- HEADING -->
			<h1>Search Organisations</h1>
			<br/>

			<!-- SEARCH FIELD -->
			<div class="form-group">
				<label>Search:</label>
				<input
					type="text"
					class="form-control search-organisation"
					v-model="searchModel"
				/>
			</div>

			<!-- LIST OUT SEARCH RESULTS -->
			<hr/>
			<list-organisations
				v-bind:organisation-results="localOrganisationResults"
			></list-organisations>

			<!-- SHOW IF NO RESULTS -->
			<div
				class="alert alert-warning"
				v-if="localOrganisationResults.length === 0"
			>
				There are no organisations with the search parameters used.
				Please try again.
			</div>

			<hr>
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						v-bind:href="`${rootUrl}new_organisation/`"
						class="btn btn-primary save-changes"
					>
						Add new Organisation
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//Vue Components
import ListOrganisations from "../organisations/ListOrganisations.vue";

export default {
	name: "SearchOrganisations",
	components: {
		ListOrganisations,
	},
	props: {
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			localOrganisationResults: this.organisationResults,
			searchModel: "",
			searchTimeout: "",
		};
	},
	methods: {
		getSearchResults() {
			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);

			//Use axios to obtain the data we require
			this.axios
				.post(
					`${this.rootUrl}search/organisation/data/`,
					data_to_send
				)
				.then((response) => {
					this.localOrganisationResults = response.data;
				})
				.catch((error) => {
				});
		},
	},
	watch: {
		searchModel() {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (this.searchModel.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getSearchResults();
				}, 500);
			}
		},
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});
	},
};
</script>

<style scoped></style>
