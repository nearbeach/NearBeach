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
							Start and End date are automatically calculated from the change tasks.
						</p>
						<p class="text-instructions">
							The release date can only be equal or greater than the end date. By default it will equal
							the end date. Changing the release date will obey the time delta if the end date changes.
						</p>
					</div>
					<div class="row col-md-8">
						<!-- Start and End date row -->
						<div class="col-md-12">
							<strong>Start Date: </strong>{{getNiceDatetimeFromInt(rfcImplementationStartModel)}}<br/>
							<strong>End Date: </strong>{{getNiceDatetimeFromInt(rfcImplementationEndModel)}}
						</div>

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
								<label>Release Date: </label>
								<n-date-picker
									type="datetime"
									v-model:value="localReleaseDate"
									input-class="form-control"
									:is-date-disabled="checkDisableDate"
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
							<strong v-if="!isReadOnly">
								<a v-on:click="openChangeLeadModal">Update Change Lead</a>
							</strong>
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
									<strong>{{ localChangeLead[0].username }}: </strong>
									{{ localChangeLead[0].first_name }}
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

				<hr v-if="parseInt(rfcResults[0].fields.rfc_status) === 2"/>
				<div v-if="parseInt(rfcResults[0].fields.rfc_status) === 2"
					 class="row"
				>
					<div class="col-md-4">
						<strong>Waiting for approval</strong>
						<p class="text-instructions">
							The following users will be able to approve or reject this RFC. Please contact them.
						</p>
					</div>
					<div v-if="approvalUsersList.length === 0"
						class="col-md-8"
					>
						Currently gathering User Approval List.
					</div>
					<div v-else
						 class="user-card-list col-md-8"
					>
						<div v-for="user in approvalUsersList"
							 v-bind:key="user.username"
							 class="user-card wide"
						>
							<img
								v-bind:src="profilePicture(user.profile_picture)"
								alt="default profile"
								class="user-card--profile"
							/>
							<div class="user-card--details">
								<div class="user-card--name">
									{{ user.first_name }} {{ user.last_name }}
								</div>
								<div class="user-card--email">
									{{ user.email }}
								</div>
							</div>
						</div>
					</div>
				</div>
				<hr v-if="parseInt(rfcResults[0].fields.rfc_status) === 2"/>

				<!-- Update Button -->
				<hr v-if="!isReadOnly"/>
				<div
					class="row submit-row"
					v-if="!isReadOnly"
				>
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-secondary"
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
import RfcDescription from "./tabs/RfcDescription.vue";
import UpdateChangeLead from "../modules/wizards/UpdateChangeLead.vue"
import {NSelect, NDatePicker} from "naive-ui";
import {mapGetters} from "vuex";
import {Modal} from "bootstrap";

//Import mixins
import datetimeMixin from "../../mixins/datetimeMixin";
import getThemeMixin from "../../mixins/getThemeMixin";

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
		localReleaseDate() {
			//If endDate > releaseDate - update the releaseDate to the end date
			if (this.localEndDate > this.localReleaseDate) {
				this.localReleaseDate = this.localEndDate;
			}

			//Update State Management
			this.updateReleaseDate();
		},
	},
	computed: {
		...mapGetters({
			changeTaskCount: "getChangeTaskCount",
			rfcImplementationEndModel: "getEndDate",
			rfcImplementationStartModel: "getStartDate",
			rfcReleaseModel: "getReleaseDate",
		}),
		checkDateValidation() {
			//Check the validation for each date
			return !this.v$.rfcReleaseModel.required &&
					this.v$.rfcReleaseModel.$dirty;
		},
	},
	mixins: [datetimeMixin, getThemeMixin],
	data() {
		return {
			approvalUsersList: [],
			localChangeLead: this.rfcChangeLead,
			localReleaseDate: 0,
			rfcChangeLeadFixList: [],
			rfcChangeLeadModel: "",
			rfcTitleModel: this.rfcResults[0].fields.rfc_title,
			rfcSummaryModel: this.rfcResults[0].fields.rfc_summary,
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
		checkDisableDate(date) {
			if (this.isReadOnly === true) {
				return false;
			}

			return this.disableDate(date);
		},
		getApprovalUserList() {
			//If the status isn't 2 (i.e. waiting for approval), then just return. Don't need the data
			if (parseInt(this.rfcResults[0].fields.rfc_status) !== 2) return;

			this.axios.post(
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/get_approval_users/`
			).then((response) => {
				this.approvalUsersList = response.data;
			}).catch(() => {
				this.$store.dispatch("newToast", {
					header: "Error Getting Approval User List",
					message: "Sorry, we could not get you the list of users who can approve this RFC",
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
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
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
		rejectRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "6"); //Value 6: Rejected

			//Send data
			this.sendUpdate(data_to_send);
		},
		sendUpdate(data_to_send) {
			this.axios.post(
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/update_status/`,
				data_to_send
			).then(() => {
				//Reload the page to get redirected to the correct place
				window.location.reload(true);
			}).catch(() => {
				this.$store.dispatch("newToast", {
					header: "Can not update status of RFC",
					message: "Sadly we had issues trying to update the status for the RFC.",
					delay: 0,
					extra_classes: "bg-warning text-dark",
				})
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
		updateReleaseDate() {
			//Update the vuex
			this.$store.commit({
				type: "updateRfcReleaseDate",
				releaseDateModel: this.localReleaseDate,
			});
		},
		updateRFC: async function () {
			//Check form validation
			const validation_results = await this.v$.$validate();

			if (!validation_results) {
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

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

			//Use Axios to send the data
			this.axios.post(
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/`,
				data_to_send
			).then((response) => {
				//Notify user of success update
				this.$store.dispatch("newToast", {
					header: "Save Successfully",
					message: "RFC Has saved",
					delay: 10000,
					extra_classes: "bg-success",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not save RFC",
					message: `Sadly we've had the following error ${error}`,
					delay: 0,
					extra_classes: "bg-warning text-dark",
				})
			});
		},
		updateRFCStatus() {
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "2"); //Value 2: Waiting for Approval

			this.sendUpdate(data_to_send);
		},
		updateValues(data) {
			//Update the value
			this[data.modelName] = data.modelValue;
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
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

		//Update the local release date :)
		this.localReleaseDate = release_date.getTime();

		//Update the VueX datetimes :)
		this.$store.commit({
			type: "updateRfcDates",
			endDateModel: end_date.getTime(),
			releaseDateModel: release_date.getTime(),
			startDateModel: start_date.getTime(),
		})

		//Get the list of users who can approve
		this.getApprovalUserList();
	},
};
</script>

<style scoped></style>
