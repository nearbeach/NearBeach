<template>
	<div class="modal fade"
		 id="addSprintWizardModal"
		 tabindex="-1"
		 aria-labelledby="addSprintWizard"
		 aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="addSprintWizard">Add Object to Sprint</h5>
					<button
						id="addSprintWizardButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Sprint Wizard</strong>
							<p class="text-instructions">
								Please select the appropriate sprint to add this current object too.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label>Sprint</label>
								<n-select
									v-model:value="sprintModel"
									v-bind:options="sprintOptions"
									filterable
									placeholder="Please select a sprint from the list"
								></n-select>
							</div>

							<div class="spacer"></div>

							<div
								v-for="sprint in selectedSprintObject"
								:key="sprint.value"
								class="row"
							>
								<div class="col-md-12 mb-4">
									<strong>Sprint Name: </strong>{{sprint.label}}<br/>
									<strong>Sprint Start Date: </strong>{{useNiceDatetime(sprint.sprint_start_date)}}
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
						v-bind:disabled="sprintModel === undefined"
						v-on:click="addSprint"
						type="button"
						class="btn btn-primary"
					>
						Add to Sprint
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//Naive Ui
import { NSelect } from "naive-ui";

//Vuex
import { mapGetters } from "vuex";

//Composables
import {useNiceDatetime} from "../../../composables/datetime/useNiceDatetime";

export default {
	name: "AddSprintWizard",
	components: {
		NSelect,
	},
	emits: [
		'update_sprint_list',
	],
	data() {
		return {
			selectedSprintObject: {},
			sprintModel: undefined,
			sprintOptions: [],
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	watch: {
		sprintModel(new_value) {
			this.selectedSprintObject = this.sprintOptions.filter((row) => {
				return parseInt(row.value) === parseInt(new_value);
			})
		},
	},
	methods: {
		useNiceDatetime,
		addSprint() {
			//Notify the users of the change
			this.$store.dispatch("newToast", {
				header: "Adding object to sprint",
				message: "Adding current object to sprint, please wait.",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "add_sprint_wizard",
			});

			//Construct data to send
			const data_to_send = new FormData();
			data_to_send.set("sprint_id", this.sprintModel);

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_sprint/${this.sprintModel}/`,
				data_to_send,
			).then((response) => {
				//Send the data upstream
				this.$emit("update_sprint_list", response.data);

				//Close the modal
				document.getElementById("addSprintWizardButton").click();

				//Update the user
				this.$store.dispatch("newToast", {
					header: "Added to Sprint",
					message: "Successfully added current object to Sprint",
					extra_classes: "bg-success",
					unique_type: "add_sprint_wizard",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error adding current object to sprint",
					message: `Error adding the current object to sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "add_sprint_wizard",
				});
			});
		},
		getSprintOptions() {
			this.axios.post(
				`${this.rootUrl}object_data/sprint_list/`,
			).then((response) => {
				this.sprintOptions = response.data.map((row) => {
					return {
						"value": row.sprint_id,
						"label": row.sprint_name,
						"sprint_start_date": row.sprint_start_date,
						"sprint_end_date": row.sprint_end_date,
					};
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error fetching Potential Sprint List",
					message: `Can not retrieve sprint list. ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getSprintOptions();
		});
	},
}
</script>