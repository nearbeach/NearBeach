<script setup lang="ts">
import {Folder, Trash, CornerLeftUp} from "@lucide/vue";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import {useI18n} from "petite-vue-i18n";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			"parent_folder": "Go to parent folder",
		},
		ja: {
			"parent_folder": "親フォルダへ移動",
		},
	}
})

// Define store
const documentationStore = useDocumentationStore();
const objectStore = useObjectStore();

// Define functions
async function deleteFolder(folder_id: number) {
	const body = {
		type: "folder",
	}

	try {
		await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/documents/${folder_id}/`,
			{
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: JSON.stringify(body),
			},
		);

		// Remove folder
		documentationStore.removeFolder(folder_id);
	} catch (error) {
		console.log("ERROR: ", error);
		// TODO - handle error
	}
}

function gotoParentFolder() {
	// Update current folder
	documentationStore.currentFolderId = documentationStore.getParentFolder;

	// Update bread crumbs
	documentationStore.removeBreadCrumb();
}

function updateDocumentation(folder: FolderItemInterface) {
	// Update current folder
	documentationStore.currentFolderId = folder.id;

	// Update bread crumbs
	documentationStore.addBreadCrumb(folder);
}
</script>

<template>
	<div class="folder-list">
		<div class="folder-item"
		     v-show="documentationStore.currentFolderId !== 0"
		     v-on:click="gotoParentFolder()"
		>
			<div class="folder-icon">
				<CornerLeftUp/>
			</div>
			<div class="folder-details">
				{{ t("parent_folder") }}
			</div>
			<div class="folder-delete"></div>
		</div>
		<div
			class="folder-item"
			v-for="item in documentationStore.getFolders"
			:key="item.id"
		>
			<div class="folder-icon"
			     v-on:click="updateDocumentation(item)"
			>
				<Folder/>
			</div>
			<div class="folder-details"
			     v-on:click="updateDocumentation(item)"
			>
				<p>{{ item.description }}</p>
			</div>
			<div class="folder-delete"
			     @click="deleteFolder(item.id)"
			>
				<Trash/>
			</div>
		</div>
	</div>
</template>

<style scoped>
.folder-list {
	display: flex;
	flex-direction: column;

	> .folder-item {
		display: grid;
		grid-template-columns: [icon] 2rem [details] minmax(0, 1fr) [delete] 1rem;
		margin: 0 0 0.375rem 0;

		> .folder-icon {
			grid-column: icon;
			display: flex;
			align-items: center;

			> svg {
				flex: 1;
				width: 2rem;
				height: 2rem;
				stroke-width: 1px;
				color: var(--document-links);

				&:hover {
					fill: var(--document-links-hover);
				}
			}
		}

		> .folder-details {
			padding-left: 0.25rem;
			grid-column: details;
			display: flex;
			align-items: center;

			> p {
				margin: 0;
				font-size: 0.75rem;
				padding: 0;
				line-height: 1rem;
				font-family: "Roboto", sans-serif;
				text-overflow: ellipsis;
				overflow: hidden;
				white-space: nowrap;

				> a {
					text-decoration: none;
				}

				&:last-child {
					font-weight: 100;
				}
			}
		}

		> .folder-delete {
			grid-column: delete;
			display: flex;
			align-items: center;

			> svg {
				opacity: 0;
				transition: opacity 0.5s;
				flex: 1;
				width: 1rem;
				height: 1rem;
				stroke-width: 1px;
				color: var(--danger);

				&:hover {
					color: var(--danger-hover);
				}
			}
		}

		&:hover {
			> .folder-delete {
				> svg {
					transition: opacity 1s;
					opacity: 1;
				}
			}
		}
	}

	&:hover {
		cursor: pointer;
	}
}
</style>