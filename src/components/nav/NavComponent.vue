<script setup lang="ts">
import NavMenu from '@/components/nav/nav_menu/NavMenu.vue';
import NavMenuSkeleton from '@/components/nav/nav_menu_skeleton/NavMenuSkeleton.vue';
import NavSettingMenu from '@/components/nav/nav_setting_menu/NavSettingMenu.vue';
import { useNavStore } from '@/stores/nav/nav.ts';

// Stores
const navStore = useNavStore();
</script>

<template>
    <Transition>
        <nav v-show="navStore.isNavOpen" role="navigation">
            <div class="nav-bar--menu">
                <ul class="nav-bar--menu--list">
                    <suspense>
                        <NavMenu />
                        <template #fallback>
                            <NavMenuSkeleton :count="4" />
                        </template>
                    </suspense>
                </ul>
            </div>
            <div class="nav-bar--settings">
                <ul class="nav-bar--settings--list">
                    <suspense>
                        <NavSettingMenu />
                        <template #fallback>
                            <NavMenuSkeleton />
                        </template>
                    </suspense>
                </ul>
            </div>
        </nav>
    </Transition>
</template>

<style scoped>
nav {
    background-color: white;
    width: 100vw;
    height: calc(100dvh - 60px);
    position: fixed;
    top: 60px;
    left: 0;
    overflow-x: scroll;
    flex-direction: column;
    display: flex;
    justify-content: space-between;
    z-index: 1000;

    @media (--small-screen) {
        width: 255px;
        height: calc(100vh - 45px);
        top: 45px;
        padding: 0 4px;
    }

    > .nav-bar--menu {
        margin-top: 15px;

        @media (--small-screen) {
            margin-top: 5px;
        }
    }
}

.nav-bar--menu--list,
.nav-bar--settings--list {
    display: flex;
    flex-direction: column;
    padding: 0;
    width: calc(100vw - 16px);
    margin: auto;
    font-size: 1.5rem;
    line-height: 2rem;
    font-weight: 500;
    font-family: 'Open Sans', sans-serif;
    font-style: normal;

    @media (--small-screen) {
        width: 243px;
        font-size: 1.125rem;
        line-height: 1.5rem;
    }
}

.v-enter-active,
.v-leave-active {
    transition: transform 0.5s ease;
}

.v-enter-from,
.v-leave-to {
    transform: translateX(-100%);
}
</style>
