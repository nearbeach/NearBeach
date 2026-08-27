<script setup lang="ts">
import {WlkCard, WlkCardHeader} from "whelk-ui";

</script>

<template>
    <WlkCard class="server-error-page">
        <WlkCardHeader>
            <h1 id="main-title">Forbidden</h1>
        </WlkCardHeader>
	    <p>Sorry, you do not have permission to view that object</p>
    </WlkCard>
</template>

<style scoped>
.server-error-page {
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
