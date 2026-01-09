<script setup lang="ts">
import type { MenuItemInterface } from '@/utils/interfaces/MenuItemInterface.ts';
// Icons
import { Cog, LogOut } from 'lucide-vue-next';
import { ref } from 'vue';
import NavMenuItem from '../nav_menu/nav_menu_item/NavMenuItem.vue';

// Data
const navSettingMenu = ref<MenuItemInterface[]>([]);

// Computed
const fetchNavSettingMenuItems = async () => {
    return new Promise<MenuItemInterface[]>((resolve) => {
        setTimeout(() => {
            resolve([
                {
                    ariaLabel: 'Go to NearBeach Settings',
                    destination: 'settings',
                    icon: Cog,
                    route: '/settings',
                    routeNew: '',
                    title: 'Settings',
                },
                {
                    ariaLabel: 'Logout of NearBeach',
                    destination: 'logout',
                    icon: LogOut,
                    route: '/logout',
                    routeNew: '',
                    title: 'Logout',
                },
            ]);
        });
    });
};

// Async
navSettingMenu.value = await fetchNavSettingMenuItems();
</script>

<template>
    <NavMenuItem
        v-for="menuItem in navSettingMenu"
        :key="menuItem.destination"
        :destination="menuItem.destination"
        :override-aria-label="menuItem.ariaLabel"
        :routeAddress="menuItem.route"
        :routeAddressNew="menuItem.routeNew"
        :title="menuItem.title"
    >
        <component :is="menuItem.icon" :size="14" />
    </NavMenuItem>
</template>

<style scoped></style>
