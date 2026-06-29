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
        addBreadCrumb(folder: FolderItemInterface) {
            // Push the folder onto the bread crumbs array
            this.breadCrumbsArray.push({
                folderId: folder.id,
                label: folder.description,
            });
        },
        goToRootFolder() {
            // Set default values
            this.breadCrumbsArray = [];
            this.currentFolderId = 0;
        },
        removeBreadCrumb() {
            // Remove the last item
            this.breadCrumbsArray.pop();
        },
        removeDocument(document_key: string) {
            this.documents = this.documents.filter((row) => {
                return row.key !== document_key;
            });
        },
        removeFolder(folder_id: number) {
            this.folders = this.folders.filter((row) => {
                return row.id !== folder_id;
            });
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
                const parent_folder_id = row.parent_folder_id?.toString() ?? "0";

                return parent_folder_id === state.currentFolderId.toString();
            });
        },
        getFolders: (state) => {
            return state.folders.filter((row) => {
                // If the row.parent_folder is null - we assume it is a "0"
                const parent_folder_id = row.parent_folder_id ?? "0";

                return parent_folder_id.toString() === state.currentFolderId.toString();
            });
        },
        getParentFolder: (state) => {
            // Get the data for the current folder
            const current_folder = state.folders.filter((row) => {
                return state.currentFolderId === row.id;
            });

            // If there are no results - just return 0 as the parent folder
            if (current_folder.length === 0) {
                return  0;
            }

            // Return the first result with a fallback of 0
            return current_folder[0]?.parent_folder_id ?? 0;
        },
    }
})