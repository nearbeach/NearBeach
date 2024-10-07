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
					Please confirm you would like to delete this group. This is permanent.
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
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		})
	},
	props: {
		groupId: {
			type: Number,
			default: 0,
		},
	},
	methods: {
		closeModal() {
			//Close the modal
			document.getElementById("confirmGroupDeleteButton").click();
		},
		deleteGroup() {
			//Check to make sure group id is valid
			if (this.groupId === 0) {
				this.$store.dispatch("newToast", {
					header: "Group ID not valid",
					message: "Sorry, current group ID is not valid",
					extra_classes: "bg-danger",
					delay: 0,
				});

				//Do nothing and return
				return;
			}

			//Send to backend
			this.axios.post(
				`${this.rootUrl}group_information/${this.groupId}/delete/`,
			).then(() => {
				window.location = `${this.rootUrl}search/group/`;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Deleting Group",
					message: `Sorry could not delete the group. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
}
</script>
