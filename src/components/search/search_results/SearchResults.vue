<script setup lang="ts">
import SearchCard from '@/components/search/search_results/search_card/SearchCard.vue';
import SearchHeader from '@/components/search/search_results/search_header/SearchHeader.vue';
import {CardComponent} from "whelk-ui";
import {useSearchStore} from "@/stores/search/search.ts";
import {useRoute} from "vue-router";
import {computed} from "vue";

// Define route
const route = useRoute();

// Define stores
const store = useSearchStore();

// Define computed
const destination = computed(() => {
	return `${route.meta.destination}`;
});
</script>

<template>
    <CardComponent class="search-results">
        <SearchHeader />
        <SearchCard
			v-for="item in store.searchResults"
			:id="item.id"
			:key="item.id"
			:higher-order-status="item.status.higher_order_status.value"
			:object-type="destination"
			:status="item.status.status"
			:title="item.title"
		/>
    </CardComponent>
</template>

<style scoped>
.search-results {
	@media (--medium-screen) {
		margin: 0 0.5rem;
	}
}
</style>
