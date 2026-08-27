<script setup lang="ts">
import {WlkCard, WlkCardHeader} from "whelk-ui";
import {useErrorStore} from "@/stores/error/error.ts";

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
});

// Define store
const errorStore = useErrorStore();
</script>

<template>
	<WlkCard class="error-component">
		<WlkCardHeader>
			<h1 id="main-title">{{ title }}</h1>
		</WlkCardHeader>
		<textarea
			rows="20"
			v-model="errorStore.message"
		/>
	</WlkCard>
</template>

<style scoped>

</style>