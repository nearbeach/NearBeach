<template>
	<div
		class="modal fade"
		id="confirmNoteDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmLinkDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmNoteDelete"
					>
						Please confirm Note Deletion
					</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmNoteDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete the note?
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
						v-on:click="deleteNote"
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
import {useReopenCardInformation} from "../../../composables/card_information/useReopenCardinformation";

export default {
	name: "ConfirmNoteDelete",
	props: {},
	computed: {
		...mapGetters({
			destination: "getDestination",
			noteId: "getSingleNoteId",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		useReopenCardInformation,
		deleteNote() {
			//Tell the user we are deleting the note
			this.$store.dispatch("newToast", {
				header: "Deleting Note",
				message: "Currently deleting note",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "delete_note",
			});

			//If destination is an organisation, we have a slightly different URL due to permissions.
			let url = `${this.rootUrl}note/delete/${this.noteId}/`;
			if (this.destination === "organisation") {
				url =  `${this.rootUrl}note/organisation/delete/${this.noteId}/`;
			}

			//Send the data
			this.axios.post(
				url,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Note is deleted",
					message: "Successfully Deleted Note",
					extra_classes: "bg-success",
					unique_type: "delete_note",
				});

				this.$store.commit({
					type: "removeNote",
					noteId: this.noteId,
				});

				//Close the modal
				this.closeModal();

				//Reshow the card information modal if exists
				useReopenCardInformation();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to Delete Note",
					message: `Sorry, we failed to delete the note. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "delete_note",
				});
			})
		},
		closeModal() {
			document.getElementById("confirmNoteDeleteButton").click();

			//Open the card information modal, if it exists
			useReopenCardInformation();
		},
	},
}
</script>
