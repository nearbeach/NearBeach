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
					@update:value="modifiedStartDate"
				/>
			</div>
			<div class="gantt-row--end-date">
				<n-date-picker
					v-model:value="localEndDate"
					type="datetime"
					@update:value="modifiedEndDate"
				></n-date-picker>
			</div>
			<div class="gantt-row--status">
				<n-select
					v-model:value="localStatusId"
					:options="statusList"
					:on-update-value="updateStatus"
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
		objectId: {
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
			rootUrl: "getRootUrl",
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
		modifiedEndDate() {
			//If the end date is before the start date - we modify the start date to be the end date minus one day
			if (this.localEndDate < this.localStartDate) {
				this.localStartDate = this.localEndDate - (24 * 60 * 60 * 1000);
			}

			this.updateGanttData();
		},
		modifiedStartDate() {
			//If the start date is after the end date - we modify the end date to be the start date plus one day
			if (this.localStartDate > this.localEndDate) {
				this.localEndDate = this.localStartDate + (24 * 60 * 60 * 1000);
			}

			this.updateGanttData();
		},
		mouseDown(event) {
			//Send data up stream
			this.$emit("mouse_down", {
				mdClientXInitial: event.clientX,
				mdHigherOrderStatus: this.higherOrderStatus,
				mdIndex: this.index,
				mdObjectId: this.objectId,
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
			//Update the VueX with the new data
			this.$store.dispatch("updateGanttChartSingleRow", {
				index: this.index,
				value: {
					end_date: this.localEndDate,
					higher_order_status: this.higherOrderStatus,
					object_id: this.objectId,
					object_type: this.objectType,
					start_date: this.localStartDate,
					status_id: this.localStatusId,
					title: this.title,
				},
			});

			//Next tick is required - we have a race condition if this is not here. :'(
			this.$nextTick(() => {
				//Send updated data to the backend
				const data_to_send = new FormData();
				data_to_send.set('status_id', this.localStatusId);

				//Handle the start and end date
				const end_date = new Date(this.localEndDate);
				const start_date = new Date(this.localStartDate);
				data_to_send.set('end_date', end_date.toISOString());
				data_to_send.set('start_date', start_date.toISOString());

				//Use axios to update backend
				this.axios.post(
					`${this.rootUrl}gantt_data/${this.objectType}/${this.objectId}/update_data/`,
					data_to_send
				).catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Error Updating the Object",
						message: `Sorry, we could not update the object's information. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
			});
		},
		updateStatus(data) {
			//Race condition issues - we will manually update the local status id here
			//Then run the update gantt data.
			//In chrome we were having race conditions.
			this.localStatusId = data;

			this.updateGanttData();
		}
	},
	mounted() {
		this.getStatusList();
	}
}
</script>