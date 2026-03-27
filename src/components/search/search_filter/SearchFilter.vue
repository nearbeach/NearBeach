<script setup lang="ts">
import {inject, ref, onMounted, watch} from 'vue';
import type {AxiosInstance} from 'axios';
import {useRoute} from 'vue-router';
import {useSearchStore} from '@/stores/search/search.ts';
import SearchInput from '@/components/search/search_filter/search_input/SearchInput.vue';
import {WlkCard, WlkCardHeader, WlkCheckBox} from 'whelk-ui';
import { useI18n } from "petite-vue-i18n";

// Define i18n
const { t} = useI18n({
	messages: {
		en: {
			closed: "Show closed objects",
			instructions: "User the filters below to refine your results.",
			search_kanban_board: "Search Kanban Board",
			search_placeholder_kanban_board: "Search for a kanban board",
			search_request_for_change: "Search Request For Change",
			search_placeholder_request_for_change: "Search for a request for change",
			search_requirement: "Search Requirement",
			search_placeholder_requirement: "Search for a requirement",
			search_project: "Search Project",
			search_placeholder_project: "Search for a project",
			search_task: "Search Task",
			search_placeholder_task: "Search for a task",
		},
		ja: {
			closed: "閉じたオブジェクトを表示",
			instructions: "以下のフィルターを使用して結果を絞り込みます",
			search_kanban_board: "カンバンボードを検索",
			search_placeholder_kanban_board: "カンバンボードを検索",
			search_request_for_change: "検索変更リクエスト",
			search_placeholder_request_for_change: "変更要求を検索する",
			search_requirement: "要件を検索する",
			search_placeholder_requirement: "要件を検索する",
			search_project: "プロジェクトを検索",
			search_placeholder_project: "プロジェクトを検索",
			search_task: "タスクを検索する",
			search_placeholder_task: "タスクを検索する",
		},
	}
})

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
	<WlkCard class="search-filter">
		<WlkCardHeader>
			<h1 id="main-title">{{ t(`search_${ route.meta.destination }`)}}</h1>
		</WlkCardHeader>
		<p class="instructions">{{t("instructions")}}</p>
		<SearchInput
			:placeholder="t(`search_placeholder_${ route.meta.destination }`)"
			v-model="search"
			v-on:keydown="startTimer"
		/>
		<WlkCheckBox
			:label="t('closed')"
			id="show-closed-objects"
			v-model="showClosed"
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
