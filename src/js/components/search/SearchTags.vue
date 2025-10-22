<template xmlns:v-bind="http://www.w3.org/1999/xhtml">
	<div class="card">
		<div class="card-body">
			<h1>Search Tags</h1>
			<hr/>

			<div class="row">
				<div class="col-md-4">
					<strong>Tags</strong>
					<p class="text-instructions">
						Use the search bar to help you find any tags.
					</p>

					<p class="text-instructions">
						Click on the icon
						<carbon-information></carbon-information>
						to edit the tag.
					</p>

					<p class="text-instructions">
						To add in any new tags - please click on the "New Tag"
						button.
					</p>
				</div>

				<div class="col-md-8 tag-list">
					<div
						v-for="tag in localTagResults"
						:key="tag.pk"
						:style="`background-color: ${tag.fields.tag_colour};color: ${tag.fields.tag_text_colour}`"
						class="single-tag"
						@dblclick="editTag(tag.pk)"
					>
						{{ tag.fields.tag_name }}
						<span @click="editTag(tag.pk)">
							<carbon-information></carbon-information>
						</span>
					</div>
				</div>

				<!-- ADD NEW TAG BUTTON -->
				<hr v-if="userLevel >= 3"/>
				<div class="row submit-row">
					<div class="col-md-12">
						<a
							v-if="userLevel >= 3"
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							@click="addTag"
						>Add Tag</a
						>
					</div>
				</div>
			</div>

			<!-- MODALS -->
			<edit-tag-modal
				:existing-tags="localTagResults"
				:tag-colour="singleTagColour"
				:tag-id="singleTagId"
				:tag-name="singleTagName"
				:tag-text-colour="singleTagTextColour"
				@new_tag="newTag"
				@delete_tag="deleteTag($event)"
				@update_tags="updateTags"
			></edit-tag-modal>
		</div>
	</div>
</template>

<script>
//Imports
import {Modal} from "bootstrap";

//Components
import EditTagModal from "../tags/EditTagModal.vue";
import CarbonInformation from "Components/icons/CarbonInformation.vue";

export default {
	name: "SearchTags",
	components: {
		CarbonInformation,
		EditTagModal,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		tagResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			/*singleTag: {
				tagName: '',
				tagColour: '',
			},*/
			singleTagColour: "",
			singleTagId: 0,
			singleTagName: "#37cbd2",
			singleTagTextColour: "#ffffff",
			localTagResults: this.tagResults,
		};
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});
	},
	methods: {
		addTag() {
			//Send data down to the modal
			this.singleTagName = "default tag";
			this.singleTagId = 0;
			this.singleTagColour = "#37cbd2";
			this.singleTagTextColour = "#ffffff";

			//Open up modal
			const edit_tag_modal = new Modal(
				document.getElementById("editTagModal")
			);
			edit_tag_modal.show();
		},
		deleteTag(data) {
			//Filter out the tag
			this.localTagResults = this.localTagResults.filter((row) => {
				return row.pk !== data.tag_id;
			});
		},
		editTag(tag_id) {
			//Filter for the tag information
			const single_tag = this.localTagResults.filter((row) => {
				return row.pk === tag_id;
			})[0];

			//Send data down to the modal
			this.singleTagName = single_tag.fields.tag_name;
			this.singleTagId = tag_id;
			this.singleTagColour = single_tag.fields.tag_colour;
			this.singleTagTextColour = single_tag.fields.tag_text_colour;

			//Open up modal
			const edit_tag_modal = new Modal(
				document.getElementById("editTagModal")
			);
			edit_tag_modal.show();
		},
		newTag(data) {
			this.localTagResults.push(data[0]);
		},
		updateTags(data) {
			//Get the index location of the object we are updating
			const index = this.localTagResults.findIndex((row) => {
				return row.pk === data.tag_id;
			});

			// Update the data
			this.localTagResults[index].fields.tag_name = data.tag_name;
			this.localTagResults[index].fields.tag_colour = data.tag_colour;
			this.localTagResults[index].fields.tag_text_colour = data.tag_text_colour;
		},
	},
};
</script>
