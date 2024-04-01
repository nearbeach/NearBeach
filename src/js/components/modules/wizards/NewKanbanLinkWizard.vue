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
						<Icon v-bind:icon="icons.linkOut"></Icon>
						New Kanban
						Link Wizard
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
									objectFilteredResults.length > 0 &&
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
								<tbody v-if="objectModel == 'Project'">
								<tr
									v-for="result in objectFilteredResults"
									:key="result.pk"
								>
									<td>
										<div class="form-check">
											<input
												class="form-check-input"
												type="radio"
												name="link-option"
												v-bind:value="result.pk"
												v-bind:id="`radio_project_${result.pk}`"
												v-model="linkModel"
											/>
											<label
												class="form-check-label"
												v-bind:for="`radio_project_${result.pk}`"
											>
												{{
													result.fields
														.project_name
												}}
											</label>
										</div>
										<div class="spacer"></div>
										<p class="small-text">
											Project {{ result.pk }}
										</p>
									</td>
									<td>
										{{ result.fields.project_status }}
									</td>
								</tr>
								</tbody>

								<!-- REQUIREMENTS -->
								<tbody v-if="objectModel == 'Requirement'">
								<tr
									v-for="result in objectFilteredResults"
									:key="result.pk"
								>
									<td>
										<div class="form-check">
											<input
												class="form-check-input"
												type="radio"
												name="link-option"
												v-bind:value="result.pk"
												v-bind:id="`radio_requirement_${result.pk}`"
												v-model="linkModel"
											/>
											<label
												class="form-check-label"
												v-bind:for="`radio_task_${result.pk}`"
											>
												{{
													result.fields
														.requirement_title
												}}
											</label>
										</div>
										<div class="spacer"></div>
										<p class="small-text">
											Requirement {{ result.pk }}
										</p>
									</td>
									<td>
										{{
											result.fields.requirement_status
										}}
									</td>
								</tr>
								</tbody>

								<!-- TASKS -->
								<tbody v-if="objectModel === 'Task'">
								<tr
									v-for="result in objectFilteredResults"
									:key="result.pk"
								>
									<td>
										<div class="form-check">
											<input
												class="form-check-input"
												type="radio"
												v-bind:value="result.pk"
												v-bind:id="`radio_task_${result.pk}`"
												v-model="linkModel"
											/>
											<label
												class="form-check-label"
												v-bind:for="`radio_task_${result.pk}`"
											>
												{{
													result.fields
														.task_short_description
												}}
											</label>
										</div>
										<div class="spacer"></div>
										<p class="small-text">
											Task {{ result.pk }}
										</p>
									</td>
									<td>{{ result.fields.task_status }}</td>
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
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewKanbanLinkWizard",
	components: {
		Icon,
		NSelect,
	},
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
	mixins: [iconMixin],
	data() {
		return {
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
			searchTermModel: "",
		};
	},
	methods: {
		saveLinks() {
			// Set up the data object to send
			const data_to_send = new FormData();

			//Get the modal to extract data from
			// const self_modal = document.getElementById("newLinkModal");

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
				//Data has been successfully saved. Time to add the card to the board
				this.$emit("new_card", response.data);

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
			this.axios.post(
				`${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel}/link_list/`
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
		searchTermModel() {
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
