<script setup lang="ts">

import LoginImage from "@/components/login/login_image/LoginImage.vue";
import LoginPanel from "@/components/login/login_page/login_panel/LoginPanel.vue";

</script>

<template>
	<div class="login">
		<LoginImage />
		<LoginPanel />
	</div>
</template>

<style scoped>
.login {
	display: flex;
	flex-direction: row;
	height: 100%;
}
</style>