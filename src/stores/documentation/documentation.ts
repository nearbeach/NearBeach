// store/documentation.ts
import {defineStore} from 'pinia'
import type {BreadCrumbsArrayInterface} from "@/utils/interfaces/documents/BreadCrumbsArrayInterface.ts";
import type {DocumentItemInterface} from "@/utils/interfaces/documents/DocumentItemInterface.ts";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";

export const useDocumentationStore = defineStore('documentation', {
    state: () => ({
        breadCrumbsArray: [] as BreadCrumbsArrayInterface[],
        currentFolderId: 0,
        documents: [] as DocumentItemInterface[],
        folders: [] as FolderItemInterface[],
        isDocumentationLoaded: false,
        maxUploadSize: 0,
    }),
    actions: {
        goToRootFolder() {
            // Set default values
            this.breadCrumbsArray = [];
            this.currentFolderId = 0;
        },
        resetDocumentation() {
            // Place everything onto defaults
            this.breadCrumbsArray = [];
            this.currentFolderId = 0;
            this.documents = [];
            this.folders = [];
            this.isDocumentationLoaded = false;
        },
        updateFolderLocation(index: number) {
            // Remove the unwanted folders
            this.breadCrumbsArray = this.breadCrumbsArray.slice(0, index + 1);

            // Update folder id
            this.currentFolderId = this.breadCrumbsArray[index]?.folderId ?? 0;
        },
    },
    getters: {
        getDocuments: (state) => {
            return state.documents.filter((row) => {
                // If the row.folder is null - we assume it is a "0"
                const folder_id = row.folder ?? "0";

                return folder_id === state.currentFolderId.toString();
            });
        },
        getFolders: (state) => {
            return state.folders.filter((row) => {
                // If the row.parent_folder is null - we assume it is a "0"
                const parent_folder_id = row.parent_folder ?? "0";

                return parent_folder_id === state.currentFolderId.toString();
            });
        },
    }
})