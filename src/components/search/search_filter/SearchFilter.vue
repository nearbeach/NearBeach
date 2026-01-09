<script setup lang="ts">
import { ref } from 'vue';
import CardComponent from '@/components/prefab/card/CardComponent.vue';
import CardHeader from '@/components/prefab/card/card_header/CardHeader.vue';
import SearchInput from '@/components/search/search_filter/search_input/SearchInput.vue';
import CheckboxComponent from '@/components/prefab/checkbox_component/CheckboxComponent.vue';

// Ref
const filterOutClosedObjects = ref(true);
const filterOutExternalGroups = ref(true);
</script>

<template>
    <CardComponent class="search-filter">
        <CardHeader>
            <h1 id="main-title">Search Projects</h1>
        </CardHeader>
        <p class="instructions">
            User the filters below to refine your results.
        </p>
        <SearchInput />
        <CheckboxComponent
            class="closed-objects"
            label="Filter out closed objects"
            id="filter-out-closed-objects"
            v-model="filterOutClosedObjects"
        />
        <CheckboxComponent
            class="external-groups"
            label="Filter out external groups"
            id="filter-out-external-groups"
            v-model="filterOutExternalGroups"
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
