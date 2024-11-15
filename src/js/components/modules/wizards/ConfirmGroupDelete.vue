<template>
	<div
		class="modal fade"
		id="confirmGroupDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmGroupDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmGroupDelete"
					>
						Please confirm Group Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmGroupDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the Group from the object?
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="deleteGroup"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "ConfirmGroupDelete",
	props: {
		groupId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			objectGroupList: "getObjectGroupList",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteGroup() {
			//Optimistic Update - we assume everything is going to be ok
			//Remove the group from the list
			this.$store.commit("updateGroupsAndUsers", {
				objectGroupList: this.objectGroupList.filter(row => {
					return row.group_id !== this.groupId;
				}),
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("group_id", `${this.groupId}`);

			//Tell the backend to remove this group
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_group/`,
				data_to_send
			).then((response) => {
				//Update VueX with the required data
				this.$store.commit("updateGroupsAndUsers", {
					objectGroupList: response.data.object_group_list,
					objectUserList: response.data.object_user_list,
					potentialGroupList: response.data.potential_group_list,
					potentialUserList: response.data.potential_user_list,
					userGroupList: response.data.user_group_list,
				});

				if (this.hasUserAccessBeenRemoved(
					response.data.object_group_list,
					response.data.user_group_list
				)) {
					//Access has been removed. User removed their last group from object
					document.location.reload();
				}
			})
			.catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing group from object",
					message: `We encounted an error moving the group from the object. Error -> ${error}`,
					extra_classes: 'bg-danger',
					delay: 0,
				});
			});

			//Close the modal
			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmGroupDeleteButton").click();
		},
		hasUserAccessBeenRemoved(objectGroupList, userGroupList) {
			//Make sure there is some overlap between objectGroupList and userGroupList. If there is no overlap
			//it means the user has removed all their groups.
			const count = objectGroupList.filter((row) => {
				return userGroupList.some(level => row.group_id === level.group_id);
			}).length;

			return count === 0;
		}
	},
}
</script>
