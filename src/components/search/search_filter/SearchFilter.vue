<script setup lang="ts">
import {ref, onMounted, watch} from 'vue';
import {useRoute} from 'vue-router';
import {useSearchStore} from '@/stores/search/search.ts';
import SearchInput from '@/components/search/search_filter/search_input/SearchInput.vue';
import {WlkCard, WlkCardHeader, WlkCheckBox} from 'whelk-ui';
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useErrorStore} from "@/stores/error/error.ts";
import router from "@/router/router.ts";

// Define i18n
const {t} = useI18n()

// Define route
const errorStore = useErrorStore();
const route = useRoute();

// Define store
const store = useSearchStore();

// Ref
const showClosed = ref(false);
const search = ref('');
const timer = ref(0);

// Define Watch
watch(
	() => route.meta.destination,
	() => {
		// Stop Timer
		stopTimer();

		// Clear search and results
		search.value = "";
		store.searchResults = [];

		// Re-search
		getSearchResults();
	}
);

// Define onMounted
onMounted(() => {
	getSearchResults();
});

// Functions
function checkboxClicked() {
	// Stop Timer
	stopTimer();

	// Get search results
	getSearchResults();
}

async function getSearchResults() {
	// FAIL CONDITION - we just escape
	const fail_con_1 = search.value.length <= 3 && search.value.length > 0;
	const fail_con_2 = isNaN(parseInt(search.value))
	if (fail_con_1 && fail_con_2) {
		// Nothing to search
		return;
	}

	// Setup query string
	const queryString = `?search=${search.value}&show_closed=${showClosed.value ? 'true' : 'false'}`;

	// Fetch data
	const response = await fetch(
		`/api/v1/${route.meta.destination}/${queryString}`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		}
	)

	switch (response.status) {
		case 200: {
			// Get data
			const data = await response.json();

			// Patch data
			store.$patch({
				previous: data.previous,
				next: data.next,
				searchResults: data.results,
			});
			break;
		}
		default:
			errorStore.setError(response.statusText);
			await router.push({name: "server-error"});
	}

}

function startTimer() {
	// Stop timer
	stopTimer();

	// Set timer
	timer.value = setTimeout(() => {
		getSearchResults();
	}, 500);
}

function stopTimer() {
	// Clear any previous timeout
	if (timer.value !== 0) {
		clearTimeout(timer.value);
	}
}
</script>

<template>
	<WlkCard class="search-filter">
		<WlkCardHeader>
			<h1 id="main-title">{{ t(`search_filter.search_${route.meta.destination}`) }}</h1>
		</WlkCardHeader>
		<p class="instructions">{{ t("search_filter.instructions") }}</p>
		<SearchInput
			:placeholder="t(`search_filter.search_placeholder_${ route.meta.destination }`)"
			v-model="search"
			v-on:keydown="startTimer"
		/>
		<WlkCheckBox
			:label="t('search_filter.closed')"
			id="show-closed-objects"
			v-model="showClosed"
			v-on:change="checkboxClicked"
		/>
	</WlkCard>
</template>

<style scoped>
.search-filter {
	display: grid;
	grid-template-columns: 1fr;
	grid-template-rows: 2.125rem 2.125rem 3.125rem 1.5rem 1.5rem;
	padding: 0 0.5rem;

	@media (--small-screen) {
		padding: 0.5rem 1rem;
	}

	@media (--medium-screen) {
		margin: 0 0.5rem;
	}

	@media (--large-screen) {
		padding: 1rem 2rem;
		grid-template-rows: 3.25rem 2.125rem 3.125rem 1.5rem 1.5rem;
	}

	> .instructions {
		font-weight: lighter;
		margin: 0 0 0.5rem 0;
		font-size: 1rem;
	}
}
</style>
