<template>
	<div class="row">
		<div class="col-md-4">
			<strong>New Customer</strong>
			<p class="text-instructions">
				Please fill out the following details.
			</p>
			<strong>Please Note:</strong>
			<p class="text-instructions">
				Customers do not go through a duplication process. Please search
				for the potential customer first before adding them into
				NearBeach.
			</p>
		</div>
		<div class="col-md-8">
			<!-- CUSTOMER DETAILS -->
			<div class="row">
				<div class="form-group col-sm-3">
					<label>
						Title:
						<validation-rendering
							v-bind:error-list="v$.titleModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						:options="titleFixList"
						label="title"
						placeholder=""
						v-model:value="titleModel"
					></n-select>
				</div>
				<div class="form-group col-sm-4">
					<label>
						First Name:
						<validation-rendering
							v-bind:error-list="v$.customerFirstNameModel.$errors"
						></validation-rendering>
					</label>
					<input
						type="text"
						class="form-control"
						v-model="customerFirstNameModel"
					/>
				</div>
				<div class="form-group col-sm-5">
					<label>
						Last Name:
						<validation-rendering
							v-bind:error-list="v$.customerLastNameModel.$errors"
						></validation-rendering>
					</label>
					<input
						type="text"
						class="form-control"
						v-model="customerLastNameModel"
					/>
				</div>
			</div>

			<!-- Customer Email -->
			<div class="form-group col-sm-8 mt-4 mb-4">
				<label>
					Email:
					<validation-rendering
						v-bind:error-list="v$.customerEmailModel.$errors"
					></validation-rendering>
				</label>
				<input
					type="text"
					class="form-control"
					v-model="customerEmailModel"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, email} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "NewCustomerForm",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NSelect,
		ValidationRendering,
	},
	emits: [
		'update_customer_data',
	],
	props: {
		flagValidationCheck: {
			type: Boolean,
			default: false,
		},
		titleList: {
			type: Array,
			default() {
				return [];
			},
		},
	},
	data() {
		return {
			customerEmailModel: "",
			customerFirstNameModel: "",
			customerLastNameModel: "",
			organisationModel: {},
			searchTimeout: "",
			titleFixList: [],
			titleModel: [],
		};
	},
	validations: {
		customerEmailModel: {
			required,
			email,
		},
		customerFirstNameModel: {
			required,
		},
		customerLastNameModel: {
			required,
		},
		titleModel: {
			required,
		},
	},
	methods: {},
	watch: {
		customerEmailModel() {
			//Emit up this function's data
			this.$emit("update_customer_data", {
				field: "customerEmailModel",
				value: this.customerEmailModel,
			});
		},
		customerFirstNameModel() {
			//Emit up this function's data
			this.$emit("update_customer_data", {
				field: "customerFirstNameModel",
				value: this.customerFirstNameModel,
			});
		},
		customerLastNameModel() {
			//Emit up this function's data
			this.$emit("update_customer_data", {
				field: "customerLastNameModel",
				value: this.customerLastNameModel,
			});
		},
		flagValidationCheck() {
			//Don't worry if it is false
			if (!this.flagValidationCheck) return;

			//Touch the validation

			this.v$.$touch();
		},
		titleModel() {
			//Emit up this function's data
			this.$emit("update_customer_data", {
				field: "titleModel",
				value: this.titleModel,
			});
		},
	},
	mounted() {
		//Get the data formatted how the NSelect wants
		this.titleFixList = this.titleList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.title,
			};
		});
	},
};
</script>


