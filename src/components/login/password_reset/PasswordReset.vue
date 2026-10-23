<script setup lang="ts">

import {LoginImage} from "../login_image";
import {PasswordResetPanel} from "./password_reset_panel"
</script>

<template>
	<div class="password-reset">
		<LoginImage/>
		<PasswordResetPanel />

	</div>
</template>

<style scoped>
.password-reset {
	display: flex;
	flex-direction: row;
	height: 100%;
}
</style>