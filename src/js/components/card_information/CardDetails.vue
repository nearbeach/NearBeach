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
		<hr v-if="cardLink.id !== undefined && cardLink.id !== null" />

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
				/>
			</div>
		</div>
		<hr />

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
					<div class="col-md-12 mt-4">
						<label>Card Column</label>
						<n-select
							v-bind:options="listColumns"
							label="column"
							v-model:value="cardColumn"
							:disabled="kanbanStatus === 'Closed'"
						></n-select>
					</div>

					<div class="col-md-12 mt-4">
						<label>Card Level</label>
						<n-select
							v-bind:options="listLevels"
							label="level"
							v-model:value="cardLevel"
							:disabled="kanbanStatus === 'Closed'"
						></n-select>
					</div>
				</div>
			</div>
		</div>

		<hr v-if="userLevel > 1" />
		<div
			class="row"
			v-if="userLevel > 1"
		>
			<div class="col-md-12">
				<button
					class="btn btn-secondary"
					v-on:click="closeModal"
				>
					Close
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
					v-on:click="updateCard"
					v-if="kanbanStatus !== 'Closed'"
				>
					Update Card
				</button>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");
	import { NSelect } from "naive-ui";
	import { mapGetters } from "vuex";
	import { Modal } from "bootstrap";

	export default {
		name: "CardDetails",
		components: {
			// mapGetters,
			NSelect,
		},
		data() {
			return {
				tempModel: "",
			};
		},
		computed: {
			...mapGetters({
				cardId: "getCardId",
				cardLevel: "getCardLevel",
				cardLink: "getCardLink",
				cardTitle: "getCardTitle",
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
						value: value,
					});
				},
			},
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
			updateCard() {
				this.$store.commit({
					type: "updateKanbanCard",
					card_id: this.cardId,
					kanban_card_text: this.cardTitle,
					kanban_column: this.cardColumn,
					kanban_level: this.cardLevel,
				});

				//TEMP - need to replace with a close functionality
				this.$emit("update_card");
			},
		},
	};
</script>
