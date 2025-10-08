<template>
	<div class="modal fade"
		 id="addObjectWizardModal"
		 tabindex="-1"
		 aria-labelledby="addObjectWizardLabel"
		 aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title"
						id="addObjectWizardLabel"
					>
						Add Objects to Sprint Wizard
					</h5>
					<button
						id="addObjectWizardButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<!-- OBJECT SELECTOR-->
					<div class="row">
						<div class="col-md-4">
							<strong>Object Selector</strong>
							<p class="text-instructions">
								Please select which object you would like to link to this task.
							</p>
						</div>
						<div class="col-md-8">
							<n-select
								filterable
								placeholder="Please select an object"
								v-model:value="objectModel"
								v-bind:options="objectOptions"
								v-bind:disabled="searchStatus==='currently_searching'"
							></n-select>
						</div>
					</div>

					<hr>

					<div class="row">
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the objects you want to connect to this sprint.
							</p>
						</div>
						<div class="col-md-8"
							 v-bind:style="styleHeight"
							 ref="wizardResults"
						>
							<div
								v-if="objectModel === ''"
								class="alert alert-info"
							>
								Please select an object.
							</div>

							<div class="row"
								 v-if="objectModel !== ''"
							>
								<div class="col-12">
									<label class="form-label">Search Terms</label>
									<input
										id="search_terms"
										class="form-control"
										v-model="searchModel"
										type="text"
									/>
								</div>
							</div>

							<div
								v-if="searchStatus === 'currently_searching'"
								class="wizard-results"
							>
								<div class="wizard-results--card">
									<div class="wizard-results--card--tick"></div>
									<div class="wizard-results--card--content">
										<span class="placeholder col-1"></span><br/>
										<span class="placeholder col-11"></span>
										<span class="placeholder col-8"></span>
									</div>
								</div>
							</div>

							<div class="wizard-results"
								 v-if="objectResults.length > 0 && objectModel != null"
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
											<strong>{{ result.description }}</strong>
										</div>
										<div>
											Status:
											<span class="text-instructions">{{ result.status }}</span>
										</div>
									</div>
								</div>
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-md-4"></div>
						<div class="col-md-8">
							<nav aria-label="Pagination for New Link Sprint Wizard"
								 v-if="setOfPages.length >= 1"
							>
								<ul class="pagination justify-content-center"
								>
									<li v-for="index in setOfPages"
										v-bind:key="index.destinationPage"
										v-bind:class="getClasses(index.destinationPage)"
									>
										<a v-if="parseInt(index.destinationPage) !== parseInt(currentPage)"
										   class="page-link"
										   href="javascript:void(0)"
										   v-on:click="changePage(index.destinationPage)"
										>
											{{ index.text }}
										</a>
										<span v-else
											  class="page-link"
										>
											{{ index.text }}
										</span>
									</li>
								</ul>
							</nav>
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
						v-on:click="addObjects"
					>
						Add Objects
					</button>
				</div>
			</div>
		</div>
	</div>

</template>

<script>
//Naive-ui
import { NSelect } from "naive-ui";

//VueX
import { mapGetters } from "vuex";
import {DateTime} from "luxon";
import {getSetOfPages} from "Composables/pagintation/getSetOfPages";

export default {
	name: "AddObjectWizard",
	components: {
		NSelect,
	},
	data() {
		return {
			currentPage: 1,
			linkModel: [],
			objectModel: "",
			objectOptions: [
				{
					value: "project",
					label: "Project",
				},
				{
					value: "requirement_item",
					label: "Requirement Item",
				},
				{
					value: "task",
					label: "Task",
				},
			],
			objectResults: [],
			searchModel: "",
			searchStatus: "",
			searchTimeout: "",
			setOfPages: [],
			styleHeight: "",
		};
	},
	watch: {
		objectModel(new_value) {
			//Blank out the previous link model
			this.linkModel = [];
			this.setOfPages = [];

			//Get new list of objects
			this.getObjectList(new_value, 1);
		},
		searchModel() {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (this.searchModel.length >= 3 || this.searchModel.length === 0) {
				// Solidify the height of the object
				this.styleHeight = `height: ${this.$refs.wizardResults.offsetHeight}px`;

				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getObjectList(this.objectModel, 1);
				}, 500);
			}
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addObjects() {
			//Notify user we want to add these objects
			this.$store.dispatch("newToast", {
				header: "Adding objects to Sprint",
				message: "Currently adding object to sprint. Please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "add_objects_to_sprint",
			});

			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("object_type", this.objectModel);

			// Go through all link models to add to data_to_send
			this.linkModel.forEach((link) => {
				data_to_send.append("object_id", link)
			});

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}api/v0/sprint/${this.locationId}/link/`,
				data_to_send,
			).then((response) => {
				//Get the gantt chart data
				const gantt_chart_data = response.data.map((row) => {
					//Convert the dates
					const end_date = DateTime.fromISO(row.end_date);
					const start_date = DateTime.fromISO(row.start_date);

					//Mutate the row
					row.end_date = end_date.toMillis();
					row.start_date = start_date.toMillis();

					return row;
				});

				//Update Gantt Chart Data
				this.$store.commit({
					type: "updateGanttChartData",
					ganttChartData: gantt_chart_data,
				});

				//Update user of status
				this.$store.dispatch("newToast", {
					header: "Added Objects to Sprint",
					message: "Objects successfully added to Sprint",
					extra_classes: "bg-success",
					unique_type: "add_objects_to_sprint",
					delay: 600,
				});

				//Close the modal
				document.getElementById("addObjectWizardButton").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Adding Objects to Sprint",
					message: `Sorry - we came across an issue adding objects to the sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "add_objects_to_sprint",
				});
			});
		},
		changePage(destination_page)
		{
			// Solidify the height of the object
			this.styleHeight = `height: ${this.$refs.wizardResults.offsetHeight}px`;

			// Then fetch the data
			this.getObjectList(this.objectModel, destination_page);
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
		getObjectList(new_value, destination_page) {
			//Update the search status
			this.searchStatus = "currently_searching";

			// Clear out data
			this.objectResults = [];

			//Create form data
			const data_to_send = new FormData();
			data_to_send.set("object_lookup", new_value);
			data_to_send.set("destination_page", destination_page);
			data_to_send.set("search", this.searchModel);

			//Use axios to get the list
			this.axios.post(
				`${this.rootUrl}sprint_information/${this.locationId}/potential_object_list/`,
				data_to_send,
			).then((response) => {
				//Update local response
				this.objectResults = response.data[this.objectModel.toLowerCase()];
				this.numberOfPages = response.data[`${this.objectModel.toLowerCase()}_number_of_pages`];
				this.currentPage = response.data[`${this.objectModel.toLowerCase()}_current_page`];
				this.setOfPages = getSetOfPages(this.currentPage, this.numberOfPages);
				this.styleHeight = "";

				//Update status
				this.searchStatus = 'search_completed';
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting potential object list",
					message: `Sorry, we could not get a list of potential objects. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		}
	},
}
</script>