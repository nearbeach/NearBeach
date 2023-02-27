<template>
	<div
		class="alert alert-secondary"
		v-if="userList.length === 0"
	>
		Sorry, there are no users currently assigned to this card.
	</div>
	<div v-else>
		<table class="table">
			<thead>
				<tr>
					<td scope="col">Username</td>
					<td scope="col">Name</td>
					<td
						scope="col"
						v-if="userLevel === 4"
					>
						Delete
					</td>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="user in userList"
					v-bind:key="user.id"
				>
					<td>{{ user.id }} - {{ user.username }}</td>
					<td>{{ user.first_name }} {{ user.last_name }}</td>
					<td v-if="userLevel >= 2">
						<Icon
							v-bind:icon="icons.trashCan"
							v-on:click="removeUser(user.username)"
						/>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	<div
		class="row"
		v-if="userLevel > 1"
	>
		<div class="col-md-12">
			<button
				class="btn btn-primary"
				v-on:click="addUser"
			>
				Add User
			</button>
		</div>
	</div>
</template>

<script>
	import axios from "axios";
	import { Modal } from "bootstrap";
	import { Icon } from "@iconify/vue";

	//Vuex components
	import { mapGetters } from "vuex";

	//Mixins
	import iconMixin from "../../mixins/iconMixin";

	export default {
		name: "CardUsers",
		components: {
			Icon,
		},
		computed: {
			...mapGetters({
				cardId: "getCardId",
				locationId: "getLocationId",
				rootUrl: "getRootUrl",
				userLevel: "getUserLevel",
				userList: "getUserList",
			}),
		},
		mixins: [iconMixin],
		methods: {
			addUser: function () {
				//Close the current modal
				document
					.getElementById("cardInformationModalCloseButton")
					.click();

				//Open the user wizard model
				const addUserWizard = new Modal("#addUserModal");
				addUserWizard.show();
			},
			removeUser: function (username) {
				//Data to send
				const data_to_send = new FormData();
				data_to_send.set("username", username);

				//Axios
				axios
					.post(
						`${this.rootUrl}object_data/kanban_card/${this.locationId}/remove_user/`,
						data_to_send
					)
					.then(() => {
						//Remove any user where username matches
						const user_list = this.userList.filter((row) => {
							return row.username !== username;
						});

						//update user list
						this.$store.commit({
							type: "updateUserList",
							userList: user_list,
						});
					});
			},
		},
	};
</script>
