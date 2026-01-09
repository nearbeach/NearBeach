<script setup lang="ts">
import CardComponent from '@/components/prefab/card/CardComponent.vue';
import SearchCard from '@/components/search/search_results/search_card/SearchCard.vue';
import SearchHeader from '@/components/search/search_results/search_header/SearchHeader.vue';
</script>

<template>
    <CardComponent class="search-results">
        <SearchHeader />
        <SearchCard
            higher-order-status="backlog"
            :id="12"
            object-type="project"
            status="Up for discussion"
            title="Redevelop the NearBeach UI/UX."
        />
        <SearchCard
            higher-order-status="normal"
            :id="24"
            object-type="project"
            status="In Development"
            title="Develop mockup site for NearBeach UI/UX testing and feedback."
        />
        <SearchCard
            higher-order-status="normal"
            :id="11"
            object-type="project"
            status="Up for discussion"
            title="Redevelop the NearBeach UI/UX."
        />
        <SearchCard
            higher-order-status="blocked"
            :id="11"
            object-type="project"
            status="Blocked"
            title="Redevelop the NearBeach UI/UX."
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
