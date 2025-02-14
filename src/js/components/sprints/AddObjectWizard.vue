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
						<div class="col-md-8">
							<div
								v-if="objectModel === ''"
								class="alert alert-info"
							>
								Please select an object.
							</div>

							<div
								v-if="searchStatus === 'currently_searching'"
								class="alert alert-warning mb-4"
							>
								Currently searching for potential objects...
							</div>

							<div class="wizard-results"
								 v-if="searchResults.length > 0 && objectModel != null"
							>
								<div class="wizard-results--card"
									 v-for="result in searchResults"
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
							<div class="alert alert-info"
								 v-if="searchResults.length === 0 && objectModel != null"
							>
								Sorry, could not find any applicable {{ objectModel }}s
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

export default {
	name: "AddObjectWizard",
	components: {
		NSelect,
	},
	data() {
		return {
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
			searchResults: [],
			searchStatus: "",
		};
	},
	watch: {
		objectModel(new_value) {
			//Blank out the previous link model
			this.linkModel = [];

			//Get new list of objects
			this.getObjectList(new_value);
		}
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

			// Go through all link models to add to data_to_send
			this.linkModel.forEach((link) => {
				data_to_send.append(
					`${this.objectModel.toLowerCase()}`,
					link
				);
			});

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}object_data/sprint/${this.locationId}/add_object_to_sprint/`,
				data_to_send,
			).then((response) => {
				//ADD CODE
				//Get the gantt chart data
				const gantt_chart_data = response.data.gantt_chart_data.map((row) => {
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
		getObjectList(new_value) {
			//Update the search status
			this.searchStatus = "currently_searching";

			//Use axios to get the list
			this.axios.post(
				`${this.rootUrl}object_data/sprint/${this.locationId}/${new_value}/potential_object_list/`,
			).then((response) => {
				//Update local response
				this.searchResults = response.data;

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