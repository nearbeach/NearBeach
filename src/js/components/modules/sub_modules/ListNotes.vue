<template>
	<div>
		<!-- NOTE HISTORY -->
		<div
			v-if="noteHistoryResults.length === 0"
			class="module-spacer"
		>
			<div class="alert alert-dark">
				Sorry - but there are no notes for this {{ destination }}.
			</div>
		</div>
		<div class="note-history"
			 v-else
		>
			<div class="note-history--row"
				 v-for="note in noteHistoryResults"
				 v-bind:key="note.object_note_id"
			>
				<div class="note-history--profile">
					<img
						v-bind:src="profilePicture(note.profile_picture)"
						alt="default profile"
						class="note-history--profile-picture"
					/>
					<div class="text-instruction">
						{{note.first_name}} {{note.last_name}}
					</div>
					<div class="text-instruction">
						{{getNiceDate(note.date_modified)}}
					</div>
				</div>
				<div class="note-history--note">
					<editor
						:init="{
						height: 250,
						menubar: false,
						plugins: ['lists', 'image', 'codesample', 'table'],
						toolbar: [],
						skin: `${this.skin}`,
						content_css: `${this.contentCss}`,
					}"
						v-model="note.object_note"
						v-bind:disabled="true"
					/>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

//Mixins
import datetimeMixin from "../../../mixins/datetimeMixin";


export default {
	name: "ListNotes",
	components: {
		editor: Editor,
	},
	mixins: [datetimeMixin],
	props: {
		destination: {
			type: String,
			default: "",
		},
		noteHistoryResults: {
			type: Array,
			default() {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			skin: "getSkin",
		}),
	},
	methods: {
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
	}
};
</script>

<style scoped></style>
