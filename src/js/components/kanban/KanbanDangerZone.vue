<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card text-bg-warning">
			<div class="card-body">
				<h1>DANGER ZONE</h1>
				<hr>

				<div class="row">
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
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import getThemeMixin from "../../mixins/getThemeMixin";
import {Modal} from "bootstrap";

export default {
	name: "KanbanDangerZone",
	props: {
		theme: {
			type: String,
			default: "",
		},
	},
	mixins: [getThemeMixin],
	methods: {
		closeKanban() {
			const modal = new Modal("#confirmKanbanBoardClosure");
			modal.show();
		},
	},

}
</script>