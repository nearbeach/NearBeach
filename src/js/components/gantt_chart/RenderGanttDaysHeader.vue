<template>
	<div class="gantt-header">
		<div class="gantt-header--information">
			<div class="gantt-header--title">Object Title</div>
			<div class="gantt-header--start-date">Start Date</div>
			<div class="gantt-header--end-date">End Date</div>
			<div class="gantt-header--status">Status</div>
		</div>
		<div class="gantt-header--dates">
			<div
				v-for="index in deltaDays + 1"
				:key="index"
				class="gantt-header--date"
			>
				<div class="dayDate">
					{{getDayDate(index - 1)}}
				</div>
				<div class="dayText">
					{{getDayText(index - 1)}}
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "RenderGanttDaysHeader",
	props: {},
	data() {
		return {
			dateDictionary: {
				0: "Sun",
				1: "Mon",
				2: "Tue",
				3: "Wed",
				4: "Thu",
				5: "Fri",
				6: "Sat",
			},
		};
	},
	computed: {
		...mapGetters({
			deltaDays: "getDeltaDays",
			endDateGantt: "getEndDateGantt",
			startDateGantt: "getStartDateGantt",
		}),
	},
	methods: {
		getDayDate(index) {
			const delta = index * 24 * 60 * 60 * 1000;
			const new_date = new Date(this.startDateGantt + delta);
			return this.dateDictionary[new_date.getDay()];
		},
		getDayText(index) {
			const delta = index * 24 * 60 * 60 * 1000;
			const new_date = new Date(this.startDateGantt + delta);
			return new_date.getDate();
		},
	},
}
</script>