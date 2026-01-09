<script setup lang="ts">
import CardComponent from '@/components/prefab/card/CardComponent.vue';
import CardHeader from '@/components/prefab/card/card_header/CardHeader.vue';
import { computed } from 'vue';

const objectType = computed(() => {
    // TODO - Add in router to find what item they are trying to search
    // TODO - Add unit tests around above todo
    return 'unknown';
});
</script>

<template>
    <CardComponent class="not-found-page">
        <CardHeader>
            <h1 id="main-title">404 Not Found</h1>
        </CardHeader>
        <p>Sorry, we could not find the object {{ objectType }}</p>
    </CardComponent>
</template>

<style scoped>
.not-found-page {
    display: grid;
    grid-template-columns: 1fr;
    margin: auto;
    grid-row-gap: 1rem;
    max-width: calc(var(--small-grid-width));
    padding: 0.5rem;

    > p {
        font-size: 1rem;
        font-weight: lighter;
        margin: 1rem 0 0.25rem 0;
    }
}
</style>
