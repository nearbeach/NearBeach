<script setup lang="ts">
import {ref, inject} from "vue";
import type {AxiosInstance} from "axios";
import LoginImage from "../login_image/LoginImage.vue"
import ForgottenPasswordPanel from "./forgotten_password_panel/ForgottenPasswordPanel.vue"
import PasswordResetDone from "./password_reset_done/PasswordResetDone.vue";

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Define ref
const isDone = ref(false);
const emailAddress = ref("");
const errorMessage = ref("");

// Define functions
function submitPasswordReset(): void {
	isDone.value = true;

	// Send request to backend
	const data_to_send = new FormData();
	data_to_send.set("email", emailAddress.value);

	apiClient?.post(
		`/api/v1/authentication/forgotten-password/`,
		data_to_send,
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