<template>
	<div>
		<div
			v-if="cardLink.id !== undefined && cardLink.id !== null"
			class="row link-to-object"
		>
			<strong>Object Link: </strong>
			<a
				:href="cardLink.hyperlink"
				target="_blank"
				rel="noopener noreferrer"
			>
				{{ cardLink.type }} - {{ cardLink.id }}
			</a>
		</div>
		<hr v-if="cardLink.id !== undefined && cardLink.id !== null"/>

		<!-- Card Text -->
		<div class="row">
			<div class="col-md-4">
				<strong>Card Title</strong>
				<p class="text-instructions">
					Write an appropriate name for the kanban card. To update
					click on the "Update" button.
				</p>
			</div>
			<div class="col-md-8">
				<label>Card Title</label>
				<input
					v-model="cardTitle"
					class="form-control"
					v-bind:disabled="userLevel<=1"
				/>
			</div>
		</div>

		<hr/>
		<div class="row">
			<div class="col-md-4">
				<strong>Card Priority</strong>
				<p class="text-instructions">
					Define what the priority of the card is.
				</p>
			</div>
			<div class="col-md-4">
				<label>Card Priority</label>
				<n-select
					v-bind:options="listPriority"
					v-model:value="cardPriority"
					:disabled="kanbanStatus === 'Closed' || userLevel <= 1"
				></n-select>
			</div>
		</div>
		<hr/>

		<!-- CARD LOCATION -->
		<div class="row">
			<div class="col-md-4">
				<strong>Card Location</strong>
				<p class="text-instructions">
					Select the appropriate location for this card.
				</p>
			</div>

			<div class="col-md-8">
				<div class="row">
					<div class="col-md-6 mt-4">
						<label>Card Column</label>
						<n-select
							v-bind:options="listColumns"
							label="column"
							v-model:value="cardColumn"
							:disabled="kanbanStatus === 'Closed' || userLevel <= 1"
						></n-select>
					</div>

					<div class="col-md-6 mt-4">
						<label>Card Level</label>
						<n-select
							v-bind:options="listLevels"
							label="level"
							v-model:value="cardLevel"
							:disabled="kanbanStatus === 'Closed' || userLevel <= 1"
						></n-select>
					</div>
				</div>
			</div>
		</div>

		<hr>
		<div class="row">
			<div class="col-md-4">
				<strong>Card Dates</strong>
			</div>
			<div class="col-md-8">
				<div class="row">
					<div class="col-md-6">
						Creation Date
						<p class="text-instructions">
							{{useNiceDatetime(dateCreated)}}
						</p>
					</div>
					<div class="col-md-6">
						Last Modified Date
						<p class="text-instructions">
							{{useNiceDatetime(dateModified)}}
						</p>
					</div>
				</div>
			</div>
		</div>

		<hr v-if="userLevel > 1"/>
		<div
			class="row"
			v-if="userLevel > 1"
		>
			<div class="col-md-12 card-detail--buttons">
				<button
					class="btn btn-warning"
					v-on:click="closeModal"
				>
					Close & Discard Changes
				</button>
				<button
					class="btn btn-danger archive-card"
					v-on:click="archiveCard"
					v-if="kanbanStatus !== 'Closed'"
				>
					Archive Card
				</button>
				<button
					class="btn btn-primary save-changes"
					v-on:click="updateCard(true)"
					v-if="kanbanStatus !== 'Closed'"
				>
					Save & Close
				</button>
				<button
					class="btn btn-success save-changes"
					v-on:click="updateCard(false)"
					v-if="kanbanStatus !== 'Closed'"
				>
					Save & Continue
				</button>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";
import {mapGetters} from "vuex";
import {Modal} from "bootstrap";

//Composables
import { useNiceDatetime } from "../../composables/datetime/useNiceDatetime";

export default {
	name: "CardDetails",
	components: {
		NSelect,
	},
	emits: [
		"update_card",
	],
	data() {
		return {
			listPriority: [
				{
					label: "Highest",
					value: 0,
				},
				{
					label: "High",
					value: 1,
				},
				{
					label: "Normal",
					value: 2,
				},
				{
					label: "Low",
					value: 3,
				},
				{
					label: "Lowest",
					value: 4,
				},
			],
			tempModel: "",
		};
	},
	computed: {
		...mapGetters({
			cardId: "getCardId",
			cardLink: "getCardLink",
			dateCreated: "getDateCreated",
			dateModified: "getDateModified",
			kanbanStatus: "getKanbanStatus",
			listColumns: "getListColumns",
			listLevels: "getListLevels",
			userLevel: "getUserLevel",
		}),
		cardColumn: {
			get() {
				return this.$store.state.card.cardColumn;
			},
			set(value) {
				this.$store.commit({
					type: "updateValue",
					field: "cardColumn",
					value,
				});
			},
		},
		cardLevel: {
			get() {
				return this.$store.state.card.cardLevel;
			},
			set(value) {
				this.$store.commit({
					type: "updateValue",
					field: "cardLevel",
					value,
				});
			},
		},
		cardPriority: {
			get() {
				return this.$store.state.card.cardPriority;
			},
			set(value) {
				this.$store.commit({
					type: "updateValue",
					field: "cardPriority",
					value,
				});
			},
		},
		cardTitle: {
			get() {
				return this.$store.state.card.cardTitle;
			},
			set(value) {
				this.$store.commit({
					type: "updateValue",
					field: "cardTitle",
					value,
				});
			},
		}
	},
	methods: {
		archiveCard() {
			//Close the current modal
			document
				.getElementById("cardInformationModalCloseButton")
				.click();

			//Open up the archive card modal
			const confirmCardArchive = new Modal(
				"#confirmCardArchiveModal"
			);
			confirmCardArchive.show();
		},
		closeModal() {
			document
				.getElementById("cardInformationModalCloseButton")
				.click();
		},
		async differentDestination(close_modal, old_card) {
			//The card is assumed to be placed at the end of the new destination. So lets look up how many cards are there
			//and then use that number
			const new_index = this.$store.getters.getCardsOrder(this.cardColumn, this.cardLevel).length;

			//Create the EVENT object for VueX
			const event = {
				to: {
					dataset: {
						column: this.cardColumn,
						level: this.cardLevel,
					},
				},
				from: {
					dataset: {
						column: old_card.kanban_column,
						level: old_card.kanban_level,
					}
				},
				item: {
					dataset: {
						cardId: this.cardId,
						cardPriority: this.cardPriority,
					}
				},
				newIndex: new_index,
			};

			//Send this information up to vueX :)
			//VueX will move everything around for us - like we have moved the card manually
			await this.$store.dispatch("kanbanCardMoved", {
				event,
			});

			//Now we get the new destination and old destination
			const new_destination = this.$store.getters.getCardsOrder(this.cardColumn, this.cardLevel);
			const old_destination = this.$store.getters.getCardsOrder(
				old_card.kanban_column,
				old_card.kanban_level
			).filter((row) => {
				//We don't want the old destination to have the card id...
				return parseInt(row.pk) !== parseInt(this.cardId);
			});

			//Tell the parent node that we have updated the data
			this.$emit("update_card", {
				close_modal,
				new_destination,
				old_destination,
			});
		},
		sameDestination(close_modal) {
			//Update the card title
			this.$store.commit({
				type: "updateKanbanCard",
				card_id: this.cardId,
				kanban_card_text: this.cardTitle,
				kanban_card_priority: this.cardPriority,
			});

			//Tell the parent node that we have updated the data
			this.$emit("update_card", {
				close_modal,
			});
		},
		updateCard(close_modal) {
			/* METHOD
			 * ~~~~~~
			 * 1. Determine if there is a change in either column/level
			 * 2. If no change - just send back basic information to save
			 * 3.
			 */

			//Get the old card information
			const old_card = this.$store.getters.getCard(this.cardId);

			//Determine if we are changing levels or columns
			const condition_1 = parseInt(this.cardColumn) === parseInt(old_card.kanban_column);
			const condition_2 = parseInt(this.cardLevel) === parseInt(old_card.kanban_level);

			//If there are no changes - just send the data upstream
			if (condition_1 && condition_2) {
				this.sameDestination(close_modal)
			} else {
				this.differentDestination(close_modal, old_card);
			}
		},
		useNiceDatetime,
	},
};
</script>
