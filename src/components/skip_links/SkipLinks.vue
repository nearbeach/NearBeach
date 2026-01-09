<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const backToTop = ref();

watch(
    () => route.path,
    () => {
        backToTop.value.focus();
    }
);
</script>

<template>
    <span ref="backToTop" tabindex="-1" />
    <ul class="skip-links">
        <li>
            <a href="#main" ref="skipLink" class="skip-link"
                >Skip to main content</a
            >
        </li>
    </ul>
</template>

<style scoped>
.skip-links {
    list-style: none;
    margin: 0;
}
.skip-link {
    white-space: nowrap;
    margin: 1em auto;
    top: 0;
    position: fixed;
    left: 50%;
    margin-left: -72px;
    opacity: 0;
}
.skip-link:focus {
    opacity: 1;
    background-color: white;
    padding: 0.5em;
    border: 1px solid black;
}
</style>
