<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<ul
					class="nav nav-tabs"
					id="misc_module_tabs"
					role="tablist"
				>
					<!-- GROUPS AND USERS -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="group-and-users-tab"
							data-bs-toggle="tab"
							data-bs-target="#group-and-users"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Group and Users
						</button>
					</li>

					<!-- RISK -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="rfc-risk-tab"
							data-bs-toggle="tab"
							data-bs-target="#rfc-risk"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Risk
						</button>
					</li>

					<!-- IMPLEMENTATION -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="rfc-implementation-tab"
							data-bs-toggle="tab"
							data-bs-target="#rfc-implementation"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Implementation
						</button>
					</li>

					<!-- BACKOUT PLAN -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="rfc-backout-tab"
							data-bs-toggle="tab"
							data-bs-target="#rfc-backout"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Backout Plan
						</button>
					</li>

					<!-- TEST PLAN -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link"
							id="rfc-test-plan-tab"
							data-bs-toggle="tab"
							data-bs-target="#rfc-test"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Test Plan
						</button>
					</li>

					<!-- RUN SHEET -->
					<li
						class="nav-item"
						role="presentation"
					>
						<button
							class="nav-link active"
							id="rfc-run-sheet-tab"
							data-bs-toggle="tab"
							data-bs-target="#rfc-run-sheet"
							type="button"
							role="tab"
							aria-controls="home"
							aria-selected="true"
						>
							Run Sheet
						</button>
					</li>
				</ul>
				<hr/>

				<div
					class="tab-content"
					id="misc_module_content"
				>
					<div
						class="tab-pane fade"
						id="group-and-users"
						role="tabpanel"
						aria-labelledby="contact-tab"
					>
						<groups-and-users-module
							v-bind:location-id="locationId"
							v-bind:destination="destination"
							v-bind:is-read-only="isReadOnly"
						></groups-and-users-module>
					</div>
					<div
						class="tab-pane fade"
						id="rfc-risk"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<rfc-risk
							v-bind:rfc-results="rfcResults"
							v-bind:is-read-only="isReadOnly"
							v-on:update_validation="updateValidation($event)"
							v-on:update_values="updateValues($event)"
						></rfc-risk>

						<!-- Update Button -->
						<hr v-if="!isReadOnly"/>
						<div
							class="row submit-row"
							v-if="!isReadOnly"
						>
							<div class="col-md-12">
								<a
									href="javascript:void(0)"
									class="btn btn-primary save-changes"
									v-on:click="updateRisk"
									v-if="userLevel > 1"
								>Update Risks</a
								>
							</div>
						</div>
					</div>

					<div
						class="tab-pane fade"
						id="rfc-implementation"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<rfc-implementation-plan
							v-bind:rfc-results="rfcResults"
							v-bind:is-read-only="isReadOnly"
							v-on:update_validation="updateValidation($event)"
							v-on:update_values="updateValues($event)"
						></rfc-implementation-plan>

						<!-- Update Button -->
						<hr v-if="!isReadOnly"/>
						<div
							class="row submit-row"
							v-if="!isReadOnly"
						>
							<div class="col-md-12">
								<a
									href="javascript:void(0)"
									class="btn btn-primary save-changes"
									v-on:click="updateImplementation"
									v-if="userLevel > 1"
								>Update Implementation Plan</a
								>
							</div>
						</div>
					</div>

					<div
						class="tab-pane fade"
						id="rfc-backout"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<rfc-backout-plan
							v-bind:rfc-results="rfcResults"
							v-bind:is-read-only="isReadOnly"
							v-on:update_validation="updateValidation($event)"
							v-on:update_values="updateValues($event)"
						></rfc-backout-plan>

						<!-- Update Button -->
						<hr v-if="!isReadOnly"/>
						<div
							class="row submit-row"
							v-if="!isReadOnly"
						>
							<div class="col-md-12">
								<a
									href="javascript:void(0)"
									class="btn btn-primary save-changes"
									v-on:click="updateBackoutPlan"
									v-if="userLevel > 1"
								>Update Backout Plan</a
								>
							</div>
						</div>
					</div>

					<div
						class="tab-pane fade"
						id="rfc-test"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<rfc-test-plan
							v-bind:rfc-results="rfcResults"
							v-bind:is-read-only="isReadOnly"
							v-on:update_validation="updateValidation($event)"
							v-on:update_values="updateValues($event)"
						></rfc-test-plan>

						<!-- Update Button -->
						<hr v-if="!isReadOnly"/>
						<div
							class="row submit-row"
							v-if="!isReadOnly"
						>
							<div class="col-md-12">
								<a
									href="javascript:void(0)"
									class="btn btn-primary save-changes"
									v-on:click="updateTestPlan"
									v-if="userLevel > 1"
								>Update Test Plan</a
								>
							</div>
						</div>
					</div>

					<div
						class="tab-pane fade active show"
						id="rfc-run-sheet"
						role="tabpanel"
						aria-labelledby="home-tab"
					>
						<change-task-list
							v-bind:is-read-only="isReadOnly"
							v-bind:location-id="locationId"
							v-bind:user-list="userList"
							v-bind:rfc-id="rfcResults[0].pk"
							v-bind:rfc-status="rfcResults[0].fields.rfc_status"
						></change-task-list>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import ChangeTaskList from "./modules/ChangeTaskList.vue";
import RfcBackoutPlan from "./tabs/RfcBackoutPlan.vue";
import RfcImplementationPlan from "./tabs/RfcImplementationPlan.vue";
import RfcRisk from "./tabs/RfcRisk.vue";
// import RfcRunSheetList from "./modules/ChangeTaskList.vue";
import RfcTestPlan from "./tabs/RfcTestPlan.vue";
import GroupsAndUsersModule from "../modules/sub_modules/GroupsAndUsersModule.vue";

//VueX
import {mapGetters} from "vuex";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "RfcModules",
	components: {
		ChangeTaskList,
		GroupsAndUsersModule,
		RfcBackoutPlan,
		RfcImplementationPlan,
		RfcRisk,
		// RfcRunSheetList,
		RfcTestPlan,
	},
	props: {
		locationId: {
			type: Number,
			default: 0,
		},
		destination: {
			type: String,
			default: "request_for_change",
		},
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		rfcResults: {
			type: Array,
			default: [],
		},
		theme: {
			type: String,
			default: "",
		},
		userList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	mixins: [getThemeMixin],
	data: () => ({
		rfcData: {
			rfcBackoutPlan: "",
			rfcImpactModel: {},
			rfcImplementationPlanModel: "",
			rfcPriorityModel: {},
			rfcRiskModel: {},
			rfcRiskSummaryModel: "",
			rfcTestPlanModel: "",
			rfcTypeModel: {},
		},
		validationData: {
			tab_2: true,
			tab_3: true,
			tab_4: true,
			tab_5: true,
		},
	}),
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		sendData(data_to_send, url, object) {
			//Notify user of updating
			this.$store.dispatch("newToast", {
				header: `Updating ${object}`,
				message: `Currently updating ${object} - please wait`,
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_risk",
			})

			//Use axios to send the data
			this.axios.post(
				url,
				data_to_send
			).then(() => {
				//Notify user of success update
				this.$store.dispatch("newToast", {
					header: `Successfully Updated ${object}`,
					message: `${object} is now updated`,
					extra_classes: "bg-success",
					unique_type: "save_risk",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: `Updating ${object} Failed`,
					message: `Sorry, but ${object} has failed to update. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "save_risk",
				});
			});
		},
		updateBackoutPlan() {
			if (this.validationData.tab_4 === false) {
				//The data isn't valid. Notify the user, and do nothing else
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Doing nothing else
				return;
			}

			const data_to_send = new FormData();
			data_to_send.set("text_input", this.rfcData.rfcBackoutPlan);

			//Send data
			this.sendData(
				data_to_send,
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/backout/`,
				"Back-out plan"
			);
		},
		updateImplementation() {
			if (this.validationData.tab_3 === false) {
				//The data isn't valid. Notify the user, and do nothing else
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Doing nothing else
				return;
			}

			const data_to_send = new FormData();
			data_to_send.set(
				"text_input",
				this.rfcData.rfcImplementationPlanModel
			);

			//Send data
			this.sendData(
				data_to_send,
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/implementation/`,
				"Implementation"
			);
		},
		updateRisk() {
			if (this.validationData.tab_2 === false) {
				//The data isn't valid. Notify the user, and do nothing else
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Doing nothing else
				return;
			}

			//Create the data to send
			const data_to_send = new FormData();
			data_to_send.set(
				"priority_of_change",
				this.rfcData.rfcPriorityModel
			);
			data_to_send.set("risk_of_change", this.rfcData.rfcRiskModel);
			data_to_send.set(
				"impact_of_change",
				this.rfcData.rfcImpactModel
			);
			data_to_send.set(
				"text_input",
				this.rfcData.rfcRiskSummaryModel
			);

			//Send the data
			this.sendData(
				data_to_send,
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/risk/`,
				"Risk"
			);
		},
		updateValidation(data) {
			//Update the value
			this.validationData[data.tab] = data.value;
		},
		updateTestPlan() {
			if (this.validationData.tab_5 === false) {
				//The data isn't valid. Notify the user, and do nothing else
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Doing nothing else
				return;
			}

			const data_to_send = new FormData();
			data_to_send.set("text_input", this.rfcData.rfcTestPlanModel);

			//Send data
			this.sendData(
				data_to_send,
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/save/test/`,
				"Test Plan"
			);
		},
		updateValues(data) {
			//Update the value
			this.rfcData[data.modelName] = data.modelValue;
		},
	},
	mounted() {
		//Send data to required VueX states
		this.$store.commit({
			type: "updateDestination",
			destination: this.destination,
			locationId: this.locationId,
		});
	},
};
</script>

<style scoped></style>
