<script setup lang="ts">

</script>

<template>
	<main id="main" aria-labelledby="main-title" role="main">
		<RouterView v-slot="{ Component }">
			<transition name="fade" mode="out-in">
				<component :is="Component"/>
			</transition>
		</RouterView>
	</main>
</template>

<style scoped>
main {
	width: 100vw;
	height: 100dvh;
	background-color: var(--bg-dark);
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>