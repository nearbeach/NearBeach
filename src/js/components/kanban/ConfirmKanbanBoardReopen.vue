<template>
	<div
		id="confirmKanbanBoardReopen"
		class="modal fade"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmKanbanBoardReopen"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						id="confirmKanbanBoardOpen"
						class="modal-title"
					>
						Please confirm Kanban Board Reopen
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
					Are you sure you want to reopen the current Kanban Board?
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
						@click="reopenKanbanBoard"
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
	name: "ConfirmKanbanBoardOpen",
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		reopenKanbanBoard() {
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.locationId}/reopen_board/`
			).then(() => {
				window.location.reload();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					heading: "Error Reopening Kanban board",
					message: `Error typing to reopen kanban board: Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		closeModal() {
			document.getElementById("confirmKanbanBoardOpen").click();
		}
	},
}
</script>
