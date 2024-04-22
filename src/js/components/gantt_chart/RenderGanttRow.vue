<template>
	<div class="gantt-row">
		<div class="gantt-row--information">
			<div class="gantt-row--title">
				{{title}}
			</div>
			<div class="gantt-row--start-date">
  				<n-date-picker
					v-model:value="localStartDate"
					type="datetime"
					:on-update-value="updateStartDate"
				/>
			</div>
			<div class="gantt-row--end-date">
				<n-date-picker
					v-model:value="localEndDate"
					type="datetime"
					:on-update-value="updateEndDate"
				></n-date-picker>
			</div>
		</div>

		<div class="gantt-row--render">
			<div class="gantt-row--render-bar">
				<div
					class="gantt-row--spacer"
					v-bind:style="`width: ${spacerWidth}px`"
				></div>
				<div
					class="gantt-row--bar"
					v-bind:style="`width: ${barWidth}px`"
					v-on:mousedown="mouseDown"
				></div>
			</div>
		</div>
	</div>
</template>

<script>
//Components
import { NDatePicker } from "naive-ui";
export default {
	name: "RenderGanttRow",
	props: {
		endDate: {
			type: Number,
			default: 0,
		},
		index: {
			type: Number,
			default: 0,
		},
		objectType: {
			type: String,
			default: "",
		},
		startDate: {
			type: Number,
			default: 0,
		},
		statusId: {
			type: Number,
			default: 0,
		},
		title: {
			type: String,
			default: "",
		},
	},
	components: {
		NDatePicker,
	},
	data() {
		return {
			barWidth: 0,
			localEndDate: this.endDate,
			localStartDate: this.startDate,
			spacerWidth: 0,
			statusId: 0,
		};
	},
	methods: {
		mouseDown() {
			//ADD CODE
		},
		updateEndDate(data) {
			this.$store.dispatch("updateSingleGanttChartRow", {
				index: this.index,
				field: "start_date",
				value: data,
			});
		},
		updateStartDate(data) {
			this.$store.dispatch("updateSingleGanttChartRow", {
				index: this.index,
				field: "start_date",
				value: data,
			});
		}
	},
	mounted() {}
}
</script>