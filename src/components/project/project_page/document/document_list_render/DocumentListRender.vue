<script setup lang="ts">
import {ref} from 'vue'
import type {DocumentItemInterface} from "@/utils/interfaces/DocumentItemInterface.ts";
import type {FolderItemInterface} from "@/utils/interfaces/FolderItemInterface.ts";
import DocumentList from './document_list/DocumentList.vue';
import FolderList from "@/components/project/project_page/document/document_list_render/folder_list/FolderList.vue";

// Define ref
const documentList = ref<DocumentItemInterface[]>([
	{ documentKey: "0000-0000-0000-0000", filename: "Book this hotel", type: "link"},
	{ documentKey: "0000-0000-0000-0001", filename: "Pictures of Socks in a kimono.jpg", type: "image"},
	{ documentKey: "0000-0000-0000-0002", filename: "Planning trip to Japan.docx", type: "text"},
	{ documentKey: "0000-0000-0000-0003", filename: "Power point presentation of Socks in Japan", type: "powerpoint"},
]);
const folderList = ref<FolderItemInterface[]>([
	{ folderId: 13, folderName: "Cat photos"},
	{ folderId: 10, folderName: "Design specs"},
	{ folderId: 11, folderName: "User Flow Diagrams"},
	{ folderId: 12, folderName: "User Stories"},
]);
</script>

<template>
	<div class="document-list-render">
		<div
			v-show="documentList.length + folderList.length === 0"
			class="empty-folder"
		>
			No Items in folder
		</div>
		<FolderList
			v-if="folderList.length > 0"
			:folder-list="folderList"
		/>
		<DocumentList
			v-if="documentList.length > 0"
			:document-list="documentList"
		/>
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