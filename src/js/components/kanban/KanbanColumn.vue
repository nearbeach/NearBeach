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
			:key="element.kanban_card_id"
			:id="element.kanban_card_id"
			v-bind:data-sort-number="element.kanban_card_sort_number"
			v-bind:data-card-id="element.kanban_card_id"
			v-on:dblclick="doubleClickCard($event)"
		>
			<div
				v-bind:class="`card-priority-line priority-${priorityList[element.kanban_card_priority]}`">
			</div>
			<carbon-link v-if="isLinkedObject(element)"
				  class="card-external-link"
			></carbon-link>
			<b>#{{ element.kanban_card_id }}</b>
			<br/>
			{{ element.kanban_card_text }}
			<div v-if="element.tag_list.length > 0"
				 class="tag-list"
			>
				<div v-for="single_tag in element.tag_list"
					 :key="single_tag.tag_assignment_id"
					 v-bind:style="`background-color:${single_tag.tag_colour};color:${single_tag.tag_text_colour};`"
					 class="single-tag-thin"
				>
					{{ single_tag.tag_name }}
				</div>
			</div>
			<carbon-information
				class="kanban-card-info-icon"
				width="25px"
				height="25px"
				v-on:click="singleClickCard(element.kanban_card_id)"
				v-on:dblclick="singleClickCard(element.kanban_card_id)"
			></carbon-information>
		</div>
	</div>
</template>

<script>
import {Modal} from "bootstrap";

//Components
import CarbonInformation from "../icons/CarbonInformation.vue"
import CarbonLink from "../icons/CarbonLink.vue"


//VUEX MAP GETTERS
import {mapGetters} from "vuex";

export default {
	name: "KanbanColumn",
	components: {
		CarbonInformation,
		CarbonLink,
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
					parseInt(card.kanban_column) === this.columnId &&
					parseInt(card.kanban_level) === this.levelId
				);
			});

			//Make sure it is sorted
			return_array = return_array.sort((a, b) => {
				return (
					a.kanban_card_sort_number -
					b.kanban_card_sort_number
				);
			});

			return return_array;
		},
	},
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
				return row.kanban_card_sort_number;
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
					row.kanban_column
				);
				data_to_send.set("old_card_level", row.kanban_level);
				data_to_send.set(
					"old_card_sort_number",
					row.kanban_card_sort_number
				);
				data_to_send.set("card_id", row.kanban_card_id);

				//Update kanban card
				this.$store.commit({
					type: "updateKanbanCard",
					card_id: row.kanban_card_id,
					kanban_column: this.columnId,
					kanban_level: this.levelId,
					kanban_card_sort_number: index,
				});

				//Use axios to send the data to the database
				this.axios.post(
					`${this.rootUrl}kanban_information/${row.kanban_card_id}/move_card/`,
					data_to_send
				);
			});

			//Done - hide the error screen
			document.getElementById("sort_error").style.display = "";
		},
		doubleClickCard(event) {
			//Retrieve the card id from the event
			const card_id = this.getCardIdFromObject(event.target);

			//Check to make sure we card is not 0
			if (card_id === 0) return;

			//Filter out the data we want to send up stream
			const filtered_data = this.masterList.filter((row) => {
				return parseInt(row.kanban_card_id) === parseInt(card_id);
			})[0];

			//Check to see if there are any results
			if (filtered_data === undefined) return;

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
		getCardIdFromObject(object) {
			//Recursive function, that checks to see if we can get the card id. If not we look at the parent.
			//The break points are where the parent is undefined, OR the id === "kanban_container"
			const card_id = object.dataset.cardId;

			//Got the card id, lets return
			if (card_id !== undefined) return card_id;

			//Check to make sure we not at the escapte point
			if (object.id === "kanban_container") return 0;
			if (object.parentElement === undefined || object.parentElement === null) return 0;

			//Recursive call the function
			return this.getCardIdFromObject(object.parentElement);
		},
		isLinkedObject(object) {
			let results = "";

			if (object.project !== null && object.project !== undefined) results = "project";
			if (object.requirement !== null && object.requirement !== undefined) results = "requirement";
			if (object.task !== null && object.requirement !== undefined) results = "task";

			return results;
		},
		sendDataUpstream(filtered_data) {
			// Check to make sure this is a linked object
			const is_link = this.isLinkedObject(filtered_data);
			if (is_link.length > 0) {
				//Open a new tab with that linked object
				const url = `${this.rootUrl}${is_link}_information/${filtered_data[is_link]}/`;

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
				cardId: filtered_data.kanban_card_id,
				cardTitle: filtered_data.kanban_card_text,
				cardDescription:
				filtered_data.kanban_card_description,
				cardColumn: filtered_data.kanban_column,
				cardLevel: filtered_data.kanban_level,
				cardLink: {},
				cardPriority: filtered_data.kanban_card_priority,
				dateCreated: filtered_data.date_created,
				dateModified: filtered_data.date_modified,
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
				return row.kanban_card_id === data;
			})[0];

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
	},
	watch: {
		newCardInfo() {
			//Only add the card if the column and the level match
			if (
				this.columnId === this.newCardInfo[0].kanban_column &&
				this.levelId === this.newCardInfo[0].kanban_level
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
			const condition_1 = row.kanban_card_id === this.openCardOnLoad;
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


