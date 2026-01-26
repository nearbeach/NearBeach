<script setup lang="ts">
import {defineModel} from "vue";
import {ButtonComponent, PasswordInput, TextInput, ObjectStateEnum} from "whelk-ui"

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

// Define models
const username = defineModel("username", {
	type: String,
	required: true,
})
const password = defineModel("password", {
	type: String,
	required: true,
})

</script>

<template>
	<div class="login-panel">
		<h1 id="main-title">NearBeach Login</h1>
		<p class="error-message">{{ errorMessage }}</p>
		<TextInput class="compact"
				   label="Email"
				   placeholderText="Your email address"
				   :isRequired="true"
				   v-model="username"
		/>
		<PasswordInput class="compact"
					   label="Password"
					   type="password"
					   placeholderText="Your password"
					   :isRequired="true"
					   :minLength="8"
					   v-model="password"
		/>

		<ButtonComponent
			class="primary"
			:object-state="buttonState"
			@click="emit('signIn')"
		>
			Sign In
		</ButtonComponent>

		<RouterLink to="/login/forgotten-password">Forgotten Password</RouterLink>
	</div>
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
		font-size: 0.75rem;
		line-height: 1rem;
		color: var(--text-red);
		font-weight: bold;
		margin: 0 0 0.25rem 0;

		&:before {
			content: "";
		}
	}
}

</style>