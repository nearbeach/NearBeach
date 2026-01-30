<script setup lang="ts">
import {inject, ref} from 'vue'
import {ButtonComponent, PasswordInput} from "whelk-ui";
import type {AxiosInstance} from "axios";
import router from '@/router/loginRouter.ts';

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Define refs
const password1 = ref('');
const password2 = ref('');
const errorMessage = ref('');

// Define functions
function submitPasswordReset(): void {
	// Check both password math
	if (password1.value !== password2.value) {
		errorMessage.value = "Passwords don't match";
		return;
	}

	// Check the query string
	const urlParams = new URLSearchParams(window.location.search);
	const uid : string | null = urlParams.get('uid');
	const token : string | null = urlParams.get('token');

	if (uid === '' || uid === null || token === '' || token === null) {
		errorMessage.value = "Query string missing";
		return;
	}

	// Send data to the backend
	const data_to_send = new FormData();
	data_to_send.set('password', password1.value);
	data_to_send.set('uid', `${uid}`);
	data_to_send.set('token', `${token}`);

	apiClient?.post(
		`/api/v1/authentication/reset-password/`,
		data_to_send,
	).then(() => {
		// Navigate to the login screen
		router.push('/login');
	}).catch(error => {
		errorMessage.value = error;
	});
}
</script>

<template>
	<div class="password-reset-panel">
		<h1 id="main-title">Reset Password</h1>
		<p class="error-message">
			{{ errorMessage }}
		</p>
		<PasswordInput
			class="compact"
			label="New Password"
			:isRequired="true"
			v-model="password1"
		/>

		<PasswordInput
			class="compact"
			label="Confirm Password"
			:isRequired="true"
			v-model="password2"
		/>

		<ButtonComponent
			class="primary"
			@click="submitPasswordReset"
		>
			Reset Password
		</ButtonComponent>


	</div>

</template>

<style scoped>
.password-reset-panel {
	display: flex;
	flex-direction: column;
	width: 100vw;
	margin: 5rem 1rem auto 1rem;

	@media (--small-screen) {
		width: 75vw;
		margin: auto;
	}

	@media (--medium-screen) {
		width: 100%;
		margin: auto 1rem;
	}

	@media (--large-screen) {
		max-width: var(--x-small-grid-width);
		margin: auto;
	}

	> .error-message {
		font-size: 1rem;
		line-height: 1.25rem;
		color: var(--text-red);
		font-weight: bold;
		margin: 0 0 0.25rem 0;

		&:before {
			content: " ";
			min-height: 1.25rem;
			display: inline-block;
		}
	}
}

</style>