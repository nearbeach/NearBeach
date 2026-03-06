<script setup lang="ts">
import { CardComponent, CardHeader } from "whelk-ui";

// Declare props
defineProps({
	message: {
		type: String,
		required: true,
	},
	title: {
		type: String,
		required: true,
	},
})
</script>

<template>
	<CardComponent class="error-component">
		<CardHeader>
			<h1 id="main-title">{{ title }}</h1>
		</CardHeader>
		<p>{{ message }}</p>
	</CardComponent>
</template>

<style scoped>

</style>