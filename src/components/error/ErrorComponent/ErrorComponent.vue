<script setup lang="ts">
import { WlkCard, WlkCardHeader } from "whelk-ui";

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
	<WlkCard class="error-component">
		<WlkCardHeader>
			<h1 id="main-title">{{ title }}</h1>
		</WlkCardHeader>
		<p>{{ message }}</p>
	</WlkCard>
</template>

<style scoped>

</style>