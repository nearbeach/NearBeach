<template>
	<div
		class="modal fade"
		id="addTagModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Tags Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addTagsCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Add Tag</strong>
							<p class="text-instructions">
								Use the dropdown to select one or many lables to
								add to the {{ getDestination() }}.
							</p>
						</div>
						<div class="col-md-8">
							<label>All Tag List</label>
							<n-select
								label="tag"
								multiple
								:options="availableTagList"
								v-model:value="tagModel"
							></n-select>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="addTag"
					>
						Add Tag
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript extras
import {NSelect} from "naive-ui";
import {Modal} from "bootstrap";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "AddTagWizard",
	components: {
		NSelect,
	},
	props: {
		overrideDestination: {
			type: String,
			default: "",
		},
		overrideLocationId: {
			type: Number,
			default: 0,
		},
		reopenModal: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			tagModel: [],
		};
	},
	computed: {
		...mapGetters({
			allTagList: "getAllTagList",
			availableTagList: "getAvailableTagList",
			assignedTags: "getAssignedTags",
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addTag() {
			if (this.getLocationId() === 0) return;

			//Construct data_to_send
			const data_to_send = new FormData();

			//Loop through all the models results
			this.tagModel.forEach((row) => {
				data_to_send.append("tag_id", row);
			});

			//Use Axios to send data to backend
			this.axios.post(
				`${this.rootUrl}object_data/${this.getDestination()}/${this.getLocationId()}/add_tags/`,
				data_to_send
			).then((response) => {
				//Emit data up
				this.$store.commit({
					type: "updateAssignedTags",
					assignedTags: response.data,
				});

				//Close the modal
				document.getElementById("addTagsCloseButton").click();

				//Clear the results
				this.tagModel = [];

				//If there is anything in reopenModal, we reopen that modal
				if (this.reopenModal !== "") {
					const modal = new Modal(
						document.getElementById(this.reopenModal)
					);
					modal.show();
				}

				//Check to see if we have added a tag to a kanban card - if so, update that kanban card
				if (this.getDestination() === "kanban_card") {
					//Update the kanban card's tags
					this.$store.commit({
						type: "updateKanbanCard",
						card_id: this.getLocationId(),
						tag_list: response.data,
					});
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to add tag",
					message: `Sorry, we could not add tag. Errors -> ${error}`,
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
		getTagList() {
			this.axios.post(
				`${this.rootUrl}object_data/tag_list_all/`
			).then((response) => {
				//Map data to the preferred data format for vue-select
				this.$store.commit({
					type: "updateAllTagList",
					allTagList: response.data,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get tag list",
					message: `Sorry, we could not get the tag list. Errors -> ${error}`,
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

		this.$nextTick(() => {
			//Get the tag list
			this.getTagList();
		});
	},
};
</script>


