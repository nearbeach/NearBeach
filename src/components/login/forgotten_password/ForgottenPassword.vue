<script setup lang="ts">
import {ref} from "vue";
import LoginImage from "../login_image/LoginImage.vue"
import ForgottenPasswordPanel from "./forgotten_password_panel/ForgottenPasswordPanel.vue"
import PasswordResetDone from "./password_reset_done/PasswordResetDone.vue";

// Define ref
const isDone = ref(false);

// Define functions
function submitPasswordReset(): void {
	isDone.value = true;

	// DEAL WITh AXIOS
}
</script>

<template>
	<div class="forgotten-password">
		<LoginImage/>
		<PasswordResetDone
			v-if="isDone"
		/>
		<ForgottenPasswordPanel
			v-else
			@passwordReset="submitPasswordReset"
		/>
	</div>
</template>

<style scoped>
.forgotten-password {
	display: flex;
	flex-direction: row;
	height: 100%;
}

</style>