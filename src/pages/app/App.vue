<script setup lang="ts">
import HeaderComponent from '@/components/header/HeaderComponent.vue';
import NavComponent from '@/components/nav/NavComponent.vue';
import SkipLinks from '@/components/skip_links/SkipLinks.vue';
import { useNavStore } from '@/stores/nav/nav.ts';
import { onMounted, computed } from 'vue';

// Stores
const navStore = useNavStore();

// Computed
const mainClass = computed(() =>
    navStore.isNavOpen ? 'main nav-open' : 'main'
);

// On Mounted
onMounted(() => {
    // If user is on mobile, the menu will not appear by default
    if (window.innerWidth > 1280) {
        navStore.toggleNav();
    }
});
</script>

<template>
    <SkipLinks />
    <HeaderComponent />
    <NavComponent />
    <main id="main" :class="mainClass" aria-labelledby="main-title" role="main">
        <RouterView v-slot="{ Component }">
            <transition name="fade" mode="out-in">
                <component :is="Component" />
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
