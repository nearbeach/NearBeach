<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="gantt-chart"
			 v-on:mouseup="mouseUp"
			 v-on:mouseleave="mouseLeave"
			 v-on:mousemove="mouseMove"
		>
			<render-gantt-monthly-header></render-gantt-monthly-header>
			<render-gantt-days-header></render-gantt-days-header>

			<!-- RENDER EACH GANTT ROW-->
			<render-gantt-row
				v-for="(row, index) in ganttChartData"
				:key="index"
				v-bind:end-date="row.end_date"
				v-bind:index="index"
				v-bind:object-type="row.object_type"
				v-bind:higher-order-status="row.higher_order_status"
				v-bind:start-date="row.start_date"
				v-bind:status-id="row.status_id"
				v-bind:title="row.title"
				v-on:mouse_down="mouseDown"
			></render-gantt-row>
		</div>
	</n-config-provider>
</template>

<script>
import {mapGetters} from "vuex";
import {DateTime} from "luxon";
import {NConfigProvider} from "naive-ui";

//Components
import RenderGanttDaysHeader from "./RenderGanttDaysHeader.vue";
import RenderGanttMonthlyHeader from "./RenderGanttMonthlyHeader.vue";
import TestGanttChart from "./TestGanttChart.vue";
import RenderGanttRow from "./RenderGanttRow.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "GanttChart",
	components: {
		RenderGanttRow,
		RenderGanttDaysHeader,
		RenderGanttMonthlyHeader,
		TestGanttChart
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
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "light",
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			isMouseDown: false,

			//Mouse Down Variables
			mdClientXInitial: 0,
			mdIndex: 0,
			mdObjectType: "",
			mdColumn: "",
			mdEndDateInitial: 0,
			mdHigherOrderStatus: "",
			mdStartDateInitial: 0,
			mdStatus: "",
			mdTitle: "",
		}
	},
	mixins: [
		getThemeMixin,
	],
	computed: {
		...mapGetters({
			ganttChartData: "getGanttChartData",
		}),
	},
	methods: {
		initialiseData() {
			//Escape conditions
			if (this.destination === "") return;
			if (this.locationId === 0) return;

			//Get Data from backend
			this.axios.post(
				`${this.rootUrl}gantt_data/${this.destination}/${this.locationId}/get_data/`,
			).then((response) => {
				//Get the dates
				const end_date = DateTime.fromISO(this.ganttEndDate);
				const start_date = DateTime.fromISO(this.ganttStartDate);

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
		mouseDown(data) {
			//Update the mouse down variables
			this.mdClientXInitial = data.mdClientXInitial;
			this.mdHigherOrderStatus = data.mdHigherOrderStatus;
			this.mdIndex = data.mdIndex;
			this.mdObjectType = data.mdObjectType;
			this.mdColumn = data.mdColumn;
			this.mdEndDateInitial = data.mdEndDateInitial;
			this.mdStartDateInitial = data.mdStartDateInitial;
			this.mdStatus = data.mdStatus;
			this.mdStatusId = data.mdStatusId;
			this.mdTitle = data.mdTitle;

			//Mouse is now down
			this.isMouseDown = true;
		},
		mouseLeave(event) {
			event.preventDefault();

			//Tell the system the mouse is no longer down
			this.isMouseDown = false;
		},
		mouseMove(event) {
			//Prevents default
			event.preventDefault();

			//Make sure not on a touch device
			const touch = matchMedia('(hover: none)').matches;
			if (touch) return;

			//Make sure mouse is down
			if (this.isMouseDown !== true) return

			//Deal with the mouse movement
			const client_x_final = event.clientX;

			//Get the number of dates from this
			const delta = Math.floor((client_x_final - this.mdClientXInitial) / 35) * (24 * 60 * 60 * 1000);

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
			this.isMouseDown = false;
		},
		updateEnd(delta) {
			//Apply the delta to the dates
			const end_date = new Date(this.mdEndDateInitial + delta);

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				index: this.mdIndex,
				value: {
					end_date: end_date.getTime(),
					higher_order_status: this.mdHigherOrderStatus,
					object_type: this.mdObjectType,
					start_date: this.mdStartDateInitial,
					status_id: this.mdStatusId,
					title: this.mdTitle,
				},
			});
		},
		updateMiddle(delta) {
			//Apply the delta to the dates
			const end_date = new Date(this.mdEndDateInitial + delta);
			const start_date = new Date(this.mdStartDateInitial + delta);

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				index: this.mdIndex,
				value: {
					end_date: end_date.getTime(),
					higher_order_status: this.mdHigherOrderStatus,
					object_type: this.mdObjectType,
					start_date: start_date.getTime(),
					status_id: this.mdStatusId,
					title: this.mdTitle,
				},
			});
		},
		updateStart(delta) {
			//Apply the delta to the dates
			const start_date = new Date(this.mdStartDateInitial + delta);

			//Update VueX with the new dates\
			this.$store.dispatch("updateGanttChartSingleRow", {
				index: this.mdIndex,
				value: {
					end_date: this.mdEndDateInitial,
					higher_order_status: this.mdHigherOrderStatus,
					object_type: this.mdObjectType,
					start_date: start_date.getTime(),
					status_id: this.mdStatusId,
					title: this.mdTitle,
				},
			});
		},
	},
	mounted() {
		this.initialiseData();
	},
}
</script>