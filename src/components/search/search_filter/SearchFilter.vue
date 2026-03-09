<script setup lang="ts">
import {inject, ref, onMounted, watch} from 'vue';
import type {AxiosInstance} from 'axios';
import {useRoute} from 'vue-router';
import {useSearchStore} from '@/stores/search/search.ts';
import SearchInput from '@/components/search/search_filter/search_input/SearchInput.vue';
import {CardComponent, CardHeader, CheckBox} from 'whelk-ui';

// Define route
const route = useRoute();

// Define store
const store = useSearchStore();

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Ref
const showClosed = ref(false);
const search = ref('');
const timer = ref(0);

// Define Watche
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

function getSearchResults() {
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
	apiClient?.get(
		`/api/v1/${route.meta.destination}/${queryString}`,
	).then((response) => {
		store.$patch({
			previous: response.data.previous,
			next: response.data.next,
			searchResults: response.data.results,
		});
	}).catch((error) => {
		// TODO - put in method to handle the errors
		console.error(error);
	})
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
	<CardComponent class="search-filter">
		<CardHeader>
			<h1 id="main-title">Search {{ route.meta.destination }}s</h1>
		</CardHeader>
		<p class="instructions">
			User the filters below to refine your results.
		</p>
		<SearchInput
			:placeholder="`Search for ${route.meta.destination}s`"
			v-model="search"
			v-on:keydown="startTimer"
		/>
		<CheckBox
			:label="`Show closed ${ route.meta.destination }s`"
			id="show-closed-objects"
			v-model="showClosed"
		/>
	</CardComponent>
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
