<script setup lang="ts">
import {onMounted, useTemplateRef} from "vue";
import {WlkTextInput, WlkButton, ObjectStateEnum, required} from "whelk-ui"
import {useI18n} from "petite-vue-i18n";

// Implement i18y
const {t} = useI18n()

// Define emits
const emit = defineEmits(['signIn']);

// Define props
defineProps({
	buttonState: {
		required: true,
		type: String,
		validator(value: string): boolean {
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
});

// On Mounted
onMounted(() => {
	document.getElementById("input-two-factor-password")
});

// Define functions
function signIn(event: Event) {
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
		<h1 id="main-title">{{ t("two_factor_panel.login_message") }}</h1>
		<p class="error-message">{{ errorMessage }}</p>
		<WlkTextInput class="compact"
		              :label="t('two_factor_panel.tfa')"
		              :placeholderText="t('two_factor_panel.tfa_placeholder')"
		              :validationRules="[required()]"
		              v-model="otpToken"
		              ref="otp-token-ref"
		/>

		<WlkButton
			class="primary"
			:disabled="buttonState === ObjectStateEnum.Disable"
			@click="signIn"
		>
			{{ t('two_factor_panel.submit_tfa') }}
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