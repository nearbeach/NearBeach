<script setup lang="ts">
import {Cog} from '@lucide/vue';
import {NavMenuItem} from '../nav_menu/nav_menu_item';
import {NavMenuLogout} from "@/components/nav/nav_menu/nav_menu_logout";
import { usePermissionStore} from "@/stores/permissions/permission.ts";
import {useI18n} from "petite-vue-i18n";

// Define i18y
const { t}  = useI18n({
	messages: {
		en: {
			setting_title: "Settings",
			setting_aria_label: "Go to NearBeach Settings",
		},
		ja: {
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

	<NavMenuLogout />

</template>
