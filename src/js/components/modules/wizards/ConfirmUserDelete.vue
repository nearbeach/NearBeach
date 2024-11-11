<template>
	<div
		class="modal fade"
		id="confirmUserDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmUserDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmUserDelete"
					>
						Please confirm User Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmUserDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the User from the object?
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
						v-on:click="deleteUser"
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
	name: "ConfirmUserDelete",
	props: {
		username: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			objectUserList: "getObjectUserList",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteUser() {
			//Optimistic Update - we assume everything is going to be ok
			//Remove the user from the list
			this.$store.commit("updateGroupsAndUsers", {
				objectUserList: this.objectUserList.filter(row => {
					return row.username !== this.username;
				}),
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("username", this.username);

			//Tell the backend we no longer want this user attached
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_user/`,
				data_to_send
			).then(response => {
				//Update VueX with the required data
				this.$store.commit("updateGroupsAndUsers", {
					objectGroupList: response.data.object_group_list,
					objectUserList: response.data.object_user_list,
					potentialGroupList: response.data.potential_group_list,
					potentialUserList: response.data.potential_user_list,
					userGroupList: response.data.user_group_list,
				})
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing user from object",
					message: `We encounted an error moving the user from the object. Error -> ${error}`,
					extra_classes: 'bg-danger',
					delay: 0,
				});
			});

			//Close the modal
			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmUserDeleteButton").click();
		}
	},
}
</script>
