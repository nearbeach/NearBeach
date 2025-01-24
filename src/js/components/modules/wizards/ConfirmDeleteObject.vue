<template>
	<div
		class="modal fade"
		id="confirmDeleteObjectModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmDeleteObject"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmDeleteObject"
					>
						Please confirm {{destination}} deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmDeleteObjectButton"
					></button>
				</div>
				<div class="modal-body">
					Can you please confirm the title of the {{ destination }} you are deleting.
					<br/>
					<div class="mt-2">
						<strong>Title: </strong>{{ title }}
					</div>
					<div class="form-group mt-2">
						<label>Confirm Title: </label>
						<input
							type="text"
							v-model="confirmTitle"
							class="form-control"
							onpaste="return false"
							ondrop="return false"
							autocomplete="off"
						/>
					</div>
				</div>
				<div class="modal-footer justify-content-between">
					<button
						type="button"
						class="btn btn-primary btn-sm"
						v-on:click="closeModal"
					>
						No - Keep {{ destination }}
					</button>
					<button
						type="button"
						class="btn btn-danger btn-sm"
						v-on:click="deleteObject"
						v-bind:disabled="isButtonDisabled"
					>
						Yes - Delete {{ destination }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "ConfirmDeleteObject",
	data() {
		return {
			confirmTitle: "",
			isButtonDisabled: true,
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			title: "getTitle",
		}),
	},
	watch: {
		confirmTitle() {
			this.isButtonDisabled = this.confirmTitle.toLowerCase() !== this.title.toLowerCase();
		}
	},
	methods: {
		closeModal() {
			//Clear content
			this.confirmTitle = "";

			//Close
			document.getElementById("confirmDeleteObjectButton").click();
		},
		deleteObject() {
			this.$store.dispatch("newToast", {
				header: "Deleting Object",
				message: "Deleting Object, please wait",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "delete_object",
			});

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/delete/`,
			).then(() => {
				window.location.href = this.rootUrl;
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error deleting Object",
					message: `Could not delete the ${this.destination}. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "delete_object",
				});
			});
		},
	}
}
</script>