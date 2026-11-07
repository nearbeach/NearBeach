<script setup lang="ts">
import CreateAndFilter from "@/components/object_components/document/create_and_filter/CreateAndFilter.vue";
import DocumentListRender from "@/components/object_components/document/document_list_render/DocumentListRender.vue";
import BreadCrumbs from "@/components/object_components/document/document_list_render/bread_crumbs/BreadCrumbs.vue";
import {onMounted, watch} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import type {FileSystemInterface} from "@/utils/interfaces/documents/FileSystemInterface.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define stores
const documentationStore = useDocumentationStore();
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Watch a specific state property
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
)

// Define onMount
onMounted(async () => {
	// Only load data if the object has loaded in
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
async function loadData() {
	// If documentation is loaded - don't load again
	if (documentationStore.isDocumentationLoaded) {
		return;
	}

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/documents/`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			}
		},
	)

	switch (response.status) {
		case 200:
			// Get the data
			const data: FileSystemInterface = await response.json();

			// Divie the data out
			documentationStore.documents = data.documents;
			documentationStore.folders = data.folders;
			documentationStore.maxUploadSize = data.max_upload_size;
			documentationStore.isDocumentationLoaded = true;
			break;
		default:
			errorStore.setError(response.statusText);
			errorStore.showErrorModal = true;
			break;
	}

}
</script>

<template>
	<div class="document">
		<CreateAndFilter/>
		<BreadCrumbs/>
		<DocumentListRender/>
	</div>
</template>

<style scoped>
.document {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}

	@media (--large-screen) {
		padding: 0.5rem 1rem;
	}
}
</style>