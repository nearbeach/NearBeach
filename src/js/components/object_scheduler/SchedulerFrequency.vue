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

			<!-- START DATE -->
			<div class="row mt-4">
				<div class="col-md-6">
					<label>
						Start Date
						<span class="error"
							  v-if="startDateModel === null || startDateModel === ''"
						>
							Please select a date
						</span>
					</label>
					<n-date-picker
						v-bind:type="calendarType"
						v-model:value="startDateModel"
						v-bind:actions="[]"
						v-bind:format="calendarFormat"
						:is-date-disabled="startDateDisabled"
						month-format="MMM"
					></n-date-picker>
				</div>
				<div class="col-md-6">
					<label>End Date Condition</label>
					<n-select
						v-bind:options="endDateConditionList"
						v-model:value="endDateConditionModel"
					></n-select>
				</div>
			</div>

			<div class="row mt-4"
				 v-if="endDateConditionModel === 'end-date'"
			>
				<div class="col-md-6">
					<label>
						End Date
						<span class="error"
							  v-if="endDateModel === null"
						>
							Please select a date
						</span>
					</label>
					<n-date-picker
						v-bind:type="calendarType"
						v-model:value="endDateModel"
						v-bind:actions="[]"
						v-bind:format="calendarFormat"
						:is-date-disabled="endDateDisabled"
					></n-date-picker>
				</div>
			</div>

			<div class="row mt-4"
				 v-if="endDateConditionModel === 'number-of-repeats'"
			>
				<div class="col-md-6">
					<label>
						Number of Repeats
						<span v-if="numberOfRepeatsModel === null"
							  class="error"
						>
							Please fill out
						</span>
					</label>
					<n-input-number
						v-model:value="numberOfRepeatsModel"
						min="0"
					></n-input-number>
				</div>
			</div>

			<!-- Day picker -->
			<div class="row mt-4"
				v-if="schedulerFrequencyModel === 'Set Day of the Week'"
			>
				<div class="text-center col-md-1 d-flex flex-column justify-content-between px-0"
					 v-for="dayLoop in dayOfTheWeekArray"
					 :key="dayLoop.value"
				>
					<label v-bind:for="`checkbox_${dayLoop.value}`">{{ dayLoop.shortLabel }}</label>
					<input type="checkbox"
						   v-bind:value="dayLoop.value"
						   v-bind:id="`checkbox_${dayLoop.value}`"
						   v-model="dayModel"
					/>
				</div>
				<div class="col-md-5">
					<label
						class="error"
						v-if="dayModel.length === 0"
					>
						Please select at least one day.
					</label>
				</div>
			</div>

			<!-- Weekly picker -->
			<div class="row mt-4"
				 v-if="['Weekly','Fortnightly'].includes(schedulerFrequencyModel)"
			>
				<div class="col-md-3">
					<label>Day of Week</label>
					<n-select
						:options="dayOfTheWeekArray"
						v-model:value="singleDayModel"
						class="form-group"
					></n-select>
				</div>
			</div>

			<!-- X Days before End of the Month -->
			<div class="row mt-4"
				 v-if="schedulerFrequencyModel === 'X Days before End of the Month'"
			>
				<div class="col-md-3">
					<label>
						Days Before
						<span class="error"
							  v-if="daysBeforeModel === null"
						>
							Please fill
						</span>
					</label>
					<n-input-number
						v-model:value="daysBeforeModel"
						min="0"
						max="14"
					></n-input-number>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//Components
import { NDatePicker, NInputNumber, NSelect } from "naive-ui";

export default {
	name: "SchedulerFrequency",
	components: {
		NDatePicker,
		NInputNumber,
		NSelect,
	},
	emits: [
		'update_scheduler_frequency',
	],
	props: {
		daysBefore: {
			type: Number,
			default: 0,
		},
		day: {
			type: Array,
			default: () => {
				return [];
			},
		},
		endDateCondition: {
			type: String,
			default: "no-end-date"
		},
		endDate: {
			type: Number,
			default: 0,
		},
		numberOfRepeats: {
			type: Number,
			default: 0,
		},
		schedulerFrequency: {
			type: String,
			default: "Set Day of the Week",
		},
		singleDay: {
			type: String,
			default: "monday",
		},
		startDate: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			daysBeforeModel: this.daysBefore,
			dayModel: this.day,
			dayOfTheWeekArray: [
				{ value: "monday", shortLabel: "Mon", label: "Monday" },
				{ value: "tuesday", shortLabel: "Tue", label: "Tuesday" },
				{ value: "wednesday", shortLabel: "Wed", label: "Wednesday" },
				{ value: "thursday", shortLabel: "Thur", label: "Thursday" },
				{ value: "friday", shortLabel: "Fri", label: "Friday" },
				{ value: "saturday", shortLabel: "Sat", label: "Saturday" },
				{ value: "sunday", shortLabel: "Sun", label: "Sunday" },
			],
			endDateConditionList: [
				{ value: "no-end-date", label: "No End Date" },
				{ value: "number-of-repeats", label: "Number of Repeats" },
				{ value: "end-date", label: "End Date" },
			],
			endDateConditionModel: this.endDateCondition,
			endDateModel: this.endDate,
			isFormValid: false,
			numberOfRepeatsModel: this.numberOfRepeats,
			schedulerFrequencyModel: this.schedulerFrequency,
			schedulerFrequencyOptions: [
				{ value: "Set Day of the Week", label: "Set Day of the Week" },
				{ value: "Weekly", label: "Weekly"},
				{ value: "Fortnightly", label: "Fortnightly"},
				{ value: "Monthly", label: "Monthly"},
				{ value: "Start of the Month", label: "Start of the Month"},
				{ value: "End of the Month", label: "End of the Month"},
				{ value: "X Days before End of the Month", label: "X Days before End of the Month"},
			],
			singleDayModel: this.singleDay,
			startDateModel: this.startDate,
		}
	},
	computed: {
		calendarType() {
			if (['Start of the Month', 'End of the Month'].includes(this.schedulerFrequencyModel)) {
				return "month";
			}

			return "date";
		},
		calendarFormat() {
			if (['Start of the Month', 'End of the Month'].includes(this.schedulerFrequencyModel)) {
				return "y-MMM";
			}

			return "y-MM-dd";
		},
	},
	watch: {
		dayModel() {
			this.updateIsValid();
		},
		daysBeforeModel() {
			this.updateIsValid();
		},
		endDateConditionModel() {
			this.updateIsValid();
		},
		endDateModel() {
			this.updateIsValid();
		},
		numberOfRepeatsModel() {
			this.updateIsValid();
		},
		schedulerFrequencyModel() {
			this.updateIsValid();
		},
		singleDayModel() {
			this.updateIsValid();
		},
		startDateModel() {
			this.updateIsValid();
		},
	},
	methods: {
		endDateDisabled(end_date) {
			return this.startDateModel >= end_date;
		},
		sendDataUpstream() {
			this.$emit("update_scheduler_frequency", {
				dayModel: this.dayModel,
				daysBeforeModel: this.daysBeforeModel,
				endDateConditionModel: this.endDateConditionModel,
				endDateModel: this.endDateModel,
				isFormValid: this.isFormValid,
				numberOfRepeatsModel: this.numberOfRepeatsModel,
				schedulerFrequencyModel: this.schedulerFrequencyModel,
				singleDayModel: this.singleDayModel,
				startDateModel: this.startDateModel,
			});
		},
		startDateDisabled(start_date) {
            //Get date but level the time to 23:59:59
            const date = new Date();
            date.setMilliseconds(999);
            date.setSeconds(59);
            date.setMinutes(59);
            date.setHours(23);

            //Return anything that is less than today
            return start_date <= date.getTime();
        },
		updateIsValid() {
			//Assume the best
			let is_valid = true;

			//Common
			if (this.startDateModel === null || this.startDateModel === "") {
				is_valid = false;
			}

			//Conditional Validation
			if (this.endDateConditionModel === "number-of-repeats" && this.numberOfRepeatsModel === null) {
				this.numberOfRepeatsModel = 0;
			}

			if (this.endDateConditionModel === "end-date" && this.endDateModel === null) {
				this.endDateModel = this.startDateModel;
			}

			//Specific Validation
			if (this.schedulerFrequencyModel === "Set Day of the Week" && this.dayModel.length === 0) {
				is_valid = false;
			}

			if (this.schedulerFrequencyModel === "X Days before End of the Month" && this.daysBeforeModel === null) {
				//Go default
				this.daysBeforeModel = 0;
			}

			//Update the value
			this.isFormValid = is_valid;

			//Send data upstream
			this.sendDataUpstream();
		},
	},
	mounted() {
		//Update start date
		const temp_date = new Date();
		temp_date.setHours(9);
		temp_date.setMinutes(0);
		temp_date.setSeconds(0);
		temp_date.setMilliseconds(0);

		if (this.startDateModel === 0) {
			this.startDateModel = temp_date.getTime() + (1000 * 60 * 60 * 24);
		}

		if (this.endDateModel === 0) {
			this.endDateModel = temp_date.getTime() + (1000 * 60 * 60 * 24 * 7);
		}
	}

}
</script>