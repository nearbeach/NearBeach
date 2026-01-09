<script setup lang="ts">
import SearchFilter from '@/components/search/search_filter/SearchFilter.vue';
import SearchResults from '@/components/search/search_results/SearchResults.vue';
</script>

<template>
    <div class="search-page">
        <SearchFilter />
        <SearchResults />
    </div>
</template>

<style scoped>
.search-page {
    display: grid;
    grid-template-columns: 1fr;
    max-width: var(--x-large-grid-width);
    margin: auto;

    grid-row-gap: 1rem;
}
</style>
