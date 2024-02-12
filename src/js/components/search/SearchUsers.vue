<template>
	<div class="card">
		<div class="card-body">
			<!-- Search bar and heading -->
			<h1>Search Users</h1>
			<br/>
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
				v-if="userList.length > 0"
			>
				<a
					class="list-group-item list-group-item-action"
					v-for="user in userList"
					v-bind:key="user.username"
					v-bind:href="`/user_information/${user.id}/`"
				>
					<strong>
						{{ user.username }}: {{ user.first_name }}
						{{ user.last_name }}
					</strong>
					<div class="spacer"></div>
					<p class="small-text">{{ user.email }}</p>
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
						v-bind:href="`${rootUrl}new_user/`"
						class="btn btn-primary save-changes"
					>
						Add new User
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "SearchUsers",
	props: {
		userResults: {
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
			searchModel: "",
			searchTimeout: "",
			userList: this.userResults,
		};
	},
	methods: {
		getSearchResults() {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);

			//Use Axios to send data
			this.axios
				.post(`${this.rootUrl}search/user/data/`, data_to_send)
				.then((response) => {
					this.userList = response.data;
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
};
</script>

<style scoped></style>
