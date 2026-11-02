<script setup lang="ts">
import {onMounted, useTemplateRef} from "vue";
import {WlkButton, WlkPasswordInput, WlkTextInput, required, minLength, ObjectStateEnum} from "whelk-ui"
import {useI18n} from "petite-vue-i18n";

// Define i18y
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
const usernameRef = useTemplateRef("username-ref");
const passwordRef = useTemplateRef("password-ref")

// Define models
const username = defineModel("username", {
	type: String,
	required: true,
})
const password = defineModel("password", {
	type: String,
	required: true,
});

// Customer directives
const vFocus = {
	mounted: (el: HTMLElement) => el.focus()
}

// On Mount
onMounted(() => {
	// Username should be in focus
	document.getElementById("input-username")?.focus();
});

// Declare functions
function signIn(event: Event) {
	// Prevent form from submitting
	event.preventDefault();

	// Validate every field
	usernameRef?.value?.checkValidation();
	passwordRef?.value?.checkValidation();

	// Sign in
	emit("signIn");
}
</script>

<template>
	<form class="login-panel"
	      @submit="signIn"
	>
		<h1 id="main-title">{{ t("login_panel.login_message") }}</h1>
		<p class="error-message">{{ errorMessage }}</p>
		<WlkTextInput class="compact"
		              :label="t('login_panel.username')"
		              :placeholderText="t('login_panel.username_placeholder')"
		              :validationRules="[required()]"
		              v-model="username"
		              v-focus
		              ref="username-ref"
		/>
		<WlkPasswordInput class="compact"
		                  :label="t('login_panel.password')"
		                  :placeholderText="t('login_panel.password_placeholder')"
		                  :validationRules="[required(), minLength(8)]"
		                  v-model="password"
		                  ref="password-ref"
		/>

		<WlkButton
			class="primary"
			:disabled="buttonState === ObjectStateEnum.Disable"
			:is-action-running="buttonState === ObjectStateEnum.LoggingIn"
			@click="signIn"
		>
			{{ t("login_panel.sign_in") }}
		</WlkButton>

		<RouterLink to="/login/forgotten-password">{{ t("login_panel.forgotten_password") }}</RouterLink>
	</form>
</template>

<style scoped>
.login-panel {
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