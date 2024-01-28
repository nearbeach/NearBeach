<template>
	<div class="card">
		<div class="card-body">
			<h1>New User</h1>
			<hr/>

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
						<validation-rendering v-bind:error-list="v$.usernameModel.$errors"
						></validation-rendering>
					</label>
					<input
						type="text"
						v-model="usernameModel"
						class="form-control"
					/>
				</div>
			</div>
			<hr/>

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
								<validation-rendering v-bind:error-list="v$.firstNameModel.$errors"
								></validation-rendering>
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
								<validation-rendering v-bind:error-list="v$.lastNameModel.$errors"
								></validation-rendering>
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
								<validation-rendering v-bind:error-list="v$.emailModel.$errors"
								></validation-rendering>
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
			<hr/>

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
							<label>
								Password
								<validation-rendering v-bind:error-list="v$.password1Model.$errors"
								></validation-rendering>
							</label>
							<input
								type="password"
								v-model="password1Model"
								class="form-control"
							/>
						</div>
						<div class="col-md-6">
							<label>
								Retype Password
								<validation-rendering v-bind:error-list="v$.password2Model.$errors"
								></validation-rendering>
							</label>
							<input
								type="password"
								v-model="password2Model"
								class="form-control"
							/>
						</div>
					</div>
				</div>
			</div>

			<hr/>
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
//Validation
import useVuelidate from "@vuelidate/core";
import {email, helpers, required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";
const usernameRegex = helpers.regex(/^[0-9a-zA-Z,_@+.\-]{1,150}$/);

export default {
	name: "NewUser",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		ValidationRendering,
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
			usernameRegex: helpers.withMessage(
				"Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.",
				usernameRegex
			),
		},
	},
	methods: {
		addUser: async function () {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
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

			this.axios.post(
				`${this.rootUrl}new_user/save/`,
				data_to_send
			).then((response) => {
				//Send user to the user information page
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to create user",
					message: `Sorry. Failed to create user. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>

<style scoped></style>
