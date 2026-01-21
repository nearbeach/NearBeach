<script setup lang="ts">

import LoginImage from "@/components/login/login_image/LoginImage.vue";
import ForgottenPasswordPanel
	from "@/components/login/forgotten_password/forgotten_password_panel/ForgottenPasswordPanel.vue";
</script>

<template>
	<div class="forgotten-password">
		<LoginImage/>
		<ForgottenPasswordPanel/>
	</div>
</template>

<style scoped>
.forgotten-password {
	display: flex;
	flex-direction: row;
	height: 100%;
}

</style>