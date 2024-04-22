<template>
	<div class="gantt-chart">
		<render-gantt-monthly-header></render-gantt-monthly-header>
		<render-gantt-days-header></render-gantt-days-header>

		<!-- RENDER EACH GANTT ROW-->
		<render-gantt-row
			v-for="(row, index) in ganttChartData"
			:key="index"
			v-bind:end-date="row.end_date"
			v-bind:index="index"
			v-bind:object-type="row.object_type"
			v-bind:start-date="row.start_date"
			v-bind:status-id="row.status_id"
			v-bind:title="row.title"
		></render-gantt-row>
	</div>
</template>

<script>
import {mapGetters} from "vuex";
import {DateTime} from "luxon";

//Components
import RenderGanttDaysHeader from "./RenderGanttDaysHeader.vue";
import RenderGanttMonthlyHeader from "./RenderGanttMonthlyHeader.vue";
import TestGanttChart from "./TestGanttChart.vue";
import RenderGanttRow from "./RenderGanttRow.vue";

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

				this.$store.dispatch("initialiseGanttChartData", {
					ganttChartData: response.data,
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
	},
	mounted() {
		this.initialiseData();
	},
}
</script>