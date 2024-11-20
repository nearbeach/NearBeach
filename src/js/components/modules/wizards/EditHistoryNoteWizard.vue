<template>
	<!-- EDIT HISTORY NOTE -->
	<div
		class="modal fade"
		id="editNoteModal"
		tabindex="-1"
		role="dialog"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div
			class="modal-dialog modal-lg modal-fullscreen-lg-down"
			role="document"
		>
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Edit Note
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="editNoteCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<p class="text-instructions">
						Use the text editor to edit your note. Click on the "Update" button
						to submit the changes.
					</p>
					<editor
						license-key="gpl"
						:init="{
							license_key: 'gpl',
							height: 300,
							menubar: false,
							plugins: ['lists', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 				 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            				skin: `${this.skin}`,
			            	content_css: `${this.contentCss}`,
			            	relative_urls: false,
						}"
						v-model="noteModel"
					/>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-primary"
						v-bind:disabled="noteModel == ''"
						v-on:click="updateNote"
					>
						Update Note
					</button>
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript components
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";
import {useReopenCardInformation} from "../../../composables/card_information/useReopenCardinformation";


export default {
	name: "EditHistoryNoteWizard",
	components: {
		editor: Editor,
	},
	data() {
		return {
			noteModel: "",
		};
	},
	computed: {
		...mapGetters({
			description: "getSingleNoteDescription",
			destination: "getDestination",
			contentCss: "getContentCss",
			noteDescription: "getSingleNoteDescription",
			noteId: "getSingleNoteId",
			rootUrl: "getRootUrl",
			skin: "getSkin",
		}),
	},
	watch: {
		noteDescription() {
			//Update local noteModel
			this.noteModel = this.noteDescription;
		},
	},
	methods: {
		useReopenCardInformation,
		closeModal() {
			//Close the current modal
			document.getElementById("editNoteCloseButton").click();

			//Open the card information modal, if it exists
			useReopenCardInformation();
		},
		updateNote() {
			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("object_note_id", `${this.noteId}`);
			data_to_send.set("object_note", this.noteModel);

			this.$store.dispatch("newToast", {
				header: "Updating Note",
				message: "Please wait - updating your note",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_note",
			});

			//If the destination is organisation, we have a different url due to permissions
			let url = `${this.rootUrl}note/update/${this.noteId}/`;
			if (this.destination === "organisation") {
				url = `${this.rootUrl}note/organisation/update/${this.noteId}/`;
			}

			this.axios.post(
				url,
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Note",
					message: "The note updated successfully.",
					extra_classes: "bg-success",
					unique_type: "save_note",
				});

				//Update the vueX
				this.$store.dispatch({
					type: "editSingleNote",
					noteId: this.noteId,
					noteDescription: this.noteModel,
				});

				//Close the modal
				document.getElementById("editNoteCloseButton").click();

				//Reshow the card information modal if exists
				useReopenCardInformation();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed Updating Note",
					message: `Failed to update note - Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "save_note",
				});
			});
		}
	},
};
</script>


