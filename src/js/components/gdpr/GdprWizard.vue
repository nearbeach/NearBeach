<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card gdpr-wizard-card">
			<div class="card-body">
				<h1>GDPR Wizard</h1>
				<hr/>

				<gdpr-wizard-steps v-bind:current-tab="currentTab"></gdpr-wizard-steps>

				<div class="alert alert-info gdpr-wizard-alert">
					Please use a larger monitor, as there is a large amount of data to process. Doing this task on a
					small screen is considered hard/annoying.
				</div>

				<!-- OBJECT-->
				<gdpr-wizard-object
					v-bind:style="displayTab(0)"
				></gdpr-wizard-object>

				<!-- SEARCH-->
				<gdpr-wizard-search
					v-bind:style="displayTab(1)"
				></gdpr-wizard-search>

				<!-- DATA VERIFICATION-->
				<gdpr-wizard-data-verification
					v-bind:style="displayTab(2)"
				></gdpr-wizard-data-verification>

				<!-- CONFIRMATION-->
				<gdpr-wizard-confirmation
					v-bind:style="displayTab(3)"
				></gdpr-wizard-confirmation>

				<!-- NAVIGATION -->
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
								v-if="currentTab!==4"
						>
							Next
						</button>

						<!-- SUBMIT -->
						<button class="btn btn-primary save-changes"
								v-on:click="submitGdpr"
								v-if="currentTab===4"
								v-bind:disabled="disableSubmitButton"
						>

						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import GdprWizardSteps from "./GdprWizardSteps.vue";
import GdprWizardObject from "./tabs/GdprWizardObject.vue";
import GdprWizardSearch from "./tabs/GdprWizardSearch.vue";
import GdprWizardDataVerification from "./tabs/GdprWizardDataVerification.vue";
import GdprWizardConfirmation from "./tabs/GdprWizardConfirmation.vue";

//Composable
import {useNBTheme} from "../../composables/theme/useNBTheme";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "GdprWizard",
	components: {
		GdprWizardConfirmation,
		GdprWizardDataVerification,
		GdprWizardSearch,
		GdprWizardObject,
		GdprWizardSteps
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "light",
		},
	},
	data() {
		return {
			currentTab: 0,
			disableSubmitButton: false,
			pickedObject: "",
		}
	},
	computed: {
		...mapGetters({
			validationData: "getValidationData",
		})
	},
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
			//Do nothing if tab >= 4
			if (this.currentTab >= 4) return;

			//Validate the current tab
			if (this.validationData[`tab_${this.currentTab}`] === false) {
				//Notify the user of the unvalidated data and return
				this.$store.dispatch("newToast", {
					header: "Please check your input",
					message: "Sorry, we are being told that some of the data is not valid",
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
		submitGdpr() {
			//ADD CODE
		},
	}
}
</script>
