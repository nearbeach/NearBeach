<script setup lang="ts"></script>

<template>
    <div class="search-header">
        <div class="object-title">Title</div>
        <div class="object-status-tag">Status</div>
    </div>
</template>

<style scoped>
.search-header {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    background-color: var(--primary);
    padding: 0.5rem;

    @media (--medium-screen) {
        grid-template-columns: repeat(6, minmax(0, 1fr));
    }

    > .object-title {
        grid-column-start: 1;
        grid-column-end: 3;

        @media (--medium-screen) {
            grid-column-start: 1;
            grid-column-end: 6;
        }
    }

    > .object-status-tag {
        grid-column-start: 3;
        grid-column-end: 4;

        @media (--medium-screen) {
            grid-column-start: 6;
            grid-column-end: 7;
        }
    }
}
</style>
