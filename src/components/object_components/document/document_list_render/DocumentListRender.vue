<script setup lang="ts">
import DocumentList from './document_list/DocumentList.vue';
import FolderList from "@/components/object_components/document/document_list_render/folder_list/FolderList.vue";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import {computed} from "vue";

// Define stores
const documentationStore = useDocumentationStore();

// Define computed
const hasNoResults = computed(() => {
	return documentationStore.documents.length + documentationStore.folders.length === 0;
})
</script>

<template>
	<div class="document-list-render">
		<div
			v-show="hasNoResults"
			class="empty-folder"
		>
			No Items in folder
		</div>
		<FolderList/>
		<DocumentList/>
	</div>
</template>

<style scoped>
.document-list-render {
	width: 100%;
	padding: 1.25rem 0 0.75rem 0;

	> .empty-folder {
		height: 7rem;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.25rem;
		font-weight: 100;
		font-family: "Roboto", sans-serif;
		border: dashed;
		border-radius: var(--border-radius);
		border-width: var(--border-width);
	}
}
</style>