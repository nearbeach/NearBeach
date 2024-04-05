<template>
	<div class="row">
		<strong>Run Sheet List</strong>
		<p class="text-instructions">
			The run sheet will specify specific tasks for each user to
			implement. Each run item can be specified to;<br/>
			- Block other run items<br/>
			- Block out downtime
		</p>
	</div>

	<!-- LOOP FOR CHANGE TASKS -->
	<div v-if="changeTaskList.length > 0">
		<div v-for="changeTask in changeTaskList"
			 v-bind:key="changeTask.change_task_id"
             v-bind:class="detailClasses(changeTask.change_task_status)"
    >
			<a class="change-task--name"
			   v-bind:href="`${rootUrl}change_task_information/${changeTask.change_task_id}/`"
			>
				{{ changeTask.change_task_title }}
			</a>

			<a class="change-task--dates"
			   v-bind:href="`${rootUrl}change_task_information/${changeTask.change_task_id}/`"
			>
				{{ getNiceDatetime(changeTask.change_task_start_date) }} -
				{{ getNiceDatetime(changeTask.change_task_end_date) }}
			</a>

			<a class="change-task--responsibility"
			   v-bind:href="`${rootUrl}change_task_information/${changeTask.change_task_id}/`"
			>
				<div>
					Assigned User:
					<span class="small-text">
						{{ getUserName(changeTask.change_task_assigned_user_id) }}
					</span>
				</div>
				<div>
					QA User:
					<span class="small-text">
						{{ getUserName(changeTask.change_task_qa_user_id) }}
					</span>
				</div>
			</a>

			<div class="change-task--status">
				Status:
				<span class="small-text">
					{{ getStatus(changeTask.change_task_status) }}
				</span>
			</div>

			<div v-if="changeTask.is_downtime">Downtime Scheduled</div>

			<div v-if="blockedBy(changeTask.change_task_id).length > 0">
				<div class="change-task--blocked-by">
					Change task currently blocked by;
					<ul>
						<li v-for="singleBlock in blockedBy(changeTask.change_task_id)"
							:key="singleBlock.object_assignment_id"
						>
							<a v-bind:href="`${this.rootUrl}change_task_information/${singleBlock.change_task_id}/`"
							>
								{{ singleBlock.change_task_title }}
							</a>
						</li>
					</ul>
				</div>
			</div>
			<div v-else-if="userLevel > 1 && rfcStatus === 4"
				 class="change-task--buttons"
			>
				<!-- START TASK -->
				<button class="btn btn-primary"
						v-on:click="updateChangeTaskStatus(changeTask.change_task_id, 4)"
						v-if="[3, 7, 8].includes(changeTask.change_task_status)"
				>
					Start Task
				</button>

				<!-- PAUSE -->
				<button class="btn btn-secondary"
						v-on:click="updateChangeTaskStatus(changeTask.change_task_id, 7)"
						v-if="[4].includes(changeTask.change_task_status)"
				>
					Pause Task
				</button>

				<!-- READY FOR QA -->
				<button class="btn btn-info"
						v-on:click="updateChangeTaskStatus(changeTask.change_task_id, 8)"
						v-if="[4].includes(changeTask.change_task_status)"
				>
					Set Task Ready for QA
				</button>

				<!-- SUCCESS -->
				<button class="btn btn-success"
						v-on:click="openConfirmModal(changeTask.change_task_id, 'Success', 5)"
						v-if="[8].includes(changeTask.change_task_status)"
				>
					Set Task to Success
				</button>

				<!-- FAIL -->
				<button class="btn btn-danger"
						v-on:click="openConfirmModal(changeTask.change_task_id, 'Failure', 9)"
						v-if="[4, 8].includes(changeTask.change_task_status)"
				>
					Set Task to Fail
				</button>
			</div>
		</div>
	</div>

	<div
		class="alert alert-primary"
		v-else
	>
		Currently there are no Change Tasks associated with this Request
		for Change. Please add some by clicking on the button below.
	</div>
	<div class="row">
		<!-- ADD NEW CHANGE TASK TO RUN SHEET -->
		<div
			class="row submit-row"
			v-if="!isReadOnly"
		>
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="addNewChangeItem"
					v-if="userLevel > 1"
				>New Change Item</a
				>
			</div>
		</div>

		<!-- If ALL Change Tasks have been completed - you can close the RFC -->
		<div
			class="row submit-row"
			v-if="isCompleted"
		>
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-warning save-changes"
					v-on:click="closeRfc"
					v-if="userLevel > 1"
				>Close Request for Change</a
				>
			</div>
		</div>

		<!-- Modal -->
		<new-change-task
			v-bind:location-id="locationId"
			v-bind:user-list="userList"
			v-on:update_change_task_list="updateChangeTaskList($event)"
			v-if="!isReadOnly"
		></new-change-task>
	</div>

	<!-- Confirm Change Task Closure -->
	<confirm-change-task-closure
		v-bind:closure-id="closureId"
		v-bind:closure-status="closureStatus"
		v-bind:closure-status-id="closureStatusId"
		v-on:close_change_task="closeChangeTask($event)"
	></confirm-change-task-closure>
</template>

<script>
import {Modal} from "bootstrap";
import ConfirmChangeTaskClosure from "./ConfirmChangeTaskClosure.vue";
import NewChangeTask from "../../change_task/NewChangeTask.vue";

// Mixins
import datetimeMixin from "../../../mixins/datetimeMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "ChangeTaskList",
	components: {
		ConfirmChangeTaskClosure,
		NewChangeTask,
	},
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		locationId: {
			type: Number,
			default: 0,
		},
		rfcId: {
			type: Number,
			default: 0,
		},
		rfcStatus: {
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
	mixins: [datetimeMixin],
	data: () => ({
		blockedTaskList: [],
		changeTaskList: [],
		closureId: 0,
		closureStatus: "",
		closureStatusId: 0,
	}),
	computed: {
		...mapGetters({
			userLevel: "getUserLevel",
			rfcEndDate: "getEndDate",
			rfcReleaseDate: "getReleaseDate",
			rootUrl: "getRootUrl",
		}),
		isCompleted() {
			const count_of_uncompleted_tasks = this.changeTaskList.filter(
				(changeTask) => {
					const change_task_status =
						changeTask.change_task_status;
					return (
						//Finished, Rejected, Failed
						change_task_status !== 5 && change_task_status !== 6 && change_task_status !== 9
					);
				}
			).length;

			//Return true when there are no uncompleted tasks (all finished)
			return (
				count_of_uncompleted_tasks === 0 &&
				(this.rfcStatus === 3 || this.rfcStatus === 4)
			);
		},
	},
	methods: {
		addNewChangeItem() {
			const newChangeTaskModal = new Modal(
				document.getElementById("newRunItemModal")
			);
			newChangeTaskModal.show();
		},
		blockedBy: function (change_task_id) {
			/*
			The blockedBy function accepts the current change_task_id.

			We are trying to find out which change tasks currently block the change_task_id.

			There are two possible solutions;
			1. parent link = change_task + meta_object = change_task_id
			2. parent link = meta_object + change_task_id = change_task_id

			We ignore all change tasks that are currently completed. i.e. failed or success.
			*/
			let condition_1 = this.blockedTaskList.filter((row) => {
				return row.parent_link === "change_task" & row.meta_object === change_task_id;
			}).map((row) => {
				return row.change_task_id;
			}) //Meta object is blocked by change task

			let condition_2 = this.blockedTaskList.filter((row) => {
				return row.parent_link === "meta_object" & row.change_task_id === change_task_id;
			}).map((row) => {
				return row.meta_object;
			}) //Change task is blocked by meta object

			//Finished Change Task status ids
			const finished_status = [5, 6];

			//Filter and map out data we want
			condition_1 = this.changeTaskList.filter((row) => {
				return condition_1.includes(row.change_task_id) && !finished_status.includes(row.change_task_status);
			}).map((row) => {
				return {
					"change_task_id": row.change_task_id,
					"change_task_title": row.change_task_title,
				}
			});

			condition_2 = this.changeTaskList.filter((row) => {
				return condition_2.includes(row.change_task_id) && !finished_status.includes(row.change_task_status);
			}).map((row) => {
				return {
					"change_task_id": row.change_task_id,
					"change_task_title": row.change_task_title,
				}
			});

			//Add both arrays together and send back
			return condition_1.concat(condition_2);
		},
		closeChangeTask(options) {
			//User has selectes YES to close the change task from the modal
			this.updateChangeTaskStatus(options.closureId, options.closureStatusId);
		},
		closeRfc() {
			//Construct the data to send
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", 5);

			this.axios.post(
				`${this.rootUrl}rfc_information/${this.rfcId}/update_status/`,
				data_to_send
			).then((response) => {
				//Refresh Page
				window.location.reload(true);
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error closing the RFC",
					message: `Sorry, we could not close the rfc. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
        detailClasses(status) {
            //If status is fail (9), then return the change-task--fail
            if (parseInt(status) === 9) {
                return "row change-task--detail bg-danger";
            }

            return "row change-task--detail";
        },
		getRunSheetList() {
			this.axios.post(
				`${this.rootUrl}rfc_information/${this.locationId}/change_task_list/`
			).then((response) => {
				// Update the blockedTaskList and changeTaskList
				this.blockedTaskList = response.data.blocked_list;
				this.changeTaskList = response.data.change_tasks;

				// Update the changeTaskCount in statemanagement
				this.$store.commit({
					type: "updateChangeTaskCount",
					changeTaskCount: response.data.change_tasks.length,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting run sheet list",
					message: `Sorry, we could not retrieve the run sheet list. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getStatus(status_id) {
			switch (status_id) {
				case 1:
					return "Draft";

				case 2:
					return "Waiting for approval";

				case 3:
					return "Waiting to start";

				case 4:
					return "Task Started";

				case 5:
					return "Task Finished Successfully";

				case 6:
					return "Task REJECTED";

				case 7:
					return "PAUSED Task"

				case 8:
					return "Ready for QA"

				case 9:
					return "Task FAILED";

				default:
					return "---";
			}
		},
		getUserName(user_id) {
			//Filter for the user by using the user_id
			const single_user = this.userList.filter((row) => {
				return row.id == user_id;
			});

			//If there are no results - default to ---
			if (single_user.length === 0) {
				return "---";
			}

			//User was filtered out - return their name
			return `${single_user[0].username}: ${single_user[0].first_name} ${single_user[0].last_name}`;
		},
		openConfirmModal(closureId, closureStatus, closureStatusId) {
			//Update the data
			this.closureId = closureId;
			this.closureStatus = closureStatus;
			this.closureStatusId = closureStatusId;

			//Open the modal
			const confirmModal = new Modal(
				document.getElementById("confirmChangeTaskClosure")
			);
			confirmModal.show();
		},
		updateChangeTaskList(data) {
			//Update blocked task & change task list
			this.blockedTaskList = data.blocked_list;
			this.changeTaskList = data.change_tasks;

			//Send the new count upstream
			this.$store.commit({
				type: "updateChangeTaskCount",
				changeTaskCount: data.change_tasks.length,
			});

			//Update the rfc start/end/release dates based off the data
			this.updateRfcDates();
		},
		updateChangeTaskStatus(
			change_task_id,
			change_task_status
		) {
			//Construct data to send
			const data_to_send = new FormData();
			data_to_send.set("change_task_status", change_task_status);

			this.axios.post(
				`${this.rootUrl}change_task_update_status/${change_task_id}/`,
				data_to_send
			).then((response) => {
				/*
				We are using the map function to make a single variable change without having to write a loop function.
				The change task has been update, so we are only changing that task when mapping the results back
				to itself.
				 */
				this.changeTaskList = this.changeTaskList.map((changeTask) => {
					//The change task that we have just updated :)
					if (changeTask.change_task_id === change_task_id) {
						//Update the change Task Status
						changeTask.change_task_status = change_task_status;

						//Send back the change task status
						return changeTask;
					} else {
						// Not the change task we updated :(
						return changeTask;
					}
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting user list",
					message: `Sorry, we could not retrieve the user user. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateRfcDates() {
			//If there is no data - do nothing
			if (this.changeTaskList.length === 0) return;

			//Get the delta between the end and release date
			const delta = this.rfcReleaseDate - this.rfcEndDate;

			//Get the minimum start date from the change task list
			const start_object = this.changeTaskList.reduce((a, b) => {
				const a_date = new Date(a.change_task_start_date);
				const b_date = new Date(b.change_task_start_date);

				return a_date < b_date ? a : b;
			});
			const start_date = new Date(start_object.change_task_start_date);

			//Get the maximum end date from the change task list
			const end_object = this.changeTaskList.reduce((a, b) => {
				const a_date = new Date(a.change_task_end_date);
				const b_date = new Date(b.change_task_end_date);

				return a_date > b_date ? a : b;
			});
			const end_date = new Date(end_object.change_task_end_date);

			const release_date = end_date.getTime() + delta;

			this.$store.commit({
				type: "updateRfcDates",
				endDateModel: end_date.getTime(),
				releaseDateModel: release_date,
				startDateModel: start_date.getTime(),
			});
		},
	},
	mounted() {
		// Get the run sheet list
		this.getRunSheetList();
	},
};
</script>

<style scoped></style>
