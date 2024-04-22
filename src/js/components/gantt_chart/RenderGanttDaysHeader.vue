<template>
	<div class="gantt-header">
		<div class="gantt-header--information"></div>
		<div class="gantt-header--dates">
			<div
				v-for="index in deltaDays"
				:key="index"
				class="gantt-header--date"
			>
				<div class="dayDate">
					{{getDayDate(index)}}
				</div>
				<div class="dayText">
					{{getDayText(index)}}
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
				0: "S",
				1: "M",
				2: "T",
				3: "W",
				4: "T",
				5: "F",
				6: "S",
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