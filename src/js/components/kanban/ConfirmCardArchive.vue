<template>
	<div
		class="modal fade"
		id="confirmCardArchiveModal"
		tabindex="-1"
		aria-labelledby="confirmCardArchiveModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>Card Information</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmCardArchiveModalCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="alert alert-danger">
						Please note - archiving the card can not be undone.
					</div>
					<h3>
						Are you sure you want to archive the following card?
					</h3>
					<div class="row">
						<div class="col">Card No. - {{ cardId }}</div>
					</div>
					<br/>
					<div class="row">
						<div class="col">Card Title - {{ cardTitle }}</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-danger"
						v-on:click="archiveCard"
					>
						Yes Archive Card
					</button>
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="goBack"
					>
						No go back
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
	name: "ConfirmCardArchive",
	computed: {
		...mapGetters({
			cardId: "getCardId",
			cardTitle: "getCardTitle",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		archiveCard() {
			//Create data to send
			const data_to_send = new FormData();

			//Append the kanban_card_id, not set, as the form is expecting an array/list
			data_to_send.append("kanban_card_id", this.cardId);

			//TODO - update VueX to remove single card
			//Mutate the data to exlcude the archived card
			this.$store.commit({
				type: "archiveCard",
				cardId: this.cardId,
			});

			//Close the modal
			document
				.getElementById("confirmCardArchiveModalCloseButton")
				.click();

			//Send the data to backend
			this.axios
				.post(
					`${this.rootUrl}kanban_information/archive_kanban_cards/`,
					data_to_send
				)
				.catch(() => {
					//TODO: show card error
				});
		},
		goBack() {
			//Close current modal
			document
				.getElementById("confirmCardArchiveModalCloseButton")
				.click();

			//Open previous modal
			const modal = new Modal("#cardInformationModal");
			modal.show();
		},
	},
};
</script>
