<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Email Test</strong>
			<p class="text-instructions">
				Please click "Send Email", to send an email to yourself. If you do not receive an email, it means there
				is something broken.
			</p>
			<p class="text-instructions">
				Potential Issues
				<ul>
					<li>Spam Blocking Email</li>
					<li>Server not sending</li>
					<li>Email Credentials Incorrect</li>
				</ul>
			</p>
		</div>
		<div class="col-md-8">
			<button class="btn btn-warning"
					v-if="emailState === 'not_started'"
					v-on:click="sendEmail"
			>Send Email</button>

			<div class="alert alert-warning"
				 v-if="emailState === 'sending_email'"
			>
				Currently sending the email. Please wait.
			</div>

			<div class="alert alert-success"
				 v-if="emailState === 'sent_email'"
			>
				Email sent by backend. Please check your inbox. If you do not receive the email, please check to make
				sure it is not in spam.
			</div>

			<div class="alert alert-danger"
				 v-if="emailState === 'failed_sending'"
			>
				Sorry. The backend server could not send the email. Please check logs
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "DiagnosticEmailTest",
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	data() {
		return {
			emailState: "not_started",
		}
	},
	methods: {
		sendEmail() {
			//Update email state
			this.emailState = "sending_email";

			this.axios.post(
				`${this.rootUrl}diagnostic_information/email_test/`,
			).then(() => {
				this.emailState = "sent_email";
			}).catch((error) => {
				this.emailState = "failed_sending";

				this.$store.dispatch("newToast", {
					header: "Error sending Email",
					message: `${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})
		}
	}
}
</script>