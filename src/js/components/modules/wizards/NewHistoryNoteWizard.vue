<template>
	<!-- NEW HISTORY NOTE -->
	<div
		class="modal fade"
		id="newNoteModal"
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
						New Note
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="newNoteCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<p class="text-instructions">
						Use the text editor to type out your note. Click on the
						submit button to submit the note.
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
						v-model="newNoteModel"
					/>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-primary"
						v-bind:disabled="newNoteModel == ''"
						v-on:click="submitNote"
					>
						Submit Note
					</button>
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
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

export default {
	name: "NewHistoryNoteWizard",
	components: {
		editor: Editor,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			newNoteModel: "",
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
		}),
	},
	methods: {
		submitNote() {
			//Notify user of submitting note
			this.$store.dispatch("newToast", {
				header: "Submitting new note",
				message: "Please wait. Submitting new note",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "submit_note",
			});

			//Construct the form data to send
			const data_to_send = new FormData();
			data_to_send.set("destination", this.destination);
			data_to_send.set("location_id", `${this.locationId}`);
			data_to_send.set("note", this.newNoteModel);

			//If the destination is organisation, we have a different url due to permissions
			let add_notes = "add_notes";
			if (this.destination === "organisation") {
				add_notes = "organisation_add_notes";
			}

			//Add the data to data_to_send
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/${add_notes}/`,
				data_to_send
			).then((response) => {
				//Notify user of success
				this.$store.dispatch("newToast", {
					header: "New Note Submitted",
					message: "The new note submitted successfully.",
					extra_classes: "bg-success",
					unique_type: "submit_note",
				});

				//Use VueX to add the note to the note list
				this.$store.commit({
					type: "addNote",
					newNote: response.data[0],
				});

				//Clear the notes
				this.newNoteModel = "";

				//Close the modal
				document.getElementById("newNoteCloseButton").click();

			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Submitting Note",
					message: `Sorry, the note did not submit. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "submit_note",
				});
			});
		},
	},
};
</script>


