<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<h1 class="planner-header">My Planner</h1>
		<button class="btn btn-primary planner-button"
				v-on:click="showModal"
		>Add Object</button>

		<div class="my-planner">
			<!-- HEADER -->
			<div class="my-planner--header">
				<div
					v-for="day in dateArray"
					:key="day.date"
					class="my-planner--header-single-day"
				>
					<p>
						{{ day.day }}<br/>
						<span class="text-instructions">{{ day.date }}</span>
					</p>
				</div>
			</div>

			<!-- BODY -->
			<div class="my-planner--body">
				<draggable
					class="my-planner--single-day list-group"
					group="objects"
					ghost-class="ghost"
					itemKey="user_job_id"
					v-for="(day, index) in dateArray"
					v-bind:data-job-date="day.date"
					v-bind:data-index="index"
					v-bind:move="move"
					:key="day.date"
					:list="day.data"
					@end="onEnd($event)"

				>
					<template #item="{ element }">
						<div class="list-group-item"
							 v-bind:data-user-job-id="element.user_job_id"
							 v-bind:data-object-type="element.object_type"
							 v-bind:data-location-id="element.location_id"
						>
							<div v-if="element.higher_order_status !== 'Closed'"
								class="card-priority-line priority-normal"></div>
							<div class="text-instructions">
								  {{ formatObjectId(element) }}
							</div>
							<div><strong v-bind:class="getClass(element.higher_order_status)">
								{{ element.title }}
							</strong></div>
							<div>Status: <span class="text-instructions">{{ element.status }}</span></div>
							<carbon-trash-can
								class="kanban-card-info-icon"
								style="color: red;"
								v-on:click="confirmCardDelete(element.user_job_id, index)"
								v-on:dblclick="confirmCardDelete(element.user_job_id, index)"
							></carbon-trash-can>
						</div>
					</template>
				</draggable>

			</div>
		</div>

		<confirm-user-job-delete
			v-bind:user-job-id="confirmIdToDelete"
			v-on:remove_user_job="removeUserJob"
		></confirm-user-job-delete>

		<new-planner-object-wizard
			v-bind:date-array="dateArray"
			v-on:update_date_array="updateDateArray($event)"
		></new-planner-object-wizard>
	</n-config-provider>
</template>

<script>
import draggable from "vuedraggable";
import { DateTime } from "luxon";
import { Modal } from "bootstrap";

//Component
import ConfirmUserJobDelete from "./ConfirmUserJobDelete.vue";
import NewPlannerObjectWizard from "./NewPlannerObjectWizard.vue";

//Composable
import {CarbonTrashCan} from "../../components";

//Composables
import { useNiceDatetime } from "../../composables/datetime/useNiceDatetime";
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "MyPlanner",
	components: {
		CarbonTrashCan,
		ConfirmUserJobDelete,
		draggable,
		NewPlannerObjectWizard,
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		objectData: {
			type: Array,
			default: () => {
				return [];
			},
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			confirmIdToDelete: 0,
			confirmIndex: 0,
			dateArray: [],
		}
	},
	methods: {
		useNBTheme,
		confirmCardDelete(user_job_id, index) {
			//Update the confirm id
			this.confirmIdToDelete = user_job_id;
			this.confirmIndex = index;

			//Open the modal
			const modal = new Modal(document.getElementById("confirmUserJobDeleteModal"));
			modal.show();
		},
		getClass(closed_status) {
			if (closed_status === "Closed") {
				return "text-decoration-line-through";
			}

			return "";
		},
		formatObjectId(element) {
			const end_date = useNiceDatetime(element.end_date);
			switch (element.object_type) {
				case "kanban_card":
					return `Card${element.location_id}`;
				case "project":
					return `Pro${element.location_id} - ${end_date}`;
				case "task":
					return `Task${element.location_id} - ${end_date}`;
				default:
					return "----";
			}
		},
		move(event) {
			//Get object data
			const new_elem = event.to;
			const object_type = event.dragged.dataset.objectType;
			const location_id = event.dragged.dataset.locationId;

			//Check to make sure the object does not already exist in the final location
			const object_exists = this.dateArray.filter((row) => {
				return row.date === new_elem.dataset.jobDate;
			})[0].data.filter((row) => {
				const condition_1 = row.object_type.toLowerCase() === object_type.toLowerCase();
				const condition_2 = parseInt(row.location_id) === parseInt(location_id);

				return condition_1 && condition_2;
			}).length > 0;

			//Check to see if the object exists
			if (object_exists) {
				//Notify the user
				this.$store.dispatch("newToast", {
					header: "Object Already Exists",
					message: `Sorry, the ${object_type} already exists on ${new_elem.dataset.jobDate}.`,
					extra_classes: "bg-info",
					unique_type: "move_planner_card",
					delay: 1750,
				});

				//Do nothing
				return false;
			}

			return true;
		},
		removeUserJob() {
			this.dateArray[this.confirmIndex].data = this.dateArray[this.confirmIndex].data.filter((row) => {
				return row.user_job_id !== this.confirmIdToDelete;
			});
		},
		onEnd(event) {
			//Short hand some variables
			const new_elem = event.to;
			const old_elem = event.from;
			const user_job_id = event.item.dataset.userJobId;

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("user_job_id", user_job_id);
			data_to_send.set("job_date", new_elem.dataset.jobDate);

			//Setup the sort order for the new destination
			const new_elem_index = new_elem.dataset.index;
			const old_elem_index = old_elem.dataset.index;

			this.dateArray[new_elem_index].data.forEach((row) => {
				data_to_send.append("new_destination", row.user_job_id);
			})

			//Setup the sort order for the old destination
			//Only if the destinations are NOT the same
			if (new_elem_index !== old_elem_index) {
				this.dateArray[old_elem_index].data.forEach((row) => {
					data_to_send.append("old_destination", row.user_job_id);
				});
			}

			//User Axios to update backend
			this.axios.post(
				`${this.rootUrl}my_planner/update_object_list/`,
				data_to_send,
			).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error updating my planner",
					message: `Sorry, we could not update your planner. ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		showModal() {
			const modal = new Modal(document.getElementById("newPlannerObjectWizardModal"));
			modal.show();
		},
		updateDateArray(data) {
			this.dateArray = this.dateArray.map((row) => {
				//Get the latest data for today's date
				const update_data = data.filter((filtered_row) => {
					return filtered_row.job_date === row.date;
				});

				return {
					date: row.date,
					day: row.day,
					data: update_data,
				};
			});
		},
	},
	mounted() {
		//Send root url to the vuex
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//Create an array for the next 7 days, starting from today.
		const today = DateTime.now();

		//Loop for the days
		for (let i = 0; i < 7; i++) {
			//Getting the day information
			const new_day = today.plus({days: i})

			//Filter for the data for this specific day
			const data = this.objectData.filter((row) => {
				return row.job_date === new_day.toFormat("yyyy-LL-dd");
			});

			//Push the data into the data array
			this.dateArray.push({
				date: new_day.toFormat("yyyy-LL-dd"),
				day: new_day.toFormat("cccc"),
				data,
			});
		}
	},
}
</script>