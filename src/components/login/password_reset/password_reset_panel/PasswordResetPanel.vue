<script setup lang="ts">
import {inject, ref} from 'vue'
import {WlkButton, WlkPasswordInput} from "whelk-ui";
import type {AxiosInstance} from "axios";
import router from '@/router/loginRouter.ts';
import {useI18n} from "petite-vue-i18n";

// Define i18y
const {t} = useI18n({
	messages: {
		en: {
			reset_password: "Reset Password",
			confirm_password: "Confirm password",
			new_password: "New password",
			non_matching_password: "Passwords don't match",
			query_string_missing: "Query string missing",
		},
		ja: {
			reset_password: "パスワードをリセットする",
			confirm_password: "パスワードを認証する",
			new_password: "新しいパスワード",
			non_matching_password: "パスワードが一致しません",
			query_string_missing: "クエリ文字列がありません",
		}
	}
});

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
		errorMessage.value = t("non_matching_password");
		return;
	}

	// Check the query string
	const urlParams = new URLSearchParams(window.location.search);
	const uid : string | null = urlParams.get('uid');
	const token : string | null = urlParams.get('token');

	if (uid === '' || uid === null || token === '' || token === null) {
		errorMessage.value = t('query_string_missing');
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
		<h1 id="main-title">{{t("reset_password")}}</h1>
		<p class="error-message">
			{{ errorMessage }}
		</p>
		<WlkPasswordInput
			class="compact"
			:label="t('new_password')"
			:isRequired="true"
			v-model="password1"
		/>

		<WlkPasswordInput
			class="compact"
			:label="t('confirm_password')"
			:isRequired="true"
			v-model="password2"
		/>

		<WlkButton
			class="primary"
			@click="submitPasswordReset"
		>
			{{t('reset_password')}}
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