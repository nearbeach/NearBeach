<template>
	<draggable
		class="list-group kanban-cell"
		v-bind:id="`kanban_cell_${levelId}_${columnId}`"
		v-bind:data-level="levelId"
		v-bind:data-column="columnId"
		v-bind:data-column-property="columnProperty"
		:disabled="kanbanStatus === 'Closed' || !canDragCards"
		group="tasks"
		@end="onEnd($event)"
		v-model="masterList"
		item-key="pk"
		v-if="!levelCollapseStatus(levelId)"
	>
		<template #item="{ element }">
			<div
				class="list-group-item"
				:key="element.pk"
				:id="element.pk"
				v-bind:data-sort-number="element.fields.kanban_card_sort_number"
				v-bind:data-card-id="element.pk"
				v-on:dblclick="doubleClickCard($event)"
			>
				<div v-bind:class="`card-priority-line priority-${priorityList[element.fields.kanban_card_priority]}`"
					 v-bind:data-card-id="element.pk"
					 v-bind:data-sort-number="element.fields.kanban_card_sort_number"
				></div>
				<Icon v-if="isLinkedObject(element).length > 0"
					  v-bind:icon="icons.linkOut"
					  v-bind:data-card-id="element.pk"
					  v-bind:data-sort-number="element.fields.kanban_card_sort_number"
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
		</template>

		<!--         ADD NEW CARDS + LINK OBJECTS -->
		<template #footer>
			<div class="kanban-add-new-cards">
				<a
					class="kanban-link btn btn-primary"
					href="javascript:void(0)"
					v-on:click="addNewKanbanCard"
					v-if="columnProperty !== 'Closed'"
				>
					New Card
				</a>
				<a
					class="kanban-link btn btn-warning"
					href="javascript:void(0)"
					v-on:click="addNewLink"
					v-if="columnProperty !== 'Closed'"
				>
					Link Object
				</a>
				<a
					class="kanban-link btn btn-danger"
					href="javascript:void(0)"
					v-on:click="archiveCards"
					v-if="masterList.length > 0"
				>
					Archive Cards
				</a>
			</div>
		</template>
	</draggable>
</template>

<script>
import axios from "axios";
import {Icon} from "@iconify/vue";
import draggable from "vuedraggable";

import {Modal} from "bootstrap";

//Mixins
import iconMixin from "../../mixins/iconMixin";

//VUEX MAP GETTERS
import {mapGetters} from "vuex";

export default {
	name: "kanbanColumnDraggable",
	components: {
		Icon,
		draggable,
	},
	props: {
		columnId: {
			type: Number,
			default: 0,
		},
		columnProperty: {
			type: String,
			default: "Normal",
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
			canDragCards: "getCanDragCards",
			kanbanStatus: "getKanbanStatus",
			levelCollapseStatus: "getLevelCollapseStatus",
			openCardOnLoad: "getOpenCardOnLoad",
			rootUrl: "getRootUrl",
		}),
		masterList() {
			return this.filterCards(this.columnId, this.levelId);
		},
	},
	mixins: [iconMixin],
	methods: {
		addNewKanbanCard() {
			//Update the modal's data-attributes to reflect the column ID and Level ID
			var addKanbanCardModal =
				document.getElementById("addKanbanCardModal");
			addKanbanCardModal.dataset.kanbanLevel = this.levelId;
			addKanbanCardModal.dataset.kanbanColumn = this.columnId;

			//Get the Modal from the above modal
			var addKanbanCardModal = new Modal(addKanbanCardModal);
			addKanbanCardModal.show();
		},
		addNewLink() {
			//Update the modal's data-attributes to reflect the column ID and Level ID
			var newLinkModal = document.getElementById("newLinkModal");
			newLinkModal.dataset.kanbanLevel = this.levelId;
			newLinkModal.dataset.kanbanColumn = this.columnId;

			//Get the Modal from the above modal
			var newLinkModal = new Modal(newLinkModal);
			newLinkModal.show();
		},
		archiveCards() {
			//Send the archive destination to state - it will trigger the modal
			this.$store.commit({
				type: "updateArchiveDestination",
				column: this.columnId,
				level: this.levelId,
			});
		},
		checkCardOrder() {
			// /* Due to an issue - sometimes some of the cards will contain a -1 for the sort order. This sadly
			// throws a spanner into the dragging and dropping functionality. When the board boots up, we will check to
			// make sure the cards are in order. If they are not - we adjust them and upload the changes.
			//
			// Checks
			// ~~~~~~
			// 1. Make sure there are no values under 0
			// 2. Make sure the lowest value is 0
			// 3. Make sure the highest value is length of the set minus 1.
			//  */
			//
			// //Don't worry about it when masterList is empty
			// if (this.masterList.length === 0) {
			// 	//Escape
			// 	return;
			// }
			//
			// //Get the list of values for sort array
			// const sort_array = this.masterList.map((row) => {
			// 	return row.fields.kanban_card_sort_number;
			// });
			//
			// //Get the min and max
			// const min_value = Math.min.apply(null, sort_array),
			// 	max_value = Math.max.apply(null, sort_array);
			//
			// if (
			// 	min_value === 0 &&
			// 	max_value === this.masterList.length - 1
			// ) {
			// 	//Nothing to do :) YAY
			// 	return;
			// }
			//
			// //Show error screen
			// document.getElementById("sort_error").style.display = "flex";
			//
			// //There is an issue - we need to fix all the variables and send that information upstream to the
			// //backend AND the VueX
			// //Loop through the data
			// this.masterList.forEach((row, index) => {
			// 	//Setup data_to_send
			// 	const data_to_send = new FormData();
			// 	data_to_send.set(
			// 		"new_card_column",
			// 		this.columnId.toString()
			// 	);
			// 	data_to_send.set("new_card_level", this.levelId.toString());
			// 	data_to_send.set("new_card_sort_number", index.toString());
			// 	data_to_send.set(
			// 		"old_card_column",
			// 		row.fields.kanban_column
			// 	);
			// 	data_to_send.set("old_card_level", row.fields.kanban_level);
			// 	data_to_send.set(
			// 		"old_card_sort_number",
			// 		row.fields.kanban_card_sort_number
			// 	);
			// 	data_to_send.set("card_id", row.pk);
			//
			// 	//Update kanban card
			// 	this.$store.commit({
			// 		type: "updateKanbanCard",
			// 		card_id: row.pk,
			// 		kanban_column: this.columnId,
			// 		kanban_level: this.levelId,
			// 		kanban_card_sort_number: index,
			// 	});
			//
			// 	//Use axios to send the data to the database
			// 	console.log("Kanban Column Draggable - 2 | ", row);
			// 	axios.post(
			// 		`${this.rootUrl}kanban_information/${row.pk}/move_card/`,
			// 		data_to_send
			// 	);
			// });
			//
			// //Done - hide the error screen
			// document.getElementById("sort_error").style.display = "";
		},
		doubleClickCard(data) {
			//Filter out the data we want to send up stream
			const filtered_data = this.masterList.filter((row) => {
				return row.pk == data.target.dataset.cardId;
			})[0];

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
		dragDifferentColumn(data) {
			//Short hand - making it easy to read code later
			let new_card_column = data.get("new_card_column"),
				new_card_level = data.get("new_card_level"),
				new_card_sort_number = parseInt(
					data.get("new_card_sort_number")
				),
				old_card_column = data.get("old_card_column"),
				old_card_level = data.get("old_card_level"),
				old_card_sort_number = parseInt(
					data.get("old_card_sort_number")
				),
				card_id = data.get("card_id");

			//Create return array
			let return_array = [];

			//Move new column first
			//Filter for all data effected in the new column
			let filter_new_column = this.allCards.filter((row) => {
				//return where column = new_card_column, and sort level >= new sort level
				return (
					row.fields.kanban_column == new_card_column &&
					row.fields.kanban_level == new_card_level &&
					row.fields.kanban_card_sort_number >=
					new_card_sort_number
				);
			});

			//Loop through the filtered new columns and add the required data to the return array
			filter_new_column.forEach((row) => {
				//Move the cards up by one
				return_array.push({
					card_id: row.pk,
					kanban_column: new_card_column,
					kanban_level: new_card_level,
					kanban_card_sort_number:
						row.fields.kanban_card_sort_number + 1,
				});
			});

			//Filter for all data effected in old column
			let filter_old_column = this.allCards.filter((row) => {
				//Return where column = old_card_column, and the sort level >= old sort level
				return (
					row.fields.kanban_column == old_card_column &&
					row.fields.kanban_level == old_card_level &&
					row.fields.kanban_card_sort_number >=
					old_card_sort_number
				);
			});

			//Loop through the filter old columns and add the required data to return array
			filter_old_column.forEach((row) => {
				if (row.pk == card_id) {
					//Move this to the new column
					return_array.push({
						card_id: row.pk,
						kanban_column: new_card_column,
						kanban_level: new_card_level,
						kanban_card_sort_number: new_card_sort_number,
					});
				} else {
					//Move the cards down by 1
					return_array.push({
						card_id: row.pk,
						kanban_column: old_card_column,
						kanban_level: old_card_level,
						kanban_card_sort_number:
							row.fields.kanban_card_sort_number - 1,
					});
				}
			});

			return return_array;
		},
		dragSameColumn(data) {
			//Short hand - making it easy to read code later
			let new_sort = parseInt(data.get("new_card_sort_number")),
				old_sort = parseInt(data.get("old_card_sort_number")),
				column = parseInt(data.get("new_card_column")),
				level = parseInt(data.get("new_card_level")),
				card_id = parseInt(data.get("card_id"));

			//Determine the delta - -1 or 1.
			//Negative number if old_sort is less than new sort, i.e. move
			//everything back one
			let delta = 1 - 2 * (old_sort < new_sort);

			//Get the largest and smallest values
			let largest =
					(new_sort >= old_sort) * new_sort +
					(new_sort < old_sort) * old_sort,
				smallest =
					(new_sort >= old_sort) * old_sort +
					(new_sort < old_sort) * new_sort;

			//If they are the same (i.e. drag and dropped in same place) - return
			if (largest === smallest) {
				return [];
			}

			//Filter for the data we need
			let filtered_data = this.allCards.filter((row) => {
				//Return when same column and level, whilst also in range of smallest and largest
				return (
					parseInt(row.fields.kanban_column) === column &&
					parseInt(row.fields.kanban_level) === level &&
					row.fields.kanban_card_sort_number >= smallest &&
					row.fields.kanban_card_sort_number <= largest
				);
			});

			//Create the return array
			let return_array = [];

			//Loop through the filtered data, and apply the changes required
			filtered_data.forEach((row) => {
				if (row.pk == card_id) {
					//Make sure this card has the new sort number
					return_array.push({
						card_id: row.pk,
						kanban_column: column,
						kanban_level: level,
						kanban_card_sort_number: new_sort,
					});
				} else {
					//Not the card we moved, apply the delta to move the sort order
					return_array.push({
						card_id: row.pk,
						kanban_column: column,
						kanban_level: level,
						kanban_card_sort_number:
							row.fields.kanban_card_sort_number + delta,
					});
				}
			});

			return return_array;
		},
		filterCards(column_id, level_id) {
			//Filter the data
			let return_array = this.allCards.filter((card) => {
				return (
					parseInt(card.fields.kanban_column) === column_id &&
					parseInt(card.fields.kanban_level) === level_id
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
		isLinkedObject(object) {
			let results = "";

			if (object.fields.project !== null) results = "project";
			if (object.fields.requirement !== null) results = "requirement";
			if (object.fields.task !== null) results = "task";

			return results;
		},
		onEnd(event) {
			/* Update the sort order
			If both the old and new level/column destinations are the same,
			we take the difference between the two values. Otherwise we apply
			two sort orders to both the old and the new*/

			this.$store.dispatch("kanbanCardMoved", {
				event: event,
			});

			return;


			//Get the y=data
			var new_elem = event.to,
				old_elem = event.from,
				card_id = event.item.dataset.cardId;

			//Setup variables (for shorthand)
			let new_card_column = new_elem.dataset.column,
				new_card_level = new_elem.dataset.level,
				new_card_sort_number = event.newIndex,
				old_card_column = old_elem.dataset.column,
				old_card_level = old_elem.dataset.level,
				old_card_sort_number = event.oldIndex,
				column_property = new_elem.dataset.columnProperty;

			//For the unlucky chance a sort number is less than 0.
			if (new_card_sort_number < 0) new_card_sort_number = 0;

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("new_card_column", new_card_column);
			data_to_send.set("new_card_level", new_card_level);
			data_to_send.set("new_card_sort_number", new_card_sort_number);
			data_to_send.set("old_card_column", old_card_column);
			data_to_send.set("old_card_level", old_card_level);
			data_to_send.set("old_card_sort_number", old_card_sort_number);
			data_to_send.set("card_id", card_id);

			//Define cards_to_change
			let cards_to_change = [];

			//Depending if the card moves columns depends what we do
			if (
				new_card_column === old_card_column &&
				new_card_level === old_card_level
			) {
				//The card stayed in the same place.

				cards_to_change = this.dragSameColumn(data_to_send);
			} else {
				//The card move to a different place

				cards_to_change = this.dragDifferentColumn(data_to_send);
			}

			//ADD CODE - loop through the cards to change
			cards_to_change.forEach((row) => {
				this.$store.commit({
					type: "updateKanbanCard",
					card_id: row.card_id,
					kanban_column: row.kanban_column,
					kanban_level: row.kanban_level,
					kanban_card_sort_number: row.kanban_card_sort_number,
				});
			});

			//Get the new sort orders for the new destination and the old destination
			const new_destination = this.filterCards(new_card_column, new_card_level);
			console.log("New Destination: ", new_destination);
			new_destination.forEach(row => {
				data_to_send.append('new_destination', row.pk);
			});
			const old_destination = this.filterCards(old_card_column, old_card_level);
			console.log("Old Destination: ", old_destination);
			old_destination.forEach(row => {
				data_to_send.append('old_destination', row.pk);
			});

			//Use axios to send the data to the database
			axios
				.post(
					`${this.rootUrl}kanban_information/${card_id}/move_card/`,
					data_to_send
				)
				.then(() => {
					//We need to look at the DESTINATION's Column Properties
					if (column_property !== "Blocked") {
						//Nothing needs to be done if not blocked
						return;
					}

					//Update the card id focus in the state management
					this.$store.commit({
						type: "updateValue",
						field: "cardId",
						value: parseInt(card_id),
					});

					//Open the BlockedCardModal
					const blockedNotes = new Modal("#blockedNotesModal");
					blockedNotes.show();
				});
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
				return row.pk == data;
			})[0];

			//Setup data to send upstream
			this.sendDataUpstream(filtered_data);
		},
	},
	watch: {
		newCardInfo() {
			//Only add the card if the column and the level match
			if (
				this.columnId == this.newCardInfo[0].fields.kanban_column &&
				this.levelId == this.newCardInfo[0].fields.kanban_level
			) {
				//The new card is for this level and column. Add it to the masterList
				this.masterList.push(this.newCardInfo[0]);
			}
		},
	},
	mounted() {
		this.checkCardOrder();

		//Check to see if the "openCardOnLoad" card ID exists on in this section
		const count = this.masterList.filter((row) => {
			//Conditions
			// 1 row primary key is the same as openCardOnLoad value
			// 2 row is not a linked object, i.e. not value under project, task, or requirement field
			const condition_1 = row.pk == this.openCardOnLoad;
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
