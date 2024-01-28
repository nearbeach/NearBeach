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
						<Icon v-bind:icon="icons.linkOut"></Icon>
						New
						Requirement Link Wizard
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
					<div class="row">
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the objects you want to
								connect to this requirement.
							</p>
						</div>
						<div class="col-md-8">
							<!-- LOADING PLACEHOLDER -->
							<div
								id="link_wizard_results"
								v-if="isSearching || objectModel == null"
							>
								<img
									v-bind:src="`${staticUrl}/NearBeach/images/placeholder/search.svg`"
									alt="Searching..."
								/>
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
									v-model="searchTermModel"
									type="text"
								/>
							</div>
							<br/>

							<!-- TABLE CONTAINING RESULTS -->
							<table
								class="table"
								v-if="
									!isSearching &&
									objectResults.length > 0 &&
									objectModel != null
								"
							>
								<thead>
								<tr>
									<td>{{ objectModel }} Description</td>
									<td>Status</td>
								</tr>
								</thead>

								<!-- PROJECTS -->
								<tbody>
								<tr
									v-for="result in objectFilteredResults"
									:key="result.id"
								>
									<td>
										<div class="form-check">
											<input
												class="form-check-input"
												type="checkbox"
												v-bind:value="result.id"
												v-bind:id="`checkbox_${objectModel.toLowerCase()}_${result.id}`"
												v-model="linkModel"
											/>
											<label
												class="form-check-label"
												v-bind:for="`checkbox_${objectModel.toLowerCase()}_${result.id}`"
											>
												{{ result.description }}
											</label>
										</div>
										<div class="spacer"></div>
										<p class="small-text">
											{{objectModel}} {{ result.id }}
										</p>
									</td>
									<td>
										{{ result.status }}
									</td>
								</tr>
								</tbody>
							</table>
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
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewRequirementLinkWizard",
	components: {
		Icon,
		NSelect,
	},
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
	mixins: [iconMixin],
	data() {
		return {
			isSearching: false,
			linkModel: [],
			objectModel: null,
			objectFilteredResults: [],
			objectResults: [],
			objectSelection: [
				{value: "Project", label: "Project"},
				{value: "Task", label: "Task"},
			],
			searchTermModel: "",
		};
	},
	methods: {
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
			)
			.then((response) => {
				//Data has been successfully saved. Time to update the requirement links
				this.$emit("update_module", response.data);

				//Click on the close button - a hack, but it should close the modal
				document
					.getElementById("requirementLinkCloseButton")
					.click();

				//Clear results
				this.objectModel = null;
			});
		},
	},
	watch: {
		objectModel() {
			//Clear data
			this.linkModel = [];

			//User has chosen an object.
			if (this.objectModel === null) {
				//Ok - then removed the objects. We don't need to do anything
				this.isSearching = false;
				return;
			}

			//Tell the form that we are searching
			this.isSearching = true;

			//Now to use axios to get the data we require
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${
						this.locationId
					}/${this.objectModel.toLowerCase()}/link_list/`
				)
				.then((response) => {
					//Load the data into the array
					this.objectResults = response.data;
					this.objectFilteredResults = response.data;

					//Tell the user we are no longer searching
					this.isSearching = false;

					//Clear the search term results
					this.searchTermModel = "";
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error retrieving links",
						message: "We are currently having issues obtaining data",
						delay: 0,
						extra_classes: "bg-danger",
					});
				});
		},
		searchTermModel() {
			//If search term model is empty - just return all results
			if (
				this.searchTermModel === "" ||
				this.searchTermModel === null
			) {
				this.objectFilteredResults = this.objectResults;
				return;
			}

			//Update the filters by checking to see if the string matches
			this.objectFilteredResults = this.objectResults.filter(
				(row) => {
					//Get the description from either task or project
					let description = "";
					if (row.fields.project_description !== undefined) {
						description =
							row.fields.project_description.toLowerCase();
					} else {
						description =
							row.fields.task_short_description.toLowerCase();
					}

					//Return true or false if the string is inside the description
					return description.includes(
						this.searchTermModel.toLowerCase()
					);
				}
			);
		},
	},
};
</script>

<style scoped></style>
