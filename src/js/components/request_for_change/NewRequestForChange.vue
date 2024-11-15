<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Request for Change</h1>
				<hr/>

				<rfc-wizard v-bind:current-tab="currentTab"></rfc-wizard>

				<!-- DESCRIPTION -->
				<rfc-description
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:static-url="staticUrl"
					v-bind:style="displayTab(0)"
				></rfc-description>

				<!-- Details -->
				<rfc-details
					v-bind:uuid="uuid"
					v-bind:group-results="groupResults"
					v-bind:user-group-permissions="userGroupPermissions"
					v-on:update_validation="updateValidation($event)"
					v-on:update_values="updateValues($event)"
					v-bind:style="displayTab(1)"
				></rfc-details>

				<!-- Risk -->
				<rfc-risk
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:style="displayTab(2)"
				></rfc-risk>

				<!-- Implementation Plan -->
				<rfc-implementation-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:style="displayTab(3)"
				></rfc-implementation-plan>

				<!-- Backout Plan -->
				<rfc-backout-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:style="displayTab(4)"
				></rfc-backout-plan>

				<!-- Test Plan -->
				<rfc-test-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:style="displayTab(5)"
				></rfc-test-plan>

				<!-- NAVIGATIONS-->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<!-- PREVIOUS -->
						<button class="btn btn-primary"
								v-on:click="previousTab"
								v-if="currentTab!==0"
						>
							Previous
						</button>

						<!-- NEXT -->
						<button class="btn btn-primary save-changes"
								v-on:click="nextTab"
								v-if="currentTab!==5"
						>
							Next
						</button>

						<!-- SUMBIT-->
						<button class="btn btn-primary save-changes"
								v-on:click="submitRfc"
								v-if="currentTab===5"
								v-bind:disabled="disableSubmitButton"
						>
							Create new Request for Change
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import RfcDescription from "./tabs/RfcDescription.vue";
import RfcDetails from "./tabs/RfcDetails.vue";
import RfcRisk from "./tabs/RfcRisk.vue";
import RfcTestPlan from "./tabs/RfcTestPlan.vue";
import RfcBackoutPlan from "./tabs/RfcBackoutPlan.vue";
import RfcImplementationPlan from "./tabs/RfcImplementationPlan.vue";
import RfcWizard from "./RfcWizard.vue";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useReplaceIncorrectImageUrl} from "../../composables/uploads/useReplaceIncorrectImageUrl";

export default {
	name: "NewRequestForChange",
	components: {
		RfcBackoutPlan,
		RfcDescription,
		RfcDetails,
		RfcImplementationPlan,
		RfcRisk,
		RfcTestPlan,
		RfcWizard,
	},
	props: {
		groupResults: {
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
		userGroupPermissions: {
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
	emits: ["onComplete"],
	data: () => ({
		currentTab: 0,
		disableSubmitButton: false,
		rfcData: {
			groupModel: [],
			rfcBackoutPlan: "",
			rfcChangeLeadModel: {},
			rfcImpactModel: {},
			rfcImplementationPlanModel: "",
			rfcPriorityModel: {},
			rfcRiskModel: {},
			rfcRiskSummaryModel: "",
			rfcSummaryModel: "",
			rfcTestPlanModel: "",
			rfcTitleModel: "",
			rfcTypeModel: {},
			rfcVersionModel: "",
		},
		validationData: {
			tab_0: false,
			tab_1: false,
			tab_2: false,
			tab_3: false,
			tab_4: false,
			tab_5: false,
		},
	}),
	methods: {
		useNBTheme,
		displayTab(tab_id) {
			if (parseInt(tab_id) === parseInt(this.currentTab)) {
				//We want to display this tab
				return "";
			}

			//We want to hide this tab
			return "display:none;";
		},
		nextTab() {
			//Do nothing if tab >= 5
			if (this.currentTab >= 5) return;

			//Validate the current tab
			if (this.validationData[`tab_${this.currentTab}`] === false) {
				//Notify the user of the unvalidated data and return.
				this.$store.dispatch("newToast", {
					header: "Please check your inputs",
					message: "Sorry, we are being told that some of the data is not passing validation. Please check",
					extra_classes: "bg-danger",
					delay: 1500,
				});

				//Do nothing
				return;
			}

			//Validation has passed move the user to the next tab
			this.currentTab = this.currentTab + 1;

			//Scroll to the top
			window.scrollTo({top: 0, behavior: 'smooth'});
		},
		previousTab() {
			//Do nothing if tab <= 0
			if (this.currentTab <= 0) return;

			//Move to previous tab
			this.currentTab = this.currentTab - 1;
		},
		submitRfc() {
			// Check validation
			let validation_is_true = true;
			for (const tab of Object.keys(this.validationData)) {
				//If there are any FALSE, then the "validation_is_true" will be false
				validation_is_true = validation_is_true && this.validationData[tab];
			}

			if (validation_is_true === false) {
				this.$store.dispatch("newToast", {
					header: "Please check your inputs",
					message: "Sorry, we are being told that some of the data is not passing validation. Please check",
					extra_classes: "bg-danger",
					delay: 1500,
				});

				return;
			}

			this.disableSubmitButton = true;

			// Setup the new data form
			const data_to_send = new FormData();
			const data = this.rfcData;

			data_to_send.set("rfc_title", data.rfcTitleModel);
			data_to_send.set(
				"rfc_summary",
				useReplaceIncorrectImageUrl(data.rfcSummaryModel)
			);
			data_to_send.set("rfc_type", data.rfcTypeModel);
			data_to_send.set("rfc_version_number", data.rfcVersionModel);
			data_to_send.set("rfc_lead", data.rfcChangeLeadModel);
			data_to_send.set("rfc_priority", data.rfcPriorityModel);
			data_to_send.set("rfc_risk", data.rfcRiskModel);
			data_to_send.set("rfc_impact", data.rfcImpactModel);
			data_to_send.set(
				"rfc_risk_and_impact_analysis",
				useReplaceIncorrectImageUrl(data.rfcRiskSummaryModel)
			);
			data_to_send.set(
				"rfc_implementation_plan",
				useReplaceIncorrectImageUrl(data.rfcImplementationPlanModel)
			);
			data_to_send.set("rfc_backout_plan", useReplaceIncorrectImageUrl(data.rfcBackoutPlan));
			data_to_send.set("rfc_test_plan", useReplaceIncorrectImageUrl(data.rfcTestPlanModel));

			// Insert a new row for each group list item
			data.groupModel.forEach((row) => {
				data_to_send.append("group_list", row);
			});

			this.axios.post(
				`${this.rootUrl}new_request_for_change/save/`,
				data_to_send
			).then((response) => {
				// Just go to the location the data sent back
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not submit RFC",
					message: `Sorry there was an error. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});

				this.disableSubmitButton = false;
			});
		},
		updateValidation(data) {
			//Update the value
			this.validationData[data.tab] = data.value;
		},
		updateValues(data) {
			//Update the value
			this.rfcData[data.modelName] = data.modelValue;
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Send the Root and Static URL to VueX
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});
	},
};
</script>


