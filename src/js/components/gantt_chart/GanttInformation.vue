<template>
	<div class="gantt-chart">
	</div>
</template>

<script>
import {mapGetters} from "vuex";
import TestGanttChart from "./TestGanttChart.vue";
import {DateTime} from "luxon";

export default {
	name: "GanttChart",
	components: {TestGanttChart},
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