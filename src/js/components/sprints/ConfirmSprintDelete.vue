<template>
	<div
		class="modal fade"
		id="confirmSprintDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmSprintDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmSprintDelete"
					>
						Please confirm Sprint Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmSprintDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the sprint?
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
						v-on:click="deleteSprint"
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
	name: "confirmSprintDelete",
	props: {
		parentObjectLocationId: {
			type: Number,
			default: 0,
		},
		parentObjectDestination: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteSprint() {
			//Tell user we are deleting the sprint
			this.$store.dispatch("newToast", {
				header: "Deleting Sprint",
				message: "Please wait, whilst we delete the sprint",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "delete_sprint",
			});

			this.axios.post(
				`${this.rootUrl}sprint_information/${this.locationId}/delete/`,
			).then(() => {
				window.location = `${this.rootUrl}${this.parentObjectDestination}_information/${this.parentObjectLocationId}/`
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Deleting Sprint",
					message: `Sorry, could not delete the sprint. Error -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
					unique_type: "delete_sprint",
				});
			});
		},
		closeModal() {
			document.getElementById("confirmSprintDeleteButton").click();
		}
	},
}
</script>
