<script setup lang="ts">
import {defineModel, defineEmits, onMounted} from "vue";
import {TextInput, ButtonComponent, ObjectStateEnum} from "whelk-ui"

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
const otpToken = defineModel("otpToken", {
	type: String,
	required: true,
})

// On Mounted
onMounted(() => {
	document.getElementById("input-two-factor-password")
})
</script>

<template>
	<div class="two-factor-panel">
		<h1 id="main-title">NearBeach Login</h1>
		<p class="error-message">{{ errorMessage }}</p>
		<TextInput class="compact"
				   label="Two Factor Password"
				   placeholderText="Please insert the two factor password"
				   :isRequired="false"
				   v-model="otpToken"
		/>

		<ButtonComponent
			class="primary"
			:object-state="buttonState"
			@click="emit('signIn')"
		>
			Submit 2FA
		</ButtonComponent>
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
}

</style>