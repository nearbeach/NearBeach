<script setup lang="ts">
import { useNavStore } from '@/stores/nav/nav.ts';
import { Plus } from 'lucide-vue-next';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

// Route
const route = useRoute();

// Store
const navStore = useNavStore();

// Setup Props
const props = defineProps({
    destination: {
        type: String,
        required: true,
    },
    overrideAriaLabel: {
        type: String,
        required: true,
    },
    routeAddress: {
        type: String,
        required: true,
    },
    routeAddressNew: {
        type: String,
        default: '',
        required: false,
    },
    title: {
        type: String,
        required: true,
    },
});

// Computed
const defineClass = computed(() => {
    // Set default class
    const baseClass = 'nav-bar--menu--item';

    // If the route name contains the destination - we are currently on that route
    const routeName = route?.name?.toString().toLowerCase();
    let isActive = routeName?.includes(props.destination.toLowerCase()) == true;

    // If the route is the same as the props route - we are currently on that route
    isActive =
        isActive ||
        route?.path?.toLowerCase() === props.routeAddress?.toLowerCase();

    // If the route is the same as the props routeNew - we are currently on that route
    isActive =
        isActive ||
        route?.path?.toLowerCase() === props.routeAddressNew.toLowerCase();

    // Return the appropriate class
    return isActive ? baseClass + ' current' : baseClass;
});

// Method
function closeMenu(): void {
    // If use is in mobile mode, close the window
    if (window.innerWidth < 1280) {
        navStore.toggleNav();
    }
}
</script>

<template>
    <li :class="defineClass">
        <RouterLink
            class="nav-bar--menu--item-search"
            :to="props.routeAddress"
            v-on:click="closeMenu"
            :aria-label="props.overrideAriaLabel"
        >
            <span class="nav-bar--menu--icon" aria-hidden="true">
                <slot></slot>
            </span>
            {{ props.title }}
        </RouterLink>
        <RouterLink
            v-if="routeAddressNew !== ''"
            class="nav-bar--menu--item-new"
            :to="props.routeAddressNew"
            v-on:click="closeMenu"
        >
            <span class="nav-bar--menu--plus" aria-hidden="true">
                <Plus />
            </span>
            <span class="hidden-visually">Create new {{ destination }}</span>
        </RouterLink>
    </li>
</template>

<style scoped>
.nav-bar--menu--item {
    display: flex;
    flex-direction: row;
    border: 1px solid lightgray;
    margin-bottom: 1rem;
    border-radius: var(--border-radius);
}

.nav-bar--menu--item:hover,
.current {
    border-color: deepskyblue;
    background-color: lightcyan;
}

.nav-bar--menu--item-search,
.nav-bar--menu--item-new {
    text-decoration: none;
    color: var(--text-muted);
    padding: 10px;
}

.nav-bar--menu--item-search {
    width: calc(100% - 20px);
}

.nav-bar--menu--item-new {
    width: 20px;
    border-radius: 0 4px 4px 0;
}

.nav-bar--menu--item-new:hover {
    background-color: cornflowerblue;
}

.nav-bar--menu--plus {
    display: block;
    transform: translateY(1px);

    > svg {
        width: 24px;
        height: 24px;

        @media (--small-screen) {
            width: 16px;
            height: 16px;
        }
    }
}
</style>
