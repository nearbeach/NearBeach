<template>
	<div
		v-if="userList.length > 0"
		class="card"
	>
		<div class="card-body">
			<h1>Users with no groups</h1>
			<hr />
			<div class="row">
				<div class="col-md-4">
					<h2>Users with no groups</h2>
					<p class="text-instructions">
						Please take action! The following users DO NOT have any
						groups associated with them. They will not be able to
						log in.
					</p>
				</div>
				<div class="col-md-8 user-card-layouts">
					<div
						v-for="user in userList"
						:key="user.id"
						class="user-card"
						v-on:click="goToUser(user.id)"
					>
						<img
							v-bind:src="`${staticUrl}NearBeach/images/placeholder/people_tax.svg`"
							alt="default profile"
							class="default-user-profile"
						/>
						<div class="user-details">
							<strong
								>{{ user.first_name }}
								{{ user.last_name }}</strong
							><br />
							{{ user.username }}
							<div class="spacer"></div>
							{{ user.email }}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");

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
				axios
					.post(`${this.rootUrl}dashboard/get/users_with_no_groups/`)
					.then((response) => {
						this.userList = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			goToUser(user_id) {
				window.location.href = `${this.rootUrl}user_information/${user_id}/`;
			},
		},
		mounted() {
			this.getUserList();
		},
	};
</script>
