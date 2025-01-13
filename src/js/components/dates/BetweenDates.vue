<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Between Dates</strong>
			<p class="text-instructions">
				Choose the start and end date of the {{ destination }}. Please
				note the end date can not be earlier than the start date. They
				can be equal.
			</p>
		</div>
		<div class="col-md-4">
			<div class="form-group">
				<label class="text-capitalize">
					{{ destination }} Start Date:
					<validation-rendering
						v-bind:error-list="v$.localStartDateModel.$errors"
					></validation-rendering>
				</label>
				<n-date-picker
					type="datetime"
					v-model:value="localStartDateModel"
					:disabled="userLevel<=1 || isReadOnly"
				></n-date-picker>
			</div>
		</div>
		<div class="col-md-4">
			<div class="form-group">
				<label class="text-capitalize">
					{{ destination }} End Date:
					<validation-rendering
						v-bind:error-list="v$.localEndDateModel.$errors"
					></validation-rendering>
				</label>
				<n-date-picker
					type="datetime"
					v-model:value="localEndDateModel"
					:disabled="userLevel<=1 || isReadOnly"
				></n-date-picker>
			</div>
		</div>
	</div>
</template>

<script>
import {NDatePicker} from "naive-ui";

//Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "BetweenDates",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NDatePicker,
		ValidationRendering,
	},
	emits: ['update_dates'],
	props: {
		destination: {
			type: String,
			default: "",
		},
		endDateModel: {
			type: Number,
			default: () => {
				const temp_date = new Date();
				temp_date.setHours(16);
				temp_date.setMinutes(0);
				temp_date.setSeconds(0);
				temp_date.setMilliseconds(0);

				return temp_date.getTime();
			},
		},
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		startDateModel: {
			type: Number,
			default: () => {
				const temp_date = new Date();
				temp_date.setHours(9);
				temp_date.setMinutes(0);
				temp_date.setSeconds(0);
				temp_date.setMilliseconds(0);

				return temp_date.getTime();
			},
		},
	},
	computed: {
		...mapGetters({
			userLevel: "getUserLevel",
		}),
	},
	validations: {
		localEndDateModel: {
			required,
		},
		localStartDateModel: {
			required,
		},
	},
	data() {
		return {
			localEndDateModel: this.endDateModel,
			localStartDateModel: this.startDateModel,
		};
	},
	methods: {
		emitDates() {
			//Send this data upstream
			this.$emit("update_dates", {
				start_date: this.localStartDateModel,
				end_date: this.localEndDateModel,
			});
		},
	},
	watch: {
		localEndDateModel() {
			//If the user update the end date to appear BEFORE the start date, we should update the start date to be
			// 1 day BEFORE the end date
			if (this.localEndDateModel < this.localStartDateModel) {
				this.localStartDateModel = this.localEndDateModel - (24 * 60 * 60 * 1000);
			}

			//Send the new results up steam
			this.emitDates();
		},
		localStartDateModel() {
			//If the user updates the start date to appear AFTER the end date, we should update the end date to be
			// 1 day AFTER the start date
			if (this.localStartDateModel > this.localEndDateModel) {
				this.localEndDateModel = this.localStartDateModel + (24 * 60 * 60 * 1000);
			}

			//Send the new results up stream
			this.emitDates();
		},
	},
	mounted() {
		//In case the dates fall on default - send up stream
		this.emitDates();
	},
};
</script>


