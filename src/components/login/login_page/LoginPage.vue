<script setup lang="ts">
import {ref} from 'vue'
import LoginImage from "@/components/login/login_image/LoginImage.vue";
import LoginPanel from "@/components/login/login_page/login_panel/LoginPanel.vue";
import {ObjectStateEnum} from "@/utils/enums/ObjectStateEnum.ts";
import TwoFactorPanel from "@/components/login/login_page/two_factor_panel/TwoFactorPanel.vue";
import {useI18n} from 'petite-vue-i18n'
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18y
const {t} = useI18n({
	messages: {
		en: {
			error_message: "Credentials have failed",
			error_final_message: "Impostor detected, initiating self-destruction",
			validation_error_message: "Please fill out all fields",
		},
		ja: {
			error_message: "資格情報が失敗しました",
			error_final_message: "詐欺師が検出され、自己破壊を開始します",
			validation_error_message: "すべての項目にご記入ください",
		}
	}
});

// Define ref
let failCount = 0;
const usernameModel = ref<string>('');
const passwordModel = ref<string>('');
const otpTokenModel = ref<string>('');
const errorMessage = ref<string>('');
const buttonState = ref(ObjectStateEnum.NoAction);
const isLoginPage = ref<boolean>(true);

// Methods
function ActivateLoginPanel() {
	// Go back to the login page
	isLoginPage.value = true;

	// Tell the user they can use the button again
	buttonState.value = ObjectStateEnum.NoAction;
}

function ActiveTwoFactorPanel() {
	// Backend requires a 2FA key
	isLoginPage.value = false;

	// Tell the user they can use the button again
	buttonState.value = ObjectStateEnum.NoAction;
}

async function signIn() {
	// Check field validation
	if (usernameModel.value === "" || usernameModel.value === null || passwordModel.value === "" || passwordModel.value === null) {
		errorMessage.value = t("validation_error_message");
		return;
	}

	// Set the data we want to send
	const body = {
		username: usernameModel.value,
		password: passwordModel.value,
		otp_token: otpTokenModel.value,
	}

	// Tell the user we are logging in
	buttonState.value = ObjectStateEnum.LoggingIn;

	// Attempt the login
	const response = await fetch(
		"/api/v1/authentication/",
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		}
	);

	// Depending on the status code - depends what we do next
	switch (response.status) {
		case 200:
			// Username and Password are correct
			const data: { status: string } = await response.json();

			// Depends on the status - initiates the correct action
			data.status === "success"
				? UserLoggedIn()
				: ActiveTwoFactorPanel();
			break;
		case 401:
			errorMessage.value = failCount <= 5
				? t("error_message")
				: t("error_final_message");
			usernameModel.value = "";
			passwordModel.value = "";
			otpTokenModel.value = "";
			ActivateLoginPanel();
			break;
		default:
			// Something went wrong
			errorMessage.value = response.statusText;
			break;
	}
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
			:error-message="errorMessage"
			v-model:password="passwordModel"
			v-model:username="usernameModel"
			@signIn="signIn"
		/>

		<TwoFactorPanel
			v-show="!isLoginPage"
			:button-state="buttonState"
			:error-message="errorMessage"
			v-model:otp-token="otpTokenModel"
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