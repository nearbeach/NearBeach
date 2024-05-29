<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Scheduler Frequency</h2>
			<p class="text-instructions">
				Choose the appropriate schedule frequency. Then fill out the required data. Please take note of the
				fields; number of repeats.
			</p>
		</div>
		<div class="col-md-8">
			<div>
				<label>Scheduler Object Frequency</label>
				<n-select
					v-bind:options="schedulerFrequencyOptions"
					v-model:value="schedulerFrequencyModel"
				></n-select>
			</div>

			<br/>
			<div>
				<label>Start Date</label>
				<n-date-picker
					type="date"
					v-model:value="startDateModel"
					v-bind:actions="[]"
					class="form-control"
					:is-date-disabled="startDateDisabled"
				></n-date-picker>
			</div>
		</div>
	</div>
</template>

<script>
//Components
import { NDatePicker, NSelect } from "naive-ui";

export default {
	name: "SchedulerFrequency",
	components: {
		NDatePicker,
		NSelect,
	},
	props: {},
	data() {
		return {
			schedulerFrequencyModel: "Set Day of the Week",
			schedulerFrequencyOptions: [
				{ value: "Set Day of the Week", label: "Set Day of the Week" },
				{ value: "Weekly", label: "Weekly"},
				{ value: "Fortnightly", label: "Fortnightly"},
				{ value: "Monthly", label: "Monthly"},
				{ value: "Start of the Month", label: "Start of the Month"},
				{ value: "End of the Month", label: "End of the Month"},
				{ value: "X Days before End of the Month", label: "X Days before End of the Month"},
			],
			startDateModel: 0,
		}
	},
	methods: {
		startDateDisabled(start_date) {
            //Get date but level the time to 23:59:59
            const date = new Date();
            date.setMilliseconds(999);
            date.setSeconds(59);
            date.setMinutes(59);
            date.setHours(23);

            //Return anything that is less than today
            return start_date <= date.getTime();
        }
	},
	mounted() {
		//Update start date
		let temp_date = new Date();
		temp_date.setHours(9);
		temp_date.setMinutes(0);
		temp_date.setSeconds(0);
		temp_date.setMilliseconds(0);

		this.startDateModel = temp_date.getTime() + (1000 * 60 * 60 * 24);
	}

}
</script>