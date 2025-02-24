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
						<div class="col-md-8">
							<!-- LOADING PLACEHOLDER -->
							<div
								class="alert alert-info"
								v-if="isSearching || objectModel == null"
							>
								Please select the object type.
							</div>

							<div
								v-if="
									objectResults.length === 0 &&
									objectModel != null
								"
								class="alert alert-warning"
							>
                                Sorry. It currently looks like there are no {{ this.objectModel }}s assigned to you.
                                Only assigned {{ this.objectModel }}s will show up here.
							</div>

							<!-- SEARCH RESULTS -->
							<div
								class="form-group mb-4"
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

							<div class="wizard-results"
								 v-if="!isSearching &&
										objectFilteredResults.length > 0 &&
										objectModel != null"
							>
								<div class="wizard-results--card"
									 v-for="result in objectFilteredResults"
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
						v-bind:disabled="filteredLinkModel.length === 0"
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

export default {
	name: "NewPlannerObjectWizard",
	components: {
		NSelect,
	},
	emits: ['update_date_array'],
	props: {
		dateArray: {
			type: Array,
			default: () => {
				return [];
			},
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
			dayModel: "",
			filteredLinkModel: [],
			isSearching: false,
			linkModel: [],
			listOfDays: [],
			objectModel: null,
			objectFilteredResults: [],
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
			searchTermModel: "----",
		};
	},
	methods: {
		getFilteredLinkModel() {
			//Filter the object results and exclude any objects that already exist on today
			const data_array = this.dateArray.filter(row => row.date === this.dayModel);

			//Make sure we have data, if we don't silently fail
			if (data_array.length === 0) return;

			//Get the data from the first array
			let existing_data = data_array[0].data;

			this.filteredLinkModel = this.linkModel.filter((row) => {
				const count = existing_data.filter((existing_row) => {
					return parseInt(existing_row.location_id) === parseInt(row);
				}).length

				return count === 0;
			});
		},
		getFilteredResults() {
			//Filter the object results and exclude any objects that already exist on today
			const data_array = this.dateArray.filter(row => row.date === this.dayModel);

			//Make sure we have data, if we don't silently fail
			if (data_array.length === 0) return;

			//Get the data from the first array
			let data = data_array[0].data;


			const object_results = this.objectResults.filter((row) => {
				const count_of_already_existing = data.filter((row_object) => {
					//Match the object results to those already existing on today
					const condition_1 = row.destination.toLowerCase() === row_object.object_type.toLowerCase();
					const condition_2 = parseInt(row.location_id) === parseInt(row_object.location_id);

					return condition_1 && condition_2;
				}).length;

				//Only return if there are no objects on today
				return count_of_already_existing === 0;
			});

			//If the search bar is empty - we don't do anything
			if (
				this.searchTermModel === "" ||
				this.searchTermModel === null
			) {
				this.objectFilteredResults = object_results;
				return;
			}

			//Update the filters by checking to see if the string matches
			this.objectFilteredResults = object_results.filter((row) => {
				return row.title.toLowerCase().includes(
					this.searchTermModel.toLowerCase()
				)
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
			if (this.filteredLinkModel.length === 0) return;

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
			this.filteredLinkModel.forEach((row) => {
				data_to_send.append(this.objectModel, row);
			});

			//Set the date
			data_to_send.set("job_date", this.dayModel);

			// Use axios to send data
			this.axios.post(
				// `${this.rootUrl}kanban_information/${this.locationId}/${this.objectModel.toLowerCase()}/add_link/`,
				`${this.rootUrl}my_planner/add_object/`,
				data_to_send
			).then((response) => {
				//Send data to parent
				this.$emit("update_date_array", response.data)

				//Clear the object model
				this.objectModel = null;

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
		dateArray: {
			handler() {
				this.getFilteredLinkModel();
				this.getFilteredResults();
			},
			deep: true,
		},
		dayModel() {
			//The day has changed, update the filtered link models to exclude any duplicates
			this.getFilteredLinkModel();

			//Update filted results
			this.getFilteredResults();
		},
		linkModel: {
			handler() {
				this.getFilteredLinkModel();
			},
			deep: true,
		},
		objectModel() {
			//Clear data
			this.linkModel = [];
			this.getFilteredLinkModel();

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
				`${this.rootUrl}my_planner/get_object_list/${this.objectModel}/`,
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
					header: "Error Getting Object List",
					message: `We had an issue getting Object List. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		searchTermModel() {
			this.getFilteredResults();
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

		//Set the default to the first result
		this.dayModel = this.listOfDays[0].value;
	}
};
</script>


