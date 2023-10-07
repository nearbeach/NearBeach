<template>
	<div>
		<!-- GROUPS -->
		<h2>
			<Icon v-bind:icon="icons.groupPresentation"></Icon>
			Groups
		</h2>
		<p class="text-instructions">
			The following list are all the Groups connected to this
			{{ destination }}. Users will have to be included in these groups to
			be added to this {{ destination }}
		</p>
		<div v-if="objectGroupList.length == 0 && !addingGroupStatus"
			 class="alert alert-dark"
		>
			Sorry - there are no groups active.
		</div>
		<div v-else
			 class="group-card-list"
		>
			<div v-for="group in objectGroupList"
				 v-bind:key="group.group_id"
				 class="group-card"
			>
				<div class="group-card--details">
					{{ group.group_name }}
				</div>
				<div class="group-card--remove"
					 v-if="userLevel >= 3"
				>
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="removeGroup(group.group_id)"
					/>
				</div>
			</div>
			<div v-if="addingGroupStatus"
				 class="group-card"
			>
				<div class="group-card--details">++ Adding New Group ++</div>
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
		<hr/>

		<!-- USERS -->
		<h2>
			<Icon v-bind:icon="icons.userIcon"></Icon>
			Users
		</h2>
		<p class="text-instructions">
			The following are a list of users who are connected to this
			{{ destination }}. Please note - users have to be a part of the
			groups list above.
		</p>
		<div
			v-if="objectUserList.length === 0 && !addingUserStatus"
			class="alert alert-dark"
		>
			Sorry - there are no current users active.
		</div>
		<div
			v-else
			class="user-card-list"
		>
			<div
				v-for="user in objectUserList"
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
			<div v-if="addingUserStatus"
				 class="user-card"
			>
				<div class="user-card--details">++ Adding User(s) ++</div>
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
		<add-group-wizard></add-group-wizard>
		<add-user-wizard></add-user-wizard>
	</div>
</template>

<script>
//JavaScript extras
import errorModalMixin from "../../../mixins/errorModalMixin";
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import axios from "axios";
import {Modal} from "bootstrap";
import AddGroupWizard from "../wizards/AddGroupWizard.vue";
import AddUserWizard from "../wizards/AddUserWizard.vue";

//VueX
import {mapGetters} from "vuex";

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
			addingGroupStatus: "getAddingGroupStatus",
			addingUserStatus: "getAddingUserStatus",
			destination: "getDestination",
			locationId: "getLocationId",
			objectGroupList: "getObjectGroupList",
			objectUserList: "getObjectUserList",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
	},
	mixins: [errorModalMixin, iconMixin],
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
		getGroupAndUserData() {
			//Get the data from the database
			axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/group_and_user_data/`
			).then((response) => {
				//Update VueX with the required data
				this.$store.commit("updateGroupsAndUsers", {
					objectGroupList: response.data.object_group_list,
					objectUserList: response.data.object_user_list,
					potentialGroupList: response.data.potential_group_list,
					potentialUserList: response.data.potential_user_list,
				})
			}).catch((error) => {
				this.showErrorModal(error, "Fetching Group and Users data");
			})
		},
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
		removeGroup(group_id) {
			//Optimistic Update - we assume everything is going to be ok
			//Remove the group from the list
			this.$store.commit("updateGroupsAndUsers", {
				objectGroupList: this.objectGroupList.filter(row => {
					return row.group_id !== group_id;
				}),
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("group_id", group_id);

			//Tell the backend to remove this group
			axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_group/`,
					data_to_send
				)
				.then((response) => {
					//Update VueX with the required data
					this.$store.commit("updateGroupsAndUsers", {
						objectGroupList: response.data.object_group_list,
						objectUserList: response.data.object_user_list,
						potentialGroupList: response.data.potential_group_list,
						potentialUserList: response.data.potential_user_list,
					})
				})
				.catch((error) => {
					this.showErrorModal(error, this.destination);
				});
		},
		removeUser(username) {
			//Optimistic Update - we assume everything is going to be ok
			//Remove the user from the list
			this.$store.commit("updateGroupsAndUsers", {
				objectUserList: this.objectUserList.filter(row => {
					return row.username !== username;
				}),
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
				.then(response => {
					//Update VueX with the required data
					this.$store.commit("updateGroupsAndUsers", {
						objectGroupList: response.data.object_group_list,
						objectUserList: response.data.object_user_list,
						potentialGroupList: response.data.potential_group_list,
						potentialUserList: response.data.potential_user_list,
					})
				})
				.catch((error) => {
					this.showErrorModal(error, this.destination);
				});
		},
	},
	mounted() {
		//Get the data with the 0'th count
		this.$nextTick(() => {
			// If location Id = 0, we have a problem
			if (this.locationId === 0) {
				setTimeout(() => {
					this.getGroupAndUserData();
				}, 100);
				return;
			}

			//All is good - get the data
			this.getGroupAndUserData();
		});
	},
};
</script>

<style scoped></style>
