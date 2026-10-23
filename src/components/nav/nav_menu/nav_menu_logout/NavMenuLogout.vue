<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {LogOut} from "@lucide/vue";

// i18n
const {t} = useI18n({
	messages: {
		en: {
			logout_aria_label: "Logout of NearBeach",
			logout_title: "Logout",
		},
		ja: {
			logout_aria_label: "NearBeachからログアウト",
			logout_title: "ログアウト",
		}
	}
});
</script>

<template>
    <li class="nav-bar--menu--item">
        <a href="/logout/"
            class="nav-bar--menu--item-search"
            :aria-label="t('logout_aria_label')"
        >
            <span class="nav-bar--menu--icon" aria-hidden="true">
				<component :is="LogOut" :size="14"/>
            </span>
            {{ t("logout_title") }}
        </a>
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

.nav-bar--menu--item:hover {
    border-color: deepskyblue;
    background-color: lightcyan;
}

.nav-bar--menu--item-search {
    text-decoration: none;
    color: var(--text-muted);
    padding: 10px;
}

.nav-bar--menu--item-search {
    width: calc(100% - 20px);
}
</style>
