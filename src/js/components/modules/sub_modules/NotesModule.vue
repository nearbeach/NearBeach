<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.noteAdd"></Icon>
			Note History
		</h2>
		<p class="text-instructions">
			The following are saved notes against this {{ destination }}. Add
			notes by clicking on the button below.
		</p>

		<list-notes
			v-bind:destination="destination"
		></list-notes>

		<!-- ADD NOTE HISTORY -->
		<!-- TO DO - limit it to certain users -->
		<hr/>
		<div class="row submit-row">
			<div class="col-md-12">
				<button
					class="btn btn-primary save-changes"
					v-on:click="createNewNote"
					v-if="userLevel > 1"
				>
					Add Note to {{ destination }}
				</button>
			</div>
		</div>
	</div>
</template>

<script>
// JavaScript Libraries
import {Modal} from "bootstrap";
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import ListNotes from "./ListNotes.vue";
import NewHistoryNoteWizard from "../wizards/NewHistoryNoteWizard.vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NotesModule",
	components: {
		Icon,
		ListNotes,
		NewHistoryNoteWizard,
	},
	mixins: [iconMixin],
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
			const newNoteModal = new Modal(
				document.getElementById("newNoteModal")
			);
			newNoteModal.show();
		},
		getNoteHistoryResults() {
			//Depends if we are using note_list or organisation_note_list
			let note_list = "note_list";
			if (this.destination === "organisation") {
				note_list = "organisation_note_list";
			}

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/${note_list}/`,
			).then((response) => {
				// this.noteHistoryResults = response.data;
				this.$store.commit({
					type: "initNoteList",
					noteList: response.data,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Note History",
					message: `Can not retrieve the note history. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getNoteHistoryResults();
		});
	},
};
</script>

<style scoped></style>
