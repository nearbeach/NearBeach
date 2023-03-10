<template>
	<div>
		<h2><Icon v-bind:icon="icons.noteAdd"></Icon> Note History</h2>
		<p class="text-instructions">
			The following are saved notes against this {{ destination }}. Add
			notes by clicking on the button below.
		</p>

		<list-notes
			v-bind:note-history-results="noteHistoryResults"
			v-bind:destination="destination"
		></list-notes>

		<!-- ADD NOTE HISTORY -->
		<!-- TO DO - limit it to certain users -->
		<hr />
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="createNewNote"
					v-if="userLevel > 1"
					>Add Note to {{ destination }}</a
				>
			</div>
		</div>

		<!-- Modals for Notes section -->
		<new-history-note-wizard
			v-bind:location-id="locationId"
			v-bind:destination="destination"
			v-on:update_note_history_results="updateNoteHistoryResults($event)"
		></new-history-note-wizard>
	</div>
</template>

<script>
	// JavaScript Libraries
	import { Modal } from "bootstrap";
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";
	import axios from "axios";
	import { Icon } from "@iconify/vue";
	import ListNotes from "./ListNotes.vue";
	import NewHistoryNoteWizard from "../wizards/NewHistoryNoteWizard.vue";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "NotesModule",
		components: {
			Icon,
			ListNotes,
			NewHistoryNoteWizard,
		},
		mixins: [errorModalMixin, iconMixin],
		data() {
			return {
				noteHistoryResults: [],
			};
		},
		computed: {
			...mapGetters({
				destination: "getDestination",
				locationId: "getLocationId",
				userLevel: "getUserLevel",
				rootUrl: "getRootUrl",
			}),
		},
		methods: {
			createNewNote() {
				var newNoteModal = new Modal(
					document.getElementById("newNoteModal")
				);
				newNoteModal.show();
			},
			getNoteHistoryResults() {
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/note_list/`
					)
					.then((response) => {
						this.noteHistoryResults = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			updateNoteHistoryResults(data) {
				//Add the extra data
				this.noteHistoryResults.push(data[0]);
			},
		},
		mounted() {
			setTimeout(() => {
				this.getNoteHistoryResults();
			}, 200);
		},
	};
</script>

<style scoped></style>
