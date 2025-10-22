<template>
	<div class="list-group kanban-cell">
		<div
v-for="element in masterList"
			 :id="element.pk"
			 :key="element.pk"
			 class="list-group-item"
			 @dblclick="doubleClickCard($event)"
		>
			<div
				:class="`card-priority-line priority-${priorityList[element.fields.kanban_card_priority]}`">
			</div>
			<carbon-link
				v-if="isLinkedObject(element)"
				:data-sort-number="element.fields.kanban_card_sort_number"
				:data-card-id="element.pk"
				class="card-external-link"
			></carbon-link>
			<b>#{{ element.pk }}</b
			><br/>
			{{ element.fields.kanban_card_text }}
			<div
v-if="element.tag_list.length > 0"
				 class="tag-list"
			>
				<div
v-for="single_tag in element.tag_list"
					 :key="single_tag.tag_assignment_id"
					 :style="`background-color:${single_tag.tag_colour};color:${single_tag.tag_text_colour};`"
					 class="single-tag-thin"
				>
					{{ single_tag.tag_name }}
				</div>
			</div>
			<carbon-information
				class="kanban-card-info-icon"
				width="25px"
				height="25px"
				@click="singleClickCard(element.pk)"
				@dblclick="singleClickCard(element.pk)"
			></carbon-information>
		</div>
	</div>
</template>

<script>
//Components
import CarbonInformation from "Components/icons/CarbonInformation.vue";
import CarbonLink from "Components/icons/CarbonLink.vue";

export default {
	name: "PublicKanbanColumn",
	components: {
		CarbonInformation,
		CarbonLink,
	},
	props: {
		masterList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	emits: [
		'card_clicked',
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