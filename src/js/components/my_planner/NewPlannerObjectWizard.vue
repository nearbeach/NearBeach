<template>
	<div
		class="modal fade"
		id="newPlannerObjectWizardModal"
		tabindex="-1"
		aria-labelledby="newPlannerObjectModel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						New Planner Object Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="newPlannerObjectButton"
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
							></n-select>
						</div>
					</div>

					<!-- OBJECT LOCATION -->
					<hr/>
					<div class="row"
					>
						<div class="col-md-4">
							<strong>Select Day</strong>
							<p class="text-instructions">
								Select the appropriate day for this object.
							</p>
						</div>

						<div class="col-md-8">
							<div class="row">
								<div class="col-md-6 mt-4">
									<label>Day</label>
									<n-select
										v-bind:options="listOfDays"
										label="column"
										v-model:value="dayModel"
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
						<div class="col-md-8"
							 ref="wizard"
							 v-bind:style="styleHeight"
						>
							<!-- SEARCH RESULTS -->
							<div
								class="form-group mb-4"
								v-if="
									objectModel !== null &&
									dayModel !== null
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

							<!-- LOADING PLACEHOLDER -->
							<div
								class="alert alert-info"
								v-if="objectModel == null || dayModel == null"
							>
								Please make sure you have populated the Object Type, and the Day.
							</div>

							<div
								v-if="isSearching"
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

							<div
								v-if="
									objectResults.length === 0 &&
									isSearching === false &&
									objectModel != null &&
									dayModel != null
								"
								class="alert alert-warning"
							>
                                Sorry. It currently looks like there are no {{ this.objectModel }}s assigned to you.
                                Only assigned {{ this.objectModel }}s will show up here.
							</div>

							<div class="wizard-results"
								 v-if="!isSearching &&
										objectResults.length > 0 &&
										objectModel != null"
							>
								<div class="wizard-results--card"
									 v-for="result in objectResults"
									 :key="result.location_id"
								>
									<div class="wizard-results--card--tick">
										<input
											class="form-check-input"
											type="checkbox"
											name="link-option"
											v-bind:value="result.location_id"
											v-bind:id="`checkbox_${result.location_id}`"
											v-model="linkModel"
										/>
									</div>
									<div class="wizard-results--card--content">
										<div class="text-instructions">
											{{ renderObjectId(result) }}
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
							</div>
						</div>
					</div>
					<div class="row">
						<div class="col-md-4"></div>
						<div class="col-md-8">
							<nav aria-label="Pagination for New Link Sprint Wizard"
								 v-if="setOfPages.length > 1"
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
import {DateTime} from "luxon";
import {getSetOfPages} from "Composables/pagintation/getSetOfPages";

export default {
	name: "NewPlannerObjectWizard",
	components: {
		NSelect,
	},
	emits: ['update_date_array'],
	props: {},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	data() {
		return {
			currentPage: 1,
			dayModel: null,
			isSearching: false,
			linkModel: [],
			listOfDays: [],
			numberOfPages: 0,
			objectModel: null,
			objectResults: [],
			objectSelection: [
				{
					value: "kanban_card",
					label: "Kanban Card",
				},
				{
					value: "project",
					label: "Project",
				},
				{
					value: "task",
					label: "Task",
				},
			],
			searchTermModel: "",
			setOfPages: [],
			styleHeight: "",
		};
	},
	methods: {
		changePage(destination_page) {
			// SET THE STYLE HEIGHT

			// Get data
			this.getObjectResults(this.dayModel, destination_page);
		},
		getClasses(index) {
			if (parseInt(index) === this.currentPage) {
				return "page-item active";
			}

			return "page-item";
		},
		getObjectResults(job_date, destination_page) {
			// Before cleaning results - we set the object height
			const height = this.$refs.wizard.offsetHeight > 182 ? this.$refs.wizard.offsetHeight : 182;
			this.styleHeight = `height:${height}px`

			//Clear data
			this.objectResults = [];

			//Tell the form that we are searching
			this.isSearching = true;

			// Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("object_type", this.objectModel);
			data_to_send.set("job_date", job_date);
			data_to_send.set("destination_page", destination_page);
			data_to_send.set("search", this.searchTermModel);

			//Now to use axios to get the data we require
			this.axios.post(
				`${this.rootUrl}my_planner/get_object_list/`,
				data_to_send,
			).then((response) => {
				//Update local response
				this.objectResults = response.data[this.objectModel.toLowerCase()];
				this.numberOfPages = response.data[`${this.objectModel.toLowerCase()}_number_of_pages`];
				this.currentPage = response.data[`${this.objectModel.toLowerCase()}_current_page`];
				this.setOfPages = getSetOfPages(this.currentPage, this.numberOfPages);
				this.styleHeight = "";

				//Tell the user we are no longer searching
				this.isSearching = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Object List",
					message: `We had an issue getting Object List. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		renderObjectId(data) {
			switch (data.destination) {
				case "kanban_card":
					return `Card${data.location_id}`;
				case "project":
					return `Pro${data.location_id}`;
				case "task":
					return `Task${data.location_id}`;
				default:
					return "----";
			}
		},
		saveLinks() {
			//Escape conditions
			if (this.linkModel.length === 0) return;

			//Tell user we are updating their planner
			this.$store.dispatch("newToast", {
				header: "Currenty updating your Planner",
				message: "Currently updating your planner. Please wait",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "add-objects-to-planner",
			});

			// Set up the data object to send
			const data_to_send = new FormData();

			//Depending on what the object model is - depends what is sent
			data_to_send.set(
				"destination",
				this.objectModel,
			);

			//Set the data for the link Model
			this.linkModel.forEach((row) => {
				data_to_send.append(this.objectModel, row);
			});

			//Set the date
			data_to_send.set("job_date", this.dayModel);

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}my_planner/add_object/`,
				data_to_send
			).then((response) => {
				//Send data to parent
				this.$emit("update_date_array", response.data)

				//Clear the object model
				this.objectModel = null;
				this.dayModel = null;
				this.linkModel = [];
				this.objectResults = [];

				//Click on the close button - a hack, but it should close the modal
				document.getElementById("newPlannerObjectButton").click();

				this.$store.dispatch("newToast", {
					header: "Updated your Planner",
					message: "We have successfully updated your planner",
					extra_classes: "bg-success",
					unique_type: "add-objects-to-planner",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error adding objects to your planner",
					message: `Sorry we could not add any objects to your planner. ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "add-objects-to-planner",
				})
			});
		},
	},
	watch: {
		dayModel(new_value) {
			// If nothing - do nothing
			if (new_value === null || this.objectModel === null)
			{
				this.isSearching = false;
				return;
			}

			this.getObjectResults(new_value, 1);
		},
		objectModel(new_value) {
			if (new_value === null)
			{
				this.isSearching = false;
				return;
			}

			this.linkModel = [];

			if (this.dayModel !== null)
			{
				//We could actually search
				this.getObjectResults(this.dayModel, 1);
			}
		},
		searchTermModel(new_value) {
			if (this.searchTimeout !== "")
			{
				// Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup the time so there are either more than 3 characters, or blank results
			if (new_value.length >= 3 || new_value.length === 0)
			{
				this.searchTimeout = setTimeout(() => {
					this.getObjectResults(this.dayModel, 1);
				}, 500);
			}
		},
	},
	mounted() {
		//We are setting up the list of days. The first option will always be today's date, followed by the next 7 days.
		const today = DateTime.now();

		//For loop
		for (let i = 0; i < 7; i++) {
			const new_day = today.plus({days: i});
			const new_day_date = new_day.toFormat("yyyy-LL-dd");
			const new_day_day = new_day.toFormat("cccc");

			this.listOfDays.push({
				label: `${new_day_day} - ${new_day_date}`,
				value: new_day_date,
			});
		}
	}
};
</script>


