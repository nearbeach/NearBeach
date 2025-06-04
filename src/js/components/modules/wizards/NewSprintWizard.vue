<template>
	<div
		class="modal fade"
		id="createNewSprintModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="createNewSprint"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
					>
						Please confirm Link Deletion
					</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="createNewSprintButton"
					></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Sprint Information</strong>
							<p class="text-instructions">
								Please use an appropriate name, start date, and finish date.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label>Sprint Name</label>
								<input
									class="form-control"
									type="text"
									v-model="sprintNameModel"
								/>
							</div>

							<div class="spacer"></div>

							<div class="row">
								<div class="col-md-6">
									<div class="form-group">
										<label>Start Date</label>
										<n-date-picker v-model:value="sprintStartDate" type="date"></n-date-picker>
									</div>
								</div>
								<div class="col-md-6">
									<div class="form-group">
										<label>End Date</label>
										<n-date-picker v-model:value="sprintEndDate" type="date"></n-date-picker>
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
						v-on:click="closeModal"
					>
						Cancel
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="createNewSprint"
					>
						Create New Sprint
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

//Naive UI
import { NDatePicker } from 'naive-ui';
export default {
	name: "NewSprintWizard",
	components: {
		NDatePicker,
	},
	props: {
		sprintResultsLength: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	data() {
		return {
			sprintEndDate: 0,
			sprintNameModel: "",
			sprintStartDate: 0,
		}
	},
	watch: {
		sprintResultsLength() {
			this.updateSprintNameModel();
		}
	},
	methods: {
		closeModal() {
			document.getElementById("createNewSprintButton").click();
		},
		createNewSprint() {
			//Notify user that data is being sent
			this.$store.dispatch("newToast", {
				header: "Creating New Toast",
				message: "Please wait - we are creating the new toast. It will automatically navigate you to the " +
							"new sprint information page",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "create_sprint",
			});

			//Organise dates
			const start_date = new Date(this.sprintStartDate);
			const end_date = new Date(this.sprintEndDate);

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("sprint_name", this.sprintNameModel);
			data_to_send.set(
				"sprint_start_date",
				start_date.toISOString(),
			)
			data_to_send.set(
				"sprint_end_date",
				end_date.toISOString(),
			)

			this.axios.post(
				`${this.rootUrl}new_sprint/${this.destination}/${this.locationId}/save/`,
				data_to_send,
			).then((response) => {
				//Navigate user to the new sprint page
				window.location = `${this.rootUrl}sprint_information/${response.data.id}/`;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error creating new sprint",
					message: `Could not create new sprint. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "create_sprint",
				});
			});
		},
		updateSprintNameModel() {
			const new_value = this.sprintResultsLength + 1;

			//Fix up the models
			const date = new Date().toLocaleDateString(
				'en-au',
				{ year:"numeric", month:"short", day:"numeric"}
			);

			//Update the sprint name model
			this.sprintNameModel = `${this.destination}-${this.locationId} - Sprint ${new_value} - ${date}`;
		},
	},
	mounted() {
		//Set the sprint start date as today, the end date in 7 days.
		this.sprintStartDate = new Date().getTime();
		this.sprintEndDate = this.sprintStartDate + 7 * 1000 * 60 * 60 * 24;

		this.$nextTick(() => {
			this.updateSprintNameModel();
		});
	}
}
</script>