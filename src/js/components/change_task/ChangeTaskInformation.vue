<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Change Task - {{ changeTaskResults[0].pk }}</h1>
				<br/>
				RFC Status: {{ rfcStatus }}
				<br/>
				<a
					v-bind:href="`${this.rootUrl}rfc_information/${changeTaskResults[0].fields.request_for_change}`"
				>Go back</a
				>
				<hr/>

				<!-- CHANGE TASK TITLE -->
				<div class="row">
					<div class="col-md-4">
						<strong>Change Task Title</strong>
						<p class="text-instructions">
							Please write a short title of the description for this
							task. i.e Backup of Database
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
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Date Restrictions</strong>
						<p class="text-instructions">
							Start and End dates of the RFC
						</p>
					</div>
					<div class="col-md-4">
						Start Date: <span>{{ formatDate(rfcStartDate) }}</span>
					</div>
					<div class="col-md-4">
						End Date: <span>{{ formatDate(rfcEndDate) }}</span>
					</div>
				</div>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="Change Task"
					v-bind:start-date-model="changeStartDateModel"
					v-bind:end-date-model="changeEndDateModel"
					v-bind:no-back-dating="false"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<!-- IMPLEMENTATION USER & QA USER -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Implementation & QA User</strong>
						<p class="text-instructions">
							Please indicate which user will be implementing the
							work, and the user who will QA.
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

				<!-- GO BACK -->
				<hr v-if="userLevel > 1"/>
				<!-- CANCEL -->
				<a
					v-if="userLevel > 1"
					v-bind:href="`${rootUrl}rfc_information/${changeTaskResults[0].fields.request_for_change}/`"
					class="btn btn-secondary cancel-changes"
				>Cancel</a
				>

				<!-- DELETE -->
				<a
					href="javascript:void(0)"
					class="btn btn-warning"
					v-if="
					changeTaskResults[0].fields.change_task_status == 1 &&
					userLevel == 4
				"
					v-on:click="confirmDeleteChangeTask"
				>Delete</a
				>

				<!-- SAVE -->
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-if="
					changeTaskResults[0].fields.change_task_status == 1 &&
					userLevel >= 2
				"
					v-on:click="saveChangeTask"
				>Save</a
				>

				<!-- START CHANGE TASK -->
				<a
					href="javascript:void(0)"
					class="btn btn-danger save-changes"
					v-if="
					changeTaskResults[0].fields.change_task_status == 3 &&
					userLevel >= 2 &&
					rfcStatus === 'Started'
				"
					v-on:click="updateStatus(4)"
				>Start Task</a
				>

				<!-- FINISH CHANGE TASK -->
				<a
					href="javascript:void(0)"
					class="btn btn-success save-changes"
					v-if="
					changeTaskResults[0].fields.change_task_status == 4 &&
					userLevel >= 2
				"
					v-on:click="updateStatus(5)"
				>Finish Task</a
				>

				<!-- REJECT CHANGE TASK -->
				<a
					href="javascript:void(0)"
					class="btn btn-danger save-changes"
					v-if="
					changeTaskResults[0].fields.change_task_status == 4 &&
					userLevel >= 2
				"
					v-on:click="updateStatus(6)"
				>REJECT Task</a
				>
			</div>
		</div>

		<confirm-change-task-delete
			v-bind:change-task-results="changeTaskResults"
		></confirm-change-task-delete>
	</n-config-provider>
</template>

<script>
//Widgets
import BetweenDates from "../dates/BetweenDates.vue";
import {NSelect} from "naive-ui";
import {Modal} from "bootstrap";

//Vuex
import {mapGetters} from "vuex";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

//Components
import ConfirmChangeTaskDelete from "./modules/ConfirmChangeTaskDelete.vue";

export default {
	name: "ChangeTaskInformation",
	components: {
		BetweenDates,
		ConfirmChangeTaskDelete,
		NSelect,
	},
	props: {
		changeTaskResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
		rfcStatus: {
			type: String,
			default: "Empty Status",
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
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
	data() {
		return {
			assignedUserModel:
			this.changeTaskResults[0].fields.change_task_assigned_user,
			changeTitleModel:
			this.changeTaskResults[0].fields.change_task_title,
			changeStartDateModel: new Date(
				this.changeTaskResults[0].fields.change_task_start_date
			).getTime(),
			changeEndDateModel: new Date(
				this.changeTaskResults[0].fields.change_task_end_date
			).getTime(),
			qaUserModel:
			this.changeTaskResults[0].fields.change_task_qa_user,
			userListFixed: this.userList.map((row) => {
				return {
					label: `${row.username}: ${row.first_name} ${row.last_name}`,
					value: row.id,
				};
			}),
		};
	},
	mixins: [
		getThemeMixin,
	],
	computed: {
		...mapGetters({
			rfcEndDate: "getEndDate",
			rfcStartDate: "getStartDate",
		}),
	},
	methods: {
		confirmDeleteChangeTask() {
			const modal = new Modal(document.getElementById("confirmChangeTaskDeleteModal"));
			modal.show();
		},
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
		saveChangeTask(event) {
			//Stop the usual stuff
			event.preventDefault();

			const change_task_seconds =
				this.changeEndDateModel - this.changeStartDateModel;

			// Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("change_task_title", this.changeTitleModel);
			// data_to_send.set(
			// 	"change_task_description",
			// 	this.changeDescriptionModel
			// );
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
			// data_to_send.set(
			// 	"change_task_required_by",
			// 	this.changeStakeholderModel
			// );
			// data_to_send.set("is_downtime", this.changeIsDowntimeModel);

			this.axios
				.post(
					`${this.rootUrl}change_task_information/${this.changeTaskResults[0].pk}/save/`,
					data_to_send
				)
				.then((response) => {
					//If successful, go back
					this.$store.dispatch("newToast", {
						header: "Saved Change Task",
						message: "Your change task has saved.",
						extra_classes: "bg-success",
						unique_type: "save",
					});
					//window.location.href = `${this.rootUrl}rfc_information/${this.changeTaskResults[0].fields.request_for_change}/`;
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Can not save",
						message: "Sorry, we could not save your change task",
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		updateStatus(new_status) {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("change_task_status", new_status);

			//Use axios to send the data
			this.axios
				.post(
					`${this.rootUrl}change_task_update_status/${this.changeTaskResults[0].pk}/`,
					data_to_send
				)
				.then((response) => {
					//Reload the page
					window.location.reload(true);
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Can not save",
						message: "Sorry, we could not save your change task",
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
		updateDates(data) {
			this.changeStartDateModel = data.start_date;
			this.changeEndDateModel = data.end_date;
		},
	},
	mounted() {
		//Send data to required VueX states
		this.$store.commit({
			type: "updateDestination",
			destination: this.destination,
			locationId: this.locationId,
		});
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});
		this.$store.commit({
			type: "updateChangeTask",
			description: this.changeTaskResults[0].fields.change_task_description,
			endDate: this.changeTaskResults[0].fields.change_task_end_date,
			isDowntime: this.changeTaskResults[0].fields.is_downtime,
			requiredBy: this.changeTaskResults[0].fields.change_task_required_by,
			startDate: this.changeTaskResults[0].fields.change_task_start_date,

		});
		// changeIsDowntimeModel:
	},
};
</script>

<style scoped>
.save-changes {
	margin-left: 10px;
}
</style>
