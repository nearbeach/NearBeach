<script setup lang="ts"></script>

<template>
    <div class="card">
        <slot></slot>
    </div>
</template>

<style scoped>
.card {
    border-radius: var(--border-radius);
    background-color: var(--bg-light);
}
</style>
