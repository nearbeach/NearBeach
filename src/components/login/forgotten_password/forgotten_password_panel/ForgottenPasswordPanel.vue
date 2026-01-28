<script setup lang="ts">
import { defineEmits, ref } from 'vue'
import { ButtonComponent, TextInput, ObjectStateEnum } from "whelk-ui";

// Define emit
const emit = defineEmits(['passwordReset']);

// Define ref
const buttonState = ref(ObjectStateEnum.NoAction);
const emailAddress = ref("");
</script>

<template>
	<form class="forgotten-password-panel"
		  @submit="emit('passwordReset')"
	>
		<h1 id="main-title">Forgotten Password</h1>
		<TextInput class="compact"
				   label="Email"
				   placeholderText="Your email address"
				   :isRequired="true"
				   v-model="emailAddress"
		/>

		<ButtonComponent
			class="primary"
			:object-state="buttonState"
			@click="emit('passwordReset')"
		>
			Submit
		</ButtonComponent>

		<RouterLink to="/login">Go back to login</RouterLink>
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