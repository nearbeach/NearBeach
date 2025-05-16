<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Description</strong>
			<p class="text-instructions">
				The GDPR Wizard is designed to replace/remove any data associated with any user/customer. Please note
				this can NOT be un-done, and should only be used when issued a GDPR takedown.
			</p>
			<strong>Instructions</strong>
			<p class="text-instructions">
				Please pick which object you would like to remove from the system. You can remove either; customer,
				organisation, or a user.
			</p>
		</div>
		<div class="col-md-8">
			<div class="form-group">
				<label>Selected Object</label>
				<n-select :options="objectOptions" v-model:value="objectResults" />
			</div>
		</div>
	</div>
</template>

<script>
import { NSelect } from "naive-ui";

export default {
	name: "GdprWizardObject",
	components: {
		NSelect,
	},
	data() {
		return {
			objectOptions: [
				{
					label: "Customer",
					value: "customer",
				},
				{
					label: "Organisation",
					value: "organisation",
				},
				{
					label: "User",
					value: "user",
				},
			],
			objectResults: "",
		}
	},
	watch: {
		objectResults() {
			//Send results up to VueX
			this.$store.dispatch("processGdprObjectType", {
				"gdprObject": this.objectResults,
			});
		}
	},
	methods: {}
}
</script>