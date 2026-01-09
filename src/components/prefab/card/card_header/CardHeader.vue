<script setup lang="ts"></script>
<template>
    <div class="card-header">
        <slot />
    </div>
</template>

<style scoped>
.card-header {
    border-radius: 0;

    @media (--large-screen) {
        border-radius: var(--border-radius) var(--border-radius) 0 0;
    }
}
</style>
