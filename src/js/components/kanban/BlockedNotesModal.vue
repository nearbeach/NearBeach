<template>
	<div
		class="modal fade"
		id="blockedNotesModal"
		tabindex="-1"
		aria-labelledby="blockedNotesModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>Blocked Card Notes</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="blockedNotesModalButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Blocked Card Notes</strong>
							<p class="text-instructions">
								Please write a reason why this particular card
								is blocked at the moment.
							</p>
						</div>
						<div class="col-md-8">
							<editor
								license-key="gpl"
								:init="{
									license_key: 'gpl',
									file_picker_types: 'image',
									height: 250,
									menubar: false,
									plugins: ['lists', 'image', 'codesample', 'table'],
            						toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 						 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            						skin: `${this.skin}`,
						            content_css: `${this.contentCss}`,
						            relative_urls: false,
								}"
								v-model="noteModal"
							/>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						Close
					</button>
					<button
						class="btn btn-primary save-changes"
						v-on:click="addNote"
						v-bind:disabled="noteModal === ''"
					>
						Add Note
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "BlockedNotesModal",
	components: {
		editor: Editor,
	},
	props: {},
	data() {
		return {
			noteModal: "",
		};
	},
	computed: {
		...mapGetters({
			cardId: "getCardId",
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
		}),
	},
	methods: {
		addNote() {
			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("note", this.noteModal);

			//Use axios to send the data
			this.axios
				.post(
					`${this.rootUrl}object_data/kanban_card/${this.cardId}/add_notes/`,
					data_to_send
				)
				.then(() => {
					this.closeModal();
				});
		},
		closeModal() {
			//Clear the data
			this.noteModal = "";

			//Close the modal
			document.getElementById("blockedNotesModalButton").click();
		},
	},
};
</script>


