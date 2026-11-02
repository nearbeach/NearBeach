<script setup lang="ts">

// Define i18y
import {useI18n} from "petite-vue-i18n";

const { t} = useI18n();

// Define Props
defineProps({
	errorMessage: {
		type: String,
		required: true,
	}
});
</script>

<template>
	<div class="forgotten-password-done">
		<div class="container"
			v-if="errorMessage === ''"
		>
			<h1 id="main-title">{{ t("password_reset_done.title")}}</h1>
			<p>{{ t("password_reset_done.message")}}</p>
			<p>
				<RouterLink to="/login">{{t("password_reset_done.go_back")}}</RouterLink>
			</p>
		</div>

		<div class="container"
			 v-else
		>
			<h1 id="main-title">{{t("password_reset_done.error_title")}}</h1>
			<p>{{errorMessage}}</p>
			<RouterLink to="/login">{{t("password_reset_done.go_back")}}</RouterLink>
		</div>
	</div>
</template>

<style scoped>
.forgotten-password-done {
	width: 100%;
	height: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;

	.container {
		max-width: 75%;
	}

}

</style>