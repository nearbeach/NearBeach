<script setup lang="ts">
import SearchFilter from '@/components/search/search_filter/SearchFilter.vue';
import SearchOrganisationResults from '@/components/organisation/search_organisation/search_organisation_results/SearchOrganisationResults.vue';
</script>

<template>
    <div class="search-page">
        <SearchFilter />
		<SearchOrganisationResults />
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
