<script setup lang="ts">
import {onMounted, ref} from 'vue'
import LoginImage from "@/components/login/login_image/LoginImage.vue";
import LoginPanel from "@/components/login/login_page/login_panel/LoginPanel.vue";
import {ObjectStateEnum} from "@/utils/enums/ObjectStateEnum.ts";
import TwoFactorPanel from "@/components/login/login_page/two_factor_panel/TwoFactorPanel.vue";
import {useI18n} from 'petite-vue-i18n'
import SsoPanel from "@/components/login/login_page/sso_panel/SsoPanel.vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {getSafeNextUrl} from "@/composables/getSafeNextUrl.ts";
import {useSsoProviders} from "@/composables/useSsoProviders.ts";

// Define i18y
const {t} = useI18n();

// Define ref
let failCount = 0;
const usernameModel = ref<string>('');
const passwordModel = ref<string>('');
const otpTokenModel = ref<string>('');
const errorMessage = ref<string>('');
const buttonState = ref(ObjectStateEnum.NoAction);
const isLoginPage = ref<boolean>(true);
const {providers: ssoProviders, loadProviders} = useSsoProviders();

// Why a single sign-on attempt came back to the login page
const SSO_ERROR_MESSAGES: Record<string, string> = {
	no_account: "login_page.sso_error_no_account",
	no_group: "login_page.sso_error_no_group",
	account_disabled: "login_page.sso_error_account_disabled",
	two_factor_required: "login_page.sso_error_two_factor_required",
	provider_unavailable: "login_page.sso_error_provider_unavailable",
	provider_misconfigured: "login_page.sso_error_provider_unavailable",
};

onMounted(() => {
	const ssoError = new URLSearchParams(window.location.search).get("sso_error");
	if (ssoError !== null) {
		errorMessage.value = t(SSO_ERROR_MESSAGES[ssoError] ?? "login_page.sso_error_generic");
	}

	loadProviders();
});

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
		errorMessage.value = t("login_page.validation_error_message");
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
		case 200: {
			// Username and Password are correct
			const data: { status: string } = await response.json();

			// Depends on the status - initiates the correct action
			data.status === "success"
				? UserLoggedIn()
				: ActiveTwoFactorPanel();
			break;
		}
		case 401:
			failCount++;
			errorMessage.value = failCount <= 5
				? t("login_page.error_message")
				: t("login_page.error_final_message");
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
	window.location.href = getSafeNextUrl(urlParams.get('next'));
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
		>
			<template #sso>
				<SsoPanel :providers="ssoProviders"/>
			</template>
		</LoginPanel>

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