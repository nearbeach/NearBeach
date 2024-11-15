<template>
	<div>
		<!-- GROUPS -->
		<h2>
			Groups
		</h2>
		<p class="text-instructions">
			The following list are all the Groups connected to this
			{{ destinationTitle }}. Users will have to be included in these groups to
			be added to this {{ destinationTitle }}
		</p>
		<div v-if="loadingData"
			class="alert alert-info"
		>
			Currently loading group data.
		</div>
		<div v-else-if="objectGroupList.length === 0 && !addingGroupStatus"
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
					 v-if="userLevel >= 3 && objectGroupList.length > 1"
				>
					<carbon-trash-can
						v-on:click="removeGroup(group.group_id)"
					></carbon-trash-can>
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
					v-if="userLevel > 1 && !isReadOnly"
				>Add Group to {{ destinationTitle }}</a
				>
			</div>
		</div>
		<hr/>

		<!-- USERS -->
		<h2>
			Users
		</h2>
		<p class="text-instructions">
			The following are a list of users who are connected to this
			{{ destinationTitle }}. Please note - users have to be a part of the
			groups list above.
		</p>

		<render-user-card-list
			v-bind:adding-user-status="addingUserStatus"
			v-bind:loading-data="loadingData"
			v-bind:object-user-list="objectUserList"
			v-on:remove_user="removeUser"
		></render-user-card-list>

		<div class="spacer"></div>

		<!-- TO DO - limit it to certain users -->
		<div class="row submit-row"
		     v-if="userLevel > 1 && !isReadOnly"
		>
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="addNewUser"
				>Add User to {{ destinationTitle }}</a
				>
			</div>
		</div>

		<!-- MODALS -->
		<add-group-wizard></add-group-wizard>
		<add-user-wizard></add-user-wizard>
		<confirm-group-delete v-bind:group-id="deleteGroupId"></confirm-group-delete>
		<confirm-user-delete v-bind:username="deleteUsername"></confirm-user-delete>
	</div>
</template>

<script>
//JavaScript extras
import {Modal} from "bootstrap";
import AddGroupWizard from "../wizards/AddGroupWizard.vue";
import AddUserWizard from "../wizards/AddUserWizard.vue";
import ConfirmGroupDelete from "../wizards/ConfirmGroupDelete.vue";
import ConfirmUserDelete from "../wizards/ConfirmUserDelete.vue";

//VueX
import {mapGetters} from "vuex";

//Components
import RenderUserCardList from "../../render/RenderUserCardList.vue";
import {CarbonTrashCan} from "../../../components";

export default {
	name: "GroupsAndUsersModule",
	components: {
		CarbonTrashCan,
		AddGroupWizard,
		AddUserWizard,
		ConfirmGroupDelete,
		ConfirmUserDelete,
		RenderUserCardList,
	},
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
	},
	data() {
		return {
			deleteGroupId: 0,
			deleteUsername: "",
			destinationTitle: "",
			loadingData: true,
		}
	},
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
	methods: {
		addNewGroup() {
			const addGroupModal = new Modal(
				document.getElementById("addGroupModal")
			);
			addGroupModal.show();
		},
		addNewUser() {
			const addUserModal = new Modal(
				document.getElementById("addUserModal")
			);
			addUserModal.show();
		},
		getGroupAndUserData() {
			//Get the data from the database
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/group_and_user_data/`
			).then((response) => {
				//Update VueX with the required data
				this.$store.commit("updateGroupsAndUsers", {
					objectGroupList: response.data.object_group_list,
					objectUserList: response.data.object_user_list,
					potentialGroupList: response.data.potential_group_list,
					potentialUserList: response.data.potential_user_list,
					userGroupList: response.data.user_group_list,
				});

				this.loadingData = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error fetching group and user data",
					message: `Sorry we could not get any group or user data. Error -> ${error}`,
					extra_classes: "bd-danger",
					delay: 0,
				});
			})
		},
		removeGroup(group_id) {
			//Tell the confirmation modal what group id is being deleted
			this.deleteGroupId = group_id;

			//Open the modal
			const modal = new Modal(document.getElementById("confirmGroupDeleteModal"));
			modal.show();
		},
		removeUser(username) {
			//Tell the confirmation modal what user id is being deleted
			this.deleteUsername = username;

			//Open the modal
			const modal = new Modal(document.getElementById("confirmUserDeleteModal"));
			modal.show();
		},
	},
	mounted() {
		//Get the data with the 0'th count
		this.$nextTick(() => {
			// If location Id = 0, we have a problem
			if (this.locationId === 0) {
				setTimeout(() => {
					this.getGroupAndUserData();
				}, 500);
				return;
			}

			//All is good - get the data
			this.getGroupAndUserData();

			//Use the destination string to pull out the title. i.e. request_for_change => Request For Change
			let title = this.destination;

			//Replace any _ with a space
			title = title.replaceAll("_", " ");

			//Title case
			this.destinationTitle = title.replace(
				/\w\S*/g,
				(txt) => {
					return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
				}
			);
		});
	},
};
</script>


