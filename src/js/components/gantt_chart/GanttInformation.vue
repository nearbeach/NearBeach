<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="gantt-chart"
			 v-bind:style="ganttStyle"
			 v-on:mouseup="mouseUp"
			 v-on:mouseleave="mouseLeave"
			 v-on:mousemove="mouseMove"
		>
			<render-gantt-monthly-header></render-gantt-monthly-header>
			<render-gantt-days-header></render-gantt-days-header>

			<!-- RENDER EACH GANTT ROW-->
			<render-gantt-group
				v-for="(row, index) in filteredGanttChartData"
				:key="index"
				v-bind:description="row.description"
				v-bind:end-date="row.end_date"
				v-bind:is-closed="isParentClosed()"
				v-bind:level-number="0"
				v-bind:object-id="row.object_id"
				v-bind:object-type="row.object_type"
				v-bind:parent-object-id="0"
				v-bind:parent-object-type="row.parent_object_type"
				v-bind:higher-order-status="row.higher_order_status"
				v-bind:start-date="row.start_date"
				v-bind:status-id="row.status_id"
				v-bind:title="row.title"
			></render-gantt-group>

			<render-blank-gantt-row></render-blank-gantt-row>

		</div>
	</n-config-provider>

    <div v-if="startDateIssues.length >= 1"
        class="alert alert-warning"
    >
        The following Objects have start dates BEFORE the gantt chart's start date.
        <ul>
            <li v-for="(issue, index) in startDateIssues"
                :key="index"
            >
                {{ issue.object_type }}{{ issue.object_id }} - {{issue.title }}
            </li>
        </ul>
    </div>

    <div v-if="endDateIssues.length >= 1"
         class="alert alert-warning"
    >
        The following Objects have end dates AFTER the gantt chart's end date.
        <ul>
            <li v-for="(issue, index) in endDateIssues"
                :key="index"
            >
                {{ issue.object_type }}{{ issue.object_id }} - {{issue.title }}
            </li>
        </ul>
    </div>

	<confirm-object-remove></confirm-object-remove>
</template>

<script>
import {mapGetters} from "vuex";
import {DateTime} from "luxon";


//Components
import ConfirmObjectRemove from "../modules/wizards/ConfirmObjectRemove.vue";
import RenderGanttDaysHeader from "./RenderGanttDaysHeader.vue";
import RenderGanttMonthlyHeader from "./RenderGanttMonthlyHeader.vue";
import RenderBlankGanttRow from "./RenderBlankGanttRow.vue";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";
import RenderGanttGroup from "./RenderGanttGroup.vue";

export default {
	name: "GanttChart",
	components: {
		RenderGanttGroup,
		ConfirmObjectRemove,
		RenderBlankGanttRow,
		RenderGanttDaysHeader,
		RenderGanttMonthlyHeader,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		ganttEndDate: {
			type: String,
			default: "",
		},
		ganttStartDate: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
		parentStatus: {
			type: String,
			default: "",
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "light",
		},
	},
	data() {
		return {
            endDateIssues: [],
			ganttStyle: "",
            startDateIssues: [],
		}
	},
    watch: {
		deltaDays: {
			handler() {
				this.updateGanttStyle();
			}
		},
        ganttChartData: {
            handler() {
                //Use the method
                this.checkAllObjectsAreWithinDates();
            },
            deep: true,
            immediate: false,
        },
    },
	created() {
		window.addEventListener("resize", this.updateGanttStyle);
	},
	unmounted() {
		window.removeEventListener("resize", this.updateGanttStyle);
	},
	computed: {
		...mapGetters({
			deltaDays: "getDeltaDays",
			ganttChartData: "getGanttChartData",

			//Mouse Down Variables
			isMouseDown: "getIsMouseDown",
			mdClientXInitial: "getMdClientXInitial",
			mdIndex: "getMdIndex",
			mdObjectId: "getMdObjectId",
			mdObjectType: "getMdObjectType",
			mdParentObjectId: "getMdParentObjectId",
			mdParentObjectType: "getMdParentObjectType",
			mdColumn: "getMdColumn",
			mdEndDateInitial: "getMdEndDateInitial",
			mdHigherOrderStatus: "getMdHigherOrderStatus",
			mdStartDateInitial: "getMdStartDateInitial",
			mdStatus: "getMdStatus",
			mdStatusId: "getMdStatusId",
			mdTitle: "getMdTitle",
		}),

		filteredGanttChartData() {
			return this.ganttChartData("", "");
		},
	},
	methods: {
		useNBTheme,
        checkAllObjectsAreWithinDates() {
            //Setup the dates
            const end_date = DateTime.fromISO(this.ganttEndDate);
            const start_date = DateTime.fromISO(this.ganttStartDate);

            //If any of the dates fall outside the time frame, we want to notify the user
            this.endDateIssues = this.ganttChartData.filter((row) => {
                return row.end_date > end_date.ts;
            });

            this.startDateIssues = this.ganttChartData.filter((row) => {
                return row.start_date < start_date.ts;
            });
        },
		initialiseData() {
			//Escape conditions
			if (this.destination === "") return;
			if (this.locationId === 0) return;

			//Get Data from backend
			this.axios.post(
				`${this.rootUrl}gantt_data/${this.destination}/${this.locationId}/get_data/`,
			).then((response) => {
				//Get the dates
				let end_date = DateTime.fromISO(this.ganttEndDate);
				let start_date = DateTime.fromISO(this.ganttStartDate);

				//Set the end/start date's times to 12:00:00AM
				end_date = end_date.set({hour: 0, minute: 0, second: 0, millisecond: 0});
				start_date = start_date.set({hour: 0, minute: 0, second: 0, millisecond: 0});

				//Update the status lists
				this.$store.commit({
					type: "updateGanttStatusList",
					ganttStatusList: response.data.status_results,
				});

				//Initialise gantt chart data
				this.$store.dispatch("initialiseGanttChartData", {
					ganttChartData: response.data.object_results,
					endDateGantt: end_date.ts,
					startDateGantt: start_date.ts,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error fetching Gantt Data",
					message: `Can not retrieve gantt data. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})
		},
		isParentClosed() {
			const closed_status = [
				'finished',
				'closed',
			];

			return closed_status.includes(this.parentStatus.toLowerCase());
		},
		mouseLeave(event) {
			event.preventDefault();

			//Tell the system the mouse is no longer down
			this.$store.commit("updateMouseDown", {
				isMouseDown: false,
			});

			//Check to make sure we need to update the backend
			if (this.mdObjectId !== 0) {
				//Update the backend
				// this.$nextTick(() => {
				// 	this.updateGanttData();
				// });
				this.updateGanttData();
			}
		},
		mouseMove(event) {
			//Prevents default
			event.preventDefault();

			//If closed do nothing
			if (this.isParentClosed()) return;

			//Make sure not on a touch device, simple hand gestures will cause unwanted results. aka bars moving around
			const touch = matchMedia('(hover: none)').matches;
			if (touch) return;

			//Make sure mouse is down - if it isn't, then we don't want anything to move :)
			if (this.isMouseDown !== true) return

			//Deal with the mouse movement
			const client_x_final = event.clientX;

			//Get the number of hours from this
			const delta = Math.floor((client_x_final - this.mdClientXInitial) / 2) * (60 * 60 * 1000);

			//Depending on the column, depends what functionality we are updating.
			switch (this.mdColumn) {
				case "end":
					this.updateEnd(delta);
					break;
				case "middle":
					this.updateMiddle(delta);
					break;
				case "start":
					this.updateStart(delta);
					break;
				default:
					break;
			}
		},
		mouseUp(event) {
			event.preventDefault();

			//Tell the system the mouse is no longer down
			this.$store.commit("updateMouseDown", {
				isMouseDown: false,
			});

			//Update the backend data
			if (this.mdObjectId !== 0) {
				// this.$nextTick(() => {
				// 	this.updateGanttData();
				// });
				this.updateGanttData();
			}
		},
		updateEnd(delta) {
			//Apply the delta to the dates
			const end_date = new Date(this.mdEndDateInitial + delta);

			//Do nothing if the end date is past the sprint's end date
			const g_e_d = DateTime.fromISO(
				this.ganttEndDate
			).set({
				hour: 23,
				minute: 59,
				second: 59,
				millisecond: 999,
			});
			if (this.mdEndDateInitial + delta > g_e_d.ts) return;

			//Do nothing if the end date is less than the start date
			if (this.mdEndDateInitial + delta <= this.mdStartDateInitial) return;

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				end_date: end_date.getTime(),
				higher_order_status: this.mdHigherOrderStatus,
				object_id: this.mdObjectId,
				object_type: this.mdObjectType,
				start_date: this.mdStartDateInitial,
				status_id: this.mdStatusId,
				title: this.mdTitle,
			});
		},
		updateGanttData() {
			//If we are not moving the bar itself, we don't want to complete this function.
			const required_conditions = ["end", "middle", "start"];
			if (!required_conditions.includes(this.mdColumn)) return;

			//Get the data from VueX
			const data = this.$store.getters.getGanttChartDataSingleRow(
				this.mdObjectId,
				this.mdObjectType,
				this.mdParentObjectId,
				this.mdParentObjectType,
			);

			if (data === undefined) {
				this.$store.dispatch("newToast", {
					header: "Error Updating Gantt Data",
					message: "We have had an issue isolating that particular record.",
					extra_classes: "bg-danger",
					delay: 0,
				});

				return;
			}

			//Send updated data to the backend
			const data_to_send = new FormData();
			data_to_send.set('status_id', data.status_id);

			//Handle the start and end date
			const end_date = new Date(data.end_date);
			const start_date = new Date(data.start_date);
			data_to_send.set('end_date', end_date.toISOString());
			data_to_send.set('start_date', start_date.toISOString());

			//Use axios to update backend
			this.axios.post(
				`${this.rootUrl}gantt_data/${data.object_type}/${data.object_id}/update_data/`,
				data_to_send
			).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating the Object",
					message: `Sorry, we could not update the object's information. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});

			//Release the data
			this.$store.commit("updateMouseDown", {
				mdObjectId: 0,
			});
		},
		updateGanttStyle() {
			//Function used to determine the size and margin of the gantt chart.
			//Get the max width of the gantt chart
			const gantt_max_width = 900 + ((this.deltaDays + 1) * 48);

			//Get the width of the screen
			const container_element = document.getElementsByClassName("container-wide")[0];

			//If there is no container - RUN
			if (container_element === undefined) return;

			const screen_width = container_element.clientWidth;

			//If screen width > gantt_max_width, we want to specify the gantt chart size, and margin
			if (parseInt(screen_width) > parseInt(gantt_max_width)) {
				this.ganttStyle = `width:${gantt_max_width}px; margin: 0 10;`;
			} else {
				this.ganttStyle = "width: calc(100vw - 10px);";
			}
		},
		updateMiddle(delta) {
			//Do nothing if the start date is past the sprint's start date
			const g_s_d = DateTime.fromISO(
				this.ganttStartDate
			).set({
				hour: 0,
				minute: 0,
				second: 0,
				millisecond: 0
			});
			if (this.mdStartDateInitial + delta < g_s_d.ts) return;

			//Do nothing if the end date is past the sprint's end date
			const g_e_d = DateTime.fromISO(
				this.ganttEndDate
			).set({
				hour: 23,
				minute: 59,
				second: 59,
				millisecond: 999,
			});
			if (this.mdEndDateInitial + delta > g_e_d.ts) return;

			//Apply the delta to the dates
			const end_date = new Date(this.mdEndDateInitial + delta);
			const start_date = new Date(this.mdStartDateInitial + delta);

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				end_date: end_date.getTime(),
				higher_order_status: this.mdHigherOrderStatus,
				object_id: this.mdObjectId,
				object_type: this.mdObjectType,
				start_date: start_date.getTime(),
				status_id: this.mdStatusId,
				title: this.mdTitle,
			});
		},
		updateStart(delta) {
			//Apply the delta to the dates
			const start_date = new Date(this.mdStartDateInitial + delta);

			//If the start date is less than the gantt start date - do nothing
			const g_s_d = DateTime.fromISO(
				this.ganttStartDate
			).set({
				hour: 0,
				minute: 0,
				second: 0,
				millisecond: 0
			});
			if (this.mdStartDateInitial + delta < g_s_d.ts) return;

			//If the start date is greater or equal to the end date. Do nothing
			if (this.mdStartDateInitial + delta >= this.mdEndDateInitial) return;

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				end_date: this.mdEndDateInitial,
				higher_order_status: this.mdHigherOrderStatus,
				object_id: this.mdObjectId,
				object_type: this.mdObjectType,
				start_date: start_date.getTime(),
				status_id: this.mdStatusId,
				title: this.mdTitle,
			});
		},
	},
	mounted() {
		this.initialiseData();
	},
}
</script>