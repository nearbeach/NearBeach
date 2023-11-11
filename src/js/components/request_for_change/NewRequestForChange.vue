<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Request for Change</h1>
				<hr/>

				<!-- DESCRIPTION -->
				<rfc-description
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
					v-bind:static-url="staticUrl"
				></rfc-description>
				<hr/>

				<!-- Details -->
				<rfc-details
					v-bind:uuid="uuid"
					v-bind:group-results="groupResults"
					v-bind:user-group-results="userGroupResults"
					v-on:update_validation="updateValidation($event)"
					v-on:update_values="updateValues($event)"
				></rfc-details>
				<hr/>

				<!-- Risk -->
				<rfc-risk
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
				></rfc-risk>
				<hr/>

				<!-- Implementation Plan -->
				<rfc-implementation-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
				></rfc-implementation-plan>
				<hr/>

				<!-- Backout Plan -->
				<rfc-backout-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
				></rfc-backout-plan>
				<hr/>

				<!-- Test Plan -->
				<rfc-test-plan
					v-bind:uuid="uuid"
					v-on:update_values="updateValues($event)"
					v-on:update_validation="updateValidation($event)"
				></rfc-test-plan>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="onComplete"
						>Create new Request for Change</a
						>
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
// import {FormWizard, TabContent} from "../../vue-form-wizard";

// import {FormWizard, TabContent} from 'vue-form-wizard';

// Mixins
import errorModalMixin from "../../mixins/errorModalMixin";
import getThemeMixin from "../../mixins/getThemeMixin";
import newObjectUploadMixin from "../../mixins/newObjectUploadMixin";

export default {
	name: "NewRequestForChange",
	components: {
		// FormWizard,
		RfcBackoutPlan,
		RfcDescription,
		RfcDetails,
		RfcImplementationPlan,
		RfcRisk,
		RfcTestPlan,
		// TabContent,
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
	emits: ["onComplete"],
	mixins: [errorModalMixin, getThemeMixin, newObjectUploadMixin],
	data: () => ({
		currentTab: 0,
		rfcData: {
			groupModel: [],
			rfcBackoutPlan: "",
			rfcChangeLeadModel: {},
			rfcImpactModel: {},
			rfcImplementationEndModel: "",
			rfcImplementationPlanModel: "",
			rfcImplementationStartModel: "",
			rfcPriorityModel: {},
			rfcReleaseModel: "",
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
		beforeChange() {
			return this.validationData[`tab_${this.currentTab}`];
		},
		onChange(prevIndex, nextIndex) {
			//Update current tab once the validation has been completed.
			this.currentTab = nextIndex;

			//Scroll to the top of the page
			window.scrollTo(0, 60);
		},
		onComplete() {
			// Setup the new data form
			const data_to_send = new FormData();
			const data = this.rfcData;

			data_to_send.set("rfc_title", data.rfcTitleModel);
			data_to_send.set(
				"rfc_summary",
				this.replaceIncorrectImageUrl(data.rfcSummaryModel)
			);
			data_to_send.set("rfc_type", data.rfcTypeModel);
			data_to_send.set(
				"rfc_implementation_start_date",
				new Date(data.rfcImplementationStartModel).toISOString()
			);
			data_to_send.set(
				"rfc_implementation_end_date",
				new Date(data.rfcImplementationEndModel).toISOString()
			);
			data_to_send.set(
				"rfc_implementation_release_date",
				new Date(data.rfcReleaseModel).toISOString()
			);
			data_to_send.set("rfc_version_number", data.rfcVersionModel);
			data_to_send.set("rfc_lead", data.rfcChangeLeadModel);
			data_to_send.set("rfc_priority", data.rfcPriorityModel);
			data_to_send.set("rfc_risk", data.rfcRiskModel);
			data_to_send.set("rfc_impact", data.rfcImpactModel);
			data_to_send.set(
				"rfc_risk_and_impact_analysis",
				this.replaceIncorrectImageUrl(data.rfcRiskSummaryModel)
			);
			data_to_send.set(
				"rfc_implementation_plan",
				this.replaceIncorrectImageUrl(data.rfcImplementationPlanModel)
			);
			data_to_send.set("rfc_backout_plan", this.replaceIncorrectImageUrl(data.rfcBackoutPlan));
			data_to_send.set("rfc_test_plan", this.replaceIncorrectImageUrl(data.rfcTestPlanModel));

			// Insert a new row for each group list item
			data.groupModel.forEach((row, index) => {
				data_to_send.append("group_list", row);
			});

			this.axios
				.post(
					`${this.rootUrl}new_request_for_change/save/`,
					data_to_send
				)
				.then((response) => {
					// Just go to the location the data sent back
					window.location.href = response.data;
				})
				.catch((error) => {
					this.showErrorModal(error, "request_for_change", "");
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

<style scoped></style>
