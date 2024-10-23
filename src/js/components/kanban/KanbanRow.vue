<template>
	<div
		class="kanban-row"
		v-if="userLevel > 1"
	>
		<!-- Users can edit kanban board - can drag -->
		<kanban-column-draggable
			v-for="column in columnResults"
			:key="column.pk"
			v-bind:level-id="levelId"
			v-bind:column-id="column.pk"
			v-bind:column-property="column.fields.kanban_column_property"
			v-bind:new-card-info="newCardInfo"
			v-on:double_clicked_card="doubleClickedCard($event)"
		></kanban-column-draggable>
	</div>
	<div
		class="kanban-row"
		v-else
	>
		<!-- Read Only Users -->
		<kanban-column
			v-for="column in columnResults"
			:key="column.pk"
			v-bind:level-id="levelId"
			v-bind:column-id="column.pk"
			v-bind:new-card-info="newCardInfo"
			v-on:double_clicked_card="doubleClickedCard($event)"
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
	emits: [
		'double_clicked_card',
	],
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


