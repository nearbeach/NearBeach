<template>
	<div>
		<div
			class="row"
			v-if="userLevel > 1"
		>
			<div class="col-md-4">
				<strong>Notes</strong>
				<p class="text-instructions">
					To add a note - type your note in the Note Box and hit the
					"Submit Note" button.
				</p>
			</div>
			<div class="col-md-8">
				<label>Note Box</label>
				<editor
					license-key="gpl"
					:init="{
						license_key: 'gpl',
						height: 250,
						menubar: false,
						plugins: ['lists', 'codesample', 'table'],
            			toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 			 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            			skin: `${this.skin}`,
			            content_css: `${this.contentCss}`,
			            relative_urls: false,
					}"
					v-model="cardNoteModel"
					v-bind:disabled="kanbanStatus === 'Closed'"
				/>
			</div>
		</div>
		<hr v-if="userLevel > 1"/>
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
					class="btn btn-primary save-changes"
					v-on:click="addNote"
					v-bind:disabled="cardNoteModel === ''"
				>
					Add Note
				</button>
			</div>
		</div>
		<hr v-if="userLevel > 1"/>

		<!-- NOTE HISTORY -->
		<list-notes
			v-bind:note-history-results="cardNotes"
			destination="card"
		></list-notes>
	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import ListNotes from "../modules/sub_modules/ListNotes.vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "CardNotes",
	components: {
		editor: Editor,
		ListNotes,
	},
	props: {},
	data() {
		return {
			cardNoteModel: "",
		};
	},
	computed: {
		...mapGetters({
			cardNotes: "getCardNotes",
			contentCss: "getContentCss",
			kanbanStatus: "getKanbanStatus",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		addNote() {
			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("note", this.cardNoteModel);

			this.$store.dispatch("newToast", {
				header: "Adding Note",
				message: "Currently adding note to object",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "adding_note",
			});

			//Use axios to send the data
			this.axios.post(
				`${this.rootUrl}object_data/kanban_card/${this.$store.state.card.cardId}/add_notes/`,
				data_to_send
			).then((response) => {
				//Add the response to the end of the noteHistoryResults
				this.$store.commit({
					type: "addNote",
					newNote: response.data[0],
				});

				//Clear the card note model
				this.cardNoteModel = "";

				this.$store.dispatch("newToast", {
					header: "Successfully Added Note",
					message: "Successfully Added Note to Object",
					extra_classes: "bg-success",
					unique_type: "adding_note",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can't add Note",
					message: `Sorry, we could not add a note for you. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "adding_note",
				});
			});
		},
		closeModal() {
			document
				.getElementById("cardInformationModalCloseButton")
				.click();
		},
	},
};
</script>
