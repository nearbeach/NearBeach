<template>
	<div
		v-if="userLevel > 1"
		class="kanban-row"
	>
		<!-- Users can edit kanban board - can drag -->
		<kanban-column-draggable
			v-for="column in columnResults"
			:key="column.pk"
			:level-id="levelId"
			:column-id="column.pk"
			:column-property="column.fields.kanban_column_property"
			:new-card-info="newCardInfo"
			@double_clicked_card="doubleClickedCard($event)"
		></kanban-column-draggable>
	</div>
	<div
		v-else
		class="kanban-row"
	>
		<!-- Read Only Users -->
		<kanban-column
			v-for="column in columnResults"
			:key="column.pk"
			:level-id="levelId"
			:column-id="column.pk"
			:new-card-info="newCardInfo"
			@double_clicked_card="doubleClickedCard($event)"
		></kanban-column>
	</div>
</template>

<script>
import {mapGetters} from "vuex";
import KanbanColumn from "./KanbanColumn.vue";
import KanbanColumnDraggable from "./KanbanColumnDraggable.vue";

export default {
	name: "KanbanRow",
	components: {
		KanbanColumn,
		KanbanColumnDraggable,
	},
	props: {
		levelId: {
			type: Number,
			default: 0,
		},
		newCardInfo: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	emits: [
		'double_clicked_card',
	],
	computed: {
		...mapGetters({
			columnResults: "getColumnResults",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		doubleClickedCard(data) {
			//Emit the card id up stream
			this.$emit("double_clicked_card", data);
		},
	},
};
</script>


