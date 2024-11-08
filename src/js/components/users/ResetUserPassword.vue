<template>
	<div>
		<div class="card">
			<div class="card-body">
				<h2>Reset Password</h2>
				<hr/>

				<!-- PASSWORD -->
				<div class="row">
					<div class="col-md-4">
						<strong>Passwords</strong>
						<p class="text-instructions">
							Users have the ability to reset their password from
							the login page. If needed, please click on the link
							to be taken to the password reset form.
						</p>
					</div>
					<div class="col-md-8">
						<button
							type="button"
							class="btn btn-warning"
							v-on:click="passwordResetClicked"
						>
							Password Reset
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- PASSWORD RESET MODAL -->
		<div
			class="modal fade"
			id="passwordResetModal"
			tabindex="-1"
			aria-labelledby="exampleModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h2>
							Reset User Password
						</h2>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
							id="passwordResetCloseButton"
						>
							<span aria-hidden="true"></span>
						</button>
					</div>
					<div class="modal-body">
						<div class="row">
							<div class="col-md-6">
								<label>Password</label>
								<input
									type="password"
									class="form-control"
									v-model="password1Model"
								/>
							</div>
							<div class="col-md-6">
								<label>Confirm Password</label>
								<input
									type="password"
									class="form-control"
									v-model="password2Model"
								/>
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<validation-rendering
									v-bind:error-list="v$.password1Model.$errors"
								></validation-rendering>
								<div class="col-md-12"
									 v-if="password1Model !== password2Model"
								>
									<span class="error">Passwords need to be the same
									</span>
								</div>
							</div>
						</div>
					</div>
					<div class="modal-footer">
						<button
							type="button"
							class="btn btn-secondary"
							v-on:click="closeModal"
						>
							Close
						</button>
						<button
							type="button"
							class="btn btn-primary"
							v-on:click="updatePassword"
							v-bind:disabled="disableButton"
						>
							Update Password
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript components
import {Modal} from "bootstrap";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core"
import {required, minLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "ResetUserPassword",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		ValidationRendering,
	},
	props: {
		location: {
			type: String,
			default: "/",
		},
		username: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			password1Model: "",
			password2Model: "",
		};
	},
	validations: {
		password1Model: {
			required,
			minLength: minLength(8),
		},
	},
	watch: {
		password1Model() {
			//Validate the passwords as users are typing
			this.v$.$validate();
		},
		password2Model() {
			//Validate the passwords as users are typing
			this.v$.$validate();
		}
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
		disableButton() {
			//Both passwords have to be the same
			const condition_1 = this.password1Model === this.password2Model;

			//Passwords can not be less than 8 character
			const condition_2 = this.password1Model.length >= 8;

			//If all conditions are true, send back false (to enable the button)
			return !(condition_1 && condition_2 === true);
		},
	},
	methods: {
		closeModal() {
			//Clear both passwords
			this.password1Model = "";
			this.password2Model = "";

			//Close modal
			document.getElementById("passwordResetCloseButton").click();
		},
		passwordResetClicked() {
			//Opens the password reset modal
			const passwordResetModal = new Modal(
				document.getElementById("passwordResetModal")
			);
			passwordResetModal.show();
		},
		updatePassword() {
			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("password", this.password1Model);
			data_to_send.set("username", this.username);

			//Notify User
			this.$store.dispatch("newToast", {
				header: "Updating User Password",
				message: "Please wait. Updating Password",
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: "update-user-password",
			});

			//Setup Axios to send data
			this.axios.post(
				`${this.rootUrl}${this.location}update_user_password/`,
				data_to_send
			).then(() => {
				this.closeModal();

				this.$store.dispatch("newToast", {
					header: "Updated User Password",
					message: "User Password Successfully Updated",
					extra_classes: "bg-success",
					delay: 0,
					unique_type: "update-user-password",
				});
			}).catch((error) => {
				let error_message = "There was an issue trying to save your password.";

				if (error.response !== undefined) {
					error_message = "Please fix the following issues: ";

					// Loop through each key and value and write the error message.
					for (const [key, value] of Object.entries(error.response.data)) {
						error_message = `${error_message} ${key} - ${value[0].message} `;
					}
				}

				this.$store.dispatch("newToast", {
					header: "Error Updating User Password",
					message: error_message,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update-user-password",
				});
			});
		},
	},
};
</script>


