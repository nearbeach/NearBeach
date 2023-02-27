<template>
	<div class="card">
		<div class="card-body">
			<h1>New User</h1>
			<hr />

			<!-- Username -->
			<div class="row">
				<div class="col-md-4">
					<strong>New User</strong>
					<p class="text-instructions">
						Please create a unique username, followed by the basic
						user details.
					</p>
				</div>
				<div class="col-md-8">
					<label
						>Username:
						<span
							class="error"
							v-if="
								!v$.usernameModel.required &&
								v$.usernameModel.$dirty
							"
						>
							Please supply a username.</span
						>
					</label>
					<input
						type="text"
						v-model="usernameModel"
						class="form-control"
					/>
				</div>
			</div>
			<hr />

			<!-- User Details -->
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
							<label
								>First Name:
								<span
									class="error"
									v-if="
										!v$.firstNameModel.required &&
										v$.firstNameModel.$dirty
									"
								>
									Please supply a first name.</span
								>
							</label>
							<input
								type="text"
								v-model="firstNameModel"
								class="form-control"
							/>
						</div>
						<div class="col-md-6">
							<label
								>Last Name:
								<span
									class="error"
									v-if="
										!v$.lastNameModel.required &&
										v$.lastNameModel.$dirty
									"
								>
									Please supply a last name.</span
								>
							</label>
							<input
								type="text"
								v-model="lastNameModel"
								class="form-control"
							/>
						</div>
						<div class="col-md-6">
							<label
								>Email:
								<span
									class="error"
									v-if="
										!v$.emailModel.required &&
										v$.emailModel.$dirty
									"
								>
									Please supply an email.</span
								>
								<span
									class="error"
									v-if="!v$.emailModel.email"
								>
									Please supply a valid email.</span
								>
							</label>
							<input
								type="email"
								v-model="emailModel"
								class="form-control"
							/>
						</div>
					</div>
				</div>
			</div>
			<hr />

			<!-- User Password -->
			<div class="row">
				<div class="col-md-4">
					<strong>Passwords</strong>
					<p class="text-instructions">
						Please type in a user password. The user will be able to
						reset their password to log in.
					</p>
				</div>
				<div class="col-md-8">
					<div class="row">
						<div class="col-md-6">
							<label>Password</label>
							<input
								type="password"
								v-model="password1Model"
								class="form-control"
							/>
						</div>
						<div class="col-md-6">
							<label>Retype Password</label>
							<input
								type="password"
								v-model="password2Model"
								class="form-control"
							/>
						</div>
					</div>
				</div>
			</div>

			<hr />
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						href="javascript:void(0)"
						class="btn btn-primary save-changes"
						v-on:click="addUser"
					>
						Add new User
					</a>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength, email } from "@vuelidate/validators";

	//Import mixins
	import errorModalMixin from "../../mixins/errorModalMixin";

	export default {
		name: "NewUser",
		setup() {
			return { v$: useVuelidate() };
		},
		props: {
			rootUrl: {
				type: String,
				default: "/",
			},
		},
		data() {
			return {
				emailModel: "",
				firstNameModel: "",
				lastNameModel: "",
				password1Model: "",
				password2Model: "",
				usernameModel: "",
			};
		},
		validations: {
			emailModel: {
				required,
				email,
			},
			firstNameModel: {
				required,
			},
			lastNameModel: {
				required,
			},
			password1Model: {
				required,
			},
			password2Model: {
				required,
			},
			usernameModel: {
				required,
			},
		},
		mixins: [errorModalMixin],
		methods: {
			addUser: async function () {
				//Check validation
				const isFormCorrect = await this.v$.$validate();
				if (!isFormCorrect) {
					this.showValidationErrorModal();

					//Just return
					return;
				}

				//Setup data to send
				const data_to_send = new FormData();
				data_to_send.set("username", this.usernameModel);
				data_to_send.set("email", this.emailModel);
				data_to_send.set("first_name", this.firstNameModel);
				data_to_send.set("last_name", this.lastNameModel);
				data_to_send.set("password1", this.password1Model);
				data_to_send.set("password2", this.password2Model);

				axios
					.post(`${this.rootUrl}new_user/save/`, data_to_send)
					.then((response) => {
						//Send user to the user information page
						window.location.href = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, "New User", "");
					});
			},
		},
	};
</script>

<style scoped></style>
