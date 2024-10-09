<template>
	<div
		class="modal fade"
		id="confirmChangeTaskDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmChangeTaskDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmChangeTaskDelete"
					>
						Please confirm Change Task Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmChangeTaskDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the Change Task from the Request for Change?
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
						v-on:click="deleteChangeTask"
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
	name: "ConfirmChangeTaskDelete",
	props: {
		changeTaskResults: {
			type: Array,
			default: () => {
				return [];
			},
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
		deleteChangeTask() {
			//Send the trigger
			this.axios.post(
				`${this.rootUrl}change_task_information/${this.changeTaskResults[0].pk}/delete/`
			).then(() => {
				//If successful, go back
				window.location.href = `${this.rootUrl}rfc_information/${this.changeTaskResults[0].fields.request_for_change}/`;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error deleting change task",
					message: `Sorry, we could not delete the change task. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		closeModal() {
			document.getElementById("confirmChangeTaskDeleteButton").click();
		}
	},
}
</script>
