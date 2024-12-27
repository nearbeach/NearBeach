<template>
	<div class="card">
		<div class="card-body">
			<!-- Search bar and heading -->
			<h1 class="mb-4">Search Groups</h1>
			<div class="form-group">
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
				v-if="groupList.length > 0"
			>
				<a
					class="list-group-item list-group-item-action"
					v-for="group in groupList"
					:key="group.pk"
					v-bind:href="`/group_information/${group.pk}/`"
				>
					<strong>{{ group.fields.group_name }}</strong>
					<br/>
					<p class="small-text">
						Parent Group: {{ group.fields.parent_group }}
					</p>
				</a>
			</div>

			<div
				class="alert alert-warning"
				v-else
			>
				Sorry, there are no groups.
			</div>

			<hr/>
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						v-bind:href="`${rootUrl}new_group/`"
						class="btn btn-primary save-changes"
					>
						Add new Group
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "SearchGroups",
	props: {
		groupResults: {
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
			groupList: this.groupResults,
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
			this.axios.post(
				`${this.rootUrl}search/group/data/`,
				data_to_send
			).then((response) => {
				this.groupList = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get search results",
					message: `Failed to get search results. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
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


