<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Permission Set</h1>
				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>New Permission Set</strong>
						<p class="text-instructions">
							Please enter in a unique permission set name. Please
							note - all values are default permission level of 0.
						</p>
					</div>
					<div class="col-md-8">
						<label>
							Permission Set Name
							<validation-rendering
								v-bind:error-list="v$.permissionSetNameModel.$errors"
							></validation-rendering>
							<span
								class="error"
								v-if="!uniquePermissionSetName"
							>
								Please select a unique permission set name
							</span>
							<span
								class="error"
								v-if="checkingPermissionSetName"
							>
								Please wait. Checking Name
							</span>
						</label>
						<input
							type="text"
							v-model="permissionSetNameModel"
							class="form-control"
						/>
					</div>
				</div>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							class="btn btn-primary save-changes"
							v-on:click="addNewPermissionSet"
							v-bind:disabled="isSubmitDisabled"
						>
							Create new Permission Set
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Import mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import ValidationRendering from "../validation/ValidationRendering.vue";
import editor from "@tinymce/tinymce-vue";
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";

export default {
	name: "NewPermissionSet",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor,
		ValidationRendering
	},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			checkingPermissionSetName: false,
			permissionSetNameModel: "",
			searchTimeout: "",
			uniquePermissionSetName: true,
		};
	},
	mixins: [getThemeMixin],
	validations: {
		permissionSetNameModel: {
			required,
		}
	},
	watch: {
		permissionSetNameModel(new_value) {
			// Tell user we are verifying the unqiue name
			this.checkingPermissionSetName = true;

			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Start the potential search
			this.searchTimeout = setTimeout(() => {
				this.checkPermissionSetName();
			}, 500);
		},
	},
	methods: {
		addNewPermissionSet() {
			//Check to make sure everything is validated
			this.v$.$touch();

			if (this.v$.$invalid || !this.uniquePermissionSetName) {
				//The group name is not valid, or is not unique. Show error and return
				this.$store.dispatch("newToast", {
					header: "Please check all fields",
					message: "Failed validation. Please check all fields are validated",
					extra_classes: "bg-danger",
					delay: 0,
				});

				//Just return
				return;
			}

			//Data to send
			const data_to_send = new FormData();
			data_to_send.set(
				"permission_set_name",
				this.permissionSetNameModel
			);

			this.axios.post(
				`${this.rootUrl}new_permission_set/save/`,
				data_to_send
			).then((response) => {
				//Go to the new location
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error adding permission set",
					message: `Sorry, we could not save the permission set. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		checkPermissionSetName() {
			//Send the permission set name to the backend to make sure it is unique
			const data_to_send = new FormData();
			data_to_send.set("search", this.permissionSetNameModel);

			//Use axios to send data
			this.axios.post(
				`${this.rootUrl}permission_set_information/check_permission_set_name/`,
				data_to_send,
			).then((response) => {
				// Update the unique permission set name
				this.uniquePermissionSetName = response.data.length === 0;

				// Hide the checking group name
				this.checkingPermissionSetName = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to check Permission Set Name",
					message: `Sorry, could not check the permission set name. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		isSubmitDisabled() {
			//If we are searching, or if the name is not unique
			return this.uniquePermissionSetName || this.checkingPermissionSetName;
		}
	},
};
</script>

<style scoped></style>
