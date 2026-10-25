// stores/documentation.spec.ts
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";

describe('Nav - todo', () => {
	beforeEach(() => {
		setActivePinia(createPinia());
	});

    test("Check defaults", () => {
        const documentationStore = useDocumentationStore();

        // Expects
        expect(documentationStore.currentFolderId).toBe(0);
    });
});

describe("Documentation store - actions and getters", () => {
    const folders = [
        { id: 1, description: "Top", parent_folder_id: null },
        { id: 2, description: "Child", parent_folder_id: 1 },
        { id: 3, description: "Sibling", parent_folder_id: 1 },
    ];
    const documents = [
        { key: "a", description: "root.pdf", document: null, folder: null, parent_folder_id: null, url_location: null },
        { key: "b", description: "in-top.pdf", document: null, folder: null, parent_folder_id: 1, url_location: null },
    ];

    beforeEach(() => {
        setActivePinia(createPinia());
    });

    test("addBreadCrumb and removeBreadCrumb manage the trail", () => {
        const store = useDocumentationStore();

        store.addBreadCrumb(folders[0]);
        store.addBreadCrumb(folders[1]);
        expect(store.breadCrumbsArray).toEqual([
            { folderId: 1, label: "Top" },
            { folderId: 2, label: "Child" },
        ]);

        store.removeBreadCrumb();
        expect(store.breadCrumbsArray).toEqual([{ folderId: 1, label: "Top" }]);
    });

    test("goToRootFolder clears the trail and the current folder", () => {
        const store = useDocumentationStore();
        store.currentFolderId = 2;
        store.addBreadCrumb(folders[1]);

        store.goToRootFolder();

        expect(store.currentFolderId).toBe(0);
        expect(store.breadCrumbsArray).toEqual([]);
    });

    test("removeDocument and removeFolder drop only the matching item", () => {
        const store = useDocumentationStore();
        store.documents = [...documents];
        store.folders = [...folders];

        store.removeDocument("a");
        store.removeFolder(2);

        expect(store.documents.map((d) => d.key)).toEqual(["b"]);
        expect(store.folders.map((f) => f.id)).toEqual([1, 3]);
    });

    test("resetDocumentation puts everything back to defaults", () => {
        const store = useDocumentationStore();
        store.currentFolderId = 2;
        store.documents = [...documents];
        store.folders = [...folders];
        store.isDocumentationLoaded = true;
        store.addBreadCrumb(folders[1]);

        store.resetDocumentation();

        expect(store.currentFolderId).toBe(0);
        expect(store.documents).toEqual([]);
        expect(store.folders).toEqual([]);
        expect(store.breadCrumbsArray).toEqual([]);
        expect(store.isDocumentationLoaded).toBe(false);
    });

    test("updateFolderLocation trims the trail to the chosen crumb", () => {
        const store = useDocumentationStore();
        store.breadCrumbsArray = [
            { folderId: 1, label: "Top" },
            { folderId: 2, label: "Child" },
        ];
        store.currentFolderId = 2;

        store.updateFolderLocation(0);

        expect(store.breadCrumbsArray).toEqual([{ folderId: 1, label: "Top" }]);
        expect(store.currentFolderId).toBe(1);
    });

    test("updateFolderLocation falls back to the root for an unknown crumb", () => {
        const store = useDocumentationStore();
        store.currentFolderId = 2;

        store.updateFolderLocation(4);

        expect(store.currentFolderId).toBe(0);
    });

    test("getDocuments and getFolders follow the current folder", () => {
        const store = useDocumentationStore();
        store.documents = [...documents];
        store.folders = [...folders];

        expect(store.getDocuments.map((d) => d.key)).toEqual(["a"]);
        expect(store.getFolders.map((f) => f.id)).toEqual([1]);

        store.currentFolderId = 1;

        expect(store.getDocuments.map((d) => d.key)).toEqual(["b"]);
        expect(store.getFolders.map((f) => f.id)).toEqual([2, 3]);
    });

    test("getParentFolder returns the parent of the current folder", () => {
        const store = useDocumentationStore();
        store.folders = [...folders];
        store.currentFolderId = 2;

        expect(store.getParentFolder).toBe(1);
    });

    test("getParentFolder is 0 at the top level or for an unknown folder", () => {
        const store = useDocumentationStore();
        store.folders = [...folders];

        store.currentFolderId = 1;
        expect(store.getParentFolder).toBe(0);

        store.currentFolderId = 99;
        expect(store.getParentFolder).toBe(0);
    });
});
