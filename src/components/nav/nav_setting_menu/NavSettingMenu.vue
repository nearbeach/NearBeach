<script setup lang="ts">
import {Cog, LogOut} from 'lucide-vue-next';
import NavMenuItem from '../nav_menu/nav_menu_item/NavMenuItem.vue';
import { usePermissionStore} from "@/stores/permissions/permission.ts";
import {useI18n} from "petite-vue-i18n";

// Define i18y
const { t}  = useI18n({
	messages: {
		en: {
			logout_title: "Logout",
			logout_aria_label: "Logout of NearBeach",
			setting_title: "Settings",
			setting_aria_label: "Go to NearBeach Settings",
		},
		ja: {
			logout_title: "ログアウト",
			logout_aria_label: "NearBeachからログアウト",
			setting_title: "設定",
			setting_aria_label: "NearBeachの設定に移動",
		}
	}
})

// Define Store
const permissionStore = usePermissionStore();

</script>

<template>
	<NavMenuItem
		v-if="permissionStore.hasAdministrationPermission"
		destination="settings"
		route-address="/settings"
		route-address-new=""
		:title="t('setting_title')"
		:override-aria-label="t('setting_aria_label')"
	>
		<component :is="Cog" :size="14"/>
	</NavMenuItem>

		<NavMenuItem
		destination="logout"
		route-address="/logout/"
		route-address-new=""
		:override-aria-label="t('logout_aria_label')"
		:title="t('logout_title')"
	>
		<component :is="LogOut" :size="14"/>
	</NavMenuItem>

</template>

<style scoped></style>
