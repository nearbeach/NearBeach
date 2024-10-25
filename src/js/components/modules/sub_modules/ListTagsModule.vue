<template>
	<div>
		<h2>Assigned Tags</h2>
		<p class="text-instructions">
			Here are all tags associated with this {{ getDestination() }}. You can
			add more tags by clicking on the "Add Tag" button.
		</p>
		<div class="tag-list">
			<div
				v-for="tag in assignedTags"
				:key="tag.tag_id"
				class="single-tag"
				v-bind:style="`background-color: ${tag.tag_colour};color: ${tag.tag_text_colour};`"
			>
				{{ tag.tag_name }}
				<span
					v-on:click="removeTag(tag.tag_id)"
				>
					<Icon v-bind:icon="icons.xCircle"
						  v-if="userLevel > 1"
					></Icon>
				</span>
			</div>
		</div>

		<!-- ADD TAG BUTTON -->
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="openNewTagModal"
					v-if="userLevel > 1"
				>Add Tag to {{ getDestination() }}</a
				>
			</div>
		</div>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

//Mixin
import iconMixin from "../../../mixins/iconMixin";
import AddTagWizard from "../wizards/AddTagWizard.vue";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "ListTagsModule",
	components: {
		AddTagWizard,
		Icon,
	},
	props: {
		closeModalBefore: {
			type: String,
			default: "",
		},
		overrideDestination: {
			type: String,
			default: "",
		},
		overrideLocationId: {
			type: Number,
			default: 0,
		},
	},
	watch: {
		overrideLocationId() {
			this.getAssignedTags();
		}
	},
	mixins: [iconMixin],
	computed: {
		...mapGetters({
			assignedTags: "getAssignedTags",
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		getAssignedTags() {
			if (this.getLocationId() === 0) return;
			
			this.axios.post(
				`${this.rootUrl}object_data/${this.getDestination()}/${this.getLocationId()}/tag_list/`
			).then((response) => {
				this.$store.commit({
					type: "updateAssignedTags",
					assignedTags: response.data,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Assigned Tags",
					message: `Error getting assigned tags. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
		openNewTagModal() {
			//Close any modals that exist
			if (this.closeModalBefore !== "") {
				//Click on the close button :)
				document.getElementById(this.closeModalBefore).click();
			}

			//Open up modal
			const newTagModal = new Modal(
				document.getElementById("addTagModal")
			);
			newTagModal.show();
		},
		removeTag(tag_id) {
			//If user does not have enough permissions, don't let them proceed.
			if (this.userLevel <= 1) return;

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("tag", tag_id);
			data_to_send.set("object_enum", this.getDestination());
			data_to_send.set("object_id", this.getLocationId());

			//Send data using axios
			this.axios.post(
				`${this.rootUrl}object_data/delete_tag/`,
				data_to_send
			).then(() => {
				//Remove data from tagList
				this.$store.dispatch("removeAssignedTag", {
					tag_id: tag_id,
				});

				//If destination is a kanban card, we update the card's tag list
				if (this.getDestination() === "kanban_card") {
					this.$store.commit({
						type: "updateKanbanCard",
						card_id: this.getLocationId(),
						tag_list: this.assignedTags,
					});
				}
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Error Removing Tag",
					message: `Sorry, we could not remove the tag. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (escape_array.indexOf(this.getDestination()) >= 0) return;

		//Wait 200ms before getting the data
		this.$nextTick(() => {
			this.getAssignedTags();
		});
	},
};
</script>
