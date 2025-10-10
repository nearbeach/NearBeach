<template>
	<div>
		<!-- NOTE HISTORY -->
		<div
			v-if="noteList.length === 0"
			class="module-spacer"
		>
			<div class="alert alert-dark">
				Sorry - but there are no notes for this {{ destination }}.
			</div>
		</div>
		<div
v-else
			 class="note-history"
		>
			<div
v-for="note in noteList"
				 :key="note.object_note_id"
				 class="note-history--row"
			>
				<div class="note-history--profile">
					<img
						:src="profilePicture(note.profile_picture)"
						alt="default profile"
						class="note-history--profile-picture"
					/>
					<div class="note-history--username">
						{{note.first_name}} {{note.last_name}}
					</div>
					<div class="note-history--date">
						{{useNiceDatetime(note.date_modified)}}
					</div>

					<div
v-if="note.can_edit === 'true'"
						 class="note-history--edit-button"
					>
						<button
type="button"
								class="btn btn-outline-secondary"
								@click="editNote(note.object_note_id)"
						>
							Edit Note
						</button>
						<button
type="button"
								class="btn btn-outline-danger"
								@click="deleteNote(note.object_note_id)"
						>
							Delete Note
						</button>
					</div>
				</div>
				<div class="note-history--note">
					<editor
						v-model="note.object_note"
						license-key="gpl"
						:init="{
						license_key: 'gpl',
						height: 250,
						menubar: false,
						plugins: ['lists', 'image', 'codesample', 'table'],
						toolbar: [],
						skin: `${skin}`,
						content_css: `${contentCss}`,
						relative_urls: false,
					}"
						:disabled="true"
					/>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import { Modal } from "bootstrap";

//VueX
import {mapGetters} from "vuex";

//Composables
import {useNiceDatetime} from "Composables/datetime/useNiceDatetime";

export default {
	name: "ListNotes",
	components: {
		editor: Editor,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			noteList: "getNoteList",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			skin: "getSkin",
		}),
	},
	methods: {
		useNiceDatetime,
		deleteNote(object_note_id) {
			//Tell VueX of the note id change
			this.$store.dispatch({
				type: "updateNoteId",
				noteId: object_note_id,
			});

			//Open the modal
			const modal = new Modal(document.getElementById("confirmNoteDeleteModal"));
			modal.show();

			if (this.destination === "card") {
				//Close the kanban card information
				const close_button = document.getElementById("cardInformationModalCloseButton");

				//Make sure the button exists
				if (close_button !== undefined) {
					close_button.click();
				}
			}
		},
		editNote(object_note_id) {
			//Tell VueX of the note id change
			this.$store.dispatch({
				type: "updateNoteId",
				noteId: object_note_id,
			});

			//Open the modal
			const modal = new Modal(document.getElementById("editNoteModal"));
			modal.show();

			if (this.destination === "card") {
				//Close the kanban card information
				const close_button = document.getElementById("cardInformationModalCloseButton");

				//Make sure the button exists
				if (close_button !== undefined) {
					close_button.click();
				}
			}
		},
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
	}
};
</script>


