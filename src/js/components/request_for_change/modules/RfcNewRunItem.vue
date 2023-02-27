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
				<div class="modal-body">
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
								<label>Change Title:</label>
								<input
									type="text"
									class="form-control"
									v-model="changeTitleModel"
								/>
							</div>
						</div>
					</div>

					<!-- NOTIFY USERS OF DATE RESTRICTIONS -->
					<hr />
					<div class="row">
						<div class="col-md-4">
							<strong>Date Restrictions</strong>
							<p class="text-instructions">
								Start and End dates of the RFC
							</p>
						</div>
						<div class="col-md-4">
							Start Date:
							<span>{{ formatDate(rfcStartDate) }}</span>
						</div>
						<div class="col-md-4">
							End Date: <span>{{ formatDate(rfcEndDate) }}</span>
						</div>
					</div>

					<!-- START DATE & END DATE -->
					<hr />
					<between-dates
						destination="Change Task"
						v-on:update_dates="updateDates($event)"
						v-bind:no-back-dating="false"
					></between-dates>

					<!-- IMPLEMENTATION USER & QA USER -->
					<hr />
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
										<label>Implementation User</label>
										<n-select
											v-bind:options="userListFixed"
											v-model:value="assignedUserModel"
										></n-select>
									</div>
								</div>
								<div class="col-md-6">
									<div class="form-group">
										<label>QA User</label>
										<n-select
											v-model:value="qaUserModel"
											v-bind:options="userListFixed"
										/>
									</div>
								</div>
							</div>
						</div>
					</div>

					<!-- DESCRIPTION OPTIONAL -->
					<hr />
					<div class="row">
						<div class="col-md-4">
							<strong>Description</strong>
							<p class="text-instructions">
								Write a detail description of this particular
								task.
							</p>
						</div>
						<div class="col-md-8">
							<label>Change Task Description (Optional):</label>
							<editor
								:init="{
									height: 300,
									menubar: false,
									plugins: ['lists', 'table'],
									toolbar: [
										'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
										'bold italic strikethrough underline backcolor | table | ' +
											'bullist numlist outdent indent | removeformat',
									],
								}"
								v-bind:content_css="false"
								v-bind:skin="false"
								v-model="changeDescriptionModel"
							/>
						</div>
					</div>

					<!-- MISC -->
					<hr />
					<div class="row">
						<div class="col-md-4">
							<strong>Misc</strong>
							<p class="text-instructions">
								Please fill in the stakeholders for this
								particular change task. Default value will be
								"Stakeholders".
							</p>
							<p class="text-instructions">
								To state if there is downtime, please click the
								"No Downtime" to change it's statue.
							</p>
						</div>
						<div class="col-md-8">
							<div class="form-group">
								<label>Stakeholders:</label>
								<input
									type="text"
									class="form-control"
									v-model="changeStakeholderModel"
								/>
							</div>

							<br />
							<div
								class="btn-group"
								role="group"
								aria-label="Basic checkbox toggle button group"
							>
								<input
									type="checkbox"
									id="isDowntime"
									class="btn-check"
									autocomplete="off"
									v-model="changeIsDowntimeModel"
								/>
								<label
									class="btn btn-outline-primary"
									for="isDowntime"
									>{{ isDowntime() }}</label
								>
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
						v-on:click="submitChangeTask($event)"
					>
						Add Change Task
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");
	import Editor from "@tinymce/tinymce-vue";
	import BetweenDates from "../../dates/BetweenDates.vue";
	import { NSelect } from "naive-ui";

	//Import mixins
	import errorModalMixin from "../../../mixins/errorModalMixin";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "RfcNewRunItem",
		components: {
			BetweenDates,
			editor: Editor,
			NSelect,
		},
		props: {
			locationId: {
				type: Number,
				default: 0,
			},
			userList: {
				type: Array,
				default: () => {
					return [];
				},
			},
		},
		mixins: [errorModalMixin],
		data: () => ({
			assignedUserModel: "",
			changeDescriptionModel: "",
			changeEndDateModel: "",
			changeIsDowntimeModel: false,
			changeStakeholderModel: "Stakeholder(s)",
			changeStartDateModel: "",
			changeTitleModel: "",
			qaUserModel: "",
			userListFixed: [],
		}),
		computed: {
			...mapGetters({
				rfcEndDate: "getEndDate",
				rfcStartDate: "getStartDate",
				rootUrl: "getRootUrl",
			}),
		},
		methods: {
			formatDate: function (date) {
				//Setup the date
				let new_date = new Date(date);

				//Split the date into date vs time
				new_date = new_date.toISOString().split("T");

				//Split the time
				const time_split = new_date[1].split(".");

				//Return the date as a string
				return `${new_date[0]} ${time_split[0]}`;
			},
			isDowntime: function () {
				if (this.changeIsDowntimeModel) {
					return `Downtime Scheduled`;
				}
				return `No Downtime`;
			},
			submitChangeTask: function (event) {
				//Stop the usual stuff
				event.preventDefault();

				var change_task_seconds =
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
					"change_task_description",
					this.changeDescriptionModel
				);
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
				data_to_send.set(
					"change_task_required_by",
					this.changeStakeholderModel
				);
				data_to_send.set("is_downtime", this.changeIsDowntimeModel);

				axios
					.post(
						`${this.rootUrl}rfc_information/${this.locationId}/new_change_task/`,
						data_to_send
					)
					.then((response) => {
						//Update the runsheet variables
						this.$emit("update_change_task_list", response.data);

						//Clear the modal
						this.changeDescriptionModel = "";
						//this.changeEndDateModel = '';
						this.changeIsDowntimeModel = false;
						this.changeStakeholderModel = "Stakeholder(s)";
						//this.changeStartDateModel = '';
						this.changeTitleModel = "";

						//Close the modal
						document
							.getElementById("newRunItemCloseButton")
							.click();
					})
					.catch((error) => {
						this.showErrorModal(error, "Change Task");
					});
			},
			updateDates: function (data) {
				this.changeStartDateModel = data.start_date;
				this.changeEndDateModel = data.end_date;
			},
		},
		mounted() {
			this.userListFixed = this.userList.map((row) => {
				return {
					label: `${row.username}: ${row.first_name} ${row.last_name}`,
					value: row.id,
				};
			});
		},
	};
</script>

<style scoped></style>
