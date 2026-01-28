<script setup lang="ts">

</script>

<template>
	<div class="forgotten-password-done">
		<div class="container">
			<h1 id="main-title">Password Reset Sent</h1>
			<p>Please check your inbox for the password reset, and any further instructions</p>
			<p>
				<RouterLink to="/login">Click here to return to login page.</RouterLink>
			</p>
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