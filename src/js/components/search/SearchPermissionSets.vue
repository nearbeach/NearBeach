<template>
	<div class="card">
		<div class="card-body">
			<!-- Search bar and heading -->
			<h1>Search Permission Sets</h1>
			<div class="form-group mt-4">
				<label>Search:</label>
				<input
					class="form-control search-groups"
					v-model="searchModel"
				/>
			</div>
			<hr/>

			<!-- Search Results -->
			<div
				class="list-group"
				v-if="permissionSetList.length > 0"
			>
				<a
					class="list-group-item list-group-item-action"
					v-for="permissionSet in permissionSetList"
					v-bind:key="permissionSet.pk"
					v-bind:href="`/permission_set_information/${permissionSet.pk}/`"
				>
					<strong>{{
							permissionSet.fields.permission_set_name
						}}</strong>
					<br/>
				</a>
			</div>

			<div
				class="alert alert-warning"
				v-else
			>
				Sorry, there are no permission sets.
			</div>

			<hr/>
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						v-bind:href="`${rootUrl}new_permission_set/`"
						class="btn btn-primary save-changes"
					>
						Add new Permission Set
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "SearchPermissionSets",
	props: {
		permissionSetResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			permissionSetList: this.permissionSetResults,
			searchModel: "",
			searchTimeout: "",
		};
	},
	methods: {
		getSearchResults() {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);

			//Use Axios to send data
			this.axios
				.post(
					`${this.rootUrl}search/permission_set/data/`,
					data_to_send
				)
				.then((response) => {
					this.permissionSetList = response.data;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Getting Search Results",
						message: `We had an issue getting search results. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
	},
	watch: {
		searchModel() {
			// Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getSearchResults();
				}, 500);
			}
		},
	},
};
</script>


