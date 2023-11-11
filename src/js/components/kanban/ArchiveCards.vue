<template>
	<div
		class="modal fade"
		id="archiveCardsModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="exampleModalLabel"
					>
						Are you sure?
					</h5>
					<button
						type="button"
						class="btn-close"
						aria-label="Close"
						v-on:click="closeModal"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to archive the cards? This can not be
					undone.
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="archiveCards"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";
import {Modal} from "bootstrap";

export default {
	name: "ArchiveCards",
	data() {
		return {
			archiveCardsModal: {},
		};
	},
	computed: {
		...mapGetters({
			allCards: "getCards",
			archiveDestination: "getArchiveDestination",
			archiveDestinationString: "getArchiveDestinationString",
			rootUrl: "getRootUrl",
		}),
	},
	watch: {
		archiveDestinationString(newValue) {
			//Check to make sure there are values within column or level
			if (newValue === undefined) return;

			//Open the modal
			this.archiveCardsModal = new Modal("#archiveCardsModal");
			this.archiveCardsModal.show();
		},
	},
	methods: {
		archiveCards() {
			//Simplify the variables
			let column = this.archiveDestination.column;
			let level = this.archiveDestination.level;

			// Create data_to_send
			const data_to_send = new FormData();

			// Loop through the master list and get all card ids
			this.allCards
				.filter((card) => {
					return (
						parseInt(card.fields.kanban_column) === column &&
						parseInt(card.fields.kanban_level) === level
					);
				})
				.forEach((card) => {
					data_to_send.append("kanban_card_id", card.pk);
				});

			//Mutate the data to exclude the archived cards
			this.$store.commit({
				type: "archiveCards",
				column,
				level,
			});

			//Close the modal
			this.archiveCardsModal.hide();

			//Reset the state
			this.$store.commit({
				type: "updateArchiveDestination",
				column: "",
				level: "",
			});

			// Use axios to contact backend
			this.axios
				.post(
					`${this.rootUrl}kanban_information/archive_kanban_cards/`,
					data_to_send
				)
				.catch((error) => {
					//TODO: Return cards back into state management. They errored out.
				});
		},
		closeModal() {
			//Close the modal
			this.archiveCardsModal.hide();

			//Reset the state
			this.$store.commit({
				type: "updateArchiveDestination",
				column: "",
				level: "",
			});
		},
	},
};
</script>
