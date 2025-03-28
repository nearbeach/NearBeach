<template>
	<div
		class="modal fade"
		id="newRequirementLinkModal"
		tabindex="-1"
		aria-labelledby="requirementLinkModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						New Requirement Link Wizard
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
							<div class="form-group">
								<label>Object Selection</label>
								<n-select
									:options="objectSelection"
									v-model:value="objectModel"
									class="object-selection"
								></n-select>
							</div>
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
								connect to this requirement.
							</p>
						</div>
						<div class="col-md-8">
							<div
								v-if="objectResults.length === 0 && objectModel != null"
								class="alert alert-warning"
							>
								Sorry - there are no results.
							</div>

							<!-- SEARCH RESULTS -->
							<div
								class="form-group"
								v-if="objectModel != null"
							>
								<label>Filter</label>
								<input
									id="search_terms"
									class="form-control"
									v-model="searchModel"
									type="text"
								/>
							</div>
							<br/>

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
						v-bind:disabled="linkModel.length == 0"
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
	name: "NewRequirementLinkWizard",
	components: {
		NSelect,
	},
	emits: ['update_module'],
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
			linkModel: [],
			numberOfPages: 1,
			objectModel: null,
			objectResults: [],
			objectSelection: [
				{value: "Project", label: "Project"},
				{value: "Task", label: "Task"},
			],
			searchModel: "",
			searchTimeout: "",
			styleHeight: "height: 90px",
		};
	},
	watch: {
		objectModel() {
			this.getObjects();
		},
		searchModel() {
			//Determine if there is a timeout session going on
			if (this.searchTimeout !== "") {
				clearTimeout(this.searchTimeout);
			}

			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				this.searchTimeout = setTimeout(() => {
					this.getObjects();
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
					if (select_links != undefined) {
						this.styleHeight = `height: ${select_links.clientHeight}px`;
					}
				});
			}).catch(() => {
				this.$store.dispatch("newToast", {
					header: "Error retrieving links",
					message: "We are currently having issues obtaining data",
					delay: 0,
					extra_classes: "bg-danger",
				});
			});
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

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}${this.destination}_information/${this.locationId}/add_link/`,
				data_to_send
			).then((response) => {
				//Data has been successfully saved. Time to update the requirement links
				this.$emit("update_module", response.data);

				//Click on the close button - a hack, but it should close the modal
				document
					.getElementById("requirementLinkCloseButton")
					.click();

				//Clear results
				this.objectModel = null;

				//Set style height
				this.styleHeight = "height: 90px";
			});
		},
	},
};
</script>


