<script setup lang="ts">
import { ref, watch} from 'vue'
import { WlkButton, WlkTextInput, ObjectStateEnum } from "whelk-ui";
import { type ObjectStateEnumType } from "whelk-ui";
import {useI18n} from "petite-vue-i18n";

// Define i18y
const {t} = useI18n({
	messages: {
		en: {
			forgotten_password: "Forgotten password",
			email: "Email",
			email_placeholder: "Email",
			go_back: "Go back to login",
			submit: "Submit",
		},
		ja: {
			forgotten_password: "パスワードを忘れた場合",
			email: "メール",
			email_placeholder: "あなたのメールアドレス",
			go_back: "ログインに戻る",
			submit: "提出する",
		},
	}
});

// Define emit
const emit = defineEmits(['passwordReset']);

// Define model
const emailAddress = defineModel('emailAddress', {
	type: String,
	required: true,
})

// Define ref
const buttonState = ref<ObjectStateEnumType>(ObjectStateEnum.NoAction);
const disableButton = ref<boolean>(true);
const disableTextInput = ref<boolean>(false);

// Define watch
watch(emailAddress, (new_value) => {
    if (buttonState.value !== ObjectStateEnum.NoAction) {
        // Disable this by default
        disableButton.value = true;
        disableTextInput.value = true;

        // Nothing to do
        return null;
    }

    // Make sure emailAddress is an email address
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    disableButton.value = !emailRegex.test(new_value);

    return null;
});

// Define Functions
function passwordReset() {
    // Emit the event upstream
    emit("passwordReset");

    // Update the button state
    buttonState.value = ObjectStateEnum.Loading;
    disableButton.value = true;
    disableTextInput.value = true;
}
</script>

<template>
	<form class="forgotten-password-panel"
		  @submit.prevent="passwordReset()"
	>
		<h1 id="main-title">{{ t("forgotten_password")}}</h1>
		<WlkTextInput class="compact"
                      :label="t('email')"
                      :placeholderText="t('email_placeholder')"
                      :isRequired="true"
                      :disabled="disableTextInput"
                      v-model="emailAddress"
		/>

		<WlkButton
			class="primary"
			:disabled="disableButton"
			:is-action-running="buttonState === ObjectStateEnum.Loading"
		>
			{{ t("submit") }}
		</WlkButton>

		<RouterLink to="/login">{{ t('go_back')}}</RouterLink>
	</form>
</template>

<style scoped>
.forgotten-password-panel {
	display: flex;
	flex-direction: column;
	width: 100vw;
	margin: 5rem 1rem auto 1rem;

	> a {
		font-size: 0.75rem;
		font-weight: 100;
		margin-top: 1rem;
	}

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
}

</style>