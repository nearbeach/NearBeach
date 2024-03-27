<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h2 v-if="destination === 'user'">User Permission List</h2>
        <h2 v-else>User List</h2>
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>List of Users</strong>
						<p text="text-instructions">
							The following are a list of users associated to
							{{ destination }}. To add a new user please click on the
							"Add User" at the bottom of the page.
						</p>
					</div>
					<div class="col-md-8">
						<table class="table">
							<thead>
							<tr>
								<td>User</td>
								<td>Group List</td>
								<td>Permission List</td>
								<td>Team Leader</td>
								<td></td>
							</tr>
							</thead>
							<tbody>
							<tr
								v-for="user in localListResults"
								:key="user.username"
							>
								<td>
									{{ user.username__first_name }}
									{{ user.username__last_name }}
								</td>
								<td>
									{{ user.group__group_name }}
								</td>
								<td>
									{{
										user.permission_set__permission_set_name
									}}
								</td>
								<td style="text-align: center">
									<input
										class="form-check-input"
										type="checkbox"
										v-bind:checked="user.group_leader"
										v-bind:data-group="user.group"
										v-bind:data-permission-set="
											user.permission_set
										"
										v-bind:data-user="user.username"
										v-on:change="updateGroupLeader"
									/>
								</td>
								<td>
									<span
										class="remove-link"
									>
										<Icon
											v-bind:icon="icons.trashCan"
											v-on:click="deletePermission(user.user_group_id)"
										/>
									</span>
								</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>

				<hr/>
				<div class="row">
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="addUser"
						>Add User</a
						>
					</div>
				</div>
			</div>

			<!-- MODALS -->
			<admin-add-user
				v-bind:destination="destination"
				v-bind:location-id="locationId"
			></admin-add-user>

			<confirm-permission-delete
				v-bind:permission-delete-id="permissionDeleteId"
				v-on:remove_permission="removePermission"
			></confirm-permission-delete>
		</div>
	</n-config-provider>
</template>

<script>
import {Modal} from "bootstrap";


//Import mixins
import getThemeMixin from "../../mixins/getThemeMixin";

//Vue Components
import AdminAddUser from "./AdminAddUser.vue";
import ConfirmPermissionDelete from "./ConfirmPermissionDelete.vue"

//Icon
import {Icon} from "@iconify/vue";
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "UserList",
	components: {
		AdminAddUser,
		ConfirmPermissionDelete,
		Icon,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
		theme: {
			type: String,
			default: "",
		},
		userListResults: {
			type: Array,
			default() {
				return [];
			},
		},
	},
	data() {
		return {
			localListResults: [],
			permissionDeleteId: 0,
		};
	},
	mixins: [getThemeMixin, iconMixin],
	methods: {
		addUser() {
			//Show the user's modal
			const addUserModal = new Modal(
				document.getElementById("addUserModal")
			);
			addUserModal.show();
		},
		deletePermission(user_group_id) {
			//Update variable
			this.permissionDeleteId = user_group_id;

			//Open Modal
			const permissionDeleteModal = new Modal(
				document.getElementById('confirmPermissionDeleteModal')
			)
			permissionDeleteModal.show();
		},
		isTeamLeader(username /* As an ID*/) {
			//Get count of the data from userListResults, where username and group_leader == true
			const count = this.userListResults.filter((row) => {
				return row.username === username && row.group_leader;
			}).length;

			//If length > 0, return true
			return count > 0;
		},
		removePermission(user_group_id) {
			this.localListResults = this.localListResults.filter((row) => {
				return row.user_group_id !== user_group_id;
			});
		},
		updateGroupLeader(event) {
			//Notify the user of updating the group leader
			this.$store.dispatch("newToast", {
				header: "Updating Team Leader Status",
				message: "Currently updating team leader status. Please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "update_group_leader",
			});

			//Get if the checkbox is ticked or not
			const group_leader = event.target.checked;

			// Send to the backend
			const data_to_send = new FormData();
			data_to_send.set("group_leader", group_leader);
			data_to_send.set("username", event.target.dataset.user);

			//Case specific data
			if (
				this.destination === "group" ||
				this.destination === "user"
			) {
				data_to_send.set("group", event.target.dataset.group);
			} else if (this.destination === "permission_set") {
				data_to_send.set(
					"permission_set",
					event.target.dataset.permissionSet
				);
			}

			this.axios.post(
				`/update_group_leader_status/${this.destination}/`,
				data_to_send
			).then((response) => {
				//Updated data
				this.localListResults = response.data;

				this.$store.dispatch("newToast", {
					header: "Updated Team Leader Status",
					message: "Updated team leader status.",
					extra_classes: "bg-success",
					unique_type: "update_group_leader",
				});

			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error updating group leader",
					message: `Sorry, we could not update group leader. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		this.localListResults = this.userListResults;
	},
};
</script>

<style scoped></style>
