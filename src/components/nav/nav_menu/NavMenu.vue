<script setup lang="ts">
// Types
import type { MenuItemInterface } from '@/utils/interfaces/MenuItemInterface.ts';
import NavMenuItem from '@/components/nav/nav_menu/nav_menu_item/NavMenuItem.vue';
// Icons
import {
    LayoutDashboard,
    SquareKanban,
    ClipboardList,
    FolderOpenIcon,
    ListTodo,
    ReplaceAll,
} from 'lucide-vue-next';
import { ref } from 'vue';

// Data
const navMenuItems = ref<MenuItemInterface[]>([]);

// Async
const fetchNavMenuItems = async () => {
    return new Promise<MenuItemInterface[]>((resolve) => {
        setTimeout(() => {
            resolve([
                {
                    ariaLabel: 'Go to dashboard',
                    destination: 'dashboard',
                    icon: LayoutDashboard,
                    route: '/',
                    routeNew: '',
                    title: 'Dashboard',
                },
                {
                    ariaLabel: 'Search for kanban board',
                    destination: 'kanban_board',
                    icon: SquareKanban,
                    route: '/kanban_board',
                    routeNew: '/kanban_board/new',
                    title: 'Kanban board',
                },
                {
                    ariaLabel: 'Search for requirement',
                    destination: 'requirement',
                    icon: ClipboardList,
                    route: '/requirement',
                    routeNew: '/requirement/new',
                    title: 'Requirement',
                },
                {
                    ariaLabel: 'Search for project',
                    destination: 'project',
                    icon: FolderOpenIcon,
                    route: '/project',
                    routeNew: '/project/new',
                    title: 'Project',
                },
                {
                    ariaLabel: 'Search for task',
                    destination: 'task',
                    icon: ListTodo,
                    route: '/task',
                    routeNew: '/task/new',
                    title: 'Task',
                },
                {
                    ariaLabel: 'Search for Request for Change',
                    destination: 'request_for_change',
                    icon: ReplaceAll,
                    route: '/request_for_change',
                    routeNew: '/request_for_change/new',
                    title: 'Request for change',
                },
            ]);
        }, 400);
    });
};
navMenuItems.value = await fetchNavMenuItems();
</script>

<template>
    <NavMenuItem
        v-for="menuItem in navMenuItems"
        :key="menuItem.destination"
        :destination="menuItem.destination"
        :override-aria-label="menuItem.ariaLabel"
        :routeAddress="menuItem.route"
        :routeAddressNew="menuItem.routeNew"
        :title="menuItem.title"
    >
        <component :is="menuItem.icon" />
    </NavMenuItem>
</template>

<style scoped>
.nav-bar--menu--icon {
    > svg {
        width: 20px;
        height: 20px;

        @media (--small-screen) {
            width: 14px;
            height: 14px;
        }
    }
}
</style>
