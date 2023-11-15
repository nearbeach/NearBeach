<template>
	<div
		class="modal fade"
		id="confirmKanbanBoardClosure"
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
						class="modal-title"
						id="confirmKanbanBoardClosure"
					>
						Please confirm Kanban Board Closure
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmKanbanCloseButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to close the current Kanban Board?
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
						v-on:click="closeKanbanBoard"
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
	name: "confirmKanbanBoardClosure",
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
			.then((response) => {
				window.location.href = `${this.rootUrl}`;
			})
			.catch((error) => {
				// this.showErrorModal(error, this.destination);
			});
		},
		closeModal() {
			document.getElementById("confirmKanbanCloseButton").click();
		}
	},
}
</script>
