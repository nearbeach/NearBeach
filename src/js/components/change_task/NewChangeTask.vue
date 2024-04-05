<template>
	<div
		class="modal fade"
		id="newRunItemModal"
		tabindex="-1"
		aria-labelledby="newRunItemModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-xl-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2
						class="modal-title"
						id="newRunItemModalLabel"
					>
						New Change Task
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="newRunItemCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div v-if="currentStatus === 'uploading'"
					 class="modal-body"
				>
					<div class="row">
						Currently Uploading Data...
					</div>
				</div>
				<div
					v-else
					class="modal-body"
				>
					<!-- CHANGE TASK TITLE -->
					<div class="row">
						<div class="col-md-4">
							<strong>Change Task Title</strong>
							<p class="text-instructions">
								Please write a short title of the description
								for this task. i.e Backup of Database
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label>
									Change Title:
									<validation-rendering
										v-bind:error-list="v$.changeTitleModel.$errors"
									></validation-rendering>
								</label>
								<input
									type="text"
									class="form-control"
									v-model="changeTitleModel"
								/>
							</div>
						</div>
					</div>

					<!-- START DATE & END DATE -->
					<hr/>
					<div class="row">
						<div class="col-md-4">
							<strong>Between Dates</strong>
							<p class="text-instructions">
								Choose the start and end date of the Change Task. Please
								note the end date can not be earlier than the start date.
								The release date is the datetime where users now have
								access to what you just released.
							</p>
						</div>
						<div class="col-md-8">
							<div class="row">
								<div class="col-md-6">
									<div class="form-group">
										<label>
											Start Date:
											<validation-rendering
												v-bind:error-list="v$.changeStartDateModel.$errors"
											></validation-rendering>
										</label>
										<n-date-picker
											type="datetime"
											v-model:value="changeStartDateModel"
											class="form-control"
										></n-date-picker>
									</div>
								</div>
								<div class="col-md-6">
									<div class="form-group">
										<label>
											End Date:
											<validation-rendering
												v-bind:error-list="v$.changeEndDateModel.$errors"
											></validation-rendering>
										</label>
										<n-date-picker
											type="datetime"
											v-model:value="changeEndDateModel"
											class="form-control"
										></n-date-picker>
									</div>
								</div>
							</div>
							<div v-if="changeStartDateModel < rfcStartDate"
								 class="row"
							>
								<div class="spacer"></div>
								<div class="alert alert-info">
									Saving this change task will automatically update the start date for the RFC. The
									RFC's new date will reflect this current date time.
								</div>
							</div>
							<div v-if="changeEndDateModel > rfcEndDate"
								 class="row"
							>
								<div class="spacer"></div>
								<div class="alert alert-info">
									Saving this change task will automatically update the end date for the RFC. The
									RFC's new date will reflect this current date time.
								</div>
							</div>
						</div>
					</div>

					<!-- IMPLEMENTATION USER & QA USER -->
					<hr/>
					<div class="row">
						<div class="col-md-4">
							<strong>Implementation & QA User</strong>
							<p class="text-instructions">
								Please indicate which user will be implementing
								the work, and the user who will QA.
							</p>
						</div>
						<div class="col-md-8">
							<div class="row">
								<div class="col-md-6">
									<div class="form-group">
										<label>
											Implementation User
											<validation-rendering
												v-bind:error-list="v$.assignedUserModel.$errors"
											></validation-rendering>
										</label>
										<n-select
											v-bind:options="userList"
											v-model:value="assignedUserModel"
										></n-select>
									</div>
								</div>
								<div class="col-md-6">
									<div class="form-group">
										<label>
											QA User
											<validation-rendering
												v-bind:error-list="v$.qaUserModel.$errors"
											></validation-rendering>
										</label>
										<n-select
											v-model:value="qaUserModel"
											v-bind:options="userList"
										/>
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
						v-on:click="submitAndClose($event)"
					>
						Add & Close Modal
					</button>
					<button
						type="button"
						class="btn btn-success"
						v-on:click="submitChangeTask($event)"
					>
						Add & Create another
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import {NSelect, NDatePicker} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, numeric} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";


export default {
	name: "NewChangeTask",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		NDatePicker,
		NSelect,
		ValidationRendering,
	},
	props: {
		locationId: {
			type: Number,
			default: 0,
		},
	},
	data: () => ({
		assignedUserModel: null,
		changeEndDateModel: 0,
		changeStartDateModel: 0,
		changeTitleModel: "",
		currentStatus: "ready", //Has values; ready, saving
		qaUserModel: null,
		userList: [],
	}),
	validations: {
		assignedUserModel: {
			required,
			numeric,
		},
		changeEndDateModel: {
			required,
		},
		changeStartDateModel: {
			required,
		},
		changeTitleModel: {
			required,
		},
		qaUserModel: {
			required,
			numeric,
		},
	},
	computed: {
		...mapGetters({
			objectUserList: "getObjectUserList",
			potentialUserList: "getPotentialUserList",
			rfcEndDate: "getEndDate",
			rfcStartDate: "getStartDate",
			rootUrl: "getRootUrl",
		}),
	},
	watch: {
		changeEndDateModel(new_value) {
			if (new_value < this.changeStartDateModel) {
				this.changeStartDateModel = new_value;
			}
		},
		changeStartDateModel(new_value) {
			if (new_value > this.changeEndDateModel) {
				this.changeEndDateModel = new_value;
			}
		},
		groupUserList() {
			this.updateUserList();
		},
		potentialUserList() {
			this.updateUserList();
		},
	},
	methods: {
		formatDate(date) {
			//Setup the date
			let new_date = new Date(date);

			//Split the date into date vs time
			new_date = new_date.toISOString().split("T");

			//Split the time
			const time_split = new_date[1].split(".");

			//Return the date as a string
			return `${new_date[0]} ${time_split[0]}`;
		},
		async submitAndClose(event) {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
				return;
			}

			this.submitChangeTask(event);

			//Close the modal
			document.getElementById("newRunItemCloseButton").click();
		},
		async submitChangeTask(event) {
			//Tell modal current object is saving
			this.currentStatus = 'uploading';

			//Stop the usual stuff
			event.preventDefault();

			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
				//Set the status back to "ready"
				this.currentStatus = "ready";

				//Do nothing, and return
				return;
			}

			const change_task_seconds =
				parseInt(this.changeEndDateModel) -
				parseInt(this.changeStartDateModel);

			// Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set(
				"request_for_change",
				this.locationId.toString()
			);
			data_to_send.set("change_task_title", this.changeTitleModel);
			data_to_send.set(
				"change_task_start_date",
				new Date(this.changeStartDateModel).toISOString()
			);
			data_to_send.set(
				"change_task_end_date",
				new Date(this.changeEndDateModel).toISOString()
			);
			data_to_send.set(
				"change_task_seconds",
				change_task_seconds.toString()
			);
			data_to_send.set(
				"change_task_assigned_user",
				this.assignedUserModel
			);
			data_to_send.set("change_task_qa_user", this.qaUserModel);

			this.axios.post(
				`${this.rootUrl}rfc_information/${this.locationId}/new_change_task/`,
				data_to_send
			).then((response) => {
				//Update the runsheet variables
				this.$emit("update_change_task_list", response.data);

				//Clear the modal
				this.changeTitleModel = "";
				this.assignedUserModel = "";
				this.qaUserModel = "";

				//Adjust the times
				this.changeStartDateModel = this.changeEndDateModel;
				this.changeEndDateModel = this.changeEndDateModel + (15 * 1000 * 60);

				//Set the current status back to ready
				this.currentStatus = 'ready';
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error submitting change task",
					message: `Sorry, we could not submit the change task. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateUserList() {
			//Grab a map of the potential and current users
			const a = this.objectUserList.map((row) => {
				return {
					label: `${row.username}: ${row.first_name} ${row.last_name}`,
					value: row.id,
				}
			});

			const b = this.potentialUserList.map((row) => {
				return {
					label: `${row.username}: ${row.first_name} ${row.last_name}`,
					value: row.id,
				}
			});

			//Concatenate the lists
			this.userList = a.concat(b);
		},
	},
	mounted() {
		//Update the user fixed list
		this.$nextTick(() => {
			this.updateUserList();
		});

		//Update Times
		this.changeEndDateModel = this.rfcEndDate + (15 * 1000 * 60);
		this.changeStartDateModel = this.rfcEndDate;
	},
};
</script>

<style scoped></style>
