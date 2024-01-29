<template>
	<div>
		<!-- Request for Change Types and Release Number -->
		<div class="row">
			<div class="col-md-4">
				<h2>Type and Version</h2>
				<p class="text-instructions">
					Please specify how urgent this RFC's status really is.
					Optionally you can also specify the version or release
					number.
				</p>
			</div>
			<div class="col-md-4">
				<div class="form-group">
					<label>
						Request for Change Type:
						<validation-rendering
							v-bind:error-list="v$.rfcTypeModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						v-bind:options="rfcType"
						v-model:value="rfcTypeModel"
					></n-select>
				</div>
			</div>
			<div class="col-md-4">
				<div class="form-group">
					<label>
						Version/Release Number
						<validation-rendering
							v-bind:error-list="v$.rfcVersionModel.$errors"
						></validation-rendering>
					</label>
					<input
						type="text"
						maxlength="25"
						class="form-control"
						v-model="rfcVersionModel"
					/>
				</div>
			</div>
		</div>

		<!-- Implementation and Release Dates -->
		<hr/>
		<div class="row">
			<div class="col-md-4">
				<h2>Important Dates</h2>
				<p class="text-instructions">
					Please supply the implementation start and end dates. Please
					also suply the release date of the change to the general
					consumer.
				</p>
			</div>
			<div class="row col-md-8">
				<!-- Validation row -->
				<div class="col-md-12">
					<span
						class="error"
						v-if="checkDateValidation"
					>
						Please select an appropriate date for ALL fields.</span
					>
				</div>

				<!-- Dates Row -->
				<div class="col-sm-4">
					<div class="form-group">
						<label>Implementation Start: </label>
						<n-date-picker
							type="datetime"
							v-model:value="rfcImplementationStartModel"
							:is-date-disabled="disableDate"
							input-class="form-control"
						></n-date-picker>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="form-group">
						<label>Implementation End: </label>
						<n-date-picker
							type="datetime"
							v-model:value="rfcImplementationEndModel"
							:is-date-disabled="disableDate"
							input-class="form-control"
						></n-date-picker>
					</div>
				</div>
				<div class="col-sm-4">
					<div class="form-group">
						<label>Release Date: </label>
						<n-date-picker
							type="datetime"
							v-model:value="rfcReleaseModel"
							:is-date-disabled="disableDate"
							input-class="form-control"
						></n-date-picker>
					</div>
				</div>
			</div>
		</div>

		<!-- RFC Change Lead User -->
		<hr/>
		<div class="row">
			<div class="col-md-4">
				<h2>Change LEAD:</h2>
				<p class="text-instructions">
					Please supply the LEAD who will be leading this Request for
					Change.
				</p>
			</div>
			<div class="col-md-4">
				<div class="form-group">
					<label>
						LEAD:
						<validation-rendering
							v-bind:error-list="v$.rfcChangeLeadModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						:options="rfcChangeLeadFixList"
						@search="fetchOptions"
						v-model:value="rfcChangeLeadModel"
					></n-select>
					<!-- TO DO FIX THIS -->
				</div>
			</div>
		</div>

		<!-- Group Permissions -->
		<hr/>
		<group-permissions
			v-bind:display-group-permission-issue="displayGroupPermissionIssue"
			v-bind:group-results="groupResults"
			v-bind:destination="'request_for_change'"
			v-bind:is-dirty="v$.groupModel.$dirty"
			v-bind:user-group-results="userGroupResults"
			v-on:update_group_model="updateGroupModel($event)"
		></group-permissions>
	</div>
</template>

<script>
import {NSelect, NDatePicker} from "naive-ui";
import GroupPermissions from "../../permissions/GroupPermissions.vue";

//Mixins
import datetimeMixin from "../../../mixins/datetimeMixin";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../../validation/ValidationRendering.vue";

export default {
	name: "RfcDetails",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		GroupPermissions,
		NDatePicker,
		NSelect,
		ValidationRendering,
	},
	props: {
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userGroupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		uuid: {
			type: String,
			default: "",
		},
	},
	mixins: [datetimeMixin],
	data() {
		return {
			displayGroupPermissionIssue: false,
			groupModel: [],
			rfcChangeLeadFixList: [],
			rfcChangeLeadModel: "",
			rfcImplementationStartModel: this.defaultStartDate(),
			rfcImplementationEndModel: this.defaultEndDate(),
			rfcReleaseModel: this.defaultReleaseDate(),
			rfcStatus: [
				{label: "Draft", value: 1},
				{label: "Waiting for approval", value: 2},
				{label: "Approved", value: 3},
				{label: "Started", value: 4},
				{label: "Finished", value: 5},
				{label: "Rejected", value: 6},
			],
			rfcType: [
				{label: "Emergency", value: 4},
				{label: "High", value: 3},
				{label: "Medium", value: 2},
				{label: "Low", value: 1},
			],
			rfcTypeModel: "",
			rfcVersionModel: "",
			searchTimeout: "",
		};
	},
	validations: {
		groupModel: {
			required,
		},
		rfcChangeLeadModel: {
			required,
		},
		rfcImplementationStartModel: {
			required,
		},
		rfcImplementationEndModel: {
			required,
		},
		rfcReleaseModel: {
			required,
		},
		rfcTypeModel: {
			required,
		},
		rfcVersionModel: {
			maxLength: maxLength(25),
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
		checkDateValidation() {
			//Check the validation for each date
			const start_date =
					!this.v$.rfcImplementationStartModel.required &&
					this.v$.rfcImplementationStartModel.$dirty,
				end_date =
					!this.v$.rfcImplementationEndModel.required &&
					this.v$.rfcImplementationEndModel.$dirty,
				release_date =
					!this.v$.rfcReleaseModel.required &&
					this.v$.rfcReleaseModel.$dirty;

			//If there is ONE invalidation, we send back true => invalid
			return start_date || end_date || release_date;
		},
	},
	methods: {
		defaultStartDate: () => {
			let start_date = new Date();
			start_date.setHours(9);
			start_date.setMinutes(0);
			start_date.setSeconds(0);
			start_date.setMilliseconds(0);

			return start_date.getTime();
		},
		defaultEndDate: () => {
			let end_date = new Date();
			end_date.setHours(16);
			end_date.setMinutes(0);
			end_date.setSeconds(0);
			end_date.setMilliseconds(0);

			new Date(end_date.setDate(end_date.getDate() + 14));

			return end_date.getTime();
		},
		defaultReleaseDate: () => {
			let end_date = new Date();
			end_date.setHours(17);
			end_date.setMinutes(0);
			end_date.setSeconds(0);
			end_date.setMilliseconds(0);

			new Date(end_date.setDate(end_date.getDate() + 14));

			return end_date.getTime();
		},
		fetchOptions(search, loading) {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (search.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getChangeLeadData(search, loading);
				}, 500);
			}
		},
		getChangeLeadData(search, loading) {
			// Save the seach data in FormData
			const data_to_send = new FormData();
			data_to_send.set("search", search);

			// Now that the timer has run out, lets use AJAX to get the organisations.
			this.axios.post(
				`${this.rootUrl}object_data/lead_user_list/`,
				data_to_send
			).then((response) => {
				//Clear the stakeholderFixList
				this.rfcChangeLeadFixList = [];

				//Extract the required JSON data
				const extracted_data = response.data;

				//Look through the extracted data - and map the required fields into stakeholder fix list
				extracted_data.forEach((row) => {
					//Create the creation object
					const creation_object = {
						value: row.pk,
						label: `${row.fields.username} - ${row.fields.first_name} ${row.fields.last_name}`,
					};

					//Push that object into the stakeholders
					this.rfcChangeLeadFixList.push(creation_object);
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting change lead data",
					message: `Error getting change lead data. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});
		},
		updateGroupModel(data) {
			this.groupModel = data;

			//Calculate to see if the user's groups exist in the groupModel
			this.displayGroupPermissionIssue = this.userGroupResults.filter(row => {
				return this.groupModel.includes(row.group_id);
			}).length === 0;

			//Update up stream
			this.updateValues("groupModel", data);
			this.updateValidation();
		},
		updateValidation() {
			this.v$.$touch();

			this.$emit("update_validation", {
				tab: "tab_1",
				value: !this.v$.$invalid,
			});
		},
		updateValues(modelName, modelValue) {
			this.$emit("update_values", {
				modelName: modelName,
				modelValue: modelValue,
			});
		},
	},
	watch: {
		rfcChangeLeadModel() {
			this.updateValues(
				"rfcChangeLeadModel",
				this.rfcChangeLeadModel
			);
			this.updateValidation();
		},
		rfcImplementationStartModel() {
			//Check to make sure endModel >= startModel;
			if (
				this.rfcImplementationStartModel >
				this.rfcImplementationEndModel
			) {
				this.rfcImplementationEndModel =
					this.rfcImplementationStartModel;
			}

			//Send data upstream
			this.updateValues(
				"rfcImplementationStartModel",
				this.rfcImplementationStartModel
			);
			this.updateValidation();
		},
		rfcImplementationEndModel() {
			//Check to make sure the releaseModel >= endModel
			if (this.rfcImplementationEndModel > this.rfcReleaseModel) {
				this.rfcReleaseModel = this.rfcImplementationEndModel;
			}

			//Check to make sure endModel >= startModel;
			if (
				this.rfcImplementationStartModel >
				this.rfcImplementationEndModel
			) {
				this.rfcImplementationEndModel =
					this.rfcImplementationStartModel;
			}

			//Send data upstream
			this.updateValues(
				"rfcImplementationEndModel",
				this.rfcImplementationEndModel
			);
			this.updateValidation();
		},
		rfcReleaseModel() {
			//Check to make sure the releaseModel >= endModel
			if (this.rfcImplementationEndModel > this.rfcReleaseModel) {
				this.rfcReleaseModel = this.rfcImplementationEndModel;
			}

			//Send data upstream
			this.updateValues("rfcReleaseModel", this.rfcReleaseModel);
			this.updateValidation();
		},
		rfcStatus() {
			this.updateValues("rfcStatus", this.rfcStatus);
			this.updateValidation();
		},
		rfcType() {
			this.updateValues("rfcType", this.rfcType);
			this.updateValidation();
		},
		rfcTypeModel() {
			this.updateValues("rfcTypeModel", this.rfcTypeModel);
			this.updateValidation();
		},
		rfcVersionModel() {
			this.updateValues("rfcVersionModel", this.rfcVersionModel);
			this.updateValidation();
		},
	},
	mounted() {
		//Get the lead user data
		this.$nextTick(() => {
			this.getChangeLeadData();
		});

		//Send the default date time up stream
		this.updateValues(
			"rfcImplementationEndModel",
			this.rfcImplementationEndModel
		);
		this.updateValues("rfcReleaseModel", this.rfcReleaseModel);
		this.updateValues(
			"rfcImplementationStartModel",
			this.rfcImplementationStartModel
		);

		//Just run the validations to show the error messages
		this.v$.$touch();
	},
};
</script>

<style scoped></style>
