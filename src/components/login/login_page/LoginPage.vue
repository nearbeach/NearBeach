<script setup lang="ts">
import {inject, ref} from 'vue'
import LoginImage from "@/components/login/login_image/LoginImage.vue";
import LoginPanel from "@/components/login/login_page/login_panel/LoginPanel.vue";
import {ObjectStateEnum} from "@/utils/enums/ObjectStateEnum.ts";
import type {AxiosInstance} from "axios";
import TwoFactorPanel from "@/components/login/login_page/two_factor_panel/TwoFactorPanel.vue";

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Define ref
const username = ref('');
const password = ref('');
const otp_token = ref('');
const error_message = ref('');
const buttonState = ref(ObjectStateEnum.NoAction);
const isLoginPage = ref(true);

// Methods
function ActivateTwoFactorPanel() {
	// Backend requires a 2FA key
	isLoginPage.value = false;

	// Tell user they can use the button again
	buttonState.value = ObjectStateEnum.NoAction;
}

function signIn() {
	// Set the data we want to send
	const data_to_send = new FormData();
	data_to_send.set("username", username.value);
	data_to_send.set("password", password.value);
	data_to_send.set("otp_token", otp_token.value);

	// Tell the user we are logging in
	buttonState.value = ObjectStateEnum.LoggingIn;

	apiClient?.post(
		"/api/v1/authentication/",
		data_to_send
	).then((response) => {
		switch (response.data.status) {
			case "success":
				UserLoggedIn();
				break;
			default:
				ActivateTwoFactorPanel();
				break;
		}
	}).catch((error) => {
		// TODO - Add code to handle errors
	})
}

function UserLoggedIn() {
	const urlParams = new URLSearchParams(window.location.search);
	window.location.href = urlParams.get('next') ?? "/";
}

</script>

<template>
	<div class="login">
		<LoginImage/>
		<LoginPanel
			v-show="isLoginPage"
			:buttonState="buttonState"
			:error-message="error_message"
			v-model:password="password"
			v-model:username="username"
			@signIn="signIn"
		/>

		<TwoFactorPanel
			v-show="!isLoginPage"
			:button-state="buttonState"
			:error-message="error_message"
			v-model:otp-token="otp_token"
			@signIn="signIn"
		/>

	</div>
</template>

<style scoped>
.login {
	display: flex;
	flex-direction: row;
	height: 100%;
}
</style>