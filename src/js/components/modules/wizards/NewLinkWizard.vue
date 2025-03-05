<template>
	<div
		class="modal fade"
		id="newLinkModal"
		tabindex="-1"
		aria-labelledby="linkModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						New {{ destination }} Link Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="linkCloseButton"
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
								link to this {{ destination }}.
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
					<hr/>

					<!-- CHOOSE RELATIONSHIP TYPE -->
					<div class="row">
						<div class="col-md-4">
							<strong>Relationship</strong>
							<p class="text-instructions">
								Please select an appropriate relation for the objects.
								Default is "Relates"
							</p>
						</div>
						<div class="col-md-8">
							<label for="object-relation">Current object</label>
							<n-select
								id="object-relation"
								:options="objectRelation"
								v-model:value="objectRelationModel"
								class="object-selection"
								:disabled="objectModel === null"
							></n-select>
						</div>
					</div>
					<hr/>

					<!-- SELECTING WHICH OBJECTS TO LINK TO -->
					<div id="select_links"
						 class="row"
						 v-bind:style="styleHeight"
					>
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the objects you want to
								connect to this {{ destination }}.
							</p>
						</div>
						<div class="col-md-8">
							<div class="row"
								 v-if="objectModel !== '' && objectModel !== null"
							>
								<div class="form-group">
									<label>Search</label>
									<input type="text"
										   class="form-control"
										   v-model="searchModel"
									/>
								</div>
							</div>
							<div
								v-if="
									objectResults.length === 0 &&
									objectModel != null
								"
								class="alert alert-warning"
							>
								Sorry - there are no results.
							</div>

							<div class="wizard-results"
								 v-if="!isSearching &&
										objectResults.length > 0 &&
										objectModel != null"
							>
								<div class="wizard-results--card"
									 v-for="result in objectResults"
									 :key="result.id"
								>
									<div class="wizard-results--card--tick">
										<input
											class="form-check-input"
											type="checkbox"
											name="link-option"
											v-bind:value="result.id"
											v-bind:id="`checkbox_${objectModel.toLowerCase()}_${result.pk}`"
											v-model="linkModel"
										/>
									</div>
									<div class="wizard-results--card--content">
										<div class="text-instructions">
											{{objectModel}} {{ result.id }}
										</div>
										<div>
											<strong>{{ result.title }}</strong>
										</div>
										<div>
											Status:
											<span class="text-instructions">{{ result.status }}</span>
										</div>
									</div>
								</div>

								<nav aria-label="Pagination for New Link Wizard"
									 v-if="numberOfPages > 1"
								>
									<ul class="pagination justify-content-center"
									>
										<li v-for="index in numberOfPages"
											v-bind:key="index"
											v-bind:class="getClasses(index)"
										>
											<a v-if="parseInt(index) !== parseInt(currentPage)"
											   class="page-link"
											   href="javascript:void(0)"
											   v-on:click="changePage(index)"
											>
												{{ index }}
											</a>
											<span v-else
												  class="page-link"
											>
												{{ index }}
											</span>
										</li>
									</ul>
								</nav>
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
//JavaScript components
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewLinkWizard",
	components: {
		NSelect,
	},
	emits: [
		'update_link_results',
	],
	props: {
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	data() {
		return {
			currentPage: 1,
			isSearching: false,
			objectModel: null,
			objectRelation: [
				{value: "relates", label: "Relates To"},
			],
			objectRelationModel: "relates",
			objectResults: [],
			objectSelection: [
				{value: "Project", label: "Project"},
				{value: "Requirement", label: "Requirement"},
				{value: "Requirement_Item", label: "Requirement_Item"},
				{value: "Task", label: "Task"},
			],
			linkModel: [],
			numberOfPages: 1,
			searchModel: "",
			searchTimeout: "",
			styleHeight: "height: 90px",
		};
	},
	watch: {
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

			//Only search if there are either 0 characters, or more than 3
			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				this.searchTimeout = setTimeout(() => {
					//Use change page, as we should change the page back to destination page 1
					this.changePage(1);
				}, 500);
			}
		},
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

			//Handle the relationship field
			this.handleRelationship();

			//User has chosen an object.
			if (this.objectModel === null) {
				//Ok - then removed the objects. We don't need to do anything
				this.isSearching = false;
				return;
			}

			const data_to_send = new FormData();
			data_to_send.append("array_of_objects", this.objectModel.toLowerCase());
			data_to_send.set("destination_page", this.currentPage);
			data_to_send.set("exclude_destination", this.destination);
			data_to_send.set("exclude_location_id", this.locationId);
			data_to_send.set("search", this.searchModel);

			//Tell the form that we are searching
			this.isSearching = true;

			//Now to use axios to get the data we require
			this.axios.post(
				`${this.rootUrl}search/data/`,
				data_to_send,
			).then((response) => {
				//Load the data into the array
				this.objectResults = response.data[this.objectModel.toLowerCase()];
				this.numberOfPages = response.data[`${this.objectModel.toLowerCase()}_number_of_pages`];
				this.currentPage = response.data[`${this.objectModel.toLowerCase()}_current_page`];

				//Tell the user we are no longer searching
				this.isSearching = false;

				//Set style height as nothing
				this.styleHeight = "";

				this.$nextTick(() => {
					const select_links = document.getElementById("select_links");
					if (select_links !== undefined) {
						this.styleHeight = `height: ${select_links.clientHeight}px`;
					}
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Searching",
					message: `We got an error searching. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		handleRelationship() {
			//Depending on what object we are looking for, depends which relationships are allowed. For example, the
			//requirements and requirement items are only allowed to have the "Of Parent Of" relation ship
			if (this.objectModel === "Requirement" || this.objectModel === "Requirement_Item") {
				this.objectRelation = [
					{value: "parent_object_of", label: "Is Parent Object Of"},
				];

				this.objectRelationModel = "parent_object_of";

				return;
			}

			//Default :)
			this.objectRelation = [
				{value: "relates", label: "Relates To"},
				{value: "blocked_by", label: "Is Blocked By"},
				{value: "blocking", label: "Is Currently Blocking"},
				{value: "sub_object_of", label: "Is Sub Object Of"},
				{value: "parent_object_of", label: "Is Parent Object Of"},
				{value: "has_duplicate", label: "Has Duplicate Object Of"},
				{value: "duplicate_object", label: "Is Duplicate Object Of"},
			];

			this.objectRelationModel = "relates";
		},
		saveLinks() {
			// Set up the data object to send
			const data_to_send = new FormData();

			// Go through all link models to add to data_to_send
			this.linkModel.forEach((link) => {
				data_to_send.append(
					`${this.objectModel.toLowerCase()}`,
					link
				);
			});

			//Tells the backend the relationship we want
			data_to_send.set("object_relation", this.objectRelationModel);

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_link/`,
				data_to_send
			).then(() => {
				//Data has been successfully saved. Time to update the requirement links
				this.$emit("update_link_results", {});

				//Clear the data
				this.objectModel = null;

				//Click on the close button - a hack, but it should close the modal
				document.getElementById("linkCloseButton").click();

				//Shrink the style height
				this.styleHeight = "height: 90px";
			});
		},
	},
	mounted() {
		this.handleRelationship();
	}
};
</script>


