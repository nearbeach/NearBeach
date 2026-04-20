<script setup lang="ts">
</script>

<template>
	<div class="small-loading-skeleton">
		<slot></slot>
	</div>
</template>

<style scoped>
.small-loading-skeleton {
	text-align: center;
	font-family: "Roboto", sans-serif;
	font-weight: 100;
	padding: 2rem 0;
	border: 1px black dashed;
	margin: 0 2rem 3rem 2rem;
}
</style>