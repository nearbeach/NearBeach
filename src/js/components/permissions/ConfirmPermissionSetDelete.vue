<template>
	<div
		id="confirmPermissionSetDeleteModal"
		class="modal fade"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmPermissionSetDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						id="confirmPermissionSetDelete"
						class="modal-title"
					>
						Please confirm Permission Set Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						id="confirmPermissionSetDeleteButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					Please confirm you would like to delete this permission set. This is permanent.
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						@click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						@click="deletePermissionSet"
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
	name: "ConfirmPermissionSetDelete",
	props: {
		permissionSetId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		closeModal() {
			//Close the modal
			document.getElementById("confirmPermissionSetDeleteButton").click();
		},
		deletePermissionSet() {
			//Check to make sure group id is valid
			if (this.permissionSetId === 0) {
				this.$store.dispatch("newToast", {
					header: "Permission Set ID not valid",
					message: "Sorry, current permission set ID is not valid",
					extra_classes: "bg-danger",
					delay: 0,
				});

				//Do nothing and return
				return;
			}

			//Send to backend
			this.axios.post(
				`${this.rootUrl}permission_set_information/${this.permissionSetId}/delete/`,
			).then(() => {
				window.location = `${this.rootUrl}search/permission_set/`;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Deleting Permission Set",
					message: `Sorry could not delete the permission set. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
}
</script>
