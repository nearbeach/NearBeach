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
					:on-update-value="updateGanttData"
				/>
			</div>
			<div class="gantt-row--end-date">
				<n-date-picker
					v-model:value="localEndDate"
					type="datetime"
					:on-update-value="updateGanttData"
				></n-date-picker>
			</div>
			<div class="gantt-row--status">
				<n-select
					v-model:value="localStatusId"
					:options="statusList"
					v-on:change="updateGanttData"
				></n-select>
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
				>
					<div
						class="gantt-row--bar-start"
						data-column="start"
						v-on:mousedown="mouseDown"
					></div>
					<div
						class="gantt-row--bar-middle"
						data-column="middle"
						v-on:mousedown="mouseDown"
					></div>
					<div
						class="gantt-row--bar-end"
						data-column="end"
						v-on:mousedown="mouseDown"
					></div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Components
import { NDatePicker, NSelect } from "naive-ui";

export default {
	name: "RenderGanttRow",
	props: {
		endDate: {
			type: Number,
			default: 0,
		},
		higherOrderStatus: {
			type: String,
			default: "",
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
		NSelect,
	},
	data() {
		return {
			localEndDate: this.endDate,
			localStartDate: this.startDate,
			localStatusId: this.statusId,
			statusList: [],
		};
	},
	watch: {
		endDate(new_value) {
			this.localEndDate = new_value;
		},
		startDate(new_value) {
			this.localStartDate = new_value;
		},
		statusId(new_value) {
			this.localStatusId = new_value;
		},
	},
	computed: {
		...mapGetters({
			startDateGantt: "getStartDateGantt",
		}),
		barWidth() {
			//Calculate the delta (aka number of days)
			const delta = Math.ceil((this.localEndDate - this.localStartDate) / (1000 * 60 * 60 * 24));

			//Return number of days multiplied by 35 pixels
			return delta * 35;
		},
		spacerWidth() {
			//Calculate the delta (aka number of days)
			const delta = Math.floor((this.localStartDate - this.startDateGantt) / (1000 * 60 * 60 * 24));

			//Return the number of days multiplied by 35 pixels
			return delta * 35;
		}
	},
	methods: {
		getStatusList() {
			//Get the status list dependent on the object type
			this.statusList = this.$store.getters.getGanttStatusList(this.objectType);
		},
		mouseDown(event) {
			//Send data up stream
			this.$emit("mouse_down", {
				mdClientXInitial: event.clientX,
				mdHigherOrderStatus: this.higherOrderStatus,
				mdIndex: this.index,
				mdObjectType: this.objectType,
				mdColumn: event.target.dataset.column,
				mdEndDateInitial: this.endDate,
				mdStartDateInitial: this.startDate,
				mdStatus: this.status,
				mdStatusId: this.statusId,
				mdTitle: this.title,
			});
		},
		updateGanttData() {
			this.$store.dispatch("updateGanttChartSingleRow", {
				index: this.index,
				value: {
					end_date: this.localEndDate,
					higher_order_status: this.higherOrderStatus,
					object_type: this.objectType,
					start_date: this.localStartDate,
					status_id: this.statusId,
					title: this.title,
				},
			});
		},
	},
	mounted() {
		this.getStatusList();
	}
}
</script>