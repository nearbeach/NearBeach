<script setup lang="ts">
import CreateAndFilter from "@/components/object_components/document/create_and_filter/CreateAndFilter.vue";
import DocumentListRender from "@/components/object_components/document/document_list_render/DocumentListRender.vue";
import BreadCrumbs from "@/components/object_components/document/document_list_render/bread_crumbs/BreadCrumbs.vue";
import {onMounted, ref, watch} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {BreadCrumbsArrayInterface} from "@/utils/interfaces/documents/BreadCrumbsArrayInterface.ts";
import type {DocumentItemInterface} from "@/utils/interfaces/documents/DocumentItemInterface.ts";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";
import type {FileSystemInterface} from "@/utils/interfaces/documents/FileSystemInterface.ts";

// Define refs
const breadCrumbsArray = ref<BreadCrumbsArrayInterface[]>([]);
const currentFolderId = ref(0);
const documents = ref<DocumentItemInterface[]>([]);
const folders = ref<FolderItemInterface[]>([]);
const isLoaded = ref<boolean>(false);
const maxUploadSize = ref<number>(0);

// Define state
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
	// Only load data if object has loaded in
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
function goToRootFolder() {
	// Set default values
	breadCrumbsArray.value = [];
	currentFolderId.value = 0;
}

async function loadData() {
	try {
		// Tell user we are loading
		isLoaded.value = false;

		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/documents/`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				}
			},
		)

		// Get the data
		const data: FileSystemInterface = await response.json();

		// Divie the data out
		documents.value = data.documents;
		folders.value = data.folders;
		maxUploadSize.value = data.max_upload_size;
	} catch (e) {
		isLoaded.value = true;
		// TODO - handle the errors
	}
}

function updateFolderLocation(data: { index: number }) {
	// Remove the unwanted folders
	breadCrumbsArray.value = breadCrumbsArray.value.slice(0, data.index + 1);

	// Update folder id
	currentFolderId.value = breadCrumbsArray.value[data.index]?.folderId ?? 0;
}
</script>

<template>
	<div class="document">
		<CreateAndFilter
			:currentFolderId="currentFolderId"
		/>
		<BreadCrumbs
			:bread-crumbs-array="breadCrumbsArray"
			v-on:goToRootFolder="goToRootFolder"
			v-on:updateFolderLocation="updateFolderLocation"
		/>
		<DocumentListRender
			:documents="documents"
			:folders="folders"
		/>
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