<script setup lang="ts">
import { ref } from 'vue'
import ButtonComponent from "@/components/prefab/button/ButtonComponent.vue";
import TextInput from "@/components/prefab/text_input/TextInput.vue";
import {ObjectStateEnum} from '@/utils/enums/ObjectStateEnum.ts';

// Define ref
const buttonState = ref(ObjectStateEnum.NoAction);
</script>

<template>
	<div class="forgotten-password-panel">
		<h1 id="main-title">Forgotten Password</h1>
		<TextInput class="compact"
				   label="Email"
				   placeholderText="Your email address"
				   :isRequired="true"
		/>

		<ButtonComponent :object-state="buttonState"
						 label="Reset Password"
		/>

		<RouterLink to="/login">Go back to login</RouterLink>
	</div>
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