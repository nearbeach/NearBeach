<script setup lang="ts">
import {ref, inject} from "vue";
import LoginImage from "../login_image/LoginImage.vue"
import ForgottenPasswordPanel from "./forgotten_password_panel/ForgottenPasswordPanel.vue"
import PasswordResetDone from "./password_reset_done/PasswordResetDone.vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define ref
const isDone = ref(false);
const emailAddress = ref("");
const errorMessage = ref("");

// Define functions
async function submitPasswordReset(): Promise<void> {
	isDone.value = true;

	// Send request to backend
	const body = {
		email: emailAddress.value,
	}

	await fetch(
		`/api/v1/authentication/forgotten-password/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	).catch((error: string) => {
		errorMessage.value = error
	});
}
</script>

<template>
	<div class="forgotten-password">
		<LoginImage/>
		<PasswordResetDone
			v-bind:errorMessage="errorMessage"
			v-if="isDone"
		/>
		<ForgottenPasswordPanel
			v-else
			v-model:email-address="emailAddress"
			@passwordReset="submitPasswordReset"
		/>
	</div>
</template>

<style scoped>
.forgotten-password {
	display: flex;
	flex-direction: row;
	height: 100%;
}

</style>