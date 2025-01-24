<template>
	<div class="card">
		<div class="card-body">
			<h1 class="mb-4">User Information</h1>
			<a v-bind:href="`${this.rootUrl}search/user/`">
				Go back to user list
			</a>
			<hr/>

			<!-- USERNAME -->
			<div class="row">
				<div class="col-md-4">
					<strong>UserName</strong>
					<p class="text-instructions">
						The username is set and can not be changed from this
						location. If you need to change the username, please go
						to the Django Admin Panel.
					</p>
					<p class="text-instructions">
						The ID is the primary key assigned to the username. This
						can not be edited. It can be ignored.
					</p>
				</div>
				<div class="col-md-8">
					<strong>Username:</strong>
					{{ userResults[0]["fields"]["username"] }}
					<strong> | ID:</strong> {{ userResults[0]["pk"] }}
				</div>
			</div>

			<!-- USER DETAILS -->
			<hr/>
			<div class="row">
				<div class="col-md-4">
					<strong>User Details</strong>
					<p class="text-instructions">
						Please fill out the user details.
					</p>
				</div>
				<div class="col-md-8">
					<div class="row">
						<div class="col-md-6">
							<label for="first-name">
								First Name:
								<validation-rendering
									v-bind:error-list="v$.firstNameModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="first-name"
								type="text"
								v-model="firstNameModel"
								class="form-control"
							/>
						</div>
						<div class="col-md-6">
							<label for="last-name">
								Last Name:
								<validation-rendering
									v-bind:error-list="v$.lastNameModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="last-name"
								type="text"
								v-model="lastNameModel"
								class="form-control"
							/>
						</div>
						<div class="col-md-6 mt-4">
							<label for="email">
								Email:
								<validation-rendering
									v-bind:error-list="v$.emailModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="email"
								type="email"
								v-model="emailModel"
								class="form-control"
							/>
						</div>
					</div>
				</div>
			</div>
			<hr/>

			<!-- Active USER -->
			<div class="row">
				<div class="col-md-4">
					<strong>Active User</strong>
					<p class="text-instructions">
						Untick this option if the user is no longer active.
					</p>
				</div>
				<div class="col-md-8">
					<label>Is User Active? </label>
					<input
						type="checkbox"
						v-model="isActiveModel"
					/>
				</div>
			</div>
			<hr/>

			<!-- User is SUPER -->
			<div class="row">
				<div class="col-md-4">
					<strong>Is User a Superuser</strong>
					<p class="text-instructions">
						Tick this functionality if you would like the user to
						gain access to the /admin/ functionality. This is not
						recommended for anyone outside of an IT team.
					</p>
				</div>
				<div class="col-md-8">
					<label>Is User a Superuser? </label>
					<input
						type="checkbox"
						v-model="isSuperuserModel"
					/>
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
</template>

<script>
//Vue is like "I wanna write JS in my HTML" and React is like "I wanna write my HTML as JS"

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength, email} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "UserInformation",
	setup() {
		return {v$: useVuelidate()};
	},
	props: {
		userResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	components: {
		ValidationRendering,
	},
	data() {
		return {
			emailModel: this.userResults[0].fields.email,
			isActiveModel: this.userResults[0].fields.is_active,
			isSuperuserModel: this.userResults[0].fields.is_superuser,
			firstNameModel: this.userResults[0].fields.first_name,
			lastNameModel: this.userResults[0].fields.last_name,
		};
	},
	validations: {
		lastNameModel: {
			required,
			maxLength: maxLength(255),
		},
		firstNameModel: {
			required,
			maxLength: maxLength(255),
		},
		emailModel: {
			required,
			email,
			maxLength: maxLength(255),
		},
	},
	methods: {
		updateUser() {
			//Check form validation
			this.v$.$touch();

			if (this.v$.$invalid) {
				this.$store.dispatch("newToast", {
					header: "Please check all fields",
					message: "Failed validation. Please check all fields are validated",
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_user",
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Start the loading modal
			this.$store.dispatch("newToast", {
				header: "Updating Current User",
				message: "Currently Updating User",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "update_user",
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("email", this.emailModel);
			data_to_send.set("is_active", this.isActiveModel);
			data_to_send.set("is_superuser", this.isSuperuserModel);
			data_to_send.set("first_name", this.firstNameModel);
			data_to_send.set("last_name", this.lastNameModel);

			this.axios.post(
				`${this.rootUrl}user_information/${this.userResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				//Hide the loading modal
				this.$store.dispatch("newToast", {
					header: "User Updated",
					message: "User successfully updated",
					extra_classes: "bg-success",
					unique_type: "update_user",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed Updating Users",
					message: `Sorry. Failed updating your user. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_user",
				});
			});
		},
	},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});

		this.$store.commit({
			type: "updateTitle",
			title: `${this.firstNameModel} ${this.lastNameModel}`,
		});
	},
};
</script>


