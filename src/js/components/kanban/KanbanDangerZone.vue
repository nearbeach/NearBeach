<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card text-bg-warning">
			<div class="card-body">
				<h1>DANGER ZONE</h1>
				<hr>
				<div v-if="kanbanBoardStatus === 'Closed'"
					class="row"
				>
					<div class="col-md-4">
						<h2>Reopen Kanban Board</h2>
						<p>
							WARNING - this will reopen the kanban board for everyone to access it.
						</p>
					</div>
					<div class="col-md-8">
						<button
							class="btn btn-success"
							v-on:click="reopenKanban"
						>
							Reopen Kanban Board
						</button>
					</div>
				</div>
				<div v-else
					class="row"
				>
					<div class="col-md-4">
						<h2>Close Kanban Board</h2>
						<p>
							WARNING - this will close the kanban board, you will not be able to make any more edits.
						</p>
					</div>
					<div class="col-md-8">
						<button
							class="btn btn-danger"
							v-on:click="closeKanban"
						>
							Close Kanban Board
						</button>
					</div>
				</div>

				<hr/>
				
				<div class="row">
					<div class="col-md-4">
						<h2>DELETE Kanban Board</h2>
						<p>
							WARNING - this will DELETE the kanban board, this can not be reverted!
						</p>
					</div>
					<div class="col-md-8">
						<button
							class="btn btn-danger"
							v-on:click="deleteKanban"
						>
							Delete Kanban Board!
						</button>
					</div>
				</div>
			</div>
		</div>

		<confirm-delete-object></confirm-delete-object>
	</n-config-provider>
</template>

<script>
import {Modal} from "bootstrap";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";

//Components
import ConfirmDeleteObject from "../modules/wizards/ConfirmDeleteObject.vue";

export default {
	name: "KanbanDangerZone",
	components: {
		ConfirmDeleteObject
	},
	props: {
		kanbanBoardStatus: {
			type: String,
			default: "",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	methods: {
		useNBTheme,
		closeKanban() {
			const modal = new Modal("#confirmKanbanBoardClosure");
			modal.show();
		},
		deleteKanban() {
			const modal = new Modal("#confirmDeleteObjectModal");
			modal.show();
		},
		reopenKanban() {
			const modal = new Modal("#confirmKanbanBoardReopen");
			modal.show();
		},
	},

}
</script>