<script setup lang="ts">
import {inject, ref} from 'vue'
import TextInput from "@/components/prefab/text_input/TextInput.vue";
import ButtonComponent from "@/components/prefab/button/ButtonComponent.vue";
import {ObjectStateEnum} from '@/utils/enums/ObjectStateEnum.ts';
import PasswordInput from "@/components/prefab/password_input/PasswordInput.vue";

// Injection
const apiClient = inject('apiClient');

// Define ref
const buttonState = ref(ObjectStateEnum.NoAction);
const username = ref('');
const password = ref('');

// Methods
function signIn() {
	// Set the data we want to send
	const data_to_send = new FormData();
	data_to_send.set("username", username.value);
	data_to_send.set("password", password.value);

	apiClient.post(
		"/api/v1/authentication/",
		data_to_send
	).then(() => {
		window.location.href = "/";
	})

	return;
}
</script>

<template>
	<div class="login-panel">
		<h1 id="main-title">NearBeach Login</h1>
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

		<ButtonComponent :object-state="buttonState"
						 label="Sign In"
						 @click="signIn"
		/>

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
}

</style>