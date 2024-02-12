<template>
	<div
		class="modal fade"
		id="newChangeTaskLinkModal"
		tabindex="-1"
		aria-labelledby="linkModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.linkOut"></Icon>
						New
						Change Task Link Wizard
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
					<!-- CHOOSE RELATIONSHIP TYPE -->
					<div class="row">
						<div class="col-md-4">
							<strong>Relationship</strong>
							<p class="text-instructions">
								Please indicate if you are blocking future Changes Tasks, or if a
								past Change Task is blocking current Change Task.
							</p>
						</div>
						<div class="col-md-8">
							Current change task <br/>
							<n-select
								:options="changeTaskRelation"
								v-model:value="changeTaskRelationModel"
								class="object-selection"
							></n-select>
						</div>
					</div>
					<hr/>

					<!-- SELECTING WHICH OBJECTS TO LINK TO -->
					<div class="row">
						<div class="col-md-4">
							<strong>Select Links</strong>
							<p class="text-instructions">
								Please select which of the change tasks you want to
								connect to this change task.
							</p>
						</div>
						<div class="col-md-8">
							<div
								v-if="filteredChangeTaskResults.length === 0"
								class="alert alert-warning"
							>
								Sorry - there are no results.
							</div>

							<div v-for="changeTask in filteredChangeTaskResults"
								 :key="changeTask.pk"
								 v-bind:class="checkSelected(changeTask.pk)"
							>
								<div class="form-check">
									<input
										class="form-check-input"
										type="checkbox"
										v-bind:value="changeTask.pk"
										v-bind:id="`checkbox_change_task_${changeTask.pk}`"
										v-model="linkModel"
									/>
									<label
										class="form-check-label"
										v-bind:for="`checkbox_change_task_${changeTask.pk}`"
									>
										Change Task {{ changeTask.pk }} - {{ changeTask.fields.change_task_title }}
									</label>
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
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "NewChangeTaskLinkWizard",
	components: {
		Icon,
		NSelect,
	},
	data() {
		return {
			changeTaskRelation: [
				{value: "blocked_by", label: "Is Blocked By"},
				{value: "blocking", label: "Is Currently Blocking"},
			],
			changeTaskRelationModel: "blocking",
			changeTaskResults: [],
			filteredChangeTaskResults: [],
			linkModel: [],
		}
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			endDate: "getChangeTaskEndDate",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			startDate: "getChangeTaskStartDate",
			staticUrl: "getStaticUrl",
		}),
	},
	watch: {
		changeTaskRelationModel() {
			if (this.changeTaskRelationModel === "blocking") {
				this.filterBlocking();
			} else {
				this.filterBlockedBy();
			}
		},
	},
	mixins: [iconMixin],
	methods: {
		checkSelected(pk) {
			if (this.linkModel.includes(pk)) {
				return "row change-task--detail change-task--selected";
			}

			return "row change-task--detail";
		},
		filterBlockedBy() {
			//Filter out all dates where the change task end date <= start_date of current change task
			this.filteredChangeTaskResults = this.changeTaskResults.filter(row => {
				const end_date = new Date(row.fields.change_task_end_date);

				return end_date.getTime() <= this.startDate.getTime();
			})
		},
		filterBlocking() {
			//Filter out all dates where the change task start date >= end_date of the current change task
			this.filteredChangeTaskResults = this.changeTaskResults.filter(row => {
				const start_date = new Date(row.fields.change_task_start_date);

				return start_date.getTime() >= this.endDate.getTime();
			})
		},
		getAllChangeTasks() {
			//Use Axios to get data
			this.axios.post(
				`${this.rootUrl}change_task_information/${this.locationId}/get_change_task_list/`
			).then(response => {
				this.changeTaskResults = response.data;

				//Get filtered data
				this.filterBlocking();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting all change tasks",
					message: `There is an issue getting all change tasks - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})
		},
		saveLinks() {
			// Set up the data object to send
			const data_to_send = new FormData();

			// Go through all link models to add to data_to_send
			this.linkModel.forEach((link) => {
				data_to_send.append(
					"change_task",
					link
				);
			});

			//Tells the backend the relationship we want
			data_to_send.set("object_relation", this.changeTaskRelationModel);

			// Use axios to send data
			this.axios.post(
				`${this.rootUrl}object_data/change_task/${this.locationId}/add_link/`,
				data_to_send
			).then(() => {
				//Data has been successfully saved. Time to update the requirement links
				this.$emit("update_link_results", {});

				//Click on the close button - a hack, but it should close the modal
				document.getElementById("linkCloseButton").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting all change tasks",
					message: `There is an issue getting all change tasks - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		}
	},
	mounted() {
		//Get the required data
		//Have to wait a little extra - tick does not work :'(
		setTimeout(() => {
			this.getAllChangeTasks();
		}, 500);
	}
}
</script>