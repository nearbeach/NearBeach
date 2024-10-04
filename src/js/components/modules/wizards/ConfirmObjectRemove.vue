<template>
	<div
		class="modal fade"
		id="confirmObjectRemoveModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmObjectRemove"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmObjectRemove"
					>
						Please confirm object removal.
					</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmObjectRemoveButton"
					></button>
				</div>
				<div class="modal-body">
					Please confirm you would like to remove this object from the sprint.
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
						v-on:click="removeObject"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "ConfirmObjectRemove",
	props: {},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			objectId: "getConfirmDeleteObjectId",
			objectType: "getConfirmDeleteObjectType",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		closeModal() {
			document.getElementById("confirmObjectRemoveButton").click();
		},
		removeObject() {
			this.$store.dispatch("newToast", {
				header: "Removing Object from Sprint",
				message: "Please wait whilst we remove the object",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "remove_object",
			});

			const data_to_send = new FormData();
			data_to_send.set(this.objectType, this.objectId);

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_object_from_sprint/`,
				data_to_send,
			).then(() => {
				//Delete that particular data
				this.$store.dispatch("removeGanttChartSingleRow", {
					objectType: this.objectType,
					objectId: this.objectId,
				});

				//Notify the user
				this.$store.dispatch("newToast", {
					header: "Removing Object from Sprint",
					message: "Object has been removed",
					extra_classes: "bg-success text-dark",
					unique_type: "remove_object",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to remove object",
					message: `Failed to remove the object from the sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "remove_object",
				});
			});

			this.closeModal();
		}
	},
}
</script>
