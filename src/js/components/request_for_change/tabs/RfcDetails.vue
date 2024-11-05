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

		<!-- Group Permissions -->
		<hr/>
		<group-permissions
			v-bind:display-group-permission-issue="displayGroupPermissionIssue"
			v-bind:group-results="groupResults"
			destination="request_for_change"
			v-bind:is-dirty="v$.groupModel.$dirty"
			v-bind:user-group-permissions="userGroupPermissions"
			v-on:update_group_model="updateGroupModel($event)"
		></group-permissions>

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
						<span
							v-if="updatingLeadList"
							class="error"
						>
							Updating List.
						</span>
					</label>
					<n-select
						:options="rfcChangeLeadFixList"
						v-model:value="rfcChangeLeadModel"
						:disabled="updatingLeadList"
					></n-select>
					<!-- TO DO FIX THIS -->
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";
import GroupPermissions from "../../permissions/GroupPermissions.vue";

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
		NSelect,
		ValidationRendering,
	},
	emits: [
		'update_values',
		'update_validation',
	],
	props: {
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userGroupPermissions: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	data() {
		return {
			displayGroupPermissionIssue: false,
			groupModel: [],
			rfcChangeLeadFixList: [],
			rfcChangeLeadModel: "",
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
			updatingLeadList: false,
		};
	},
	validations: {
		groupModel: {
			required,
		},
		rfcChangeLeadModel: {
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
	},
	methods: {
		getChangeLeadData() {
			//Tell user we are updating the list
			this.updatingLeadList = true;
			this.rfcChangeLeadModel = "";

			//If there are no group results - blank out the options for rfcChangeLead, and just return
			if (this.groupModel.length === 0) {
				this.rfcChangeLeadFixList = [];
				this.updatingLeadList = false;

				return;
			}

			// Save the seach data in FormData
			const data_to_send = new FormData();
			this.groupModel.forEach((row) => {
				data_to_send.append("group_list", row);
			});

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

				//Tell user they can update now
				this.updatingLeadList = false;
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

			//Calculate to see if the user's groups exist in the groupModel AND
			//Make sure the user has ENOUGH permissions.
			this.displayGroupPermissionIssue = this.userGroupPermissions.filter(row => {
				//Condition 1 - group model includes current group
				//Condition 2 - user has create permissions on group
				const condition_1 = this.groupModel.includes(row.group_id);
				const condition_2 = row.object_permission_value >= 3;

				return condition_1 && condition_2;
			}).length === 0;

			//Update up stream
			this.updateValues("groupModel", data);
			this.updateValidation();

			//Update the lead list
			this.getChangeLeadData();
		},
		updateValidation() {
			this.v$.$touch();

			//Condtions 1: this.v$.$invalid === false
			//Condition 2: displayGroupPermissions === false
			//Both conditions have to be met to let the user pass
			this.$emit("update_validation", {
				tab: "tab_1",
				value: !this.v$.$invalid && !this.displayGroupPermissionIssue,
			});
		},
		updateValues(modelName, modelValue) {
			this.$emit("update_values", {
				modelName,
				modelValue,
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

		//Just run the validations to show the error messages
		this.v$.$touch();
	},
};
</script>


