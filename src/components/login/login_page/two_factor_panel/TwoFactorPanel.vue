<script setup lang="ts">
import {defineModel, defineEmits, onMounted, useTemplateRef} from "vue";
import {WlkTextInput, WlkButton, ObjectStateEnum, required} from "whelk-ui"
import {useI18n} from "petite-vue-i18n";

// Implement i18y
const {t} = useI18n({
	messages: {
		en: {
			login_message: "NearBeach Login",
			submit_tfa: "Submit 2FA",
			tfa: "Two Factor Password",
			tfa_placeholder: "Please insert the two factor password",
		},
		ja: {
			login_message: "ニアビーチログイン",
			submit_tfa: "2要素認証を送信",
			tfa: "二要素パスワード",
			tfa_placeholder: "2要素パスワードを入力してください",
		}
	}
})

// Define emits
const emit = defineEmits(['signIn']);

// Define props
defineProps({
	buttonState: {
		required: true,
		type: String,
		validator: function (value: string): boolean {
			const enumValues: string[] = Object.values(ObjectStateEnum);
			return enumValues.includes(value);
		},
	},
	errorMessage: {
		required: false,
		type: String,
	}
});

// Define template refs
const otpTokenRef = useTemplateRef("otp-token-ref");

// Define models
const otpToken = defineModel("otpToken", {
	type: String,
	required: true,
})

// On Mounted
onMounted(() => {
	document.getElementById("input-two-factor-password")
})

// Define functions
function signIn(event: any) {
	// Prevent default
	event.preventDefault();

	// Validate
	otpTokenRef?.value?.checkValidation();

	// Emit data upstream
	emit('signIn');
}
</script>

<template>
	<div class="two-factor-panel">
		<h1 id="main-title">{{ t("login_message") }}</h1>
		<p class="error-message">{{ errorMessage }}</p>
		<WlkTextInput class="compact"
		              :label="t('tfa')"
		              :placeholderText="t('tfa_placeholder')"
		              :validationRules="[required()]"
		              v-model="otpToken"
		              ref="otp-token-ref"
		/>

		<WlkButton
			class="primary"
			:object-state="buttonState"
			@click="signIn"
		>
			{{ t('signIn') }}
		</WlkButton>
	</div>
</template>

<style scoped>
.two-factor-panel {
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

	> .error-message {
		font-size: 1rem;
		line-height: 1.25rem;
		color: var(--text-red);
		font-weight: bold;
		margin: 0 0 0.25rem 0;

		&:before {
			content: ".";
			visibility: hidden;
		}
	}
}

</style>