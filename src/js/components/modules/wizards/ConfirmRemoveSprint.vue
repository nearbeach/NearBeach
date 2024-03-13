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
import {Modal} from "bootstrap";

export default {
	name: "ConfirmRemoveSprint",
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
			//ADD CODE
		},
		closeModal() {
			//ADD CODE
		}
	},
}
</script>
