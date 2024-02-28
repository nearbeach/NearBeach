<template>
	<div
		class="modal fade"
		id="confirmPermissionDeleteModal"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="confirmPermissionDeleteLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h1
						class="modal-title fs-5"
						id="confirmPermissionDeleteLabel"
					>
						Are you sure?
					</h1>
					<button type="button"
							id="confirmPermissionDeleteClose"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete that permission?
				</div>
				<div class="modal-footer">
					<button type="button"
							class="btn btn-secondary"
							data-bs-dismiss="modal"
					>
						No
					</button>
					<button type="button"
							class="btn btn-primary"
							v-on:click="removePermission"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: "ConfirmPermissionDelete",
	props: {
		permissionDeleteId: {
			type: Number,
			default: 0,
		},
	},
	methods: {
		removePermission() {
			//Create data to send
			const data_to_send = new FormData();
			data_to_send.set("user_group_id", this.permissionDeleteId);

			this.axios.post(
				"/user_information/remove_permission/",
				data_to_send
			).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing permission",
					message: `Sorry, we could not remove the permission. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});

			//Optimistic - remove data and close modal
			this.$emit("remove_permission", this.permissionDeleteId);
			document.getElementById("confirmPermissionDeleteClose").click();
		}
	}
}
</script>