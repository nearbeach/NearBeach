<script setup lang="ts">
import { CircleX } from 'lucide-vue-next';

defineProps({
    errorMessage: {
        type: String,
        required: true,
    },
});
</script>

<template>
    <p>
        <CircleX :size="14" aria-hidden="true" v-if="errorMessage.length > 0" />
        {{ errorMessage }}
    </p>
</template>

<style scoped>
p {
    color: var(--text-red);
    font-weight: lighter;
    font-size: 1rem;
    line-height: 1.125rem;
    padding: 0;
    margin: 0;

    > svg {
        transform: translateY(0.125rem);
    }

    @media (--large-screen) {
        font-size: 0.75rem;
    }
}

p:before {
    content: ' ';
    white-space: pre;
}
</style>
