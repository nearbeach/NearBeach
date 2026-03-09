<script setup lang="ts">

// Define i18y
import {useI18n} from "petite-vue-i18n";

const { t} = useI18n({
	messages: {
		en: {
			go_back: "Click here to return to login page.",
			error_title: "Password Reset Failed",
			message: "Please check your inbox for the password reset, and any further instructions",
			title: "Password Reset Sent",
		},
		ja: {
			go_back: "ログインページに戻るにはここをクリックしてください",
			error_title: "パスワードのリセットに失敗しました",
			message: "パスワードのリセットと詳細な手順については受信トレイを確認してください。",
			title: "パスワードリセットを送信しました",
		},
	}
});

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
			<h1 id="main-title">{{ t("title")}}</h1>
			<p>{{ t("message")}}</p>
			<p>
				<RouterLink to="/login">{{t("go_back")}}</RouterLink>
			</p>
		</div>

		<div class="container"
			 v-else
		>
			<h1 id="main-title">{{t("error_title")}}</h1>
			<p>{{errorMessage}}</p>
			<RouterLink to="/login">{{t("go_back")}}</RouterLink>
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