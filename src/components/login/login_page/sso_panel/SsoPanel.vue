<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import type {SsoProvider} from "@/composables/useSsoProviders.ts";

// Define i18y
const {t} = useI18n();

// Define props
defineProps<{
	providers: SsoProvider[];
}>();

// Methods
function loginUrl(provider: SsoProvider): string {
	// Keep the page the user was heading to
	const next = new URLSearchParams(window.location.search).get("next");
	return next === null
		? provider.login_url
		: `${provider.login_url}?${new URLSearchParams({next})}`;
}
</script>

<template>
	<div class="sso-panel" v-if="providers.length > 0">
		<p class="divider">{{ t("sso_panel.or") }}</p>
		<a class="sso-button"
		   v-for="provider in providers"
		   :key="provider.slug"
		   :href="loginUrl(provider)"
		>
			{{ t("sso_panel.sign_in_with", {name: provider.name}) }}
		</a>
	</div>
</template>

<style scoped>
.sso-panel {
	display: flex;
	flex-direction: column;
	gap: 0.5rem;
	margin-top: 1rem;

	> .divider {
		font-size: 0.75rem;
		text-align: center;
		margin: 0;
	}

	> .sso-button {
		display: block;
		padding: 0.5rem 1rem;
		text-align: center;
		border: 1px solid currentColor;
		border-radius: 0.25rem;
		text-decoration: none;
	}
}
</style>
