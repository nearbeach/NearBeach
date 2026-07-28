<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import type {PublicLinkInterface} from "@/utils/interfaces/PublicLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {WlkButton} from "whelk-ui";

// Define stores
const objectStore = useObjectStore();

// Define refs
const publicLinks = ref<PublicLinkInterface[]>([]);

// Define watch
watch(
    () => objectStore.is_loaded,
    async (new_value) => {
        // If object data is now loaded - fetch data
        if (new_value) {
            await loadData();
        }
    }
);

// Define onMounted
onMounted(async () => {
    if (objectStore.is_loaded) {
        await loadData();
    }
});

// Define functions
async function createPublicLink() {
    try {
        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/public_links/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFTOKEN": getCsrfToken(),
                },
            },
        );

        // Get data
        const data = await response.json();
        publicLinks.value.push(data);
    } catch (error) {
        // TODO - handle errors properly
        console.error(error);
    }
}

async function loadData() {
    try {
        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/public_links/`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            }
        )

        // Get data
        publicLinks.value = await response.json();
    } catch (error) {
        // TDOO - handle errors properly
        console.error(error);
    }
}
</script>

<template>
	<div class="public-links">
		<h3>Public Links</h3>
		<p class="sub-text">Control public access to project.</p>

        <table v-if="publicLinks.length > 0">
            <thead>
                <tr>
                    <td>Public Link</td>
                    <td>Is Active</td>
                    <td></td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="link in publicLinks"
                    :key="link.id"
                >
                    <td>{{link.id}}</td>
                    <td>{{link.is_active}}</td>
                    <td>TODO - ADD CODE</td>
                </tr>
            </tbody>
        </table>

        <WlkButton class="compact primary"
            @click="createPublicLink"
        >
            Create Public Link
        </WlkButton>
	</div>
</template>

<style scoped>

</style>