<script setup lang="ts">
import {WlkCard, WlkCardHeader} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n();

</script>

<template>
    <WlkCard class="not-found-page">
        <WlkCardHeader>
            <h1 id="main-title">{{t("error.not_found_title")}}</h1>
        </WlkCardHeader>
		<p>{{t("error.not_found_text")}}</p>
    </WlkCard>
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
