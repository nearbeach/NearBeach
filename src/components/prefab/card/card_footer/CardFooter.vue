<script setup lang="ts"></script>

<template>
    <div class="card-footer">
        <slot></slot>
    </div>
</template>

<style scoped>
.card-footer {
    padding: 0 0 0.75rem 0;

    @media (--large-screen) {
        margin: 1rem -2rem -1rem -2rem;
        padding: 1rem 2rem;
        border-radius: 0 0 var(--border-radius) var(--border-radius);
    }
}
</style>
