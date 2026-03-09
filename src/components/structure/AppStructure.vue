<script setup lang="ts">
import {computed, onMounted} from 'vue';
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import {useNavStore} from "@/stores/nav/nav.ts";
import SkipLinks from "@/components/skip_links/SkipLinks.vue";
import NavComponent from "@/components/nav/NavComponent.vue";
import HeaderComponent from "@/components/header/HeaderComponent.vue";

// Stores
const navStore = useNavStore();

onMounted(async () => {
	// If user is on mobile, the menu will not appear by default
	if (window.innerWidth > 1280) {
		navStore.toggleNav();
	}
});

// Computed
const mainClass = computed(() =>
	navStore.isNavOpen ? 'main nav-open' : 'main'
);
</script>

<template>
	<SkipLinks/>
	<HeaderComponent/>
	<NavComponent/>
	<main id="main" :class="mainClass" aria-labelledby="main-title" role="main">
		<RouterView v-slot="{ Component }">
			<transition name="fade" mode="out-in">
				<component :is="Component"/>
			</transition>
		</RouterView>
	</main>
</template>

<style scoped>
main {
	min-height: calc(100dvh - 60px);
	background-color: var(--bg-dark);
	transition: margin-left 0.5s ease;

	@media (--medium-screen) {
		min-height: calc(100dvh - 65px);
		padding-top: 20px;
	}
}

main.nav-open {
	@media (--x-large-screen) {
		margin-left: 263px;
	}
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