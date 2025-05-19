<template>
	<div class="row">
		<div class="col-md-4">
			<strong>WARNING! DELETING {{ gdprObjectType }}</strong>
			<p class="text-instructions">
				Please confirm that you are happy with deleting this data. Please type in the field "Deleting
				{{ gdprObjectType }}".
			</p>
		</div>
		<div class="col-md-8">
			<div v-if="gdprObjectType === 'user'"
				class="alert alert-info"
			>
				Due to the CASCADE effect within the NearBeach's database. Many objects will be deleted if we just remove
				the user. To stop this from happening we'll be using your user id to fill both the "Creation User" and
				"Modified User" fields.
			</div>

			<div class="alert alert-danger">
				BEWARD! This can NOT be undone. We are deleting data from the database. Please make sure you have checked
				all data before submitting this. It can NOT be undone.
			</div>

			<div class="form-group">
				<label>
					Confirm Deletion of {{ gdprObjectType }}
					<span v-if="!isValidated"
						  class="error"
					>
						Please confirm what you are deleting. Write "Deleting {{ gdprObjectType }}"
					</span>
				</label>
				<input type="text"
					   class="form-control"
					   v-model="confirmationModel"
				/>
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
	name: "GdprWizardConfirmation",
	computed: {
		...mapGetters({
			gdprObjectType: "getGdprObjectType",
			rootUrl: "getRootUrl",
		})
	},
	watch: {
		confirmationModel() {
			this.isValidated = this.confirmationModel.toLowerCase() === `deleting ${this.gdprObjectType.toLowerCase()}`;
			this.$store.commit({
				type: "updateValidationData",
				tab_id: "tab_3",
				value: this.isValidated
			});
		}
	},
	data() {
		return {
			confirmationModel: "",
			isValidated: false,
		}
	},
}
</script>