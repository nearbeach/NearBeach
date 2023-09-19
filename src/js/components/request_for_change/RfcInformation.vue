<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Request for Change</h1>
				<br/>
				<h2>{{ getStatus() }}</h2>
				<hr/>

				<rfc-description
					v-bind:rfc-results="rfcResults"
					v-bind:is-read-only="isReadOnly"
					v-on:update_values="updateValues($event)"
				></rfc-description>

				<!-- Request for Change Types and Release Number -->
				<hr/>
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
								v-bind:disabled="isReadOnly"
								v-model:value="rfcTypeModel"
							></n-select>
						</div>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label>Version/Release Number</label>
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
							Please supply the implementation start and end dates.
							Please also suply the release date of the change to the
							general consumer.
						</p>
					</div>
					<div class="row col-md-8">
						<!-- Validation row -->
						<div class="col-md-12">
						<span
							class="error"
							v-if="checkDateValidation"
						>
							Please select an appropriate date for ALL
							fields.</span
						>
						</div>

						<!-- Dates Row -->
						<div class="col-sm-4">
							<div class="form-group">
								<label>Implementation Start: </label>
								<n-date-picker
									type="datetime"
									v-model:value="localStartDate"
									input-class="form-control"
									:is-date-disabled="disableDate"
								></n-date-picker>
							</div>
						</div>
						<div class="col-sm-4">
							<div class="form-group">
								<label>Implementation End: </label>
								<n-date-picker
									type="datetime"
									v-model:value="localEndDate"
									input-class="form-control"
									:is-date-disabled="disableDate"
								></n-date-picker>
							</div>
						</div>
						<div class="col-sm-4">
							<div class="form-group">
								<label>Release Date: </label>
								<n-date-picker
									type="datetime"
									v-model:value="localReleaseDate"
									input-class="form-control"
									:is-date-disabled="disableDate"
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
							Please supply the LEAD who will be leading this Request
							for Change.<br/>
							<strong><a v-on:click="openChangeLeadModal">Update Change Lead</a></strong>
						</p>
					</div>
					<div class="col-md-4">
						<table class="table user-table-module">
							<tbody>
							<tr>
								<td>
									<img
										v-bind:src="getProfilePicture(localChangeLead[0].profile_picture)"
										alt="default profile"
										class="default-user-profile"
									/>
								</td>
								<td>
									<strong
									>{{
											localChangeLead[0].username
										}}: </strong
									>{{ localChangeLead[0].first_name }}
									{{ localChangeLead[0].last_name }}
									<div class="spacer"></div>
									<p class="user-card-email">
										{{ localChangeLead[0].email }}
									</p>
								</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Update Button -->
				<hr v-if="!isReadOnly"/>
				<div
					class="row submit-row"
					v-if="!isReadOnly"
				>
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-dark"
							v-on:click="updateRFCStatus"
							v-if="userLevel > 1 && changeTaskCount > 0"
						>Submit RFC for Approval</a
						>

						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="updateRFC"
							v-if="userLevel > 1"
						>Update Request for Change</a
						>
					</div>
				</div>
				<div
					class="row submit-row"
					v-else-if="userLevel >= 2"
				>
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="reject-rfc-button"
							aria-disabled=""
							v-on:click="rejectRFCStatus"
							v-if="
							groupLeaderCount > 0 &&
							rfcResults[0].fields.rfc_status == 2
						"
						>
							Reject RFC
						</a>

						<a
							href="javascript:void(0)"
							class="accept-rfc-button save-changes"
							v-on:click="startRFCStatus"
							v-if="
							userLevel > 1 &&
							rfcResults[0].fields.rfc_status == 3
						"
						>
							Start RFC
						</a>

						<a
							href="javascript:void(0)"
							class="accept-rfc-button save-changes"
							v-on:click="approveRFCStatus"
							v-if="
							groupLeaderCount > 0 &&
							rfcResults[0].fields.rfc_status == 2
						"
						>
							Approve RFC
						</a>

						<a
							href="javascript:void(0)"
							class="pause-rfc-button save-changes"
							v-on:click="pauseRFCStatus"
							v-if="rfcResults[0].fields.rfc_status == 4"
						>
							Pause RFC
						</a>

						<a
							href="javascript:void(0)"
							class="restart-rfc-button save-changes"
							v-on:click="startRFCStatus"
							v-if="
							userLevel > 1 &&
							rfcResults[0].fields.rfc_status == 7
						"
						>
							Restart RFC
						</a>
					</div>
				</div>
			</div>
		</div>

		<!-- RFC MODALS -->
		<update-change-lead v-on:update_change_lead="updateChangeLead"></update-change-lead>
	</n-config-provider>
</template>

<script>
const axios = require("axios");
import RfcDescription from "./tabs/RfcDescription.vue";
import UpdateChangeLead from "../modules/wizards/UpdateChangeLead.vue"
import {NSelect, NDatePicker} from "naive-ui";
import {mapGetters} from "vuex";
import {Modal} from "bootstrap";

//Import mixins
import datetimeMixin from "../../mixins/datetimeMixin";
import errorModalMixin from "../../mixins/errorModalMixin";
import getThemeMixin from "../../mixins/getThemeMixin";
import loadingModalMixin from "../../mixins/loadingModalMixin";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "RfcInformation",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NDatePicker,
		NSelect,
		RfcDescription,
		UpdateChangeLead,
		ValidationRendering,
	},
	props: {
		groupLeaderCount: {
			type: Number,
			default: 0,
		},
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		rfcChangeLead: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rfcResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	watch: {
		localEndDate() {
			//If startDate > endDate - update endDate to the start date
			if (this.localStartDate > this.localEndDate) {
				this.localEndDate = this.localStartDate;
			}

			//If endDate > releaseDate - update the releaseDate to the end date
			if (this.localEndDate > this.localReleaseDate) {
				this.localReleaseDate = this.localEndDate;
			}

			//Update State Management
			this.updateStateManagement();
		},
		localReleaseDate() {
			//If endDate > releaseDate - update the releaseDate to the end date
			if (this.localEndDate > this.localReleaseDate) {
				this.localReleaseDate = this.localEndDate;
			}

			//Update State Management
			this.updateStateManagement();
		},
		localStartDate() {
			//If startDate > endDate - update endDate to the start date
			if (this.localStartDate > this.localEndDate) {
				this.localEndDate = this.localStartDate;
			}

			//Update State Management
			this.updateStateManagement();
		},
	},
	computed: {
		...mapGetters({
			changeTaskCount: "getChangeTaskCount",
			rfcImplementationEndModel: "getEndDate",
			rfcImplementationStartModel: "getStartDate",
			rfcReleaseModel: "getReleaseDateModel",
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
	mixins: [datetimeMixin, errorModalMixin, getThemeMixin, loadingModalMixin],
	data() {
		return {
			localChangeLead: this.rfcChangeLead,
			localEndDate: 0,
			localReleaseDate: 0,
			localStartDate: 0,
			rfcChangeLeadFixList: [],
			rfcChangeLeadModel: "",
			rfcTitleModel: this.rfcResults[0].fields.rfc_title,
			rfcSummaryModel: this.rfcResults[0].fields.rfc_summary,
			// rfcImplementationStartModel: new Date(this.rfcResults[0].fields.rfc_implementation_start_date).getTime(),
			// rfcImplementationEndModel: new Date(this.rfcResults[0].fields.rfc_implementation_end_date).getTime(),
			// rfcReleaseModel: new Date(this.rfcResults[0].fields.rfc_implementation_release_date).getTime(),
			rfcStatus: [
				{label: "Draft", value: 1},
				{label: "Waiting for approval", value: 2},
				{label: "Approved", value: 3},
				{label: "Started", value: 4},
				{label: "Finished", value: 5},
				{label: "Rejected", value: 6},
			],
			rfcStatusDict: {
				1: "Draft",
				2: "Waiting for approval",
				3: "Approved",
				4: "Started",
				5: "Finished",
				6: "Rejected",
			},
			rfcType: [
				{label: "Emergency", value: 4},
				{label: "High", value: 3},
				{label: "Medium", value: 2},
				{label: "Low", value: 1},
			],
			rfcTypeModel: "",
			rfcVersionModel: this.rfcResults[0].fields.rfc_version_number,
		};
	},
	validations: {
		rfcTitleModel: {
			required,
		},
		rfcSummaryModel: {
			required,
			maxLength: maxLength(630000),
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
	methods: {
		approveRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "3"); //Value 3: Approved

			//Send data
			this.sendUpdate(data_to_send);
		},
		getProfilePicture(profile_picture) {
			//If customer profile is blank - return default picture
			if (profile_picture === "" || profile_picture === null || profile_picture === undefined) {
				return `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;
			}

			return `${this.rootUrl}private/${profile_picture}`;
		},
		getStatus() {
			return this.rfcStatusDict[this.rfcResults[0].fields.rfc_status];
		},
		openChangeLeadModal() {
			const modal = new Modal(
				document.getElementById("updateChangeLeadModal")
			);
			modal.show();
		},
		pauseRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "7"); //Value 7: Paused

			//Send data
			this.sendUpdate(data_to_send);
		},
		rejectRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "6"); //Value 6: Rejected

			//Send data
			this.sendUpdate(data_to_send);
		},
		sendUpdate(data_to_send) {
			axios
				.post(
					`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/update_status/`,
					data_to_send
				)
				.then((response) => {
					//Reload the page to get redirected to the correct place
					window.location.reload(true);
				})
				.catch((error) => {
					//Show error if there is one
					this.showErrorModal(
						error,
						"Request for Change",
						this.rfcResults[0].pk
					);
				});
		},
		startRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", 4);

			//Send data
			this.sendUpdate(data_to_send);
		},
		updateChangeLead(new_change_lead) {
			this.localChangeLead = new_change_lead;
		},
		updateRFC: async function () {
			//Check form validation
			const validation_results = await this.v$.$validate();

			if (!validation_results) {
				this.showValidationErrorModal();

				//Just return - as we do not need to do the rest of this function
				return;
			}

			const data_to_send = new FormData();
			data_to_send.set("rfc_title", this.rfcTitleModel);
			data_to_send.set("rfc_summary", this.rfcSummaryModel);
			data_to_send.set("rfc_type", this.rfcTypeModel);
			data_to_send.set("rfc_version_number", this.rfcVersionModel);
			data_to_send.set(
				"rfc_implementation_start_date",
				new Date(this.rfcImplementationStartModel).toISOString()
			);
			data_to_send.set(
				"rfc_implementation_end_date",
				new Date(this.rfcImplementationEndModel).toISOString()
			);
			data_to_send.set(
				"rfc_implementation_release_date",
				new Date(this.rfcReleaseModel).toISOString()
			);

			//Open up the loading modal
			this.showLoadingModal("Project");

			//Use Axios to send the data
			axios
				.post(
					`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/`,
					data_to_send
				)
				.then((response) => {
					//Notify user of success update
					this.closeLoadingModal();
				})
				.catch((error) => {
					this.showErrorModal(error, this.destination);
				});
		},
		updateRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "2"); //Value 2: Waiting for Approval

			this.sendUpdate(data_to_send);
		},
		updateStateManagement() {
			//Update the vuex
			this.$store.commit({
				type: "updateRfcDates",
				endDateModel: this.localEndDate,
				releaseDateModel: this.localReleaseDate,
				startDateModel: this.localStartDate,
			});
		},
		updateValues(data) {
			//Update the value
			this[data.modelName] = data.modelValue;
		},
	},
	mounted() {
		//Set the type model
		this.rfcTypeModel = this.rfcResults[0].fields.rfc_type;

		//Send root and static url to VueX
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		//Send user level to VueX
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});

		//Send release dates up
		const end_date = new Date(
			this.rfcResults[0].fields.rfc_implementation_end_date
		);
		const release_date = new Date(
			this.rfcResults[0].fields.rfc_implementation_release_date
		);
		const start_date = new Date(
			this.rfcResults[0].fields.rfc_implementation_start_date
		);

		this.localEndDate = end_date.getTime();
		this.localReleaseDate = release_date.getTime();
		this.localStartDate = start_date.getTime();

		//Update State Management
		this.updateStateManagement();
	},
};
</script>

<style scoped></style>
