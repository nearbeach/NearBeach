<template>
	<draggable
		class="list-group kanban-cell"
		v-bind:id="`kanban_cell_${levelId}_${columnId}`"
		v-bind:data-level="levelId"
		v-bind:data-column="columnId"
		v-bind:data-column-property="columnProperty"
		v-bind:animation="200"
		:disabled="kanbanStatus === 'Closed' || !canDragCards"
		group="tasks"
		ghost-class="ghost"
		@end="onEnd($event)"
		v-model="masterList"
		item-key="kanban_card_id"
		v-if="!levelCollapseStatus(levelId)"
	>
		<template #item="{ element }">
			<div
				class="list-group-item"
				:key="element.kanban_card_id"
				:id="element.kanban_card_id"
				v-bind:data-sort-number="element.kanban_card_sort_number"
				v-bind:data-card-id="element.kanban_card_id"
				v-bind:data-card-priority="element.kanban_card_priority"
				v-on:dblclick="doubleClickCard($event)"
			>
				<div v-bind:class="`card-priority-line priority-${priorityList[element.kanban_card_priority]}`"
				></div>
				<carbon-link v-if="isLinkedObject(element).length > 0"
					  class="card-external-link"
				></carbon-link>
				<b>#{{ element.kanban_card_id }}</b>
				<br/>
				{{ element.kanban_card_text }}
				<br />
				<div>
					Created Date:
					<span class="text-instructions">
						{{useNiceDatetime(element.date_created)}}
					</span>
				</div>
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
				<span v-if="!canDragCards" style="font-weight: lighter">- Movement Locked!</span>
				<span v-else style="font-weight: lighter">
					&nbsp;
				</span>
				<carbon-information
					class="kanban-card-info-icon"
					width="25px"
					height="25px"
					v-on:click="singleClickCard(element.kanban_card_id)"
					v-on:dblclick="singleClickCard(element.kanban_card_id)"
				></carbon-information>
			</div>
		</template>

		<!--         ADD NEW CARDS + LINK OBJECTS -->
		<template #footer
			v-if="kanbanStatus !== 'Closed'"
		>
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
import draggable from "vuedraggable";
import {Modal} from "bootstrap";

//Components
import {CarbonInformation, CarbonLink} from "../../components";

//VUEX MAP GETTERS
import {mapGetters} from "vuex";

//Composables
import {useNiceDatetime} from "../../composables/datetime/useNiceDatetime";

export default {
	name: "kanbanColumnDraggable",
	components: {
		CarbonInformation,
		CarbonLink,
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
		dragOptions() {
			return {
				animation: 200,
				group: "description",
				disabled: false,
				ghostClass: "ghost"
			};
		},
		masterList() {
			return this.$store.getters.getCardsOrder(this.columnId, this.levelId);
		},
	},
	methods: {
		addNewKanbanCard() {
			//Update New Card VueX to use this location
			this.$store.commit({
				type: "updateNewCardLocation",
				columnId: this.columnId,
				levelId: this.levelId,
				userCanSelectLocation: false,
			});

			//Get the Modal from the above modal
			const modalInstance = new Modal(document.getElementById("addKanbanCardModal"));
			modalInstance.show();

			//Focus on the card title
			setTimeout(() => {
				const focus_element = document.getElementById("kanbanCardText");
				focus_element.focus();
			}, 250);
		},
		addNewLink() {
			//Update New Card VueX to use this location
			this.$store.commit({
				type: "updateNewCardLocation",
				columnId: this.columnId,
				levelId: this.levelId,
				userCanSelectLocation: false,
			});

			//Get the Modal from the above modal
			const modalInstance = new Modal(document.getElementById("newLinkModal"));
			modalInstance.show();
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

			//Send the new order to the backend
			const data_to_send = new FormData();

			this.masterList.forEach((row, index) => {
				//Set the form data
				data_to_send.append("kanban_cards", row.kanban_card_id);

				//Update the VueX with the new sort ordering
				this.$store.commit({
					type: "updateKanbanCard",
					card_id: row.kanban_card_id,
					kanban_card_sort_number: index,
				});
			});

			this.axios.post(
				`${this.rootUrl}kanban_information/fix_card_ordering/`,
				data_to_send,
			).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to move card",
					message: `Sorry, we could not move your card. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
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
		async onEnd(event) {
			//Tell VueX we have moved the card - VueX will handle the logistic. Wait for vuex
			await this.$store.dispatch("kanbanCardMoved", {
				event,
			});

			//Get the y=data
			const new_elem = event.to,
				old_elem = event.from,
				card_id = event.item.dataset.cardId;

			//Setup variables (for shorthand)
			const new_card_column = new_elem.dataset.column,
				new_card_level = new_elem.dataset.level,
				
				old_card_column = old_elem.dataset.column,
				old_card_level = old_elem.dataset.level,
				
				column_property = new_elem.dataset.columnProperty;

			//Data to send
			const data_to_send = new FormData();
			data_to_send.set("new_card_column", new_card_column);
			data_to_send.set("new_card_level", new_card_level);

			//Set the new destination
			this.$store.getters.getCardsOrder(
				new_card_column,
				new_card_level
			).forEach((row) => {
				data_to_send.append("new_destination", row.kanban_card_id);
			});

			//Set the old destination
			this.$store.getters.getCardsOrder(
				old_card_column,
				old_card_level
			).forEach((row) => {
				data_to_send.append("old_destination", row.kanban_card_id);
			});

			//Use axios to send the data to the database
			this.axios.post(
				`${this.rootUrl}kanban_information/${card_id}/move_card/`,
				data_to_send
			).then(() => {
				if (column_property === "Blocked") {
					//Tell Axios about the card id
					this.$store.commit({
						type: "updateValue",
						field: "cardId",
						value: parseInt(card_id),
					});

					//Open the required modal
					const modal = new Modal(document.getElementById("blockedNotesModal"));
					modal.show();
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not update Card",
					message: `Sorry, moving the card had an error. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
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
		useNiceDatetime,
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
		this.checkCardOrder();

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


