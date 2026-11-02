<script setup lang="ts">
import {ref} from 'vue'
import {WlkButton, WlkPasswordInput} from "whelk-ui";
import router from '@/router/loginRouter.ts';
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18y
const {t} = useI18n();

// Define refs
const password1 = ref('');
const password2 = ref('');
const errorMessage = ref('');

// Define functions
async function submitPasswordReset(): Promise<void> {
	// Check both password math
	if (password1.value !== password2.value) {
		errorMessage.value = t("password_reset_panel.non_matching_password");
		return;
	}

	// Check the query string
	const urlParams = new URLSearchParams(window.location.search);
	const uid: string | null = urlParams.get('uid');
	const token: string | null = urlParams.get('token');

	if (uid === '' || uid === null || token === '' || token === null) {
		errorMessage.value = t('password_reset_panel.query_string_missing');
		return;
	}

	// Send data to the backend
	const body = {
		password: password1.value,
		uid: `${uid}`,
		token: `${token}`,
	}

	// Update password in backend
	const response = await fetch(
		"/api/v1/authentication/reset-password/",
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	);

	// Handle response codes
	switch (response.status) {
		case 200:
			// User successfully updated password
			await router.push('/login');
			break;
		default:
			// Handle other response codes
			errorMessage.value = response.statusText;
			break;
	}
}
</script>

<template>
	<div class="password-reset-panel">
		<h1 id="main-title">{{ t("password_reset_panel.reset_password") }}</h1>
		<p class="error-message">
			{{ errorMessage }}
		</p>
		<WlkPasswordInput
			class="compact"
			:label="t('password_reset_panel.new_password')"
			:isRequired="true"
			v-model="password1"
		/>

		<WlkPasswordInput
			class="compact"
			:label="t('password_reset_panel.confirm_password')"
			:isRequired="true"
			v-model="password2"
		/>

		<WlkButton
			class="primary"
			@click="submitPasswordReset"
		>
			{{ t('password_reset_panel.reset_password') }}
		</WlkButton>


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