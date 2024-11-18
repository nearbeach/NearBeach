<template>
	<div
		class="modal fade"
		id="addKanbanCardModal"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		tabindex="-1"
		aria-labelledby="addKanbanCardModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-xl-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Kanban Card Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addKanbanCardCloseButton"
					></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Please note</strong>
							<p class="text-instructions">
								The card names can not be the same as something
								that already exists on the board.
							</p>
						</div>
						<div class="col-md-8">
							<label>
                                Kanban Card Text
                                <span
                                    v-if="disableAddButton"
                                    class="error"
                                >
                                    Please supply a unique card name
                                </span>
                            </label>
							<input
								id="kanbanCardText"
								v-model="kanbanCardTextModel"
								v-on:keydown.enter="addKanbanCard"
								class="form-control"
							/>
						</div>
					</div>
					<hr />

					<!-- CARD PRIORITY -->
					<div class="row">
						<div class="col-md-4">
							<strong>Card Priority</strong>
							<p class="text-instructions">
								Please select the apprioriate card priority.
							</p>
						</div>
						<div class="col-md-8">
							<label>Card Priority</label>
							<n-select
								v-bind:options="listPriority"
								v-model:value="kanbanCardPriorityModal"
							></n-select>
						</div>
					</div>
					<hr />

					<!-- CARD DESCRIPTION -->
					<div class="row">
						<div class="col-md-4">
							<strong>Card Description</strong>
							<p class="text-instructions">
								Fill out a detailed description for the card,
								then click on the "Update Card" button to update
								the card.
							</p>
						</div>
						<div class="col-md-8">
							<editor
								license-key="gpl"
								:init="{
									license_key: 'gpl',
									file_picker_types: 'image',
									height: 300,
									images_upload_handler: useUploadImage,
									menubar: false,
									paste_data_images: true,
									plugins: ['lists', 'image', 'codesample', 'table'],
            						toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
											 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            						skin: `${this.skin}`,
						            content_css: `${this.contentCss}`,
						            relative_urls: false,
								}"
								v-model="kanbanCardDescriptionModel"
							/>
						</div>
					</div>

					<!-- CARD LOCATION -->
					<hr
						v-if="newCardLocation.userCanSelectLocation"
					/>
					<div class="row"
						 v-if="newCardLocation.userCanSelectLocation"
					>
						<div class="col-md-4">
							<strong>Card Location</strong>
							<p class="text-instructions">
								Select the appropriate location for this card.
							</p>
						</div>

						<div class="col-md-8">
							<div class="row">
								<div class="col-md-6 mt-4">
									<label>Card Column</label>
									<n-select
										v-bind:options="listColumns"
										label="column"
										v-model:value="localColumnId"
									></n-select>
								</div>

								<div class="col-md-6 mt-4">
									<label>Card Level</label>
									<n-select
										v-bind:options="listLevels"
										label="level"
										v-model:value="localLevelId"
									></n-select>
								</div>
							</div>
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
						v-on:click="addKanbanCard"
						v-bind:disabled="disableAddButton"
					>
						Add Card
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

import {useUploadImage} from "../../../composables/uploads/useUploadImage";

export default {
	name: "NewKanbanCard",
	components: {
		editor: Editor,
		NSelect,
	},
	emits: [
		'new_card',
	],
	props: {
		columnResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		levelResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		kanbanBoardResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			disableAddButton: true,
			kanbanCardDescriptionModel: "",
			kanbanCardTextModel: "",
			kanbanCardPriorityModal: 2,
			listPriority: [
				{
					label: "Highest",
					value: 0,
				},
				{
					label: "High",
					value: 1,
				},
				{
					label: "Normal",
					value: 2,
				},
				{
					label: "Low",
					value: 3,
				},
				{
					label: "Lowest",
					value: 4,
				},
			],
			localColumnId: 0,
			localLevelId: 0,
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			kanbanCardResults: "getKanbanCardResults",
			listColumns: "getListColumns",
			listLevels: "getListLevels",
			newCardLocation: "getNewCardLocation",
			rootUrl: "getRootUrl",
			skin: "getSkin",
		}),
	},
	methods: {
		useUploadImage,
		addKanbanCard() {
			//Disable the save
			this.disableAddButton = true;

			this.$store.dispatch("newToast", {
				header: "Creating new card",
				message: "Please wait as we create the new card",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "new_card",
			});

			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("kanban_card_text", this.kanbanCardTextModel);
			data_to_send.set(
				"kanban_card_description",
				this.kanbanCardDescriptionModel
			);
			data_to_send.set(
				"kanban_level",
				this.localLevelId,
			);
			data_to_send.set(
				"kanban_column",
				this.localColumnId,
			);
			data_to_send.set(
				"kanban_card_priority",
				this.kanbanCardPriorityModal
			)

			//Send the data
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.kanbanBoardResults[0].pk}/new_card/`,
				data_to_send
			).then((response) => {
				//Get the first value from the response
				const new_card = response.data[0];
				new_card.tag_list = [];

				//Emit the data upstream
				this.$emit("new_card", new_card);

				//Blank the model
				this.kanbanCardTextModel = "";
				this.kanbanCardDescriptionModel = "";

				//Close the modal
				document.getElementById("addKanbanCardCloseButton").click();

				this.$store.dispatch("newToast", {
					header: "Card created successfully",
					message: "Card created successfully",
					extra_classes: "bg-success",
					unique_type: "new_card",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error creating card",
					message: `Error creating card: Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "new_card",
				});
			});
		},
	},
	watch: {
		kanbanCardTextModel() {
			// If the model is blank OR the text already exists - turn disableAddButton to true
			this.disableAddButton = false; //People can click the "Add" button

			if (this.kanbanCardTextModel.length === 0) {
				this.disableAddButton = true;
			}

			//Check to make sure it does not exist
			const filtered_results = this.kanbanCardResults.filter((row) => {
				return (
					row.kanban_card_text === this.kanbanCardTextModel
				);
			});

			if (filtered_results.length > 0) {
				this.disableAddButton = true;
			}

			//If there are no rows or levels - we don't want the user to submit a card
			if (
				this.columnResults.length === 0 ||
				this.levelResults.length === 0
			) {
				this.disableAddButton = true;
			}
		},
		newCardLocation: {
			handler(new_value) {
				this.localColumnId = new_value.columnId;
				this.localLevelId = new_value.levelId;
			},
			deep: true,
			immediate: true,
		},
	},
};
</script>


