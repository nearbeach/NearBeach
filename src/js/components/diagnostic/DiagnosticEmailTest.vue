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
			</p>
			<ul>
				<li>Spam Blocking Email</li>
				<li>Server not sending</li>
				<li>Email Credentials Incorrect</li>
			</ul>
		</div>
		<div class="col-md-8">
			<button
v-if="emailState === 'not_started'"
					class="btn btn-warning"
					@click="sendEmail"
			>Send Email</button>

			<div
v-if="emailState === 'sending_email'"
				 class="alert alert-warning"
			>
				Currently sending the email. Please wait.
			</div>

			<div
v-if="emailState === 'sent_email'"
				 class="alert alert-success"
			>
				Email sent by backend. Please check your inbox. If you do not receive the email, please check to make
				sure it is not in spam.
			</div>

			<div
v-if="emailState === 'failed_sending'"
				 class="alert alert-danger"
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
	data() {
		return {
			emailState: "not_started",
		}
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
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