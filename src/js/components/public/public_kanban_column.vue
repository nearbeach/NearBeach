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
			<carbon-link
				v-if="isLinkedObject(element)"
				v-bind:data-sort-number="element.fields.kanban_card_sort_number"
				v-bind:data-card-id="element.pk"
				class="card-external-link"
			></carbon-link>
			<b>#{{ element.pk }}</b
			><br/>
			{{ element.fields.kanban_card_text }}
			<carbon-information
				class="kanban-card-info-icon"
				width="25px"
				height="25px"
				v-on:click="singleClickCard(element.pk)"
				v-on:dblclick="singleClickCard(element.pk)"
			></carbon-information>
		</div>
	</div>
</template>

<script>
//Components
import CarbonInformation from "../icons/CarbonInformation.vue";
import CarbonLink from "../icons/CarbonLink.vue";

export default {
	name: "PublicKanbanColumn",
	components: {
		CarbonInformation,
		CarbonLink,
	},
	emits: [
		'card_clicked',
	],
	props: {
		masterList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
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