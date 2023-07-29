<template>
	<div>
		<!-- GROUPS -->
		<h2><Icon v-bind:icon="icons.groupPresentation"></Icon> Groups</h2>
		<p class="text-instructions">
			The following list are all the Groups connected to this
			{{ destination }}. Users will have to be included in these groups to
			be added to this {{ destination }}
		</p>
		<div v-if="groupList.length == 0"
			class="alert alert-dark"
		>
			Sorry - there are no groups active.
		</div>
		<div v-else
			class="group-card-list"
		>
			<div v-for="group in groupList"
				v-bind:key="group.pk"
				class="group-card"
			>
				<div class="group-card--details">
					{{ group.fields.group_name }}
				</div>
				<div class="group-card--remove"
					v-if="userLevel >= 3"
				>
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="removeGroup(group.pk)"
					/>	
				</div>
			</div>
		</div>

		<div class="spacer"></div>

		<!-- ADD GROUP -->
		<!-- TO DO - limit it to certain users -->
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="addNewGroup"
					v-if="userLevel > 1"
					>Add Group to {{ destination }}</a
				>
			</div>
		</div>
		<hr />

		<!-- USERS -->
		<h2><Icon v-bind:icon="icons.userIcon"></Icon> Users</h2>
		<p class="text-instructions">
			The following are a list of users who are connected to this
			{{ destination }}. Please note - users have to be a part of the
			groups list above.
		</p>
		<div
			v-if="userList.length == 0"
			class="alert alert-dark"
		>
			Sorry - there are no current users active.
		</div>
		<div
			v-else
			class="user-card-list"
		>
			<div
				v-for="user in userList"
				v-bind:key="user.username"
				class="user-card"
			>
				<img
					v-bind:src="profilePicture(user.profile_picture)"
					alt="default profile"
					class="user-card--profile"
				/>
				<div class="user-card--details">
					<div class="user-card--name">
						{{ user.first_name }} {{ user.last_name }}
					</div>
					<div class="user-card--email">
						{{ user.email }}
					</div>
				</div>
				<div
					class="user-card--remove"
					v-if="userLevel >= 3"
				>
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="removeUser(user.username)"
					/>
				</div>
			</div>
		</div>

		<div class="spacer"></div>

		<!-- TO DO - limit it to certain users -->
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="addNewUser"
					v-if="userLevel > 1"
					>Add User to {{ destination }}</a
				>
			</div>
		</div>

		<!-- MODALS -->
		<!-- ADD GROUPS WIZARD -->
		<add-group-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-on:update_group_list="updateGroupList($event)"
		></add-group-wizard>

		<!-- ADD USER WIZARD -->
		<add-user-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-bind:refresh-user-list="refreshUserListBoolean"
			v-on:update_user_list="updateUserList($event)"
			v-on:reset_refresh_user_list="resetRefreshUserList($event)"
		></add-user-wizard>
	</div>
</template>

<script>
	//JavaScript extras
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";
	import { Icon } from "@iconify/vue";
	import axios from "axios";
	import { Modal } from "bootstrap";
	import AddGroupWizard from "../wizards/AddGroupWizard.vue";
	import AddUserWizard from "../wizards/AddUserWizard.vue";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "GroupsAndUsersModule",
		components: {
			AddGroupWizard,
			AddUserWizard,
			Icon,
		},
		inject: [
			'nextTick',
		],
		computed: {
			...mapGetters({
				destination: "getDestination",
				locationId: "getLocationId",
				rootUrl: "getRootUrl",
				staticUrl: "getStaticUrl",
				userLevel: "getUserLevel",
			}),
		},
		mixins: [errorModalMixin, iconMixin],
		data() {
			return {
				groupList: [],
				refreshUserListBoolean: false,
				userList: [],
			};
		},
		methods: {
			addNewGroup() {
				var addGroupModal = new Modal(
					document.getElementById("addGroupModal")
				);
				addGroupModal.show();
			},
			addNewUser() {
				var addUserModal = new Modal(
					document.getElementById("addUserModal")
				);
				addUserModal.show();
			},
			getGroupList() {
				//Get the data from the database
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/group_list/`
					)
					.then((response) => {
						this.groupList = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			getUserList() {
				//Get the data from the database
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/user_list/`
					)
					.then((response) => {
						this.userList = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			profilePicture(picture_uuid) {
				if (picture_uuid !== null && picture_uuid !== "") {
					return `${this.rootUrl}private/${picture_uuid}/`;
				}

				return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
			},
			removeGroup(group_id) {
				//Setup data to send
				const data_to_send = new FormData();
				data_to_send.set("group_id", group_id);

				//Tell the backend to remove this group
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_group/`,
						data_to_send
					)
					.then(() => {
						//HACK - for some strange reason, the groupList is behind a proxy. This is a hack around that BS
						let group_list = JSON.parse(
							JSON.stringify(this.groupList)
						);
						this.groupList = group_list.filter((row) => {
							return row.pk !== group_id;
						});
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			removeUser(username) {
				//Optimistic Update - we assume everything is going to be ok
				//Remove the user from the list
				this.userList = this.userList.filter((row) => {
					return row.username !== username;
				});

				//Setup data to send
				const data_to_send = new FormData();
				data_to_send.set("username", username);

				//Tell the backend we no longer want this user attached
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_user/`,
						data_to_send
					)
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			resetRefreshUserList() {
				this.refreshUserListBoolean = false;
			},
			updateGroupList(data) {
				//Clear the group list
				this.groupList = data;

				//Now update the list of potential users
				this.refreshUserListBoolean = true;
			},
			updateUserList(data) {
				//Loop throught the data array and add each line item
				// data.forEach(row => {
				//     this.userList.push(row);
				// });
				this.userList = data;
			},
		},
		mounted() {
			//Wait 200ms
			this.nextTick(() => {
				this.getGroupList();
				this.getUserList();
			});
		},
	};
</script>

<style scoped></style>
