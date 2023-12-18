<template>
	<div class="list-group kanban-cell">
		<div class="list-group-item"
			 v-for="element in masterList"
			 :key="element.pk"
			 :id="element.pk"
			 v-on:dblclick="doubleClickCard($event)"
		>
			<div
				v-bind:class="`card-priority-line priority-${priorityList[element.fields.kanban_card_priority]}`">
			</div>
			<Icon v-if="isLinkedObject(element)"
				  v-bind:icon="icons.linkOut"
				  v-bind:data-sort-number="element.fields.kanban_card_sort_number"
				  v-bind:data-card-id="element.pk"
				  class="card-external-link"
			></Icon>
			<b>#{{ element.pk }}</b
			><br/>
			{{ element.fields.kanban_card_text }}
			<Icon
				class="kanban-card-info-icon"
				v-bind:icon="icons.infoCircle"
				v-on:click="singleClickCard(element.pk)"
				v-on:dblclick="singleClickCard(element.pk)"
			></Icon>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "PublicKanbanColumn",
	components: {
		Icon,
	},
	props: {
		masterList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	mixins: [
		iconMixin,
	],
	data: () => ({
		priorityList: [
			'highest',
			'high',
			'normal',
			'low',
			'lowest',
		],
	}),
	methods: {
		doubleClickCard(data) {
			this.$emit("card_clicked", parseInt(data.target.id));
		},
		isLinkedObject(object) {
			let results = "";

			if (object.fields.project !== null) results = "project";
			if (object.fields.requirement !== null) results = "requirement";
			if (object.fields.task !== null) results = "task";

			return results;
		},
		singleClickCard(data) {
			this.$emit("card_clicked", data);
		}
	}
}
</script>