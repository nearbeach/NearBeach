<template>
	<div
		class="card"
		v-if="kanbanList.length > 0"
	>
		<div class="card-body">
			<h1>Open Kanban Boards</h1>
			<hr/>

			<!-- List all kanban boards -->
			<render-object-card
				v-bind:search-results="kanbanList"
				v-bind:import-variables="kanbanVariables"
				destination="kanban"
			></render-object-card>
		</div>
	</div>
</template>

<script>
//Components
import RenderObjectCard from "../render/RenderObjectCard.vue";

export default {
	name: "DashboardKanbanList",
	components: {
		RenderObjectCard,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data: () => ({
		kanbanList: [],
		kanbanVariables: {
			header: "Kanban Boards",
			prefix: "Kan",
			id: "id",
			title: "title",
			status: "status",
			end_date: "end_date",
		},
	}),
	methods: {
		getMyKanbanList() {
			//Use axios to get data
			this.axios
				.post(`${this.rootUrl}dashboard/get/kanban_list/`)
				.then((response) => {
					//Map out the data to a flatted table for rendering purposes.
					this.kanbanList = response.data.map((row) => {
						return {
							id: row.pk,
							title: row.fields.kanban_board_name,
							status: "Open",
							end_date: "",
						};
					});
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Getting Kanban List",
						message: `Error getting kanban list. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
	},
	mounted() {
		//Get list of kanban items
		this.getMyKanbanList();
	},
};
</script>


