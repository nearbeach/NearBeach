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
			class="modal-dialog modal-lg"
			role="document"
		>
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.noteAdd"></Icon>
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
						:init="{
							height: 300,
							menubar: false,
							plugins: ['lists', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 				 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            				skin: `${this.skin}`,
			            	content_css: `${this.contentCss}`
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
import errorModalMixin from "../../../mixins/errorModalMixin";
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewHistoryNoteWizard",
	components: {
		editor: Editor,
		Icon,
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
	mixins: [errorModalMixin, iconMixin],
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
			//Construct the form data to send
			const data_to_send = new FormData();
			data_to_send.set("destination", this.destination);
			data_to_send.set("location_id", this.locationId);
			data_to_send.set("note", this.newNoteModel);

			//Add the data to data_to_send
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_notes/`,
					data_to_send
				)
				.then((response) => {
					//Submit the note up
					this.$emit(
						"update_note_history_results",
						response.data
					);

					//Close the modal
					document.getElementById("newNoteCloseButton").click();

					//Clear the notes
					this.newNoteModel = "";
				})
				.catch((error) => {
					this.showErrorModal(error, this.destination);
				});
		},
	},
};
</script>

<style scoped></style>
