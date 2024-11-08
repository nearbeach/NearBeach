<template>
	<div
		class="modal fade"
		id="confirmSprintRemoveModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmSprintRemoveLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmSprintRemoveLabel"
					>
						Please confirm the sprint removal
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmSprintRemovalButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to remove the sprint from the current object.
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
						v-on:click="removeSprint"
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
	name: "ConfirmRemoveSprint",
	emits: ['update_sprint_list'],
	props: {
		confirmRemoveSprint: {
			type: Object,
			default: () => {
				return {
					sprint_name: "",
					sprint_id: 0,
				};
			},
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			documentRemoveKey: "getDocumentRemoveKey",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		removeSprint() {
			const sprint_id = this.confirmRemoveSprint.sprint_id;

			//Setup Data to Send
			const data_to_send = new FormData();
			data_to_send.set("sprint_id", sprint_id);

			//Axios
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_sprint/${sprint_id}/`,
				data_to_send,
			).then((response) => {
				//Send the updated data upstream
				this.$emit("update_sprint_list", response.data);

				//Close the modal
				document.getElementById("confirmSprintRemovalButton").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Removing Sprint",
					message: `Sorry, we could not remove the sprint from the current object. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		closeModal() {
			document.getElementById("confirmSprintRemovalButton").click();
		}
	},
}
</script>
