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
							<label>Tag Name</label>
							<input
								class="form-control"
								v-model="tagNameModel"
							/>
						</div>
					</div>
					<hr />

					<div class="row">
						<div class="col-md-4">
							<strong>Pick Colour</strong>
							<p class="text-instructions">
								Please click on a preferred colour. This will be
								tags colour.
							</p>
						</div>
						<div class="colour-picker col-md-8">
							<div
								v-for="colour in colourList"
								v-bind:key="colour"
								v-bind:class="getClasses(colour)"
								v-bind:style="`background-color: ${colour};`"
								v-on:click="updateColour(colour)"
							></div>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-danger delete-tag"
						v-on:click="deleteTag"
						v-if="tagId !== 0"
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
					>
						Save Tag
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "EditTagModal",
		props: {
			existingTags: {
				type: Array,
				default: () => {
					return [];
				},
			},
			tagColour: {
				type: String,
				default: "/",
			},
			tagId: {
				type: Number,
				default: 0,
			},
			tagName: {
				type: String,
				default: "",
			},
		},
		data() {
			return {
				colourList: [
					"#37cbd2",
					"#8b8295",
					"#6f84bb",
					"#1fc4b5",
					"#651794",
					"#7ea52c",
					"#6df79e",
					"#53ef5f",
					"#79c121",
					"#91fbde",
					"#e01059",
					"#33ae24",
				],
				tagColourModel: this.tagColour,
				tagNameModel: this.tagName,
			};
		},
		watch: {
			tagColour: function () {
				this.tagColourModel = this.tagColour;
			},
			tagName: function () {
				this.tagNameModel = this.tagName;
			},
		},
		computed: {
			...mapGetters({
				rootUrl: "getRootUrl",
			}),
			canSave: function () {
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
			deleteTag: function () {
				//Use axios to send the request
				axios
					.post(`${this.rootUrl}tag/delete/${this.tagId}/`)
					.then((response) => {
						//Tell the component up stream that we removed this tag
						this.$emit("delete_tag", {
							tag_id: this.tagId,
						});

						//Close the modal
						document.getElementById("editTagCloseModal").click();
					})
					.catch((error) => {});
			},
			getClasses: function (colour) {
				let return_class = "single-colour";

				if (colour == this.tagColourModel) {
					return_class = return_class + " selected-colour";
				}

				return return_class;
			},
			newTag: function (data_to_send) {
				//Use axios to send data
				axios
					.post(`${this.rootUrl}tag/new/`, data_to_send)
					.then((response) => {
						// Send data upstream
						this.$emit("new_tag", response.data);

						//Close the modal
						document.getElementById("editTagCloseModal").click();
					})
					.catch((error) => {
						//ADD CODE
					});
			},
			saveTag: function () {
				//Create data to send
				const data_to_send = new FormData();
				data_to_send.set("tag_id", this.tagId);
				data_to_send.set("tag_name", this.tagNameModel);
				data_to_send.set("tag_colour", this.tagColourModel);

				if (this.tagId === 0) {
					//CREATE A NEW TAG
					this.newTag(data_to_send);
				} else {
					//Save existing tag
					this.updateTag(data_to_send);
				}
			},
			updateColour: function (selected_colour) {
				this.tagColourModel = selected_colour;
			},
			updateTag: function (data_to_send) {
				//Use axios to send data
				axios
					.post(`${this.rootUrl}tag/save/`, data_to_send)
					.then((response) => {
						// Send data upstream
						this.$emit("update_tags", {
							tag_id: this.tagId,
							tag_name: this.tagNameModel,
							tag_colour: this.tagColourModel,
						});

						//Close the modal
						document.getElementById("editTagCloseModal").click();
					})
					.catch((error) => {
						//ADD CODE
					});
			},
		},
	};
</script>
