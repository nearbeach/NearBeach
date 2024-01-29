<template>
	<div
		v-if="userList.length > 0"
		class="card"
	>
		<div class="card-body">
			<h1>Users with no groups</h1>
			<hr/>
			<div class="row">
				<div class="col-md-4">
					<h2>Users with no groups</h2>
					<p class="text-instructions">
						Please take action! The following users DO NOT have any
						groups associated with them. They will not be able to
						log in.
					</p>
				</div>
				<div class="col-md-8 user-card-list">
					<div
						v-for="user in userList"
						:key="user.id"
						class="user-card-big"
						v-on:click="goToUser(user.id)"
					>
						<img
							v-bind:src="profilePicture(user.profile_picture)"
							alt="default profile"
							class="user-card--profile"
						/>
						<div class="user-card--details">
							<div class="user-card--name">
								{{ user.first_name }}
								{{ user.last_name }}
							</div>
							<div class="user-card--email">
								{{ user.email }}
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "DashboardUsersWithNoGroups",
	props: {
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
			userList: [],
		};
	},
	methods: {
		getUserList() {
			//Get the data from the database
			this.axios
				.post(`${this.rootUrl}dashboard/get/users_with_no_groups/`)
				.then((response) => {
					this.userList = response.data;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error getting user list",
						message: `Sorry, we could not retrieve the user user. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		goToUser(user_id) {
			window.location.href = `${this.rootUrl}user_information/${user_id}/`;
		},
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "" && picture_uuid !== undefined) {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
	},
	mounted() {
		this.getUserList();
	},
};
</script>
