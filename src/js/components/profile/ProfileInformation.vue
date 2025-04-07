<template>
	<n-config-provider :theme="useNBTheme(currentTheme)">
		<div class="card">
			<div class="card-body">
				<h1>My Profile</h1>
				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>User Details</strong>
						<p class="text-instructions">Please update your details.</p>
					</div>
					<div class="col-md-8">
						<p>
							<strong>Username: </strong>{{ userResults[0].username }}
						</p>
						<div class="row">
							<div class="col-md-6">
								<label>
									First Name:
									<validation-rendering
										v-bind:error-list="v$.firstNameModel.$errors"
									></validation-rendering>
									<br/>
								</label>
								<input
									type="text"
									v-model="firstNameModel"
									class="form-control"
								/>
							</div>
							<div class="col-md-6">
								<label>
									Last Name:
									<validation-rendering
										v-bind:error-list="v$.firstNameModel.$errors"
									></validation-rendering>
									<br/>
								</label>
								<input
									type="text"
									v-model="lastNameModel"
									class="form-control"
								/>
							</div>
						</div>

						<div class="spacer"></div>

						<div class="row">
							<div class="col-md-6">
								<label> Email: </label>
								<input
									type="email"
									v-model="emailModel"
									class="form-control"
									disabled="true"
								/>
							</div>
						</div>
					</div>
				</div>
				<hr/>

				<!-- THEME SETTINGS -->
				<div class="row">
					<div class="col-md-4">
						<strong>Theme Preference</strong>
						<p class="text-instructions">Please choose an appropriate theme for NearBeach</p>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label>Theme</label>
							<n-select
								v-model:value="themeModel"
								:options="themeList"
							/>
							<p class="error"
							   v-if="showMessage">
								Please update user details to save.
							</p>
						</div>
					</div>
				</div>
				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>Two Factor Authentication</strong>
						<p class="text-instructions">
							Click on "Manage Two Factor Authentication" to manage your two factor authentication.
						</p>
					</div>
					<div class="col-md-8">
						<a href="/profile_information/two_factor">Manage Two Factor Authentication.</a>
					</div>
				</div>
				<hr/>

				<!-- UPDATE USER -->
				<div class="row submit-row">
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="updateUser"
						>
							Update User Details
						</a>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NSelect} from "naive-ui";

//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "ProfileInformation",
	setup() {
		return {v$: useVuelidate()};
	},
	props: {
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
			default: "light",
		},
		userResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	components: {
		NSelect,
		ValidationRendering,
	},
	data() {
		return {
			currentTheme: this.theme,
			emailModel: this.userResults[0].email,
			firstNameModel: this.userResults[0].first_name,
			lastNameModel: this.userResults[0].last_name,
			showMessage: false,
			themeList: [
				{
					label: "Light Theme",
					value: "light",
				},
				{
					label: "Dark Theme",
					value: "dark",
				},
			],
			themeModel: this.theme,
		};
	},
	watch: {
		themeModel() {
			this.showMessage = true;
		},
	},
	validations() {
		return {
			lastNameModel: {
				required,
				maxLength: maxLength(255),
			},
			firstNameModel: {
				required,
				maxLength: maxLength(255),
			},
		};
	},
	methods: {
		useNBTheme,
		updateUser() {
			//Check form validation
			this.v$.$touch();

			if (this.v$.$invalid) {
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("username", this.userResults[0].id);
			data_to_send.set("first_name", this.firstNameModel);
			data_to_send.set("last_name", this.lastNameModel);
			data_to_send.set("theme", this.themeModel);

			//Make the default "Please save" message disappear
			this.showMessage = false;

			//Updating the theme
			document.documentElement.setAttribute("data-bs-theme", this.themeModel);

			//Notify the user we are updating
			this.$store.dispatch("newToast", {
				header: "Currently Updating",
				message: "Your Profile has been submitted. Please wait",
				unique_type: "update",
				extra_classes: "bg-warning text-dark",
				delay: 0,
			});

			//Update the current theme with the one in the model
			this.currentTheme = this.themeModel;

			//Send data via axios
			this.axios.post(
				`${this.rootUrl}profile_information/update_data/`,
				data_to_send
			).then(() => {
				//Notify user of success update
				this.$store.dispatch("newToast", {
					header: "Update Successful",
					message: "Your Profile has been updated",
					unique_type: "update",
					extra_classes: "bg-success",
				});
			}).catch((error) => {
				//There was an error
				this.$store.dispatch("newToast", {
					header: "Error updating profile",
					message: `Can not update your profile sorry. Error -> ${error}`,
					unique_type: "update",
					extra_classes: "bg-danger",
				});
			});
		},
	},
	mounted() {
		//Send Root URL to VueX
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
			staticUrl: this.staticUrl,
		});
	},
};
</script>