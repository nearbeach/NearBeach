<template>
	<div
		class="modal fade"
		id="editTagModal"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="editTagModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="editTagModalLabel"
					>
						Edit Tag
					</h5>
					<button
						type="button"
						id="editTagCloseModal"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Edit Tags</strong>
							<p class="text-instructions">
								Please give the tag an appropriate name. Please
								do not pick an existing tag name.
							</p>
						</div>
						<div class="col-md-8">
							<label>
                                Tag Name
                                <span
                                    v-if="!canSave"
                                    class="error"
                                >
                                    Please use a unique name
                                </span>
                            </label>
							<input
								class="form-control"
								v-bind:disabled="userLevel <= 1"
								v-model="tagNameModel"
							/>
						</div>
					</div>
					<hr/>

					<div class="row">
						<div class="col-md-4">
							<strong>Pick Colour</strong>
							<p class="text-instructions">
								Please choose a background and text colour for your tag.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label>Background Colour</label>
								<n-color-picker :show-alpha="false"
												v-bind:disabled="userLevel <= 1"
												v-model:value="tagColourModel"
												:modes="['hex']"
								></n-color-picker>
							</div>

							<div class="form-group">
								<label>Text Colour</label>

								<n-color-picker v-model:value="tagTextColourModel"
												v-bind:disabled="userLevel <= 1"
												:show-alpha="false"
												:modes="['hex']"
								/>
      							<span>{{ tagTextColourModel }}</span>
							</div>

							<hr>

							<div class="single-tag"
								 v-bind:style="`margin-right:0;background-color:${tagColourModel};color:${tagTextColourModel};`"
							>
								{{ tagNameModel }}
							</div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-danger delete-tag"
						v-on:click="deleteTag"
						v-if="tagId !== 0 && userLevel > 1"
					>
						Delete Tag
					</button>

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
						v-bind:disabled="!canSave"
						v-on:click="saveTag"
						v-if="userLevel > 1"
					>
						Save Tag
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

//Naive UI
import {NColorPicker} from "naive-ui";


export default {
	name: "EditTagModal",
	components: {
		NColorPicker,
	},
	emits: [
		'update_tags',
		'new_tag',
		'delete_tag',
	],
	props: {
		existingTags: {
			type: Array,
			default: () => {
				return [];
			},
		},
		tagColour: {
			type: String,
			default: "",
		},
		tagId: {
			type: Number,
			default: 0,
		},
		tagName: {
			type: String,
			default: "",
		},
		tagTextColour: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			tagColourModel: this.tagColour,
			tagNameModel: this.tagName,
			tagTextColourModel: this.tagTextColour,
		};
	},
	watch: {
		tagColour() {
			this.tagColourModel = this.tagColour;
		},
		tagName() {
			this.tagNameModel = this.tagName;
		},
		tagTextColour() {
			this.tagTextColourModel = this.tagTextColour;
		}
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		}),
		canSave() {
			//Return false if user has written a duplicate tag name
			const count = this.existingTags.filter((row) => {
				const tag_name_1 = row.fields.tag_name.toUpperCase(),
					tag_name_2 = this.tagNameModel.toUpperCase();

				//Return if the tag names are the same WHILST NOT being the same tag ID
				return tag_name_1 === tag_name_2 && row.pk !== this.tagId;
			}).length;

			//Return true if there is no duplicate
			return count === 0;
		},
	},
	methods: {
		deleteTag() {
			//Use axios to send the request
			this.axios.post(
				`${this.rootUrl}tag/delete/${this.tagId}/`
			).then(() => {
				//Tell the component up stream that we removed this tag
				this.$emit("delete_tag", {
					tag_id: this.tagId,
				});

				//Close the modal
				document.getElementById("editTagCloseModal").click();
			}).catch((error) => {
				this.$store.dispatch("newToast",{
					header: "Error deleting tag",
					message: `Sorry we could not delete your tag. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getClasses(colour) {
			let return_class = "single-colour";

			if (colour === this.tagColourModel) {
				return_class = `${return_class} selected-colour`;
			}

			return return_class;
		},
		newTag(data_to_send) {
			//Tell user of saving tag
			this.$store.dispatch("newToast", {
				header: "New Tag",
				message: "Creating new Tag - please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_tag",
			});

			//Use axios to send data
			this.axios.post(
				`${this.rootUrl}tag/new/`,
				data_to_send
			).then((response) => {
				this.$store.dispatch("newToast", {
					header: "Tag Saved",
					message: "Tag has been successfully saved",
					extra_classes: "bg-success",
					unique_type: "save_tag",
				});

				// Send data upstream
				this.$emit("new_tag", response.data);

				//Close the modal
				document.getElementById("editTagCloseModal").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not create new tag",
					message: `Sorry, we could not create your new tag. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		saveTag() {
			//Create data to send
			const data_to_send = new FormData();
			data_to_send.set("tag_id", this.tagId);
			data_to_send.set("tag_name", this.tagNameModel);
			data_to_send.set("tag_colour", this.tagColourModel);
			data_to_send.set("tag_text_colour", this.tagTextColourModel);

			if (this.tagId === 0) {
				//CREATE A NEW TAG
				this.newTag(data_to_send);
			} else {
				//Save existing tag
				this.updateTag(data_to_send);
			}
		},
		updateColour(selected_colour) {
			this.tagColourModel = selected_colour;
		},
		updateTag(data_to_send) {
			//Tell user of saving tag
			this.$store.dispatch("newToast", {
				header: "Updating Tag",
				message: "Updating Tag - please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_tag",
			});

			//Use axios to send data
			this.axios.post(
				`${this.rootUrl}tag/save/`,
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Tag Updated",
					message: "Tag has been updated successfully",
					extra_classes: "bg-success",
					unique_type: "save_tag",
				});

				// Send data upstream
				this.$emit("update_tags", {
					tag_id: this.tagId,
					tag_name: this.tagNameModel,
					tag_colour: this.tagColourModel,
					tag_text_colour: this.tagTextColourModel,
				});

				//Close the modal
				document.getElementById("editTagCloseModal").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not update tag",
					message: `Sorry, we could not update your tag. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>
