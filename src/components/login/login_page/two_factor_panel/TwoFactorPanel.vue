<script setup lang="ts">
import {defineModel, defineEmits} from "vue";
import TextInput from "@/components/prefab/text_input/TextInput.vue";
import ButtonComponent from "@/components/prefab/button/ButtonComponent.vue";
import {ObjectStateEnum} from "@/utils/enums/ObjectStateEnum.ts";

// Define emits
const emit = defineEmits(['signIn']);

// Define props
defineProps({
	buttonState: {
		required: true,
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
</script>

<template>
	<div class="two-factor-panel">
		<h1 id="main-title">NearBeach Login</h1>
		<p class="error-message">{{errorMessage}}</p>
		<TextInput class="compact"
				   label="Two Factor Password"
				   placeholderText="Please insert the two factor password"
				   :isRequired="false"
				   v-model="otpToken"
		/>

		<ButtonComponent :object-state="buttonState"
						 label="Sign In"
						 @click="emit('signIn')"
		/>
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