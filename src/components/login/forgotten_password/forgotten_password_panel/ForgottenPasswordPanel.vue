<script setup lang="ts">
import { defineEmits, ref, defineModel } from 'vue'
import { WlkButton, WlkTextInput, ObjectStateEnum } from "whelk-ui";
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
const buttonState = ref(ObjectStateEnum.NoAction);
</script>

<template>
	<form class="forgotten-password-panel"
		  @submit="emit('passwordReset')"
	>
		<h1 id="main-title">{{ t("forgotten_password")}}</h1>
		<WlkTextInput class="compact"
				   :label="t('email')"
				   :placeholderText="t('email_placeholder')"
				   :isRequired="true"
				   v-model="emailAddress"
		/>

		<WlkButton
			class="primary"
			:object-state="buttonState"
			@click="emit('passwordReset')"
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