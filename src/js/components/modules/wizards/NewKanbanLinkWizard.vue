<template>
	<div
		class="modal fade"
		id="newLinkModal"
		tabindex="-1"
		aria-labelledby="kanbanLinkModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						New Kanban Link Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="requirementLinkCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<!-- CHOOSING A OBJECT TYPE -->
					<div class="row">
						<div class="col-md-4">
							<strong>Object Selector</strong>
							<p class="text-instructions">
								Please select which object you would like to
								link to this requirement.
							</p>
						</div>
						<div class="col-md-8">
							<n-select
								:options="objectSelection"
								v-model:value="objectModel"
								class="object-selection"
								v-if="!isSearching"
							></n-select>
							<div
								v-else
								class="alert alert-success"
							>
								Searching for {{ objectModel }}s
							</div>
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


					<!-- SELECTING WHICH OBJECTS TO LINK TO -->
					<hr/>
					<div class="row">
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the objects you want to
								connect to this requirement.
							</p>
						</div>
						<div class="col-md-8">
							<div
								v-if="
									objectResults.length === 0 &&
									objectModel != null
								"
								class="alert alert-warning"
							>
								Sorry - there are no results.
							</div>

							<!-- SEARCH RESULTS -->
							<div
								class="form-group"
								v-if="
									!isSearching &&
									objectResults.length > 0 &&
									objectModel != null
								"
							>
								<label>Search Terms</label>
								<input
									id="search_terms"
									class="form-control"
									v-model="searchModel"
									type="text"
								/>
							</div>
							<br/>

							<!-- ADD CODE -->
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
						v-bind:disabled="linkModel.length === 0"
						v-on:click="saveLinks"
					>
						Save changes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";


//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewKanbanLinkWizard",
	components: {
		NSelect,
	},
	emits: ['new_card'],
	props: {
		locationId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			listColumns: "getListColumns",
			listLevels: "getListLevels",
			newCardLocation: "getNewCardLocation",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	data() {
		return {
			currentPage: 1,
			isSearching: false,
			linkModel: [],
			localColumnId: 0,
			localLevelId: 0,
			objectModel: null,
			objectFilteredResults: [],
			objectResults: [],
			objectSelection: [
				{
					value: "Project",
					label: "Project",
				},
				{
					value: "Requirement",
					label: "Requirement",
				},
				{
					value: "Task",
					label: "Task",
				},
			],
			searchModel: "",
			searchTimeout: "",
		};
	},
	methods: {
		changePage(index) {
			this.currentPage = index;
			this.getObjects();
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
		getObjects() {
			//Clear data
			this.linkModel = [];

			//User has chosen an object.
			if (this.objectModel === null) {
				//Ok - then removed the objects. We don't need to do anything
				this.isSearching = false;
				return;
			}

			const data_to_send = new FormData();
			data_to_send.append("array_of_objects", this.objectModel.toLowerCase());
			data_to_send.set("destination_page", this.currentPage);
			data_to_send.set("exclude_destination", "kanban_board");
			data_to_send.set("exclude_location_id", this.locationId);
			data_to_send.set("search", this.searchModel);

			//Tell the form that we are searching
			this.isSearching = true;

			//Now to use axios to get the data we require
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel}/link_list/`,
				data_to_send
			).then((response) => {
				//Load the data into the array
				this.objectResults = response.data;
				this.objectFilteredResults = response.data;

				//Tell the user we are no longer searching
				this.isSearching = false;

				//Clear out search term model
				this.searchTermModel = "";
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Link List",
					message: `We had an issue getting Link List. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		saveLinks() {
			// Set up the data object to send
			const data_to_send = new FormData();

			//Depending on what the object model is - depends what is sent
			data_to_send.set(
				`${this.objectModel.toLowerCase()}`,
				this.linkModel
			);
			data_to_send.set(
				"kanban_level",
				this.localLevelId,
			);
			data_to_send.set(
				"kanban_column",
				this.localColumnId,
			);

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel.toLowerCase()}/add_link/`,
				data_to_send
			).then((response) => {
				//Get the response data
				const new_link = response.data[0];
				new_link.tag_list = [];

				//Data has been successfully saved. Time to add the card to the board
				this.$emit("new_card", new_link);

				//Clear the object model
				this.objectModel = null;

				//Click on the close button - a hack, but it should close the modal
				document.getElementById("requirementLinkCloseButton").click();
			});
		},
	},
	watch: {
		newCardLocation: {
			handler(new_value) {
				this.localColumnId = new_value.columnId;
				this.localLevelId = new_value.levelId;
			},
			deep: true,
			immediate: true,
		},
		objectModel() {
			this.currentPage = 1;
			this.getObjects();
		},
		searchModel() {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Only search if there are either 0 character or more than 3
			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				this.searchTimeout = setTimeout(() => {
					//Use change page, as we should change the page back to destination page 1
					this.changePage(1);
				}, 500);
			}
		}
	},
};
</script>


