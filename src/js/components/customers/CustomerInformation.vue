<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<!-- TITLE -->
				<h1 class="mb-4">Customer Information</h1>
				<a v-bind:href="`${rootUrl}search/customer/`"
				>Go back to customer search</a
				>
				<hr/>

				<!-- FIELDS SECTION -->
				<div class="row">
					<div class="col-md-4">
						<strong>Please Note</strong>
						<p class="text-instructions">
							Please fill out the following details. If the customer
							is not assigned an organisation, NearBeach will treat
							this customer as a freelancer.
						</p>
					</div>
					<div class="col-md-8">
						<div class="row customer-profile-image">
							<!-- PROFILE IMAGE -->
							<img
								v-bind:src="profilePicture"
								alt="User Profile Picture"
								class="customer-profile-image"
							/>
							<n-upload
								v-if="userLevel > 1"
								:action="`${rootUrl}customer_information/${customerResults[0].pk}/update_profile/`"
								:headers="{
								'X-CSRFTOKEN': useToken('csrftoken'),
							}"
								:data="{}"
								@finish="updateProfilePicture"
								@error="showErrorToast"
								accept=".jpg, .jpeg, .png, *.webp"
							>
								<n-button>Update Profile Picture</n-button>
							</n-upload>
						</div>
						<div class="spacer-extra"></div>

						<!-- CUSTOMER INFORMATION -->
						<div class="row">
							<div class="form-group col-sm-3">
								<label>
									Title:
									<validation-rendering
										v-bind:error-list="v$.customerTitleModel.$errors"
									></validation-rendering>
								</label>
								<n-select
									:options="titleFixList"
									:disabled="userLevel <= 1"
									v-model:value="customerTitleModel"
								></n-select>
							</div>
							<div class="form-group col-sm-4">
								<label>
									First Name:
									<validation-rendering
										v-bind:error-list="v$.customerFirstNameModel.$errors"
									></validation-rendering>
								</label>
								<input
									type="text"
									class="form-control"
									v-model="customerFirstNameModel"
									:disabled="userLevel <= 1"
								/>
							</div>
							<div class="form-group col-sm-5">
								<label>
									Last Name:
									<validation-rendering
										v-bind:error-list="v$.customerLastNameModel.$errors"
									></validation-rendering>
								</label>
								<input
									type="text"
									class="form-control"
									v-model="customerLastNameModel"
									:disabled="userLevel <= 1"
								/>
							</div>
						</div>
					</div>
				</div>
				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<stakeholder-information
					v-bind:organisation-results="organisationResults"
					v-bind:default-stakeholder-image="defaultStakeholderImage"
					v-if="organisationResults.length > 0"
				></stakeholder-information>

				<!-- NEED TO APPLY PERMISSIONS -->
				<!-- Submit Button -->
				<hr v-if="userLevel > 1"
					class="mt-4"
				/>
				<div
					v-if="userLevel > 1"
					class="row submit-row"
				>
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="updateCustomer"
						>Update Customer</a
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NButton, NSelect, NUpload} from "naive-ui";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, email} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue"

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";
import {useToken} from "../../composables/security/useToken";

export default {
	name: "CustomerInformation",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NButton,
		NSelect,
		NUpload,
		StakeholderInformation,
		ValidationRendering,
	},
	props: {
		customerResults: {
			type: Array,
			default() {
				return [];
			},
		},
		defaultStakeholderImage: {
			type: String,
			default: "",
		},
		organisationResults: {
			type: Array,
			default() {
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
		titleList: {
			type: Array,
			default() {
				return [];
			},
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			customerEmailModel:
			this.customerResults[0].fields.customer_email,
			customerFirstNameModel:
			this.customerResults[0].fields.customer_first_name,
			customerLastNameModel:
			this.customerResults[0].fields.customer_last_name,
			customerTitleModel:
			this.customerResults[0].fields.customer_title,
			profilePicture: `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`,
			titleFixList: [],
		};
	},
	validations: {
		customerEmailModel: {
			required,
			email,
		},
		customerFirstNameModel: {
			required,
		},
		customerLastNameModel: {
			required,
		},
		customerTitleModel: {
			required,
		},
	},
	methods: {
		useToken,
		useNBTheme,
		showErrorToast() {
			this.$store.dispatch("newToast", {
				header: "Error uploading profile picture",
				message: "Sorry, we had an issue uploading the profile image.",
				extra_classes: "bg-danger",
				delay: 0,
			});
		},
		setProfilePicture() {
			//If there is a profile picture/image, update. Otherwise use default
			const profile_picture =
				this.customerResults[0].fields.customer_profile_picture;
			if (
				profile_picture !== undefined &&
				profile_picture !== null &&
				profile_picture !== ""
			) {
				//There exists a profile image for the user
				this.profilePicture = `/private${this.rootUrl}${this.customerResults[0].fields.customer_profile_picture}`;
			} else {
				//Go back to default
				this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;
			}
		},
		async updateCustomer() {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect || this.displayGroupPermissionIssue) {
				this.$store.dispatch("newToast", {
					header: "Please correct issues",
					message: "Not all fields are correctly validated. Please correct.",
					extra_classes: "bg-danger",
				})
				return;
			}

			//Construct the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("customer_email", this.customerEmailModel);
			data_to_send.set(
				"customer_first_name",
				this.customerFirstNameModel
			);
			data_to_send.set(
				"customer_last_name",
				this.customerLastNameModel
			);
			data_to_send.set("customer_title", this.customerTitleModel);

			//Notify user we are updating
			this.$store.dispatch("newToast", {
				header: "Updating Customer",
				message: "Please wait whilst we update customer",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save",
			});

			//Use axios to send the data
			this.axios.post(
				`${this.rootUrl}customer_information/${this.customerResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Customer Updated",
					message: "The Customer has updated",
					extra_classes: "bg-success",
					unique_type: "save",
				});

				//Check to see if we are updating the profile picture
				this.updateProfilePicture();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to Update Customer",
					message: `Sorry. We have encounted an error. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "save",
				});
			});
		},
		updateProfilePicture() {
			//Contact the API to get the location of the new image
			this.axios.post(
				`${this.rootUrl}customer_information/${this.customerResults[0].pk}/get_profile_picture/`,
				{}
			).then((response) => {
				this.profilePicture = response.data;
			}).catch(() => {
				this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;
			});
		},
	},
	mounted() {
		//Send up root and static url
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});

		this.$store.commit({
			type: "updateUserLevel",
			userLevel: this.userLevel,
		});

		this.$store.commit({
			type: "updateDestination",
			destination: "customer",
			locationId: this.customerResults[0].pk,
		});
		this.$store.commit({
			type: "updateTitle",
			title: `${this.customerFirstNameModel} ${this.customerLastNameModel}`,
		});

		//Convert the title list data into a format NSelect can use
		this.titleFixList = this.titleList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.title,
			};
		});

		//See if there is a profile picture
		this.setProfilePicture();
	},
};
</script>


