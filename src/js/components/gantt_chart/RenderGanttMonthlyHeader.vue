<template>
	<div class="gantt-header">
		<div class="gantt-header--information"></div>
		<div class="gantt-header--months">
			<div
				v-for="month in this.monthArray"
				:key="month.index"
				class="gantt-header--month"
				v-bind:style="`width: ${month.width}px`"
			>
				<span>{{month.month}} {{month.year}}</span>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "RenderGanttMonthlyHeader",
	props: {},
	data() {
		return {
			monthArray: [],
			monthDictionary: {
				0: "Jan",
				1: "Feb",
				2: "March",
				3: "April",
				4: "May",
				5: "June",
				6: "July",
				7: "August",
				8: "September",
				9: "October",
				10: "November",
				11: "December",
			},
		}
	},
	computed: {
		...mapGetters({
			deltaDays: "getDeltaDays",
			endDateGantt: "getEndDateGantt",
			startDateGantt: "getStartDateGantt",
		}),
	},
	watch: {
		deltaDays() {
			this.generateHeader();
		},
	},
	methods: {
		generateHeader() {
			//Blank out month array
			this.monthArray = [];

			//Setup local variables
			const start_date = new Date(this.startDateGantt);
			const end_date = new Date(this.endDateGantt);
			let point_date = start_date;
			let next_date = end_date;

			let keep_looping = true;
			let index = 0;
			while (keep_looping) {
				let delta = 0;

				//Determine if end date is in the current month
				if (point_date.getMonth() === end_date.getMonth()) {
					//Months are the same. Get the delta between the dates and call it a day
					keep_looping = false;

					//Get delta then the width of the object :)
					delta = Math.round((end_date.getTime() - point_date.getTime()) / (1000 * 60 * 60 * 24)) + 1;
				} else {
					//Months are different. Get the point date for the first of next month
					if (point_date.getMonth() === 11) {
						//Point date is in December. We want next year
						next_date = new Date(point_date.getFullYear() + 1, 0, 1);
					} else {
						next_date = new Date(point_date.getFullYear(), point_date.getMonth() + 1, 1);
					}

					//Get the delta
					delta = Math.round((next_date.getTime() - point_date.getTime()) / (1000 * 60 * 60 * 24));
				}

				this.monthArray.push({
					index,
					delta,
					width: delta * 48,
					month: this.monthDictionary[point_date.getMonth()],
					year: point_date.getFullYear(),
				});

				//Cycle up the variables
				index = index + 1;
				point_date = next_date;
			}
		},

	},
}
</script>