<template>
	<div
		class="list-group kanban-cell"
		v-bind:id="`kanban_cell_${levelId}_${columnId}`"
		v-bind:data-level="levelId"
		v-bind:data-column="columnId"
	>
		<div
			class="list-group-item"
			v-for="element in masterList"
			:key="element.pk"
			:id="element.pk"
			v-bind:data-sort-number="element.fields.kanban_card_sort_number"
			v-bind:data-card-id="element.pk"
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
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

//Mixins
import iconMixin from "../../mixins/iconMixin";

//VUEX MAP GETTERS
import {mapGetters} from "vuex";
import draggable from "vuedraggable";

export default {
	name: "KanbanColumn",
	components: {
		draggable,
		Icon,
	},
	props: {
		columnId: {
			type: Number,
			default: 0,
		},
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
	data() {
		return {
			//masterList: [],
			drag: false,
			priorityList: [
				'highest',
				'high',
				'normal',
				'low',
				'lowest',
			],
		};
	},
	computed: {
		...mapGetters({
			allCards: "getCards",
			kanbanStatus: "getKanbanStatus",
			openCardOnLoad: "getOpenCardOnLoad",
			rootUrl: "getRootUrl",
		}),
		masterList() {
			//Filter the data
			let return_array = this.allCards.filter((card) => {
				return (
					parseInt(card.fields.kanban_column) === this.columnId &&
					parseInt(card.fields.kanban_level) === this.levelId
				);
			});

			//Make sure it is sorted
			return_array = return_array.sort((a, b) => {
				return (
					a.fields.kanban_card_sort_number -
					b.fields.kanban_card_sort_number
				);
			});

			return return_array;
		},
	},
	mixins: [iconMixin],
	methods: {
		checkCardOrder() {
			/* Due to an issue - sometimes some of the cards will contain a -1 for the sort order. This sadly
			throws a spanner into the dragging and dropping functionality. When the board boots up, we will check to
			make sure the cards are in order. If they are not - we adjust them and upload the changes.

			Checks
			~~~~~~
			1. Make sure there are no values under 0
			2. Make sure the lowest value is 0
			3. Make sure the highest value is length of the set minus 1.
			 */

			//Don't worry about it when masterList is empty
			if (this.masterList.length === 0) {
				//Escape
				return;
			}

			//Get the list of values for sort array
			const sort_array = this.masterList.map((row) => {
				return row.fields.kanban_card_sort_number;
			});

			//Get the min and max
			const min_value = Math.min.apply(null, sort_array),
				max_value = Math.max.apply(null, sort_array);

			if (
				min_value === 0 &&
				max_value === this.masterList.length - 1
			) {
				//Nothing to do :) YAY
				return;
			}

			//Show error screen
			document.getElementById("sort_error").style.display = "flex";

			//There is an issue - we need to fix all the variables and send that information upstream to the
			//backend AND the VueX
			//Loop through the data
			this.masterList.forEach((row, index) => {
				//Setup data_to_send
				const data_to_send = new FormData();
				data_to_send.set(
					"new_card_column",
					this.columnId.toString()
				);
				data_to_send.set("new_card_level", this.levelId.toString());
				data_to_send.set("new_card_sort_number", index.toString());
				data_to_send.set(
					"old_card_column",
					row.fields.kanban_column
				);
				data_to_send.set("old_card_level", row.fields.kanban_level);
				data_to_send.set(
					"old_card_sort_number",
					row.fields.kanban_card_sort_number
				);
				data_to_send.set("card_id", row.pk);

				//Update kanban card
				this.$store.commit({
					type: "updateKanbanCard",
					card_id: row.pk,
					kanban_column: this.columnId,
					kanban_level: this.levelId,
					kanban_card_sort_number: index,
				});

				//Use axios to send the data to the database
				this.axios.post(
					`${this.rootUrl}kanban_information/${row.pk}/move_card/`,
					data_to_send
				);
			});

			//Done - hide the error screen
			document.getElementById("sort_error").style.display = "";
		},
		doubleClickCard(data) {
			//Filter out the data we want to send up stream
			const filtered_data = this.masterList.filter((row) => {
				return row.pk === data.target.dataset.cardId;
			})[0];

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
		isLinkedObject(object) {
			let results = "";

			if (object.fields.project !== null) results = "project";
			if (object.fields.requirement !== null) results = "requirement";
			if (object.fields.task !== null) results = "task";

			return results;
		},
		sendDataUpstream(filtered_data) {
			// Check to make sure this is a linked object
			const is_link = this.isLinkedObject(filtered_data);
			if (is_link.length > 0) {
				//Open a new tab with that linked object
				const url = `${this.rootUrl}${is_link}_information/${filtered_data.fields[is_link]}/`;

				window.open(
					url,
					'_blank'
				).focus();

				//Just return - nothing else to do
				return;
			}

			// Update VueX ACTION
			this.$store.dispatch({
				type: "updateCard",
				cardId: filtered_data.pk,
				cardTitle: filtered_data.fields.kanban_card_text,
				cardDescription:
				filtered_data.fields.kanban_card_description,
				cardColumn: filtered_data.fields.kanban_column,
				cardLevel: filtered_data.fields.kanban_level,
				cardLink: {},
				cardPriority: filtered_data.fields.kanban_card_priority,
			});

			//Show the modal
			const cardInformationModal = new Modal(
				document.getElementById("cardInformationModal")
			);
			cardInformationModal.show();
		},
		singleClickCard(data) {
			//Filter out the data we want to send up stream
			const filtered_data = this.masterList.filter((row) => {
				return row.pk === data;
			})[0];

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
	},
	watch: {
		newCardInfo() {
			//Only add the card if the column and the level match
			if (
				this.columnId === this.newCardInfo[0].fields.kanban_column &&
				this.levelId === this.newCardInfo[0].fields.kanban_level
			) {
				//The new card is for this level and column. Add it to the masterList
				this.masterList.push(this.newCardInfo[0]);
			}
		},
	},
	mounted() {
		// this.checkCardOrder();

		//Check to see if the "openCardOnLoad" card ID exists on in this section
		const count = this.masterList.filter((row) => {
			//Conditions
			// 1 row primary key is the same as openCardOnLoad value
			// 2 row is not a linked object, i.e. not value under project, task, or requirement field
			const condition_1 = row.pk === this.openCardOnLoad;
			const condition_2 = this.isLinkedObject(row).length === 0;

			return condition_1 && condition_2;
		}).length;

		if (count > 0) {
			//Card exists here. Run function to open the card
			this.singleClickCard(this.openCardOnLoad);
		}
	},
};
</script>

<style scoped></style>
