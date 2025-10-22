<template>
	<div
		id="confirmKanbanBoardClosure"
		class="modal fade"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmKanbanBoardClosure"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						id="confirmKanbanBoardClosure"
						class="modal-title"
					>
						Please confirm Kanban Board Closure
					</h5>
					<!-- TASK INFORMATION -->
					<button
						id="confirmKanbanCloseButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to close the current Kanban Board?
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
						@click="closeKanbanBoard"
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
	name: "ConfirmKanbanBoardClosure",
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		closeKanbanBoard() {
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.locationId}/close_board/`
			)
			.then(() => {
				window.location.href = `${this.rootUrl}`;
			})
			.catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error closing the kanban board",
					message: `Sorry, we could not close the kanban board. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		closeModal() {
			document.getElementById("confirmKanbanCloseButton").click();
		}
	},
}
</script>
